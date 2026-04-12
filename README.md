# The Amaravati Record

**Independent data journalism on the making of Andhra Pradesh's capital.**

Live site: <https://sahitkogs.github.io/TheAmaravatiRecord/>

A one-desk independent newsroom covering land allocation, construction progress, and the data behind the Amaravati capital region. Publishes interactive data reports, a live construction tracker, and a broadsheet-style newspaper site — all served from GitHub Pages.

---

## The Site

The site is a multi-page static newspaper built on a broadsheet aesthetic (monochrome cream/ink, Playfair Display + Source Serif 4 typography, no gradients). Every page includes an AI chatbot ("Ask The Record") powered by WebLLM (Qwen3-0.6B, runs fully in the browser, no API key needed).

| Page | URL |
|------|-----|
| Home | [/TheAmaravatiRecord/](https://sahitkogs.github.io/TheAmaravatiRecord/) |
| Reports | [/TheAmaravatiRecord/reports.html](https://sahitkogs.github.io/TheAmaravatiRecord/reports.html) |
| Caste Dashboard | [/TheAmaravatiRecord/reports/amaravati_caste_report.html](https://sahitkogs.github.io/TheAmaravatiRecord/reports/amaravati_caste_report.html) |
| Capital Tracker | [amaravati-tracker-staging](https://sahitkogs.github.io/amaravati-tracker-staging/) (separate repo) |
| About / Contact / Support | See nav links on the site |

### Policies & legal

Privacy Policy, Cookie Notice, Terms of Use, Editorial Policy, Corrections Ledger, AI Disclosure — all published on the site. Content is CC BY 4.0, datasets ODbL 1.0, code MIT. See the [Licenses page](https://sahitkogs.github.io/TheAmaravatiRecord/licenses.html).

---

## The Investigation

Examines ~48,000 land plots allocated under the APCRDA Land Pooling Scheme across 26 villages in the Krishna-Guntur region. Identifies the caste of each land beneficiary using their full name — combining a ground truth surname corpus (5,548 surnames from 19 sources) with per-name Gemini 2.5 Flash classification.

### Key findings

- **47,993 unique plots** analysed (deduplicated from 95,645 raw records)
- **Kamma: ~57.4%** of plots — the single largest beneficiary community (Kapu 13.0%, Reddy 5.0% trail)
- **5,548 surnames** in ground truth corpus with URL-backed evidence
- **351 first names** detected and excluded via frequency analysis
- **99.6% classification rate** using Gemini 2.5 Flash per-name approach

### Data sources

| Source | What | URL |
|--------|------|-----|
| APCRDA LPS Portal | Plot data, farmer names | https://gis.apcrda.org/lps/index.html |
| MyNeta.info | SC candidate names (elections) | https://www.myneta.info/ |
| Community websites | Surname-caste lists (19 sources) | Various blogspot/weebly |

### Data pipeline

```
1. Scrape       → scrape_apcrda_lps.py          → data/apcrda_lps_data.csv
2. Clean + Build → build_report.py               → Dedup, normalize, process
3. Classify     → caste_classifier_gemini.py     → data/gemini_name_caste_map.json
4. Report       → build_report.py + html_template.py → docs/reports/amaravati_caste_report.html
```

---

## Building the Site

### Site pages (13 pages)

Source files live in `docs/*.src.html`. A build script injects the chatbot widget (with broadsheet theme) and writes to `docs/*.html`, which is what GitHub Pages serves.

```bash
# Build all site pages
python build_site.py

# Build a single page
python build_site.py index
```

Each page gets a page-specific system prompt and suggestion chips. The chatbot uses a shared localStorage key (`amaravati`) so conversation persists across page navigations.

### Data reports

```bash
# Regenerate the caste dashboard (requires data + Gemini API key)
python build_report.py

# Refresh chatbot on existing report HTML (no data regeneration)
python refresh_report_chatbot.py
```

### Full pipeline

```bash
# Step 1: Scrape (if source data needs refresh)
python scrape_apcrda_lps.py

# Step 2: Classify names via Gemini (configure in .env — see .env.sample)
python caste_classifier_gemini.py

# Step 3: Generate reports
python build_report.py

# Step 4: Build site pages
python build_site.py

# Step 5: Refresh chatbot on reports (if library was updated)
python refresh_report_chatbot.py

# Tests
python -m pytest tests/ -v

# Explorer
python explorer/build_surname_explorer.py
```

---

## Project Structure

```
├── build_site.py                # Build docs/*.src.html → docs/*.html with chatbot injection
├── build_report.py              # Generate caste report from data + inject chatbot
├── refresh_report_chatbot.py    # Strip old chatbot from reports, re-inject with current library
├── html_template.py             # Dashboard HTML template
├── scrape_apcrda_lps.py         # Scrape APCRDA LPS portal
├── caste_classifier_gemini.py   # Gemini per-name caste classification
├── utils/
│   ├── gemini_client.py         # Gemini API wrapper
│   └── name_utils.py            # Name parsing utilities
├── prompts/
│   ├── __init__.py              # Prompt module init
│   └── caste_classifier.py      # Classification prompt template
├── explorer/
│   ├── build_surname_explorer.py # Build explorer HTML
│   ├── surname_explorer.html    # Interactive surname browser
│   ├── surname_ground_truth.csv # 5,548 surnames × 8 castes (19 sources)
│   └── detected_first_names.json # 351 detected first names
├── tests/
│   ├── test_build_report.py     # Unit tests
│   ├── test_data_validation.py  # Data validation tests
│   └── test_prompt_sample.py    # Prompt tests
├── data/
│   ├── apcrda_lps_data.csv      # Source: 95K plot records from APCRDA
│   ├── gemini_name_caste_map.json # Per-name caste assignments (30K names)
│   └── caste_surname_map.json   # Surname fallback + not_surnames list
├── docs/                        # GitHub Pages site: The Amaravati Record
│   ├── *.src.html               # Source pages (edit these)
│   ├── *.html                   # Built pages (generated by build_site.py)
│   ├── styles.css               # Shared broadsheet stylesheet
│   ├── consent.js               # Cookie consent banner + GA4 integration
│   ├── robots.txt               # Search engine crawl policy
│   ├── sitemap.xml              # Sitemap for search engines
│   ├── pgp-key.txt              # PGP public key (placeholder)
│   ├── .well-known/security.txt # Security contact
│   └── reports/
│       ├── amaravati_caste_report.html  # Interactive dashboard (generated)
│       └── amaravati_newspaper.html     # Broadsheet investigation (hand-maintained)
├── LICENSE.md                   # License index (three-layer stack)
├── LICENSE-CODE.md              # MIT (code)
├── LICENSE-CONTENT.md           # CC BY 4.0 (prose)
├── LICENSE-DATA.md              # ODbL 1.0 (datasets)
├── SECURITY.md                  # Responsible disclosure policy
└── archives/                    # Old versions, one-time scripts, raw extracts
```

---

## Chatbot: "Ask The Record"

Every page on the site includes an AI chatbot widget powered by [chatbot-in-html](https://github.com/sahitkogs/chatbot-in-html) with a broadsheet newspaper theme.

| Feature | Detail |
|---------|--------|
| **Model** | Qwen3-0.6B via WebLLM (runs in browser, no API key) |
| **Theme** | Broadsheet — cream/ink palette, serif fonts, dark-red accent, dark-mode aware |
| **Mobile** | Full-width chat window, bubble stays visible when open |
| **Persistence** | Conversation carries across all pages (shared localStorage) |
| **Preloading** | Model downloads on page load (background), ready by the time user opens chat |
| **Thinking dots** | Pulsing animation shown before first streaming token |
| **Suggestions** | Page-specific chips re-appear after every response |
| **Backend toggle** | Users can switch between Local (WebLLM) and Cloud |

### Updating the chatbot

If the chatbot-in-html library is updated:

```bash
# Reinstall the library
pip install -e /path/to/chatbot-in-html

# Rebuild all site pages
python build_site.py

# Refresh chatbot on report pages
python refresh_report_chatbot.py
```

---

## Disclaimer

Caste classification is based on surname patterns and LLM inference — an approximation for research purposes, not a census. Individual assignments may be inaccurate. This is independent public interest research using publicly available government data.
