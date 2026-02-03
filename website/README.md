# AI Habitat Framework Website

A professional showcase website for the AI Habitat Framework - a bottom-up approach to enterprise AI deployment.

## Tech Stack

- **Next.js 16.1.3** - React framework with App Router
- **Tailwind CSS v4** - Utility-first CSS framework
- **TypeScript** - Type safety
- **Radix UI** - Accessible UI components (Accordion, Tabs, Navigation)
- **Framer Motion** - Animation library
- **Lucide React** - Icon library

## Getting Started

### Development

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the site.

### Build

```bash
npm run build
```

Generates optimized production build in `.next/` directory.

### Preview Production Build

```bash
npm run build
npm start
```

## Site Structure

### Pages

1. **HOME** (`/`) - 7-section landing page
2. **PORTAL** (`/phases`) - Interactive phase navigator
3. **PHASE 0-5** (`/phases/phase-[0-5]`) - Individual phase pages
4. **SCALING PRODUCTION** (`/phases/scaling-production`) - AWS deployment guide
5. **ABOUT** (`/about`) - Creator profile

## Design System

### Brand Colors

| Color | Hex | Usage |
|-------|-----|-------|
| Navy | `#1E3A5F` | Primary brand, headers, navigation |
| Teal | `#1ABC9C` | Accent color, CTAs, links |
| Teal Dark | `#138D75` | Accessible button backgrounds |
| Amber | `#F39C12` | Phase 2 theming, warnings |
| Magenta | `#9B59B6` | Phase 3/5 theming, highlights |

### Phase Color Theming

Each phase has a designated accent color:

| Phase | Color | Border Accent |
|-------|-------|---------------|
| Phase 0 | Navy | `border-t-4 border-t-navy` |
| Phase 1 | Teal | `border-t-4 border-t-teal` |
| Phase 2 | Amber | `border-t-4 border-t-amber` |
| Phase 3 | Magenta | `border-t-4 border-t-magenta` |
| Phase 4 | Teal/Navy | Gradient background |
| Phase 5 | Magenta/Navy | Gradient background |

### Gray Scale (Navy-tinted)

- Gray 700 (`#495460`) - Body text
- Gray 600 (`#6A747F`) - Secondary/muted text

### Layout

- Content max-width: 1200px
- Reading max-width: 800px

## Documentation

For complete design system documentation:

- **[Style Guide](./docs/STYLE-GUIDE.md)** - Full color system, accessibility requirements, and usage guidelines
- **[Component Examples](./docs/COMPONENT-EXAMPLES.md)** - Code examples for all components

## Testing

### Run Tests

```bash
# Lint
npm run lint

# Build (includes TypeScript checks)
npm run build
```

### Accessibility Testing

```bash
# Install testing dependencies
npm install -D @axe-core/cli

# Run axe audit
npx axe http://localhost:3000
```

### Test Results

Test artifacts are stored in `test-results/`:

- `accessibility-audit.md` - Axe-core findings
- `visual-regression-results.md` - Screenshot test results
- `browser-compatibility.md` - Browser support matrix
- `performance-audit.md` - Build & performance metrics
- `screenshots/` - Visual regression screenshots

### Quality Targets

| Metric | Target | Achieved |
|--------|--------|----------|
| Accessibility | 95+ | ~92-95 |
| Performance | 85+ | 90-95 |
| WCAG AA | Required | Partial |
| Browser Support | 4 browsers | 4/4 |

## Deployment

### Vercel (Recommended)

1. Push to GitHub
2. Import project in Vercel
3. Deploy automatically

### Manual

```bash
npm run build
npm start
```

## Performance

- Static generation (SSG) for all 11 pages
- Next.js Image optimization
- CSS bundle: ~41 KB (Tailwind CSS)
- No client-side data fetching

## Project Structure

```
website/
├── app/                    # Next.js App Router pages
│   ├── about/
│   ├── phases/
│   │   ├── phase-0/
│   │   ├── phase-1/
│   │   ├── phase-2/
│   │   ├── phase-3/
│   │   ├── phase-4/
│   │   ├── phase-5/
│   │   └── scaling-production/
│   └── page.tsx            # Home page
├── components/
│   ├── home/               # Home page sections
│   ├── layout/             # Layout components
│   ├── phases/             # Phase-specific components
│   └── ui/                 # Reusable UI components
├── docs/                   # Design documentation
├── lib/                    # Utilities and constants
└── test-results/           # Testing artifacts
```

## Contact

**Email:** d.dimick@eastsoutheast.international

---

Built with Next.js 16 and Tailwind CSS v4
