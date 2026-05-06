# Palo Alto

This page documents the specific variables, fields, and query patterns used in Palo Alto PAN-OS dashboards.

## Variables

| Variable | Query Source | Notes |
|----------|--------------|-------|
| `firewall` | `_stream: {panos.type=$type}` | Populated from `panos.device_name` |
| `vsys` | `_stream: {panos.type=$type, panos.device_name in (${firewall})}` | Virtual System from `panos.vsys`. Equivalent to FortiGate's `vdom` |
| `type` | Custom (hardcoded per dashboard) | `"TRAFFIC"` in Traffic dashboard, `"THREAT"` in Threat dashboard. No `policytype` equivalent |
| `subtype` | Query | From `panos.subtype` — varies by log type |
| `direction` | Custom | Options: `outbound`, `inbound`, `internal`, `external` |
| `action` | Query | From `panos.action` — `allow`, `deny`, `drop`, `reset-both`, etc. |
| `Logsql` | Text | Custom filter, default `*` |

!!! note "No policytype"
    PAN-OS dashboards do not have a `policytype` variable. FortiGate's `fgt.policytype` distinguishes between policy types (policy, interface, any) but PAN-OS does not produce an equivalent field in its logs.

## Base Query

```plaintext
_stream:{panos.device_name in(${firewall:doublequote}),panos.vsys in(${vsys:doublequote}),panos.type=${type:doublequote},panos.subtype in(${subtype:doublequote}),network.direction=${direction:doublequote}}
| panos.action:in(${action:doublequote}) AND ${Logsql:raw}
| stats by (panos.srcloc) count() results
| sort by (results) desc
| limit 10
```

## Traffic Dashboard

The Traffic dashboard (`traffic-panos.json`) is organized into direction tabs (outbound/inbound/internal/external), each with two metric sub-tabs:

| Sub-tab | Metric |
|---------|--------|
| Sessions | `count()` — one log ≈ one connection |
| Bytes | `sum(bytes)` — total volume transferred |

