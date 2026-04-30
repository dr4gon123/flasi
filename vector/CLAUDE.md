# vector/CLAUDE.md

Vector.dev ingestion pipelines for FLASI. Each datasource has its own pipeline file. Sinks are separate and live in `sinks/`.

## File Structure

```
vector/
├── fortigate.yaml        # FortiGate: source (UDP syslog) + VRL transforms
├── fortiedr.yaml         # FortiEDR pipeline
├── fortimail.yaml        # FortiMail pipeline
├── fortiweb.yaml         # FortiWeb pipeline
├── fortiappsec.yaml      # FortiAppSec pipeline
├── panos.yaml            # Palo Alto PAN-OS pipeline
├── cortex.yaml           # Cortex XDR pipeline
├── iana.yaml             # IANA enrichment table definition
├── iana_number.csv       # Protocol number → name lookup (used by enrichment tables)
├── vector.yaml           # Optional: Vector API / playground settings
├── vector_monitoring.yaml    # Optional: Vector self-metrics
├── victoria_monitoring.yaml  # Optional: Victoria Logs health monitoring
└── sinks/
    ├── vlogs_*.yaml              # Victoria Logs (enabled by default)
    ├── elastic_*.yaml.disabled   # Elasticsearch (disabled)
    ├── loki_*.yaml.disabled      # Loki (disabled)
    └── quickwit_*.yaml.disabled  # Quickwit (disabled)
```

## Commands

**Validate all configs (including enabled sinks):**
```bash
vector validate --config-dir .
```
> Requires write access to `/var/lib/vector/` for a temp directory. Run as the vector service user or with sudo if needed.

**Validate a single pipeline + specific sink:**
```bash
vector validate fortigate.yaml sinks/vlogs_fortigate.yaml
```

**Run Vector with this directory:**
```bash
vector --config-dir .
```

**Check UDP packet drops (high-volume monitoring):**
```bash
watch -d "column -t /proc/net/snmp | grep -w Udp"
```

## Enabling / Disabling Backends

Sinks use file extension to control whether they're active:
- `.yaml` → loaded by Vector
- `.yaml.disabled` → ignored by Vector

To switch from Victoria Logs to Elasticsearch for FortiGate:
```bash
mv sinks/vlogs_fortigate.yaml sinks/vlogs_fortigate.yaml.disabled
mv sinks/elastic_fortigate.yaml.disabled sinks/elastic_fortigate.yaml
```

## Pipeline Pattern

Each datasource file follows this structure:

```yaml
sources:
  syslog_fortigate:
    type: syslog
    address: "0.0.0.0:${FORTIGATE_SYSLOG_UDP_PORT:-6140}"
    mode: udp

transforms:
  parse_fortigate:
    type: remap
    inputs: [syslog_fortigate]
    source: |
      # 1. Parse KV pairs into fgt.* namespace
      fgt = parse_logfmt!(.message)
      # 2. Map fgt.* fields to ECS
      # 3. Route by log type
```

Port numbers are configured via environment variables with defaults (e.g., `${FORTIGATE_SYSLOG_UDP_PORT:-6140}`).

## VRL (Vector Remap Language) Gotchas

**`??` is error-fallback, not null-coalescing.** Use it to handle parse errors, not to fall back between null fields:
```vrl
# Wrong — this is error fallback, not "first non-null"
.field = .fgt.srcip ?? .fgt.src

# Right — use an array when multiple fgt fields map to the same ECS target
.source.ip = array([.fgt.srcip, .fgt.src])[0] ?? null
```

**`parse_logfmt!` vs `parse_logfmt`**: The `!` variant aborts on error (use in transforms where malformed input should be dropped). Without `!`, errors are returned as values.


**Enrichment Tables**: Defined in `iana.yaml` and referenced in transforms. The CSV path must match what's configured in `iana.yaml`.

## Elasticsearch Data Stream Routing

Transforms route logs to different outputs by log type, which maps to separate data streams:
- `traffic` → `logs-fortinet.fortigate.traffic`
- `utm` → `logs-fortinet.fortigate.utm`
- `event` → `logs-fortinet.fortigate.event`

This split is important — different ILM policies apply to each stream.
