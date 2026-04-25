# Vector

This page covers Vector configuration for FLASI, based on the existing vector documentation.

## Install as a service

There are many ways for [installing Vector](https://vector.dev/docs/setup/installation/). Normally, for a Linux environment, you will [install it as a service](https://vector.dev/docs/setup/installation/package-managers/yum/), so you may need to make some adjustments for Vector to load multiple config files from a directory.

## Load multiple config files

We have split Vector config [files](https://github.com/dr4gon123/flasi/tree/main/vector) by platform, with pipelines (sources + transforms) in `vector/` and sinks in `vector/sinks/`.

### Enabling and disabling configs

The entire configuration is controlled by file extensions:

- **`.yaml`** — file is **active** and loaded by Vector
- **`.yaml.disabled`** — file is **ignored** by Vector

To enable a file, rename it to end in `.yaml`. To disable it, rename it to end in `.yaml.disabled`. No YAML editing required.

This applies to every file in both `vector/` and `vector/sinks/`.

### Example: FortiGate-only deployment

If you only receive FortiGate logs, disable every pipeline and sink for other platforms:

```bash
# Disable other platform pipelines
mv /etc/vector/panos.yaml             /etc/vector/panos.yaml.disabled
mv /etc/vector/fortiedr.yaml          /etc/vector/fortiedr.yaml.disabled
mv /etc/vector/fortimail.yaml         /etc/vector/fortimail.yaml.disabled
mv /etc/vector/fortiweb.yaml          /etc/vector/fortiweb.yaml.disabled
mv /etc/vector/fortiappsec.yaml       /etc/vector/fortiappsec.yaml.disabled
mv /etc/vector/cortex.yaml            /etc/vector/cortex.yaml.disabled

# Disable matching sinks
mv /etc/vector/sinks/vlogs_panos.yaml /etc/vector/sinks/vlogs_panos.yaml.disabled
# ... repeat for any other non-FortiGate sinks
```

### Monitoring files

`vector.yaml` (enables the Vector API) and the `*_monitoring.yaml` files are optional — they are only needed if you want to monitor Vector's own performance metrics. All other pipelines work without them.

### Full directory layout

```
/etc/vector/
├── vector.yaml               # Optional: enables Vector API
├── vector_monitoring.yaml    # Optional: Vector self-monitoring
├── victoria_monitoring.yaml  # Optional: Victoria Logs monitoring
├── fortigate.yaml            # FortiGate pipeline (source + transforms)
├── fortiedr.yaml
├── fortimail.yaml
├── fortiweb.yaml
├── fortiappsec.yaml
├── panos.yaml
├── cortex.yaml
├── iana.yaml
├── iana_number.csv
└── sinks/
    ├── vlogs_fortigate.yaml              # ✅ Victoria Logs (enabled by default)
    ├── vlogs_fortigate_traffic.yaml      # ✅ Victoria Logs
    ├── vlogs_panos.yaml                  # ✅ Victoria Logs
    ├── vlogs_fortiedr.yaml               # ✅ Victoria Logs
    ├── vlogs_fortimail.yaml              # ✅ Victoria Logs
    ├── vlogs_fortiweb.yaml               # ✅ Victoria Logs
    ├── vlogs_fortiappsec.yaml            # ✅ Victoria Logs
    ├── vlogs_cortex.yaml                 # ✅ Victoria Logs
    ├── elastic_fortigate.yaml.disabled   # ❌ Elasticsearch (disabled)
    ├── elastic_panos.yaml.disabled       # ❌ Elasticsearch (disabled)
    ├── loki_fortigate.yaml.disabled      # ❌ Loki (disabled)
    ├── quickwit_fortigate.yaml.disabled  # ❌ Quickwit (disabled)
    └── ...
```

However, Vector only loads `vector.yaml` by [default](https://vector.dev/docs/reference/configuration/#location). We need to make some adjustments on the service so it will load all files on the folder.

Edit vector service to load config files from `/etc/vector`:

```bash
sudo systemctl edit vector
```

Insert config for overridden default config:

```ini
[Service]
ExecStartPre=
ExecStartPre=/usr/bin/vector validate --config-dir /etc/vector

ExecStart=
ExecStart=/usr/bin/vector --config-dir /etc/vector

ExecReload=
ExecReload=/usr/bin/vector validate --no-environment --config-dir /etc/vector
ExecReload=/bin/kill -HUP $MAINPID
```

Restart daemon and service:

```bash
sudo systemctl daemon-reload
sudo systemctl restart vector
```

## Environment Variables

FLASI Vector config files use environmental variables for passing specific values for your setup. All variables have default values in the config files.

`INTERNAL_NETWORKS` is the only variable that must be set.

`INTERNAL_NETWORKS` is used for inferring `network.direction` of connections.

`INTERNAL_NETWORKS` must have your local private network addresses scopes as well as your public facing network addresses scopes.

Create environment variables for Vector config:

```bash
sudo vim /etc/default/vector
```

Add environment variables:

```bash
### Sources ###
#FORTIGATE_SYSLOG_UDP_PORT=5140
#FORTIGATE_SYSLOG_TCP_PORT=5140

#PANOS_SYSLOG_UDP_PORT=6140

#FORTIMAIL_SYSLOG_UDP_PORT=5150

#FORTIWEB_SYSLOG_TCP_PORT=5160
#FORTIAPPSEC_SYSLOG_UDP_PORT=5161

#FORTIEDR_SYSLOG_UDP_PORT=5180


### Sinks ###
#VICTORIA_LOGS_ENDPOINT="http://localhost:9428"
#VICTORIA_LOGS_USER=""
#VICTORIA_LOGS_PASS=""

#ELASTICSEARCH_ENDPOINT="https://localhost:9200"
#ELASTICSEARCH_USER="elastic"
#ELASTICSEARCH_PASS="mypassword"

#LOKI_ENDPOINT="http://localhost:3100"
#LOKI_USER="loki"
#LOKI_PASS="mypassword"

#QUICKWIT_ENDPOINT="http://localhost:7280"
#QUICKWIT_USER="quickwit"
#QUICKWIT_PASS="mypassword"

#PROMETHEUS_ENDPOINT="http://localhost:9090"
#PROMETHEUS_USER="prometheus"
#PROMETHEUS_PASS="mypassword"

### Transforms ###
#TENANT_NAME="mytenant"

INTERNAL_NETWORKS=["10.0.0.0/8","172.16.0.0/12","192.168.0.0/16","fc00::/7"]
```

## Sinks

Vector can send logs to multiple [sinks](https://vector.dev/docs/reference/configuration/sinks/). FLASI ships sink configs for all supported [storages](../../architecture.md/#storage) in `vector/sinks/`, one file per datasource per backend.

!!! info "Default state"
    ✅ [Victoria Logs](../storage/victoria.md) sinks are **enabled** by default (`vlogs_*.yaml`)

    ❌ [Elasticsearch](../storage/elasticsearch.md), [Loki](https://grafana.com/oss/loki/), and [Quickwit](https://quickwit.io/) sinks are **disabled** by default (`*.yaml.disabled`)

To switch backends, enable the sinks you need and disable the rest by renaming files:

```bash
# Enable Elasticsearch for FortiGate
mv /etc/vector/sinks/elastic_fortigate.yaml.disabled \
   /etc/vector/sinks/elastic_fortigate.yaml

# Disable Victoria Logs for FortiGate
mv /etc/vector/sinks/vlogs_fortigate.yaml \
   /etc/vector/sinks/vlogs_fortigate.yaml.disabled

mv /etc/vector/sinks/vlogs_fortigate_traffic.yaml \
   /etc/vector/sinks/vlogs_fortigate_traffic.yaml.disabled
```

You can also send to **multiple backends simultaneously** — just enable more than one sink for the same datasource.

## Vector Buffering

For production deployments, take into account every sink has a section that overrides Vector default values for [buffering](https://vector.dev/docs/architecture/buffering-model/) trying to mimic `Optimized for Throughput` Elastic Agent [settings](https://www.elastic.co/docs/reference/fleet/es-output-settings#es-output-settings-performance-tuning-settings). Vector works really well with defaults. Don't use this section unless you really need to fine-tune your ingest.

```yaml
    buffer:
    - type: memory
      max_events: 12800 # default 500 https://www.elastic.co/docs/reference/fleet/es-output-settings#es-output-settings-performance-tuning-settings
      #when_full: drop_newest #default block
    batch:
      #max_bytes:
      max_events: 1600 # default 1000
      timeout_secs: 5 # default 1
```

## OS Buffering

You can monitor UDP buffer usage with:

```bash
watch -d "cat /proc/net/snmp | column -t | grep -w Udp"
```

If you have errors or are dropping packets, you should increase the buffer size.

Add to `/etc/sysctl.conf` or `/etc/sysctl.d/99-network-tuning.conf`:

```ini
# UDP receive buffer tuning for high-volume logging
net.core.rmem_max = 134217728 # 128MB
net.core.rmem_default = 16777216 # 16MB
net.core.netdev_max_backlog = 5000

# Optional: increase write buffers too if you're forwarding logs
net.core.wmem_max = 134217728 # 128MB
net.core.wmem_default = 16777216 # 16MB
```

Then:

```bash
sudo sysctl -p
```

## Monitoring

We have included 2 files for monitoring Vector itself.

```
/etc/vector/
├── vector_monitoring.yaml
└── vector.yaml
```

`vector.yaml` just enables API.

```yaml
 api:
   enabled: true
   address: "127.0.0.1:8686"
```

and `vector_monitoring.yaml` scrapes metrics and logs. Logs are sent to Loki because it has a [free tier](https://grafana.com/pricing/#logs) which is enough for most cases.

Refer to the [Vector documentation](https://vector.dev/docs/) for detailed configuration options.

## Troubleshooting

After configuration, verify that logs are being received:

1. Monitor network traffic:

   ```bash
   # On your Vector host
   sudo tcpdump -i any port 5140
   ```

2. Make sure you have enabled firewall incomming rules for your Vector ports:

   ```bash
   # On your Vector host
   sudo firewall-cmd --zone=public --permanent --add-port=5140/udp
   sudo firewall-cmd --reload
   ```

3. [Troubleshoot](https://vector.dev/guides/level-up/troubleshooting/) Vector:

   ```bash
   sudo journalctl -fu vector
   ```

## Next Steps

Once Vector is configured:

1. Set up [Victoria Logs](../storage/victoria.md) or [Elasticsearch](../storage/elasticsearch.md)

2. Import dashboards in [Grafana](../viz/grafana.md) or [Kibana](../viz/kibana.md)

3. Start dancing with your logs!
