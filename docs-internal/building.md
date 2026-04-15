# Building the Site

## Quick Commands

```bash
python build_site.py                    # Build all EN + TE pages
python build_site.py index              # Build a single page
python refresh_report_chatbot.py        # Refresh chatbot on reports
```

Each page gets a page-specific system prompt and suggestion chips. The chatbot uses a shared localStorage key so conversation persists across page navigations.

## Full Pipeline

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

## Updating the Chatbot

If the chatbot-in-html library is updated:

```bash
pip install -e /path/to/chatbot-in-html
python build_site.py
python refresh_report_chatbot.py
```
