# Bilingual Support (EN + TE)

## URL Structure

- `/` — Language picker (saves preference, auto-redirects returning visitors)
- `/en/` — English content
- `/te/` — Telugu content

## How It Works

`site-header.js` auto-detects language from the URL path (`/en/` or `/te/`) and renders all header, ticker, nav, and footer text in the correct language via a `STRINGS` object.

Language preference is saved in localStorage (`andhra_lang`). A toggle button (`EN | తె`) in the header allows instant switching — it replaces `/en/` with `/te/` in the URL.

## Telugu Font

Telugu pages use **Hind Guntur** (self-hosted in `docs/fonts/`, 5 weights: Light through Bold). Loaded via `@font-face` in `site-header.css`. Applied to Telugu pages via `html[lang="te"]` CSS selectors.

Telugu body text uses `line-height: 1.8` (vs 1.5 for English) to accommodate taller glyphs. Drop caps are disabled for Telugu (conjunct characters break the float layout).

## Writing Style Guides

- `style-guides/english-style.md` — English editorial voice, data precision, technical register
- `style-guides/telugu-style.md` — Telugu voice (Eenadu-inspired Sanskritized register adapted for data journalism), Arabic numerals, keep English acronyms

## Adding Telugu Translations

1. Create the `.src.html` file in `docs/te/pages/` (or `docs/te/` for index)
2. Follow the same HTML structure as the English version
3. Use `<html lang="te">` and Telugu meta tags
4. Follow the Telugu style guide for tone and vocabulary
5. Run `python build_site.py` to inject chatbot and build

## Policies & Legal

All legal pages are published under `en/pages/`. Content is CC BY 4.0, datasets ODbL 1.0, code MIT. See the [Licenses page](https://sahitkogs.github.io/AndhraRecord/en/pages/licenses.html).
