# Enterprise AI Website Style Guide

This document outlines the color system, typography, and design patterns used across the Enterprise AI website.

## Brand Colors

| Color   | Variable       | Hex       | Usage                                      |
|---------|----------------|-----------|-------------------------------------------|
| Navy    | `--color-navy` | `#1E3A5F` | Primary brand color, headers, navigation  |
| Teal    | `--color-teal` | `#1ABC9C` | Accent color, CTAs, links, Phase 1/4      |
| Amber   | `--color-amber`| `#F39C12` | Warning states, Phase 2                   |
| Magenta | `--color-magenta`| `#9B59B6` | Highlight accents, Phase 3/5            |

### Accessible Teal

For buttons and interactive elements requiring higher contrast:

| Color      | Variable            | Hex       | Usage                    |
|------------|---------------------|-----------|--------------------------|
| Teal Dark  | `--color-teal-dark` | `#138D75` | Primary buttons          |
| Teal Hover | -                   | `#117A65` | Button hover state       |

## Navy-Tinted Gray Scale

These grays have a subtle navy tint for visual cohesion with the brand:

| Gray   | Variable           | Hex       | Usage                           |
|--------|--------------------|-----------|---------------------------------|
| 50     | `--color-gray-50`  | `#F7F9FA` | Lightest backgrounds            |
| 100    | `--color-gray-100` | `#E8ECEF` | Light backgrounds               |
| 200    | `--color-gray-200` | `#DCE1E5` | Borders, dividers               |
| 300    | `--color-gray-300` | `#CED4DA` | Disabled states                 |
| 400    | `--color-gray-400` | `#A8B2BC` | Placeholder text                |
| 500    | `--color-gray-500` | `#8A95A0` | Secondary icons                 |
| 600    | `--color-gray-600` | `#6A747F` | Secondary/muted text            |
| 700    | `--color-gray-700` | `#495460` | Body text                       |
| 800    | `--color-gray-800` | `#343A42` | Headings on light backgrounds   |
| 900    | `--color-gray-900` | `#2A3138` | High-emphasis text              |

## Text Color Rules

### Body Text
- **Main body paragraphs**: `text-gray-700`
- **Section subtitles/intros**: `text-gray-700`
- **Secondary/muted text**: `text-gray-600` (captions, metadata, timestamps)

### On Dark Backgrounds (Navy)
- **Primary text**: `text-white/95`
- **Secondary text**: `text-white/90`
- **Navigation links (inactive)**: `text-white/90`
- **Navigation links (active)**: `text-teal`

### On Colored Backgrounds (Teal, Amber, Magenta)
- **Primary text**: `text-white`
- **Secondary text**: `text-white/90` (NOT `-100` variants)
- **Badges**: `bg-white/20 text-white`

## Background Patterns

### Section Backgrounds (Updated Phase 3)

Use gradient backgrounds instead of flat colors for visual depth:

| Context | Class | Usage |
|---------|-------|-------|
| Home Context | `bg-gradient-to-b from-white to-teal/5` | Context section |
| Home Results | `bg-gradient-to-b from-white to-navy/5` | Results section |
| Phase 2 sections | `bg-gradient-to-b from-white to-amber/5` | Strategy, details |
| Phase 3 sections | `bg-gradient-to-b from-white to-magenta/5` | Strategy, details |
| Phase 4 sections | `bg-gradient-to-b from-white to-teal/5` | Strategy, details |
| Phase 5 sections | `bg-gradient-to-b from-white to-magenta/5` | Strategy, details |
| End-state sections | `bg-gradient-to-b from-white to-navy/5` | Strategy, details |

### Card Backgrounds
- **Default**: `bg-white`
- **Flat**: `bg-gray-50`
- **Accent**: `bg-teal/5`, `bg-amber/5`, `bg-magenta/5`

## Phase Color Theming

Each phase has a designated accent color with top border accent:

| Phase     | Color   | Strategy Card Class |
|-----------|---------|---------------------|
| Phase 0   | Navy    | `bg-navy/5 border-navy/20 border-t-4 border-t-navy` |
| Phase 1   | Teal    | `bg-teal/5 border-teal/20 border-t-4 border-t-teal` |
| Phase 2   | Amber   | `bg-amber/5 border-amber/20 border-t-4 border-t-amber` |
| Phase 3   | Magenta | `bg-magenta/5 border-magenta/20 border-t-4 border-t-magenta` |
| Phase 4   | Teal/Navy | `bg-gradient-to-br from-teal/5 to-navy/5 border-teal/20 border-t-4 border-t-teal` |
| Phase 5   | Magenta/Navy | `bg-gradient-to-br from-magenta/5 to-navy/5 border-magenta/20 border-t-4 border-t-magenta` |
| End-state | Navy | `bg-gradient-to-br from-navy/5 to-teal/5 border-navy/20 border-t-4 border-t-navy` |

