# The Investigation

Examines ~48,000 land plots allocated under the APCRDA Land Pooling Scheme across 26 villages in the Krishna-Guntur region. Each farmer's community identified by name — with 99.6% of names identified.

## Key Findings

- **47,993 unique plots** analysed (deduplicated from 95,645 raw records)
- **Kamma: 57.4%** of plots — the single largest beneficiary community (Kapu 13.0%, Reddy 5.0% trail)
- **5,548 surnames** in ground truth corpus with URL-backed evidence
- **351 first names** detected and excluded via frequency analysis
- **99.6%** of farmer names identified

## Data Sources

| Source | What | URL |
|--------|------|-----|
| APCRDA LPS Portal | Plot data, farmer names, GIS layers | https://gis.apcrda.org/lps/index.html |
| MyNeta.info | SC candidate names (elections) | https://www.myneta.info/ |
| Community websites | Surname-caste lists (19 sources) | Various blogspot/weebly |

## Data Pipeline

```
1. Scrape       → data_extraction/lps_village_plots/scrape_lps_village_plots.py → raw_data/apcrda_lps_data.csv
2. Classify     → data_extraction/lps_village_plots/caste_classifier_gemini.py  → processed_data/gemini_name_caste_map.json
3. Report       → data_extraction/lps_village_plots/build_report.py             → docs/en/reports/lps-caste-dashboard.html
```

## Disclaimer

Caste classification is based on surname patterns and LLM inference — an approximation for research purposes, not a census. Individual assignments may be inaccurate. This is independent public interest research using publicly available government data.
