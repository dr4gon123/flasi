# ELK/CLAUDE.md

Elasticsearch configuration for FLASI — index templates, ingest pipelines, ILM policies, transforms, and Kibana dashboards.

## Commands

**Deploy everything to Elasticsearch:**
```bash
cd ELK
./load.sh
```

**Copy `.env.example` to `.env` for local config (gitignored):**
```bash
cp .env.example .env
# Edit .env with your ES_URL, credentials, etc.
```

**Generate FortiGate component templates from datasets:**
```bash
python elasticsearch_mappings.py
# Output goes to datasets/Fortinet/Fortigate/<version>/elasticsearch_templates/
# Then copy to ELK/index_templates/component_templates/ for deployment
```

## load.sh Environment Variables

All variables can be set in `.env` or exported before running `load.sh`.

| Variable | Default | Description |
|----------|---------|-------------|
| `ES_URL` | `https://localhost:9200` | Elasticsearch endpoint |
| `AUTH_METHOD` | `user` | `user` or `apikey` |
| `ES_USERNAME` | `elastic` | Username (when `AUTH_METHOD=user`) |
| `ES_PASSWORD` | `changeme` | Password (when `AUTH_METHOD=user`) |
| `ES_API_KEY` | — | API key (when `AUTH_METHOD=apikey`) |
| `INSECURE` | `false` | Set `true` to skip SSL cert validation |
| `LOAD_ECS` | `true` | Load ECS component templates |
| `LOAD_COMPONENT` | `true` | Load FLASI component templates |
| `LOAD_ILM` | `true` | Load ILM policies |
| `LOAD_INDEX_TEMPLATES` | `true` | Load index templates |
| `LOAD_INGEST_PIPELINES` | `false` | Load ingest pipelines |
| `LOAD_TRANSFORMS` | `false` | Load transforms |
| `CONTINUE_ON_ERROR` | `true` | Continue if one component fails |
| `VERBOSE` | `false` | Detailed output |

**Example — remote cluster with API key:**
```bash
ES_URL=https://elastic.example.com:9200 AUTH_METHOD=apikey ES_API_KEY=abc123 ./load.sh
```

## Directory Structure

```
ELK/
├── load.sh                        # Deployment script
├── .env.example                   # Environment variable template
├── elasticsearch_mappings.py      # Generates fortigate_* component templates from datasets
│
├── index_templates/
│   ├── component_templates/       # Building blocks composed into index templates
│   │   ├── ecs-*                  # ECS fieldsets (fetched from elastic/ecs by load.sh)
│   │   ├── fortigate_{type}_{ver} # fgt.* field mappings per log type and FortiOS version
│   │   ├── logs-fortinet.*@ilm   # ILM policy references per data stream
│   │   └── strings_as_keyword@mappings, auto_expand_replicas@settings, etc.
│   ├── ilm/                       # ILM policy definitions (retention periods)
│   └── index_templates/           # Full index templates composing the above
│
├── ingest_pipelines/              # Elasticsearch ingest pipelines (JSON)
├── transforms/                    # 1-minute traffic aggregation transforms
├── kibana/                        # Kibana dashboard exports (.ndjson)
└── logstash (deprecated)/         # Legacy — do not use
```

## Ingest Pipelines

Pipeline filenames match the data stream they process: `logs-fortinet.fortigate.json` handles `logs-fortinet.fortigate.*`.

**Processing order within each pipeline:**
1. Set `event.ingested` timestamp
2. Remove conflicting fields (`host`, `cloud`, `agent`)
3. KV-parse `message` into `fgt.*` namespace
4. Map `fgt.*` fields to ECS (`source.*`, `destination.*`, `network.*`, `observer.*`)
5. Enrich (GeoIP, registered domain, user_agent parsing)
6. Derive fields (`network.community_id`, `network.bytes`, `event.duration`)
7. Set `event.kind`, `event.category`, `event.type` by log subtype

Files with `.deprecated` extension are kept for reference and are not loaded by `load.sh`.

## Kibana Dashboards

Dashboards are stored as `.ndjson` exports in `kibana/`. Filename format: `<product> ELK <kibana_version>.ndjson`.

**Import via Kibana UI**: Stack Management → Saved Objects → Import

**Import via API:**
```bash
curl -X POST "$ES_URL/../api/saved_objects/_import" \
  -H "kbn-xsrf: true" \
  --form file=@kibana/"fortigate ELK 871.ndjson"
```

All dashboards use Kibana Lens. The `logid=20` (close-session) duplicate filter is applied at the dashboard level, not dropped at ingest.

## Component Template Versioning

FortiGate field mappings are versioned by FortiOS release:
- `fortigate_traffic_72` — FortiOS 7.2
- `fortigate_traffic_74` — FortiOS 7.4
- `fortigate_traffic_76` — FortiOS 7.6

Index templates compose the relevant versioned component template. Current coverage: 7.2, 7.4, 7.6.
