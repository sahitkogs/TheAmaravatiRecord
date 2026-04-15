# Andhra Record

**Independent data journalism on Andhra Pradesh.**

Live site: <https://sahitkogs.github.io/AndhraRecord/>

A one-desk independent newsroom covering land allocation, construction progress, and the data behind Andhra Pradesh. Publishes interactive data reports, a live construction tracker, and a bilingual news site — all served from GitHub Pages.

---

## The Site

Bilingual (English + Telugu) static news site with a CNN-style layout. Header bar with logo + nav + dark/light toggle + language switch. Sticky header and ticker on all pages. Dark multi-column footer.

| Page | URL |
|------|-----|
| Language Picker | [/AndhraRecord/](https://sahitkogs.github.io/AndhraRecord/) |
| Home (EN) | [/AndhraRecord/en/](https://sahitkogs.github.io/AndhraRecord/en/) |
| Home (TE) | [/AndhraRecord/te/](https://sahitkogs.github.io/AndhraRecord/te/) |
| Reports | [/AndhraRecord/en/pages/reports.html](https://sahitkogs.github.io/AndhraRecord/en/pages/reports.html) |
| Caste Dashboard | [/AndhraRecord/en/reports/lps-caste-dashboard.html](https://sahitkogs.github.io/AndhraRecord/en/reports/lps-caste-dashboard.html) |

### Design principles

- **CNN-style section layout**: No persistent sidebar. Each section is full-width and decides its own internal column layout. Content flows in horizontal sections: lead story split → card rows → letters grid → dispatch grid → footer.
- **4-tier font scale**: Headlines (24px), subheads (18px), body (16px), labels (14px). Minimum 12px. No tiny text.
- **Mobile-first**: Hamburger menu (< 880px), single-column stacking, 17px body text on phones.
- **Bilingual**: English at `/en/`, Telugu at `/te/`. Language auto-detected from URL, preference saved in localStorage.
- **Dark mode**: Toggle in header, persisted in localStorage. Light mode default.
- **Sticky header**: Logo bar + ticker stick to top on scroll.
- **Dark footer**: 4-column grid (Reports, About, Legal, Contact) with dark background.

### Homepage layout structure

```
[HEADER BAR: logo + nav + theme/lang toggles]
[TICKER: scrolling headlines]

[SECTION 1: LEAD STORY]
  headline + deck + byline (full width)
  body text (60%) | stats inset box (40%)
  pull quote (full width)
  closing paragraph (full width)

[SECTION 2: 4-CARD ROW]
  Tracker | Dashboard | Sources | Methods

[SECTION 3: 2-CARD ROW]
  Privacy advisory | Archives table

[SECTION 4: EDITOR'S LETTERS]
  Q&A pair (left) | Q&A pair (right)

[SECTION 5: DISPATCH BOARD]
  5 cards in a row

[DARK FOOTER]
  Reports | About | Legal | Contact
  © 2026 Andhra Record
```

When adding new articles, follow this section-based pattern. Each section is a `<section class="section">` or `<section class="card-row">`. No sidebar columns. Use `.card` for equal-height items in a row. Use `.lead__split` for text + stats side-by-side.

### Adding a new page or report

Include in `<head>`:
```html
<link rel="stylesheet" href="../../styles.css">
<link rel="stylesheet" href="../../site-header.css?v=32">
<script src="../../site-header.js?v=32"></script>
```

In `<body>`:
```html
<div class="broadsheet">
  <div id="site-masthead"></div>
  <script>AndhraRecord.render({ page: '' });</script>

  <!-- your content here -->

  <div id="site-footer"></div>
</div>
```

`site-header.js` renders: header bar + ticker + footer. The page controls its own content layout.

### Bilingual support

English at `/en/`, Telugu at `/te/`. Root `/` is a language picker. `site-header.js` auto-detects language from URL and renders all header/ticker/footer text in the correct language. Telugu uses Hind Guntur font (self-hosted). Language toggle in header switches between `/en/` and `/te/`.

---

## The Investigation

Examines ~48,000 land plots allocated under the APCRDA Land Pooling Scheme across 26 villages in the Krishna-Guntur region. Each farmer's community identified by name — with 99.6% of names identified.

### Key findings

- **47,993 unique plots** analysed
- **Kamma: 57.4%** — the single largest beneficiary community
- **Kapu: 13.0%, Reddy: 5.0%** trail well behind
- **99.6%** of farmer names identified

### Data pipeline

```
1. Scrape   → data_extraction/lps_village_plots/scrape_lps_village_plots.py
2. Classify → data_extraction/lps_village_plots/caste_classifier_gemini.py
3. Report   → data_extraction/lps_village_plots/build_report.py
```

---

## Building the Site

```bash
python build_site.py                    # Build all EN + TE pages
python refresh_report_chatbot.py        # Refresh chatbot on reports
python data_extraction/scrape_all_layers.py  # Scrape GIS data
```

---

## Project Structure

```
├── build_site.py                  # Build site pages with chatbot injection
├── refresh_report_chatbot.py      # Re-inject chatbot into report HTML files
├── style-guides/                  # Writing style guides (EN + TE)
│
├── docs/                          # GitHub Pages site
│   ├── index.html                 # Language picker/redirector
│   ├── styles.css                 # Shared stylesheet (4-tier font scale)
│   ├── site-header.js             # Header, ticker, footer (bilingual)
│   ├── site-header.css            # Header/footer styles + font overrides
│   ├── logo.svg                   # Andhra Record logo
│   ├── fonts/                     # Hind Guntur (Telugu) TTF files
│   ├── consent.js                 # Cookie consent + GA4
│   ├── en/                        # English content
│   │   ├── index.html / index.src.html
│   │   ├── pages/                 # Secondary pages
│   │   └── reports/               # Published investigations
│   └── te/                        # Telugu content
│       ├── index.html / index.src.html
│       └── pages/                 # Translated pages
│
├── data_extraction/               # All data scraping and processing
│   ├── scrape_all_layers.py
│   ├── lps_village_plots/         # Main investigation pipeline
│   ├── surname_explorer/          # Surname ground truth
│   ├── allocated_lands/           # APCRDA GIS layers
│   ├── roads/ | burial_grounds/ | water_bodies/
│   ├── survey_parcels/ | r1_boundary/
│
└── licenses/                      # CC BY 4.0, ODbL 1.0, MIT
```

---

## Disclaimer

Caste classification is based on surname patterns and LLM inference — an approximation for research purposes, not a census. Individual assignments may be inaccurate. This is independent public interest research using publicly available government data.
