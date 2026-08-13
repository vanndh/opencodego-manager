# Design System — OpenCode GO Manager

## Palette

```
Background         #0B0D0E
Surface            #111416
Elevated Surface   #161A1D
Border             #24292D
Border muted       #1A1E22
Primary Text       #E8E8E3
Secondary Text     #7E878C
Muted Text         #565E64

--accent-primary   #3FB950   (terminal green — online/OK/progress)
--accent-secondary #D29922   (amber — bonus/limited/warn)
--accent-danger    #F85149   (red — error/failed, used sparingly)
--accent-info      #58A6FF   (blue — gateway/stats, used sparingly)
```

## Typography

```
--font-ui     "Geist", "Inter", system-ui
--font-mono   "Geist Mono", "JetBrains Mono", ui-monospace

Body    13/20  UI text
H1      15/22  uppercase, letter-spacing
H2      13/18  caps
Mono    12/18  data, limits, code
Tiny    11/16  timestamps, secondary
```

## Spacing

4px base scale: 2, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64

## Radius

- `radius-sm`: 3px (buttons, inputs)
- `radius-md`: 4px (surface cards)
- `radius-lg`: 6px (drawers, modals)

## Shadows

- `shadow-drawer`: subtle elevation for side panels/modals only
- Everything else: flat (no shadow)

## Borders

- 1px solid var(--border)
- Divider: 1px solid var(--border-muted)

## ASCII Language

Progress: `[████████░░] 82%` — rendered in mono, blocks + spaces
Status: `● ONLINE`, `○ OFFLINE`, `! ERROR` — glyph + text (never color alone)
Tree: `└─`, `├─`, `──` — section dividers, account trees
Pills: `[ACTIVE]`, `[DISABLED]`, `[BONUS]` — uppercase mono brackets
Markers: `→` flow, `>` active nav, `▸` expand, `★` favorite, `↻` refresh

## Components — Primitives

1. `Glyph` — ASCII status dot with text (`●`/`○`/`!`)
2. `Bar` — `[████░░░░] NN%` mono progress
3. `Pill` — `[TEXT]` uppercase mono bracket
4. `TreeLine` — `└─`/`├─` ASCII tree connector
5. `StatusBadge` — status dot + label + optional detail
6. `Toast` — bottom-right, auto-dismiss
7. `Modal`/`Drawer` — side/bottom panel
8. `Button` — text + optional icon
9. `Input` — label + field
10. `SearchBox` — `/` focused input
11. `CodeBlock` — mono block for credentials/logs
12. `EmptyState` — ASCII art + CTA
13. `LoadingDots` — `> refreshing_` animated
14. `ErrorState` — context + retry hint
15. `StaleIndicator` — `STALE · last refresh 12m ago`