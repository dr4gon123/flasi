# grafana/CLAUDE.md

Grafana dashboards for FLASI. Stored as Grafana SDK v2 JSON (`apiVersion: dashboard.grafana.app/v2`), organized by environment and datasource.

## File Structure

```
grafana/
├── dev/                        # Authoring environment (tag: "dev")
│   ├── FortiGate/
│   │   ├── _folder.json
│   │   ├── traffic-fortios.json
│   │   ├── utm-fortios.json
│   │   ├── system-fortios.json
│   │   ├── ssl-vpn-fortios.json
│   │   ├── ingest-fortios.json
│   │   ├── log-fields-fortios.json
│   │   └── streams-fortios.json
│   ├── Palo Alto/
│   │   ├── _folder.json
│   │   ├── traffic-panos.json
│   │   ├── threat-panos.json
│   │   ├── ingest-panos.json
│   │   ├── log-fields-panos.json
│   │   └── streams-panos.json
│   ├── FortiWeb/
│   │   ├── _folder.json
│   │   ├── traffic-fortiweb.json
│   │   ├── attack-fortiweb.json
│   │   └── attack-fortiappsec.json
│   ├── FortiEDR/
│   │   ├── _folder.json
│   │   └── security-fortiedr.json
│   ├── FortiMail/
│   │   ├── _folder.json
│   │   └── statistics-fortimail.json
│   └── Cortex/
│       ├── _folder.json
│       └── cortex-palo-alto.json
├── prod/                       # Production environment (tag: "prod"), mirrors dev/
│   └── <same structure as dev/>
└── promote.py                  # Promotion script: dev → prod
```

`_folder.json` defines the Grafana folder for each vendor group.

## Dev / Prod Split

Dashboards are authored in `dev/` and promoted to `prod/` when ready. The only difference between environments is the tag (`"dev"` vs `"prod"`), which controls which dashboards appear in each environment's nav link dropdowns.

## Promoting Dashboards

```bash
# Promote a single dashboard
python3 grafana/promote.py --file grafana/dev/FortiGate/traffic-fortios.json

# Promote an entire vendor folder
python3 grafana/promote.py --vendor FortiGate
python3 grafana/promote.py --vendor "Palo Alto"
```

`promote.py` copies the file to the mirrored `prod/` path and swaps the `"dev"` tag to `"prod"` in both `spec.tags` and `spec.links[].tags`. The dev source is never modified.

A GitHub Actions workflow (`promote-dashboard.yml`) does the same via `workflow_dispatch` and opens a PR.

**Nav link consistency**: each dashboard's nav dropdowns filter peers by tag. Promoting a single dashboard while leaving siblings in dev means those dropdowns show incomplete results until all siblings are promoted.

## Dashboard Format

Files use Grafana SDK v2 format:
```json
{
  "apiVersion": "dashboard.grafana.app/v2",
  "kind": "Dashboard",
  "metadata": { "name": "<uid>" },
  "spec": { ... }
}
```

Import via Grafana UI (**Dashboards → Import → Upload JSON**) or API:
```bash
curl -X POST http://grafana:3000/api/dashboards/import \
  -H "Content-Type: application/json" \
  -d @grafana/dev/FortiGate/traffic-fortios.json
```

## Nav Links

Every dashboard carries a nav link bar linking to sibling dashboards within the same vendor. Links filter by tag — the tag set must match the dashboard's own `spec.tags`. When adding a new dashboard, give it the correct vendor + environment tags so it appears in the nav dropdowns of its peers.

## Dashboard Philosophy

Dashboards follow FortiGate's Logs & Report structure — 3-layer hierarchy:

1. **Top Level**: Log type (traffic, UTM, event) — header navigation
2. **Middle Level**: Traffic direction (Outbound, Inbound, LAN-to-LAN)
3. **Bottom Level**: Metric type (session count, bytes sum/average)

**Layout pattern**:
- Upper panels: datasource-specific fields, split by action (allow/block)
- Lower panels: common entities (source.ip, destination.ip, network.protocol)
- Dashboard controls: filters for quick data slicing

## Key Security Indicators (KSIs)

Dashboards surface entity-behavior analytics — not just raw logs, but patterns like:
- Top talkers by bytes and sessions over time
- Allowed vs blocked traffic ratio per source
- Unusual ports or protocols per entity
