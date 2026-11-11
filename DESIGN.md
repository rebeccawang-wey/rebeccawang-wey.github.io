# DESIGN.md — The Question Board

The design system for Rebecca Wang's personal website. Every page follows it.
Values live as CSS variables at the top of `assets/css/site.css`; pages use the
variable names, never raw values.

**Feeling:** a tidy study board that someone arranged with care. Calm, warm,
spacious and exact. Professional means order and clean finishing, not corporate.

## Color

| Token | Value | Role |
|---|---|---|
| `--paper` | `#FAF7F2` | Page background, every page |
| `--board` | `#F2ECE2` | The board panel on the homepage; answer box; quiet fills |
| `--card` | `#FFFDF8` | Card fill |
| `--ink` | `#1F1F1F` | Main text, primary button, links |
| `--muted` | `#5A554D` | Secondary text, meta rows, nav links (6.9:1 on paper) |
| `--line` | `#E4DCCF` | Hairlines between page areas |
| `--card-line` | `#DED5C7` | Card and board borders |
| `--line-strong` | `#A39886` | Card border on hover, dashed future cards |
| `--finance` | `#4E6B54` sage green | Finance marker, label, filter |
| `--economics` | `#A14A29` terracotta | Economics marker, label, filter |
| `--metrics` | `#3D4A8A` indigo blue | Econometrics and Statistics marker, label, filter |
| `--risk` | `#7A3D69` plum | Risk marker, label, filter — same weight as the others |

Field colours appear only on the small dot, the field label and the selected
filter button. Never as card fills. Every field colour passes 4.5:1 on paper
and on card, and white text passes 5.9:1 or better on each. The field is always
written as text too, never shown by colour alone.

No dark mode. No gradients. No shadows except none.

## Typography

- **Headings and questions:** Lora (serif), weight 500. Warm and bookish
  without being formal.
- **Everything else:** Inter, weights 400, 500, 600.
- Both are self-hosted in `assets/fonts/` (no third-party requests).

| Token | Size / line height | Use |
|---|---|---|
| `--t-label` | 13px / 1.4, 600, caps, +0.1em | Field labels, small section labels |
| `--t-small` | 15px / 1.55 | Meta rows, card answers, footer |
| `--t-body` | 17px / 1.7 | Body text |
| `--t-lead` | 19px / 1.6 | Intro lines, answer box |
| `--t-h3` | 24px / 1.3 | Card questions, group titles |
| `--t-h2` | 30px / 1.25 | Section headings |
| `--t-h1` | clamp(36px → 52px) / 1.15 | Page titles, detail question |
| `--t-display` | clamp(48px → 76px) / 1.02 | Name on the homepage only |

Body text never below 15px. Prose lines max ~68 characters (`--prose: 680px`).
Text sizes stay the same on mobile except the two clamp sizes.

## Spacing

8px base: `--s1` 8 · `--s2` 16 · `--s3` 24 · `--s4` 32 · `--s5` 48 ·
`--s6` 64 · `--s7` 96 · `--s8` 128.

- Content width `--wide: 1200px`, page side padding 40px desktop, 20px mobile.
- Gap between cards: 36px desktop, 24px mobile — never smaller.
- Between page sections: 96–128px. Between blocks inside a page: 48–64px.
- One main idea per screen section. If a starting page feels full, move
  content to a subpage; never shrink cards or gaps.

## Shape and depth

- Radius: `--r-sm` 6px (cards, buttons, boxes), `--r-md` 10px (board panel).
- Borders: 1px everywhere.
- Shadows: none. Hover = the border darkens. Nothing lifts, tilts or moves.

## Components

- **Question card:** dot (10px, top centre) → field label → question (Lora 24)
  → one-sentence answer (15 muted) → bottom row: method left, status right.
  Whole card is one link. Same height in a row. Nothing else on it.
- **Future card ("Questions I am chasing next"):** dashed border, no fill,
  question + one line, field label at the bottom.
- **Filter button:** 44px tall, card fill, `--card-line` border. Selected =
  field-colour fill with white text. `aria-pressed` carries the state.
- **Buttons:** primary = ink outline that fills ink on hover ("Get in touch");
  quiet = underlined text link with an arrow.
- **Links:** ink, underlined with 4px offset; muted nav links turn ink on hover.
- **Focus:** 2px ink outline, 3px offset, on every interactive element.
- **Answer box (detail page):** board fill, `--r-sm`, small "Short answer" label.
- **Nav:** name left, links right, "Get in touch" at the far right. Collapses to
  a Menu button under 760px.
- **Footer:** name · Toronto · year, page links, email and LinkedIn.

## Imagery and icons

- No photos anywhere, including of Rebecca.
- Charts on detail pages only: max two per page, each with a caption and a
  one-line text summary. Flat, using the four field colours plus neutrals.
- Icons: only a thin straight arrow, drawn as inline stroke SVG at 1.5px.
  No emoji, no hand-drawn marks, no stickers, tape or pins.

## Motion

Only a near-instant border change on hover (120ms) and cards showing/hiding
when a filter is chosen. Nothing moves on load. With "reduce motion" on, even
the hover transition is removed.
