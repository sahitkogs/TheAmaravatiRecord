# Andhra Record

**Independent data journalism on Andhra Pradesh.**

Live site: <https://sahitkogs.github.io/AndhraRecord/>

A one-desk independent newsroom covering land allocation, construction progress, and the data behind Andhra Pradesh. Bilingual (English + Telugu), CNN-style layout, AI chatbot on every page.

---

## Quick Links

| Page | URL |
|------|-----|
| Language Picker | [/AndhraRecord/](https://sahitkogs.github.io/AndhraRecord/) |
| Home (EN) | [/AndhraRecord/en/](https://sahitkogs.github.io/AndhraRecord/en/) |
| Home (TE) | [/AndhraRecord/te/](https://sahitkogs.github.io/AndhraRecord/te/) |
| Reports | [/AndhraRecord/en/pages/reports.html](https://sahitkogs.github.io/AndhraRecord/en/pages/reports.html) |
| Caste Dashboard | [/AndhraRecord/en/reports/lps-caste-dashboard.html](https://sahitkogs.github.io/AndhraRecord/en/reports/lps-caste-dashboard.html) |
| Capital Tracker | [amaravati-tracker-staging](https://sahitkogs.github.io/amaravati-tracker-staging/) (separate repo) |

---

## Key Investigation

**47,993 land plots** analysed from the APCRDA Land Pooling Scheme across 26 villages. **Kamma: 57.4%** of plots — the single largest beneficiary community. **99.6%** of farmer names identified. See [full details](docs-internal/investigation.md).

---

## Documentation

| Document | What it covers |
|----------|---------------|
| [Layout Guide](docs-internal/layout-guide.md) | CNN-style section layout, CSS classes, font scale, mobile breakpoints |
| [Adding Pages](docs-internal/adding-pages.md) | How to add new pages and reports using the shared header template |
| [Building](docs-internal/building.md) | Build commands, full pipeline (scrape → classify → report → deploy) |
| [Investigation](docs-internal/investigation.md) | Key findings, data sources, data pipeline, disclaimer |
| [Bilingual](docs-internal/bilingual.md) | EN/TE support, Telugu font, writing style guides, translation workflow |
| [Chatbot](docs-internal/chatbot.md) | WebLLM model, loading strategy (desktop vs mobile), updating |
| [Project Structure](docs-internal/project-structure.md) | Full file tree with descriptions |

### Writing Style Guides

| Guide | Location |
|-------|----------|
| English | [style-guides/english-style.md](style-guides/english-style.md) |
| Telugu | [style-guides/telugu-style.md](style-guides/telugu-style.md) |

---

## Quick Start

```bash
python build_site.py                    # Build all EN + TE pages
python refresh_report_chatbot.py        # Refresh chatbot on reports
python data_extraction/scrape_all_layers.py  # Scrape GIS data
```

---

## Disclaimer

Caste classification is based on surname patterns and LLM inference — an approximation for research purposes, not a census. This is independent public interest research using publicly available government data.