## Interactive States

### Buttons

**Primary Button:**
```css
bg-[#138D75] text-white hover:bg-[#117A65] focus:ring-teal
```

**Secondary Button:**
```css
bg-transparent border-2 border-navy text-navy hover:bg-navy hover:text-white focus:ring-navy
```

### Links

**Standard Links:**
```css
text-teal hover:text-teal/80
```

**Links with Focus State (Required):**
```css
text-teal hover:text-teal/80 focus:outline-none focus:ring-2 focus:ring-teal focus:ring-offset-2 rounded transition-colors
```

**Footer Links (on dark backgrounds):**
```css
hover:text-teal focus:outline-none focus:text-teal focus:underline transition-colors rounded
```

### Focus States

All interactive elements must have visible focus states:

```css
focus:outline-none focus:ring-2 focus:ring-teal focus:ring-offset-2
```

For elements on dark backgrounds, add:
```css
focus:ring-offset-navy
```

## Component Opacity Modifiers

Use opacity modifiers for subtle variations:

| Modifier | Usage                                    |
|----------|------------------------------------------|
| `/5`     | Very subtle backgrounds                  |
| `/10`    | Light backgrounds, subtle borders        |
| `/20`    | Border colors, dividers                  |
| `/50`    | Medium opacity borders, hover states     |
| `/80`    | De-emphasized text (avoid on colored bg) |
| `/90`    | Secondary text on dark/colored backgrounds |
| `/95`    | Primary text on dark backgrounds         |

## Accessibility Requirements

### Contrast (WCAG AA)

All text must meet WCAG AA standards (4.5:1 minimum for normal text):

| Combination                    | Ratio  | Status |
|-------------------------------|--------|--------|
| White on #138D75 (teal-dark)  | 4.5:1+ | Pass   |
| #495460 (gray-700) on white   | 7.0:1  | Pass   |
| #6A747F (gray-600) on white   | 4.9:1  | Pass   |
| White/90 on brand colors      | 4.5:1+ | Pass   |

### Keyboard Navigation

- All interactive elements must be focusable
- Focus states must be visible
- Code blocks with horizontal scroll need `tabIndex={0}`

### Scrollable Regions

Code blocks and horizontally scrollable content must include:
```tsx
<pre tabIndex={0} className="... focus:outline-none focus:ring-2 focus:ring-teal focus:ring-offset-2">
```

## Results Section Color Coding

Stakeholder cards use matching colors for icons, borders, and labels:

| Stakeholder | Border | Icon Background | Result Label |
|-------------|--------|-----------------|--------------|
| The Board | `border-teal` | `bg-teal` | `text-teal` |
| C-Suite | `border-amber` | `bg-amber` | `text-amber` |
| Culture & People | `border-magenta` | `bg-magenta` | `text-magenta` |
| Customer | `border-navy` | `bg-navy` | `text-navy` |

## Color Classes Reference

### Tailwind Classes

**Brand Colors:**
- `text-navy`, `bg-navy`, `border-navy`
- `text-teal`, `bg-teal`, `border-teal`
- `text-amber`, `bg-amber`, `border-amber`
- `text-magenta`, `bg-magenta`, `border-magenta`

**Custom Values:**
- `bg-[#138D75]` - Accessible teal for buttons
- `hover:bg-[#117A65]` - Darker teal hover

**Opacity Variants:**
- `bg-teal/5`, `bg-teal/10`, `bg-teal/20`
- `border-teal/20`, `border-teal/50`
- `text-white/90`, `text-white/95`

**Gradients:**
- `bg-gradient-to-b from-white to-teal/5`
- `bg-gradient-to-br from-teal/5 to-navy/5`
- `bg-gradient-to-br from-magenta/5 to-navy/5`

## Testing Checklist

Before deploying color changes:

- [ ] Run `npm run lint` - 0 errors
- [ ] Run `npm run build` - All pages compile
- [ ] Run axe accessibility audit
- [ ] Test keyboard navigation (Tab through page)
- [ ] Verify focus states are visible
- [ ] Check contrast with browser DevTools
- [ ] Test at mobile breakpoints (375px, 768px)
