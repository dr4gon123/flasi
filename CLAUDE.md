# CLAUDE.md

FLASI is a full analytics platform for threat hunting with Fortinet datasources. It integrates Fortinet logs (FortiGate, FortiEDR, FortiMail, FortiWeb) and Palo Alto PAN-OS logs with multiple storage backends (Elasticsearch, Victoria Logs) and visualization platforms (Kibana, Grafana).

**Key Architecture Principle**: Modular design with decoupled layers — data sources, ingestion, storage, and visualization are independent and swappable.

Each component has its own `CLAUDE.md` with component-specific commands and gotchas:
- [`vector/CLAUDE.md`](vector/CLAUDE.md) — Vector.dev ingestion pipelines and VRL transforms
- [`ELK/CLAUDE.md`](ELK/CLAUDE.md) — Elasticsearch index templates, ingest pipelines, Kibana dashboards
- [`grafana/CLAUDE.md`](grafana/CLAUDE.md) — Grafana dashboards (JSON + future SDK)
- [`docs/CLAUDE.md`](docs/CLAUDE.md) — MkDocs documentation site

## Repository Structure

```
vector/          # Vector ingestion pipelines (recommended ingestion method)
ELK/             # Elasticsearch configuration: templates, pipelines, Kibana dashboards
grafana/         # Grafana dashboard JSON files, organized by datasource
docs/            # MkDocs documentation source
quickwit/        # Quickwit configuration (experimental)
victorialogs/    # Victoria Logs configuration (recommended storage)
datasets/        # Tools for processing Fortinet log reference PDFs into ES mappings
```

## Data Flow

```
Fortinet device (RFC5424 syslog)
  → Vector (parse KV into fgt.* namespace, map to ECS, route by log type)
  → Victoria Logs (recommended) or Elasticsearch
  → Grafana or Kibana dashboards
```

## Data Streams

| Stream | Content | Volume |
|--------|---------|--------|
| `logs-fortinet.fortigate.traffic` | Traffic/firewall logs | Highest |
| `logs-fortinet.fortigate.utm` | Web filter, AV, IPS | Medium |
| `logs-fortinet.fortigate.event` | System events | Low |
| `logs-fortinet.fortiedr` | FortiEDR security events | — |
| `logs-fortinet.fortimail` | Email security logs | — |
| `logs-fortinet.forticlient` | Endpoint logs | — |

## ECS Mapping Philosophy

- Raw Fortinet fields stored under `fgt.*` namespace to avoid ECS conflicts
- Fortinet fields translated to ECS equivalents in pipelines/transforms
- Custom non-ECS fields: `*.locality` (IP classification), `network.protocol_category`, `event.hour_of_day`, `event.day_of_week`

## FortiGate Log Quirks

**Null Values**: FortiGate fills empty fields with `"N/A"` — pipelines must convert these to actual nulls before IP field mapping.

**logid=20 Duplication**: Traffic close-session events duplicate aggregation counts. Dashboards filter them, but logs are kept (useful for forensics).

**Syslog Format**: Must use RFC5424. Firewall hostname must use hyphens not underscores (`MY-FIREWALL` not `MY_FIREWALL`).

**Timezone**: FortiOS 6.2+ includes `tz` field — pipelines extract and use it.

**GTP Type Conflicts**: FortiGate Carrier GTP events cause field type conflicts (`checksum`, `from`, `to`, `version` can be string or uint32). GTP events are excluded from mappings.

## Technology Stack

| Layer | Recommended | Alternative |
|-------|-------------|-------------|
| Ingestion | Vector | Elastic Agent |
| Storage | Victoria Logs | Elasticsearch |
| Visualization | Grafana | Kibana |

Logstash is **deprecated** — do not use.

## Performance

- Monitor UDP drops: `watch -d "column -t /proc/net/snmp | grep -w Udp"`
- Use Vector "throughput" preset for high EPS environments
- Transforms aggregate traffic into 1-minute summaries for policy analysis
