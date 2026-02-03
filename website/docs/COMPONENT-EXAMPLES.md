# Component Examples

Code examples for commonly used components in the Enterprise AI website.

## Button Component

### Primary Button (Default)

```tsx
import { Button } from "@/components/ui/Button";

<Button href="/phases/phase-1">
  Continue to Phase 1 →
</Button>
```

### Secondary Button

```tsx
<Button href="/about" variant="secondary">
  Learn More
</Button>
```

### Button with Click Handler

```tsx
<Button onClick={() => handleAction()} variant="primary">
  Submit
</Button>
```

## Card Component

### Default Card

```tsx
import { Card } from "@/components/ui/Card";

<Card>
  <h3 className="text-xl font-bold text-navy mb-2">Card Title</h3>
  <p className="text-gray-700">Card content goes here.</p>
</Card>
```

### Card with Hover Effect

```tsx
<Card hover>
  <h3 className="text-xl font-bold text-navy mb-2">Hover Card</h3>
  <p className="text-gray-700">This card responds to hover.</p>
</Card>
```

### Elevated Card

```tsx
<Card variant="elevated">
  <h3 className="text-xl font-bold text-navy mb-2">Important Content</h3>
  <p className="text-gray-700">Elevated with stronger shadow.</p>
</Card>
```

### Flat Card

```tsx
<Card variant="flat">
  <h3 className="text-xl font-bold text-navy mb-2">Subtle Card</h3>
  <p className="text-gray-700">Gray background, no shadow.</p>
</Card>
```

### Accent Card with Color

```tsx
<Card variant="accent" className="border-teal">
  <h3 className="text-xl font-bold text-navy mb-2">Teal Accent</h3>
  <p className="text-gray-700">Left border accent.</p>
</Card>

<Card variant="accent" className="border-amber">
  <h3 className="text-xl font-bold text-navy mb-2">Amber Accent</h3>
  <p className="text-gray-700">Left border accent.</p>
</Card>

<Card variant="accent" className="border-magenta">
  <h3 className="text-xl font-bold text-navy mb-2">Magenta Accent</h3>
  <p className="text-gray-700">Left border accent.</p>
</Card>

<Card variant="accent" className="border-navy">
  <h3 className="text-xl font-bold text-navy mb-2">Navy Accent</h3>
  <p className="text-gray-700">Left border accent.</p>
</Card>
```

### Card with Brand Background

```tsx
<Card className="bg-teal/5 border-teal/20">
  <h3 className="text-xl font-bold text-navy mb-2">Strategy Section</h3>
  <p className="text-gray-700">Teal-tinted background.</p>
</Card>

<Card className="bg-amber/5 border-amber/20">
  <h3 className="text-xl font-bold text-navy mb-2">Phase 2 Content</h3>
  <p className="text-gray-700">Amber-tinted background.</p>
</Card>

<Card className="bg-magenta/5 border-magenta/20">
  <h3 className="text-xl font-bold text-navy mb-2">Phase 5 Content</h3>
  <p className="text-gray-700">Magenta-tinted background.</p>
</Card>
```

## Phase Strategy Cards (Updated Phase 3)

Each phase page uses a distinctive strategy card with top border accent:

### Phase 0 - Navy

```tsx
<Card className="mb-12 bg-navy/5 border-navy/20 border-t-4 border-t-navy">
  <h2 className="text-3xl font-bold text-navy mb-4">Strategy</h2>
  <p className="text-gray-700">Phase 0 content...</p>
</Card>
```

### Phase 1 - Teal

```tsx
<Card className="mb-12 bg-teal/5 border-teal/20 border-t-4 border-t-teal">
  <h2 className="text-3xl font-bold text-navy mb-4">Strategy</h2>
  <p className="text-gray-700">Phase 1 content...</p>
</Card>
```

### Phase 2 - Amber

```tsx
<Card className="mb-12 bg-amber/5 border-amber/20 border-t-4 border-t-amber">
  <h2 className="text-3xl font-bold text-navy mb-4">Strategy</h2>
  <p className="text-gray-700">Phase 2 content...</p>
</Card>
```

### Phase 3 - Magenta