Within each sub-tab, rows follow the standard [panel hierarchy](usage.md#panel-hierarchy): Metrics → Action → Geo → Source\|Destination → Application → Rule.

### Zone & Interface Chord Diagrams

The Traffic dashboard includes **chord diagrams** (`esnet-chord-panel`) in the Interfaces/Zones row — a visualization unique to Palo Alto that has no FortiGate equivalent. These show traffic flow relationships:

- **Zone-to-zone** — volumes of sessions flowing between security zones (e.g., untrust → trust)
- **Interface-to-interface** — physical/logical interface pair flows

These are particularly useful for understanding traffic routing and zone policy coverage.

### Notable Traffic Panels

- **Chord diagrams** — Zone and interface flow visualization
- **Geomap** — Source and destination country distribution (`panos.srcloc`, `panos.dstloc`)
- **Sankey diagram** — Traffic flow relationship
- **Heatmap** — Session activity density over time

## Threat Dashboard

The Threat dashboard (`threat-panos.json`) focuses on security engine events (virus, spyware, IPS, URL filtering, file blocking). It has a different tab structure from Traffic:

### Tab Structure

| Tab | Purpose |
|-----|---------|
| `summary` | Aggregated view across all threat subtypes |
| `$subtype` | Dynamic per-subtype breakdown — one tab per active subtype (virus, spyware, vulnerability, url, etc.) |

The dynamic `$subtype` tab pattern means the dashboard automatically adapts to whatever threat subtypes are present in your data.

### Threat Rows

Each tab contains rows for: Metrics, Action, Geo, Source\|Destination, Application, Rule, and threat-specific dimensions:

- **Subtype row** — breakdown by `panos.subtype` (virus, spyware, vulnerability, url, file, wildfire…)
- **Threat ID | Threat Category | Misc** row — `panos.threatid`, `panos.threat_category`, severity

### Sankey Diagram

The Threat dashboard uses a Sankey diagram to visualize the relationship between:

```
panos.threat/content_type → panos.action → panos.session_end_reason
```

This is the primary way to answer "when a threat was detected, what did the firewall actually do, and how did the session end?"

## Action vs. Session End Reason

Palo Alto separates the concept of **action** (what the firewall decided to do) from **session_end_reason** (why the session ended). This is different from FortiGate's approach where both concepts collapse into `fgt.action`.

| Scenario | `panos.action` | `panos.session_end_reason` |
|----------|----------------|---------------------------|
| Normal allow | `allow` | `aged-out` or `reset` |
| Blocked by rule | `deny` | `rule-denied` |
| Dropped by threat | `drop` | `threat-detected` |
| Client reset | `reset-client` | `client-rst` |

## Ingest Dashboard

The Ingest dashboard (`ingest-panos.json`) is structurally identical to the FortiGate ingest dashboard, with one key difference: the `type` variable is a **query variable** (not custom) because PAN-OS produces more log types than FortiGate and the set varies by deployment. Available types are discovered dynamically from the data.

Ingest rows:
- **Metrics** — total logs, unique device count, unique vsys, unique type, unique subtype
- **Firewall** — per-device timeseries and bar charts
- **Type** — log type breakdown
- Cross-dimensional matrix: type×subtype, device×direction, device×vsys, device×type

## Key Fields

| Field | Description | Dashboard Usage |
|-------|-------------|-----------------|
| `panos.action` | Action taken by firewall policy | Primary action breakdown |
| `panos.threat/content_type` | Security engine classification | Threat/UTM classification |
| `panos.session_end_reason` | Why the session ended | Connection termination analysis |
| `panos.vsys` | Virtual System | Per-VSYS filtering |
| `panos.srcloc` | Source country (GeoIP) | Geographic analysis |
| `panos.dstloc` | Destination country (GeoIP) | Geographic analysis |
| `panos.subtype` | Log subtype | Threat category (virus, spyware, vulnerability…) |
| `panos.threatid` | Threat signature ID | Threat identification |
| `panos.threat_category` | Threat category | Threat classification |
| `panos.severity` | Severity level | Risk prioritization |
| `network.transport_port` | Normalized port (protocol:port) | Port-based analysis |
| `panos.nat.src` | Source NAT translation | NAT analysis |
| `panos.nat.dst` | Destination NAT translation | NAT analysis |
| `panos.user` | User identity | User tracking |
| `panos.srcuser` | Source user | Authenticated user |
| `panos.rule` | Firewall rule name | Policy attribution |
| `panos.app` | Application detected (deep inspection) | Application visibility |
| `panos.category_of_app` | Application category | Category-based analysis |
| `panos.subcategory_of_app` | Application sub-category | Granular app classification |
| `panos.technology_of_app` | Underlying technology (browser-based, client-server, etc.) | App behavior analysis |
| `panos.risk_of_app` | Risk level (1–5) | Risk prioritization |
| `panos.characteristic_of_app` | Behavioral characteristics (evasive, transfers-files, etc.) | Threat hunting |
| `panos.container_of_app` | Parent application when app runs inside another | Tunneled traffic analysis |
| `panos.tunneled_app` | Application detected inside a tunnel | Tunnel inspection |
| `panos.is_saas_of_app` | Whether the app is SaaS | SaaS visibility |
| `panos.sanctioned_state_of_app` | Whether the app is sanctioned by the organization | Shadow IT detection |
| `panos.from_zone` | Source security zone | Zone flow analysis (chord diagrams) |
| `panos.to_zone` | Destination security zone | Zone flow analysis (chord diagrams) |
| `panos.inbound_if` | Inbound interface | Interface flow analysis |
| `panos.outbound_if` | Outbound interface | Interface flow analysis |

## Overrides

Palo Alto dashboards use Grafana field overrides for:

- **Color thresholds** — Action-based coloring (green=allow, red=deny/drop)
- **Unit scaling** — Bytes displayed as KB/MB/GB automatically
- **Custom display** — IPs and users shown as drill-down links
- **Geo visualization** — Country codes mapped to world map

## Dashboard Files

| Dashboard | File | Description |
|-----------|------|-------------|
| Traffic | `traffic-panos.json` | Session/connection analysis |
| Threat | `threat-panos.json` | Security event analysis (virus, spyware, IPS, URL) |
| Ingest | `ingest-panos.json` | Ingestion health and throughput |
| Log Fields | `log-fields-panos.json` | Raw field explorer |
| Streams | `streams-panos.json` | Data stream statistics |
