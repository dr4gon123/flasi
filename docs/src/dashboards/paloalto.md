# Palo Alto Dashboard Reference

This page documents the specific variables, fields, and query patterns used in Palo Alto PAN-OS dashboards.

## Variables

| Variable | Query Source | Notes |
|----------|--------------|-------|
| `firewall` | `_stream: {panos.type=$type}` | Populated from `panos.device_name` |
| `vsys` | `_stream: {panos.type=$type, panos.device_name in (${firewall})}` | Virtual System from `panos.vsys` |
| `type` | Custom | Default: `traffic` (options: `traffic`, `threat`, `url`, etc.) |
| `subtype` | Query | From `panos.subtype` — varies by log type |
| `direction` | Custom | Options: `outbound`, `inbound`, `internal`, `external` |
| `action` | Query | From `panos.action` — `allow`, `deny`, `drop`, `reset-both`, etc. |
| `Logsql` | Text | Custom filter, default `*` |

## Base Query

```plaintext
_stream:{panos.device_name in(${firewall:doublequote}),panos.vsys in(${vsys:doublequote}),panos.type=${type:doublequote},panos.subtype in(${subtype:doublequote}),network.direction=${direction:doublequote}}
| panos.action:in(${action:doublequote}) AND ${Logsql:raw}
| stats by (panos.srcloc) count() results
```

## Key Fields

| Field | Description | Dashboard Usage |
|-------|-------------|-----------------|
| `panos.action` | Action taken by firewall policy | Primary action breakdown |
| `panos.threat/content_type` | Security engine action | Threat/UTM classification |
| `panos.session_end_reason` | Why the session ended | Connection termination analysis |
| `panos.vsys` | Virtual System | Per-VSYS filtering |
| `panos.srcloc` | Source country (GeoIP) | Geographic analysis |
| `panos.dstloc` | Destination country (GeoIP) | Geographic analysis |
| `network.transport_port` | Normalized port (protocol:port) | Port-based analysis |
| `panos.pcap_id` | Packet capture ID | Packet capture linkage |
| `panos.nat.src` | Source NAT translation | NAT analysis |
| `panos.nat.dst` | Destination NAT translation | NAT analysis |
| `panos.user` | User identity | User tracking |
| `panos.srcuser` | Source user | Authenticated user |
| `panos.rule` | Firewall rule name | Policy attribution |
| `panos.app` | Application detected | Application visibility |
| `panos.app_category` | Application category | Category-based analysis |

## Action vs. Session End Reason

Palo Alto separates the concept of **action** (what the firewall decided to do) from **session_end_reason** (why the session ended). This is different from FortiGate's approach.

| Scenario | `panos.action` | `panos.session_end_reason` |
|----------|----------------|---------------------------|
| Normal allow | `allow` | `aged-out` or `reset` |
| Blocked by rule | `deny` | `rule-denied` |
| Dropped by threat | `drop` | `threat-detected` |
| Client reset | `reset-client` | `client-rst` |

## Threat Dashboard

The Threat dashboard (`threat-panos.json`) uses a different structure focused on security events:

- **Sankey Diagram** — Visualizes the relationship between `threat/content_type`, `action`, and `session_end_reason`
- **Threat Type breakdown** — Category of detected threat (virus, spyware, vulnerability, etc.)
- **Severity analysis** — Critical, high, medium, low, informational

## Log Types

PAN-OS produces multiple log types, each with its own dashboard:

| Log Type | Dashboard | Description |
|----------|-----------|-------------|
| Traffic | `traffic-panos.json` | Session logs with allow/deny decisions |
| Threat | `threat-panos.json` | Security threat events (virus, spyware, IPS) |
| URL | (future) | URL filtering logs |
| Decryption | (future) | SSL/TLS decryption events |
| GlobalProtect | (future) | VPN and remote access logs |

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
| Threat | `threat-panos.json` | Security event analysis |
| Ingest | `ingest-panos.json` | Ingestion health and throughput |
| Log Fields | `log-fields-panos.json` | Raw field explorer |
| Streams | `streams-panos.json` | Data stream statistics |