```tsx
<Card className="mb-12 bg-magenta/5 border-magenta/20 border-t-4 border-t-magenta">
  <h2 className="text-3xl font-bold text-navy mb-4">Strategy</h2>
  <p className="text-gray-700">Phase 3 content...</p>
</Card>
```

### Phase 4 - Teal/Navy Gradient

```tsx
<Card className="bg-gradient-to-br from-teal/5 to-navy/5 border-teal/20 border-t-4 border-t-teal p-12">
  <h2 className="text-3xl font-bold text-navy mb-4">Strategy</h2>
  <p className="text-gray-700">Phase 4 content...</p>
</Card>
```

### Phase 5 - Magenta/Navy Gradient

```tsx
<Card className="bg-gradient-to-br from-magenta/5 to-navy/5 border-magenta/20 border-t-4 border-t-magenta p-12">
  <h2 className="text-3xl font-bold text-navy mb-4">Strategy</h2>
  <p className="text-gray-700">Phase 5 content...</p>
</Card>
```

### End-State - Navy Gradient

```tsx
<Card className="bg-gradient-to-br from-navy/5 to-teal/5 border-navy/20 border-t-4 border-t-navy p-12">
  <h2 className="text-3xl font-bold text-navy mb-4">Strategy</h2>
  <p className="text-gray-700">End-state content...</p>
</Card>
```

## Section Backgrounds (Updated Phase 3)

Use gradient backgrounds for visual depth:

### Gradient Section (Preferred)

```tsx
<section className="py-12 bg-gradient-to-b from-white to-teal/5">
  <Container>
    {/* Content */}
  </Container>
</section>
```

### Phase-Specific Gradient Sections

```tsx
// Phase 2
<section className="py-12 bg-gradient-to-b from-white to-amber/5">

// Phase 3
<section className="py-12 bg-gradient-to-b from-white to-magenta/5">

// Phase 4
<section className="py-12 bg-gradient-to-b from-white to-teal/5">

// Phase 5
<section className="py-12 bg-gradient-to-b from-white to-magenta/5">

// End-state
<section className="py-12 bg-gradient-to-b from-white to-navy/5">
```

### Navy Background Section

```tsx
<section className="py-12 bg-navy">
  <Container>
    <h2 className="text-white">White heading</h2>
    <p className="text-white/95">Primary text</p>
    <p className="text-white/90">Secondary text</p>
  </Container>
</section>
```

## CodeBlock Component (Accessibility Updated)

Code blocks now include keyboard accessibility:

```tsx
import { CodeBlock } from "@/components/ui/CodeBlock";

<CodeBlock
  code={`npm install
npm run dev`}
  language="bash"
/>
```

The component internally renders:

```tsx
<pre
  tabIndex={0}
  className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto focus:outline-none focus:ring-2 focus:ring-teal focus:ring-offset-2"
>
  <code>{code}</code>
</pre>
```

## Text Patterns

### Section Title with Subtitle

```tsx
<h2 className="text-3xl font-bold text-navy mb-4">Vision</h2>
<p className="text-xl text-gray-700 mb-6">
  Section subtitle with important intro text.
</p>
<p className="text-gray-700 leading-relaxed">
  Main body paragraph text.
</p>
```

### Secondary Text

```tsx
<p className="text-sm text-gray-600">
  Last updated: January 2026
</p>
```

### Text on Colored Backgrounds

```tsx
// Correct - use text-white/90 for secondary text
<div className="bg-teal text-white p-6">
  <h4 className="font-bold">Heading</h4>
  <p className="text-sm">Primary text in white</p>
  <p className="text-sm text-white/90">Secondary text</p>
</div>

// Incorrect - avoid -100 color variants
<p className="text-teal-100">Don't use this</p>
```

## Links

### Standard Link

```tsx
<a
  href="/phases/phase-5"
  className="text-teal hover:text-teal/80 font-medium"
>
  Continue to Phase 5 →
</a>
```

### Link with Focus State (Required for Accessibility)

```tsx
<Link
  href="/about"
  className="text-teal hover:text-teal/80 font-medium focus:outline-none focus:ring-2 focus:ring-teal focus:ring-offset-2 rounded transition-colors"
>
  Learn More
</Link>
```

