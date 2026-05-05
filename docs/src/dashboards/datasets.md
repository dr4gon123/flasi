# Datasets

Analyzing firewall field datasets is a massive undertaking in itself. This work is dependent on firewall vendor version releases (e.g., FortiOS 7.2 → 7.4 → 7.6), each introducing new log fields, deprecated fields, and schema changes. Additionally, each firewall vendor has specific needs — FortiGate fields differ significantly from Palo Alto PAN-OS, and both require dedicated tooling to scrape, normalize, and maintain over time. As such, field schema analysis has been migrated to two dedicated repositories.

## [FLORES](https://github.com/dr4gon123/flores) — FortiGate Log Reference Scraper

FLORES extracts FortiGate log field documentation from Fortinet's official Log Message Reference and transforms it into structured CSV datasets. It covers all three log types (Traffic, Event, UTM) across FortiOS major versions (7.2, 7.4, 7.6) and produces:

- **Per-LOGID CSVs** — raw field tables scraped directly from Fortinet docs
- **Consolidated field CSVs** — aggregated across all minor versions per log type
- **ECS mappings** — FortiGate fields mapped to Elastic Common Schema targets
- **Changelogs and field matrices** — tracking schema evolution between minor versions

FLASI's `ELK/elasticsearch_mappings.py` fetches the consolidated CSVs from this repo to generate Elasticsearch component templates.

## [PALOS](https://github.com/dr4gon123/palos) — PAN-OS Log Scraper

PALOS extracts Palo Alto Networks PAN-OS syslog field documentation from the official docs site and transforms it into structured CSV datasets. It covers 17 log types (Traffic, Threat, URL Filtering, Decryption, GlobalProtect, and more) for PAN-OS 11.1+ and produces:

- **Format CSVs** — the raw comma-separated format string as PAN-OS documents it, plus a snake_case variable name version
- **Field CSVs** — the full field reference table with variable names extracted and normalized
- **Consolidated matrices** — field × log type occurrence across all scraped types
- **ECS mappings** — PAN-OS fields mapped to Elastic Common Schema targets

Both repos include corrections for documentation inconsistencies in their respective vendor sources, catalogued in their `EDGE_CASES.md` / `ANALYSIS.md` files.
