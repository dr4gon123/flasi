# grafana/CLAUDE.md

Grafana dashboards for FLASI. Currently stored as Grafana-native JSON exports, organized by datasource.

## File Structure

```
grafana/
├── Fortigate/
│   ├── traffic.json      # Traffic/firewall sessions
│   ├── utm.json          # UTM (web filter, AV, IPS)
│   ├── system.json       # System events
│   ├── ssl vpn.json      # SSL VPN sessions
│   ├── ingest.json       # Ingestion monitoring
│   ├── log fields.json   # Raw field explorer
│   └── streams.json      # Data stream stats
├── FortiEDR/
│   └── security.json
├── Fortimail/
│   └── ...
├── Fortiweb/
│   └── ...
├── Cortex/
│   └── cortex.json
└── Palo Alto/
    ├── traffic.json
    ├── threat.json
    ├── ingest.json
    ├── log fields.json
    └── streams.json
```

## Dashboard Format

Files are Grafana-native JSON exports (not Grafana provisioning YAML). Import via:
- Grafana UI: **Dashboards → Import → Upload JSON file**
- Grafana API: `POST /api/dashboards/import`

## gcx CLI (Grafana Command-Line Tool)

`gcx` is not yet installed — it will be used for interacting with Grafana via the API (push/pull dashboards, manage datasources, etc.). Install when available:
```bash
# Check for gcx installation
gcx version
```

Once installed, typical workflows:
```bash
gcx dashboard push grafana/Fortigate/traffic.json   # Push to Grafana instance
gcx dashboard pull --uid <uid> -o grafana/Fortigate/ # Pull and save locally
```

## Dashboard Philosophy

Dashboards follow FortiGate's Logs & Report structure — 3-layer hierarchy:

1. **Top Level**: Log type (traffic, UTM, event) — header navigation
2. **Middle Level**: Traffic direction (Outbound, Inbound, LAN-to-LAN)
3. **Bottom Level**: Metric type (session count, bytes sum/average)

**Layout pattern**:
- Upper panels: datasource-specific fields, split by action (allow/block)
- Lower panels: common entities (source.ip, destination.ip, network.protocol)
- Dashboard controls: filters for quick data slicing

## Future: Programmatic Dashboard Building

The grafana directory will expand to include a Grafana SDK setup for building dashboards as code. Goals:
- Generate dashboard JSON programmatically instead of hand-editing
- Unit test dashboard definitions
- Diff dashboards in code review

When implemented, add build and test commands here.

## Key Security Indicators (KSIs)

Dashboards aim to surface entity-behavior analytics — not just raw logs, but patterns like:
- Top talkers by bytes and sessions over time
- Allowed vs blocked traffic ratio per source
- Unusual ports or protocols per entity