### Footer Link (Dark Background)

```tsx
<Link
  href="/"
  className="hover:text-teal focus:outline-none focus:text-teal focus:underline transition-colors rounded"
>
  Home
</Link>
```

## Results Section Cards

Stakeholder cards with matching color accents:

```tsx
// The Board - Teal
<Card className="border-l-4 border-teal">
  <div className="flex items-start gap-3 mb-4">
    <div className="w-8 h-8 rounded-full bg-teal flex items-center justify-center">
      <Check className="w-5 h-5 text-white" />
    </div>
    <h4 className="text-xl font-bold text-navy">The Board</h4>
  </div>
  <p className="text-sm font-semibold text-teal mb-2">Result:</p>
</Card>

// C-Suite - Amber
<Card className="border-l-4 border-amber">
  <div className="w-8 h-8 rounded-full bg-amber ...">
  <p className="text-sm font-semibold text-amber mb-2">Result:</p>
</Card>

// Culture & People - Magenta
<Card className="border-l-4 border-magenta">
  <div className="w-8 h-8 rounded-full bg-magenta ...">
  <p className="text-sm font-semibold text-magenta mb-2">Result:</p>
</Card>

// Customer - Navy
<Card className="border-l-4 border-navy">
  <div className="w-8 h-8 rounded-full bg-navy ...">
  <p className="text-sm font-semibold text-navy mb-2">Result:</p>
</Card>
```

## CTA Blocks

### Standard CTA

```tsx
<div className="bg-navy text-white p-8 rounded-lg">
  <h3 className="text-2xl font-bold mb-4">Next: Phase 2</h3>
  <p className="text-white/90 mb-6">
    Description of what comes next.
  </p>
  <a
    href="/phases/phase-2"
    className="inline-block px-6 py-3 bg-teal text-white font-medium rounded-md hover:bg-teal/90 transition-colors"
  >
    Continue to Phase 2 →
  </a>
</div>
```

### Gradient CTA

```tsx
<Card className="bg-gradient-to-br from-teal/5 to-navy/5 border-teal/20 p-12">
  <h3 className="text-2xl font-bold text-navy mb-4">Ready to Begin?</h3>
  <p className="text-gray-700 mb-6">
    Start your AI transformation journey.
  </p>
  <a
    href="/phases/phase-1"
    className="inline-flex items-center px-6 py-3 bg-teal hover:bg-teal/90 text-white font-medium rounded-lg transition-colors"
  >
    Get Started →
  </a>
</Card>
```

## Info Boxes

### Tip/Note Box

```tsx
<div className="mt-8 p-6 bg-navy/5 rounded-lg border border-gray-200">
  <h3 className="text-lg font-bold text-navy mb-2">
    Ready to see more?
  </h3>
  <p className="text-gray-700 mb-4">
    The technical details below are optional.
  </p>
  <a
    href="/phases/phase-2"
    className="inline-block px-6 py-3 bg-navy text-white font-medium rounded-md hover:bg-navy/90 transition-colors"
  >
    Skip to Phase 2 →
  </a>
</div>
```

### Highlight Box

```tsx
<div className="bg-magenta/10 border-l-4 border-magenta p-6 rounded">
  <h4 className="font-bold text-navy mb-2">Key Insight</h4>
  <p className="text-gray-700">
    Important information highlighted here.
  </p>
</div>
```

### Strategic Outcome Boxes

```tsx
<div className="bg-teal/5 border-l-4 border-teal p-4 rounded">
  <h5 className="font-bold text-navy mb-2">Competitive Moat</h5>
  <ul className="text-sm text-gray-700 space-y-1">
    <li>• Company-specific models</li>
  </ul>
</div>

<div className="bg-amber/5 border-l-4 border-amber p-4 rounded">
  <h5 className="font-bold text-navy mb-2">Deployment Flexibility</h5>
</div>

<div className="bg-magenta/5 border-l-4 border-magenta p-4 rounded">
  <h5 className="font-bold text-navy mb-2">Strategic Optionality</h5>
</div>

<div className="bg-navy/5 border-l-4 border-navy p-4 rounded">
  <h5 className="font-bold text-navy mb-2">Sustainable Advantage</h5>
</div>
```
