# Andhra Record

**Independent data journalism on Andhra Pradesh.**

Live site: <https://sahitkogs.github.io/AndhraRecord/>

A one-desk independent newsroom covering land allocation, construction progress, and the data behind Andhra Pradesh. Publishes interactive data reports, a live construction tracker, and a bilingual news site — all served from GitHub Pages.

---

## The Site

Bilingual (English + Telugu) static news site with a CNN-style layout. Every page includes an AI chatbot ("Ask The Record") powered by WebLLM (Qwen3-0.6B, runs fully in the browser, no API key needed).

| Page | URL |
|------|-----|
| Language Picker | [/AndhraRecord/](https://sahitkogs.github.io/AndhraRecord/) |
| Home (EN) | [/AndhraRecord/en/](https://sahitkogs.github.io/AndhraRecord/en/) |
| Home (TE) | [/AndhraRecord/te/](https://sahitkogs.github.io/AndhraRecord/te/) |
| Reports | [/AndhraRecord/en/pages/reports.html](https://sahitkogs.github.io/AndhraRecord/en/pages/reports.html) |
| Caste Dashboard | [/AndhraRecord/en/reports/lps-caste-dashboard.html](https://sahitkogs.github.io/AndhraRecord/en/reports/lps-caste-dashboard.html) |
| Capital Tracker | [amaravati-tracker-staging](https://sahitkogs.github.io/amaravati-tracker-staging/) (separate repo) |

### Design principles

- **CNN-style section layout**: No persistent sidebar. Each section is full-width and decides its own internal column layout. Content flows in horizontal sections.
- **4-tier font scale**: Headlines (24px), subheads (18px), body (16px), labels (14px). Minimum 12px. No tiny text.
- **Mobile-first**: Hamburger menu (< 880px), single-column stacking, 17px body text on phones.
- **Bilingual**: English at `/en/`, Telugu at `/te/`. Language auto-detected from URL, preference saved in localStorage.
- **Dark mode**: Toggle in header, persisted in localStorage. Light mode default.
- **Sticky header**: Logo bar + ticker stick to top on scroll.
- **Dark footer**: 4-column grid (Reports, About, Legal, Contact) with dark background.

### Homepage layout structure

When adding new articles or sections, follow this section-based pattern. No sidebar columns. Each section is a `<section class="section">` or `<section class="card-row">`.

```
[HEADER BAR: logo + nav + theme/lang toggles]
[TICKER: scrolling headlines]

[SECTION 1: LEAD STORY]
  headline + deck + byline (full width)
  body text (60%) | stats inset box (40%)    ← .lead__split
  pull quote (full width)
  closing paragraph (full width)

[SECTION 2: 4-CARD ROW]                      ← .card-row
  Tracker | Dashboard | Sources | Methods

[SECTION 3: 2-CARD ROW]                      ← .card-row.card-row--2col
  Privacy advisory | Archives table

[SECTION 4: EDITOR'S LETTERS]                ← .letters__grid (2-col)
  Q&A pair (left) | Q&A pair (right)

[SECTION 5: DISPATCH BOARD]                  ← .dispatch-grid (5-col)
  5 cards in a row

[DARK FOOTER]
  Reports | About | Legal | Contact
```

### Bilingual support

The site serves English at `/en/` and Telugu at `/te/`. The root page (`/`) is a language picker that saves the user's preference in localStorage (`andhra_lang`). Returning visitors are auto-redirected to their saved language. A language toggle (`EN | తె`) appears in the header on every page.

`site-header.js` auto-detects language from the URL path and renders all header, ticker, nav, and footer text in the correct language via a `STRINGS` object. Telugu pages use Hind Guntur font (self-hosted in `docs/fonts/`).

### Policies & legal

Privacy Policy, Cookie Notice, Terms of Use, Editorial Policy, Corrections Ledger, AI Disclosure — all published under `en/pages/`. Content is CC BY 4.0, datasets ODbL 1.0, code MIT. See the [Licenses page](https://sahitkogs.github.io/AndhraRecord/en/pages/licenses.html).

---

## The Investigation

Examines ~48,000 land plots allocated under the APCRDA Land Pooling Scheme across 26 villages in the Krishna-Guntur region. Each farmer's community identified by name — with 99.6% of names identified.

### Key findings

- **47,993 unique plots** analysed (deduplicated from 95,645 raw records)
- **Kamma: 57.4%** of plots — the single largest beneficiary community (Kapu 13.0%, Reddy 5.0% trail)
- **5,548 surnames** in ground truth corpus with URL-backed evidence
- **351 first names** detected and excluded via frequency analysis
- **99.6%** of farmer names identified

### Data sources

| Source | What | URL |
|--------|------|-----|
| APCRDA LPS Portal | Plot data, farmer names, GIS layers | https://gis.apcrda.org/lps/index.html |
| MyNeta.info | SC candidate names (elections) | https://www.myneta.info/ |
| Community websites | Surname-caste lists (19 sources) | Various blogspot/weebly |

### Data pipeline

```
1. Scrape       → data_extraction/lps_village_plots/scrape_lps_village_plots.py → raw_data/apcrda_lps_data.csv
2. Classify     → data_extraction/lps_village_plots/caste_classifier_gemini.py  → processed_data/gemini_name_caste_map.json
3. Report       → data_extraction/lps_village_plots/build_report.py             → docs/en/reports/lps-caste-dashboard.html
```

---

## Building the Site

### Site pages

Source files live in `docs/en/index.src.html` and `docs/en/pages/*.src.html`. All pages share a common header, ticker, and footer via `docs/site-header.js` — edit that single file to change the header across the entire site. A build script injects the chatbot widget and writes the compiled `.html` alongside each source.

```bash
# Build all EN + TE pages
python build_site.py

# Build a single page
python build_site.py index
```

Each page gets a page-specific system prompt and suggestion chips. The chatbot uses a shared localStorage key so conversation persists across page navigations.

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

  <!-- your content using .section, .card-row, .card, .lead__split -->

  <div id="site-footer"></div>
</div>
```

`site-header.js` renders: header bar (logo + nav + toggles) + ticker + footer. The page controls its own content layout. Do **not** hardcode the header/ticker/footer HTML. If the header needs to change, edit `site-header.js` (content) or `site-header.css` (styling) — changes propagate to every page automatically.

### Full pipeline

```bash
# Step 1: Scrape all GIS layers (or just the ones you need)
python data_extraction/scrape_all_layers.py

# Step 2: Classify names via Gemini (configure in .env — see .env.sample)
python data_extraction/lps_village_plots/caste_classifier_gemini.py

# Step 3: Generate reports
python data_extraction/lps_village_plots/build_report.py

# Step 4: Build site pages
python build_site.py

# Step 5: Refresh chatbot on reports (if library was updated)
python refresh_report_chatbot.py

# Tests
python -m pytest data_extraction/lps_village_plots/test_*.py -v

# Surname explorer
python data_extraction/surname_explorer/build_surname_explorer.py
```

---

## Project Structure

```
├── build_site.py                  # Build site pages with chatbot injection
├── refresh_report_chatbot.py      # Re-inject chatbot into report HTML files
├── README.md
├── SECURITY.md
├── .env.sample
├── style-guides/                  # Writing style guides
│   ├── english-style.md           # English editorial voice & conventions
│   └── telugu-style.md            # Telugu editorial voice & conventions
│
├── docs/                          # GitHub Pages site
│   ├── index.html                 # Language picker/redirector (root)
│   ├── styles.css                 # Shared stylesheet (4-tier font scale)
│   ├── site-header.js             # Header, ticker, footer (bilingual)
│   ├── site-header.css            # Header/footer styles + font overrides
│   ├── logo.svg                   # Andhra Record logo (red box)
│   ├── fonts/                     # Hind Guntur Telugu TTF files (5 weights)
│   ├── consent.js                 # Cookie consent + GA4
│   ├── sitemap.xml / robots.txt
│   ├── en/                        # English content
│   │   ├── index.html / index.src.html
│   │   ├── pages/                 # Secondary pages (about, reports, legal, etc.)
│   │   └── reports/               # Published investigations
│   │       ├── lps-caste-dashboard.html
│   │       └── lps-caste-investigation.html
│   └── te/                        # Telugu content
│       ├── index.html / index.src.html
│       └── pages/                 # Translated pages (about, reports)
│
├── data_extraction/               # All data scraping and processing
│   ├── scrape_all_layers.py       # Run all GIS layer scrapers at once
│   ├── lps_village_plots/         # APCRDA LPS plot data (95K records)
│   │   ├── scrape_lps_village_plots.py
│   │   ├── build_report.py        # Generate caste dashboard report
│   │   ├── html_template.py       # Dashboard HTML template
│   │   ├── caste_classifier_gemini.py  # Gemini per-name classification
│   │   ├── caste_classifier.py    # Prompt templates
│   │   ├── gemini_client.py       # Gemini API wrapper
│   │   ├── name_utils.py          # Name parsing utilities
│   │   ├── test_*.py              # Tests
│   │   ├── raw_data/              # apcrda_lps_data.csv, .xlsx
│   │   └── processed_data/        # Gemini classifications, surname maps
│   ├── surname_explorer/          # Surname ground truth explorer
│   │   ├── build_surname_explorer.py
│   │   ├── raw_data/              # surname_ground_truth.csv
│   │   └── processed_data/        # surname_explorer.html, detected_first_names.json
│   ├── allocated_lands/           # APCRDA Layer 0 — govt allocated parcels (165)
│   ├── roads/                     # APCRDA Layer 2 — road network (52)
│   ├── burial_grounds/            # APCRDA Layer 3 — burial ground sites (25)
│   ├── water_bodies/              # APCRDA Layer 4 — lakes, tanks, ponds (28)
│   ├── survey_parcels/            # APCRDA Layer 5 — revenue survey parcels (1,276)
│   └── r1_boundary/               # APCRDA Layer 6 — zoning boundaries (195)
│       ├── scrape_*.py            # Extraction script
│       ├── raw_data/              # CSV + GeoJSON output
│       └── processed_data/        # For downstream analysis
│
└── licenses/
    ├── LICENSE.md                 # License index (three-layer stack)
    ├── LICENSE-CODE.md            # MIT (code)
    ├── LICENSE-CONTENT.md         # CC BY 4.0 (prose)
    └── LICENSE-DATA.md            # ODbL 1.0 (datasets)
```

---

## Chatbot: "Ask The Record"

Every page includes an AI chatbot widget powered by [chatbot-in-html](https://github.com/sahitkogs/chatbot-in-html).

| Feature | Detail |
|---------|--------|
| **Model** | Qwen3-0.6B via WebLLM (runs in browser, no API key) |
| **Theme** | Cream/ink palette, serif fonts, dark-red accent, dark-mode aware |
| **Mobile** | Full-width chat window, bubble stays visible when open |
| **Persistence** | Conversation carries across all pages (shared localStorage) |
| **Suggestions** | Page-specific chips re-appear after every response |
| **Backend toggle** | Users can switch between Local (WebLLM) and Cloud |

### WebLLM loading strategy

| | Desktop | Mobile (first visit) | Mobile (repeat visits) |
|-|---------|---------------------|----------------------|
| **On page load** | Preload engine in background | Download model to cache in background | Do nothing |
| **On chatbot open** | Instant (already loaded) | Engine initializes from cache | Engine initializes from cache |
| **GPU memory** | Allocated on page load | Freed after caching, re-allocated on chat open | Allocated only on chat open |

Mobile is detected via `matchMedia('(max-width: 600px)')`. First-visit status is tracked in localStorage. After the first visit downloads and caches the model weights, the engine is torn down to free GPU memory. On subsequent visits, nothing happens until the user taps the chat bubble.

### Updating the chatbot

```bash
pip install -e /path/to/chatbot-in-html
python build_site.py
python refresh_report_chatbot.py
```

---

## Disclaimer

Caste classification is based on surname patterns and LLM inference — an approximation for research purposes, not a census. Individual assignments may be inaccurate. This is independent public interest research using publicly available government data.
