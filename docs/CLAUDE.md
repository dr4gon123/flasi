# docs/CLAUDE.md

MkDocs documentation site for FLASI, using the Material theme. Config is `docs/mkdocs.yml`, source pages are in `docs/src/`, built output goes to `site/` at the repo root.

## Commands

```bash
# From repo root:
mkdocs serve -f docs/mkdocs.yml    # Local preview at http://127.0.0.1:8000
mkdocs build -f docs/mkdocs.yml    # Build static site into site/

# Or from inside docs/:
mkdocs serve
mkdocs build
```

## Directory Structure

```
docs/
├── mkdocs.yml        # MkDocs config (docs_dir: src, site_dir: ../site)
├── CLAUDE.md         # This file
└── src/              # All MkDocs source content lives here
    ├── index.md
    ├── architecture.md
    ├── engage.md
    ├── roadmap.md
    ├── assets/           # Images and static files
    ├── dashboards/       # Dashboard documentation
    └── installation/     # Setup guides per component
        ├── datasource/   # FortiGate syslog config
        ├── ingest/       # Vector, Elastic Agent
        ├── storage/      # Victoria Logs, Elasticsearch
        └── viz/          # Grafana, Kibana
```

## Navigation

Navigation is managed by the **awesome-pages** plugin — no manual `nav:` block needed in `mkdocs.yml` (it's commented out). To control page order within a directory, add a `.pages` file:

```yaml
# docs/installation/.pages
nav:
  - index.md
  - datasource
  - ingest
  - storage
  - viz
```

## Active Plugins

| Plugin | Purpose |
|--------|---------|
| `awesome-pages` | Auto-discovery + `.pages` file ordering |
| `git-revision-date-localized` | "Last updated X ago" on each page |
| `glightbox` | Lightbox for images (loop mode enabled) |
| `social` | Auto-generated social cards |
| `minify` | HTML minification for production builds |
| `search` | Full-text search |

## Markdown Features Available

- **Mermaid diagrams**: Use ` ```mermaid ` fenced blocks
- **Admonitions**: `!!! note`, `!!! warning`, `!!! tip`, etc.
- **Tabbed content**: `=== "Tab 1"` via `pymdownx.tabbed`
- **Collapsible blocks**: `??? note` (closed by default) via `pymdownx.details`
- **Code annotations**: Add `# (1)` in code, then `1. explanation` below
- **Keyboard shortcuts**: `++ctrl+c++` renders as Ctrl+C
- **Highlighted text**: `==highlighted==`
- **Strikethrough**: `~~deleted~~`
- **Task lists**: `- [x] done` / `- [ ] todo`
- **Footnotes**: `[^1]` with `[^1]: explanation` at the bottom
- **Image captions**: Use `/// caption` block after an image

## Theme Notes

- Scheme: auto (follows OS dark/light preference), primary color: black
- Logo: `fontawesome/solid/dragon`
- Features enabled: `navigation.expand`, `navigation.path`, `navigation.top`, `search.highlight`, `toc.follow`
- `toc.integrate` and `navigation.tabs` are commented out — enable in `mkdocs.yml` if needed

## Deployment

The site is published to GitHub Pages at `https://dr4gon123.github.io/flasi/`. Versioning provider is `mike` (configured in `mkdocs.yml` extras).
