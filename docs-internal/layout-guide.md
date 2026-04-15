# Layout Guide

CNN-style section-based layout. No persistent sidebar. Each section is full-width and decides its own internal column layout.

## Design Principles

- **CNN-style section layout**: Content flows in horizontal sections — no sidebar columns.
- **4-tier font scale**: Headlines (24px), subheads (18px), body (16px), labels (14px). Minimum 12px.
- **Mobile-first**: Hamburger menu (< 880px), single-column stacking, 17px body text on phones.
- **Sticky header**: Logo bar + ticker stick to top on scroll.
- **Dark footer**: 4-column grid (Reports, About, Legal, Contact).
- **Dark mode**: Toggle in header, light mode default, persisted in localStorage.

## Homepage Structure

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

## CSS Classes

| Class | Usage |
|-------|-------|
| `.section` | Full-width section with bottom border |
| `.lead__split` | 2-column grid: text (60%) + stats (40%) |
| `.card-row` | 4-column equal-height card grid |
| `.card-row--2col` | 2-column variant |
| `.card` | Card within a row |
| `.card--bordered` | Card with visible border |
| `.letters__grid` | 2-column grid for Q&A pairs |
| `.dispatch-grid` | 5-column dispatch card grid |

## Mobile Breakpoints

| Breakpoint | Changes |
|-----------|---------|
| < 880px | Hamburger menu, `.card-row` → 2 columns, `.letters__grid` → 1 column |
| < 520px | `.card-row` → 1 column, `.dispatch-grid` → 1 column |
