# FortiGate

This page documents the specific variables, fields, and query patterns used in FortiGate dashboards.

## Variables

| Variable | Query Source | Notes |
|----------|--------------|-------|
| `firewall` | `_stream: {fgt.type=$type}` | Populated from `log.syslog.hostname` |
| `vdom` | `_stream: {fgt.type=$type, log.syslog.hostname in (${firewall})}` | Virtual Domain from `fgt.vd` |
| `type` | Custom | Default: `traffic` (options: `traffic`, `utm`, `event`) |
| `subtype` | `_stream: {fgt.type=$type, log.syslog.hostname in (${firewall}), fgt.vd in (${vdom})}` | From `fgt.subtype` — typically `forward`, `local`, `multicast` |
| `policytype` | Same as subtype | From `fgt.policytype` — typically `policy`. **FortiGate-only**, no equivalent in PAN-OS |
| `direction` | Custom | Options: `outbound`, `inbound`, `internal`, `external` |
| `action` | Base stream query | From `fgt.action` — `accept`, `drop`, `deny`, `close`, etc. |
| `Logsql` | Text | Custom filter, default `*` |

## Base Query

```plaintext
_stream:{log.syslog.hostname in (${firewall:doublequote}),fgt.vd in (${vdom:doublequote}),fgt.type=${type:doublequote},fgt.subtype=${subtype:doublequote},fgt.policytype=${policytype:doublequote},network.direction in (${direction:doublequote}),fgt.logid!=0000000020}
| fgt.action:in(${action:doublequote}) AND ${Logsql:raw}
| NOT fgt.srccountry:Reserved
| stats by (fgt.srccountry) count() results
```

!!! note "Log ID Exclusion"
    The query filters out `fgt.logid!=0000000020` to avoid duplicate traffic close-session events that inflate counts. These events duplicate aggregation counts from the initial session open.

## Traffic Dashboard

The Traffic dashboard (`traffic-fortios.json`) is organized into direction tabs (outbound/inbound/internal/external), each with two metric sub-tabs:

| Sub-tab | Metric |
|---------|--------|
| Sessions | `count()` — one log ≈ one connection |
| Bytes | `sum(bytes)` — total volume transferred |

Within each sub-tab, rows follow the standard [panel hierarchy](usage.md#panel-hierarchy): Metrics → Action → Geo → Source\|Destination → Application → Rule.

Notable Traffic panels:
- **Sankey diagram** — Visualizes the flow from `fgt.action` to `fgt.utmaction`
- **Geomap** — Source and destination country distribution
- **Heatmap** — Session activity density over time

## UTM Dashboard

The UTM dashboard (`utm-fortios.json`) focuses on security engine events. It has the same direction-based tab structure as Traffic.

### crscore Variable

The UTM dashboard adds a unique `crscore` **switch variable** that applies a risk score threshold filter when enabled. This allows toggling between "all UTM events" and "high-risk UTM events only" without modifying the base query.

### UTM Base Query

```plaintext
_stream:{fgt.type=${type:doublequote},fgt.subtype=${subtype:doublequote},log.syslog.hostname in (${firewall:doublequote}),fgt.vd in (${vdom:doublequote}),network.direction in (${direction:doublequote})}
| fgt.action:in(${action:doublequote}) AND ${Logsql:raw} AND ${crscore:raw}
| fgt.virus:*
| stats by (fgt.virus,fgt.action) count() results
| sort by (results) desc
| limit 10
```

### UTM Engines

FortiGate dashboards break down UTM actions by engine:

| Engine | Key Fields | Description |
|--------|------------|-------------|
| Web Filter | `fgt.webfilter`, `fgt.catdesc` | URL category and filter action |
| Application Control | `fgt.appcapapp`, `fgt.appcat` | Application control signature |
| Antivirus | `fgt.virus`, `fgt.viruscat` | Virus name and category matched |
| IPS | `fgt.attack`, `fgt.severity` | IPS signature matched |
| Email Filter | `fgt.emailfilter` | Email filtering action |
| DLP | `fgt.dlp` | Data Loss Prevention action |

## Risk Score

FortiGate dashboards include **Risk Score** analysis based on Fortinet's [Threat Weight](https://docs.fortinet.com/document/fortigate/7.2.0/administration-guide/903511/threat-weight) configuration.

This feature is unique to FortiGate and not available in Palo Alto dashboards.

## Key Fields

| Field | Description | Dashboard Usage |
|-------|-------------|-----------------|
| `fgt.action` | Action taken by firewall policy | Primary action breakdown |
| `fgt.utmaction` | Action taken by UTM engine when triggered | Secondary action analysis |
| `fgt.vd` | Virtual Domain | Per-VDOM filtering |
| `fgt.logid` | Log ID identifying the event type | Exclude duplicates (`!=0000000020`), categorize |
| `fgt.srccountry` | Source country (GeoIP) | Geographic analysis |
| `fgt.dstcountry` | Destination country (GeoIP) | Geographic analysis |
| `fgt.srcreputation` | [IP Reputation](https://docs.fortinet.com/document/fortigate/7.6.4/administration-guide/68937/ip-reputation-filtering) category | Threat intelligence |
| `fgt.dstreputation` | Destination IP reputation | Threat intelligence |
| `fgt.service` | Policy-defined service or Internet Service | Service analysis |
| `network.transport_port` | Normalized port (protocol:port) | Port-based analysis |
| `fgt.appcat` | Application category | Application visibility |
| `network.application` | Detected application | Application details |
| `fgt.user` | Authenticated user | User tracking |
| `fgt.srcname` | Source device name | Device visibility |
| `fgt.dstname` | Destination hostname | Destination identification |
| `rule.id_name` | Firewall policy name | Policy attribution |
| `fgt.virus` | Virus/malware name (UTM) | Threat analysis |
| `fgt.viruscat` | Virus category (UTM) | Threat categorization |
| `fgt.attack` | IPS attack name (UTM) | IPS analysis |
| `fgt.severity` | Severity level (UTM) | Risk prioritization |

## Overrides

The dashboards use Grafana field overrides for:

- **Color thresholds** — Action-based coloring (green=accept, red=drop)
- **Unit scaling** — Bytes displayed as KB/MB/GB automatically
- **Hidden fields** — Internal fields excluded from tables
- **Custom display** — IP addresses shown as clickable drill-down links

## Dashboard Files

| Dashboard | File | Description |
|-----------|------|-------------|
| Traffic | `traffic-fortios.json` | Session/connection analysis |
| UTM | `utm-fortios.json` | Web filter, AV, IPS analysis |
| Event | `system-fortios.json` | System events and configuration changes |
| SSL VPN | `ssl-vpn-fortios.json` | VPN session analysis |
| Ingest | `ingest-fortios.json` | Ingestion health and throughput |
| Log Fields | `log-fields-fortios.json` | Raw field explorer |
| Streams | `streams-fortios.json` | Data stream statistics |
