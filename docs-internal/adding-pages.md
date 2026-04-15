# Adding New Pages & Reports

## Header Template

Every page uses `site-header.js` for the header, ticker, and footer. Include in `<head>`:

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

## What `site-header.js` Renders

- **Header bar**: logo + nav links + dark mode toggle + language toggle
- **Ticker**: scrolling headlines (bilingual)
- **Footer**: 4-column dark grid (Reports, About, Legal, Contact)

The page controls its own content layout between the header and footer.

## Rules

- Do **not** hardcode the header, ticker, or footer HTML
- Do **not** write custom masthead/nav CSS — use `site-header.css`
- Follow the CNN-style section layout (see [layout-guide.md](layout-guide.md))
- Use `.section`, `.card-row`, `.card` for new content
- If the header needs to change, edit `site-header.js` (content) or `site-header.css` (styling)

## Bilingual Pages

English pages go in `docs/en/`, Telugu in `docs/te/`. Same structure in both. `site-header.js` auto-detects language from the URL path (`/en/` or `/te/`).

## Building

```bash
python build_site.py          # Builds all EN + TE pages
python refresh_report_chatbot.py  # Refreshes chatbot on reports
```
