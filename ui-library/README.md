# UI Component Intelligence Catalog

## Audit status

**Complete source audit; runtime validation remains outstanding.** The collection has 65 instruction bundles in 8 categories and **109 independently identified renderers/providers**. All embedded implementations were reviewed. The stable component ledger, source hashes, and findings are in [`../ui-catalog-audit.checkpoint.json`](../ui-catalog-audit.checkpoint.json). No components, manifests, lockfiles, or dependencies were modified or installed. Classifications are source-based guidance, not browser-test results.

**Partial audit — not a completed design decision system.** The repository contains 65 instruction bundles in 8 top-level categories, not 4,565 individual components. Some bundles contain multiple demos, variants, or supporting components; 65 is not a verified individual-component count. All files were enumerated and export declarations and installation-command lines were extracted. Full implementation review remains incomplete because the initial full-content read was truncated. Do not treat extracted symbols or folder names as design classifications.

The documented ecosystems include Assistant UI, shadcn Studio (`@ss-components`), React Bits (`@react-bits`), and Aceternity UI (`@aceternity`). These are four source families, not package versions or license guarantees. Folder spelling is preserved.

The legacy partial-audit paragraph above is retained for history and is superseded by the complete-source-audit status and checkpoint ledger.

## Quick navigation

- [Bundle inventory](#bundle-inventory)
- [Component inventory](#individual-component-inventory)
- [Domain recommendations](#domain-based-recommendations)
- [Design situation and motion](#design-situation-and-motion-index)
- [Composition recipes](#component-composition-recipes)
- [Category index](#category-index)
- [Dependency evidence](#dependency-evidence)
- [Mandatory implementation workflow](#mandatory-implementation-workflow)
- [Limitations and outstanding analysis](#limitations-and-outstanding-analysis)

## Bundle inventory

Each instruction bundle appears exactly once below. The exact relative folder path is its stable bundle ID. Symbols are extracted code evidence, not an assertion that every export is a standalone component. Functional type, visual character, intensity, animation, domains, complementarity, and compatibility: **Requires verification** for all entries until individually reviewed. Links open the original instructions and embedded source.

| Stable bundle ID / folder | Export evidence | Original instructions |
|---|---|---|
| `charts/chart-assistant-ui` | export const PlotMetricToolUI: ToolCallMessagePartComponent<; export function MyRuntimeProvider({ children }: { children: React.ReactNode }) { | [instructions.md](charts/chart-assistant-ui/instructions.md) |
| `dashboards/data-showcase/data-table-shadcn-ui` | export default DialogSignInDemo; export const columns: ColumnDef<Payment>[] = [; export default DataTableDemo | [instructions.md](dashboards/data-showcase/data-table-shadcn-ui/instructions.md) |
| `dashboards/data-showcase/data-table-with-search-shadcn-ui` | export const columns: ColumnDef<Payment>[] = [; export default DataTableDensityDemo | [instructions.md](dashboards/data-showcase/data-table-with-search-shadcn-ui/instructions.md) |
| `dashboards/data-tables/data-table-option-2-shadcn-ui` | export default TableWithVerticalLinesDemo | [instructions.md](dashboards/data-tables/data-table-option-2-shadcn-ui/instructions.md) |
| `dashboards/data-tables/simple-data-table-shadcn-ui` | export default TableDemo | [instructions.md](dashboards/data-tables/simple-data-table-shadcn-ui/instructions.md) |
| `dashboards/drawers/cart-drawer-shadcn-ui` | export default DrawerCart | [instructions.md](dashboards/drawers/cart-drawer-shadcn-ui/instructions.md) |
| `dashboards/drawers/nooverlay-scrollable-content-drawer-shadcn-ui` | export default DrawerNoOverlay | [instructions.md](dashboards/drawers/nooverlay-scrollable-content-drawer-shadcn-ui/instructions.md) |
| `dashboards/drawers/profile-drawer-shadcn-ui` | export default DrawerProfile | [instructions.md](dashboards/drawers/profile-drawer-shadcn-ui/instructions.md) |
| `dashboards/drawers/scrollable-content-drawer-shadcn-ui` | export default DrawerScrollableContent | [instructions.md](dashboards/drawers/scrollable-content-drawer-shadcn-ui/instructions.md) |
| `dashboards/kanbans/professional-karban-shadcn-ui` | export default KanbanDemo | [instructions.md](dashboards/kanbans/professional-karban-shadcn-ui/instructions.md) |
| `dashboards/kanbans/simple-kanban-shadcn-ui` | export default NavigationMenuDemo; export default KanbanDemoOutline | [instructions.md](dashboards/kanbans/simple-kanban-shadcn-ui/instructions.md) |
| `forms/drawer-signin-shadcn-ui` | export default DrawerWithSides | [instructions.md](forms/drawer-signin-shadcn-ui/instructions.md) |
| `forms/login-card-form-shadcn-ui` | export default CardDemo | [instructions.md](forms/login-card-form-shadcn-ui/instructions.md) |
| `forms/sign-in-form-shadcn-ui` | export default DialogSignUpDemo; export default DialogSignInDemo | [instructions.md](forms/sign-in-form-shadcn-ui/instructions.md) |
| `forms/signup-form-accernity-ui` | export function SignupFormDemo() { | [instructions.md](forms/signup-form-accernity-ui/instructions.md) |
| `forms/signup-form-shadcn-ui` | export default DialogSignUpDemo | [instructions.md](forms/signup-form-shadcn-ui/instructions.md) |
| `grids/chroma-grids-react-bits` | export const ChromaGrid = ({; export default ChromaGrid; | [instructions.md](grids/chroma-grids-react-bits/instructions.md) |
| `grids/magic-bento-react-bits` | export default MagicBento; | [instructions.md](grids/magic-bento-react-bits/instructions.md) |
| `landing/faqs/faq-shadcn-ui` | export default CollapsibleShowMoreDemo | [instructions.md](landing/faqs/faq-shadcn-ui/instructions.md) |
| `landing/footer-components/github-globe-accernity-ui` | export function GlobeDemo() { | [instructions.md](landing/footer-components/github-globe-accernity-ui/instructions.md) |
| `landing/heros/cloud-shader-accernity-ui` | export function CloudShaderHeroDemo() { | [instructions.md](landing/heros/cloud-shader-accernity-ui/instructions.md) |
| `landing/heros/hyperspeed-react-bits` | export default Hyperspeed; | [instructions.md](landing/heros/hyperspeed-react-bits/instructions.md) |
| `landing/heros/scroll-explained-react-bits` | export default ScrollExpand; | [instructions.md](landing/heros/scroll-explained-react-bits/instructions.md) |
| `landing/heros/splash-cursor` | export default SplashCursor; | [instructions.md](landing/heros/splash-cursor/instructions.md) |
| `landing/heros/threads-react-bits` | export default Threads; | [instructions.md](landing/heros/threads-react-bits/instructions.md) |
| `landing/heros/wavy-background-accernity-ui` | export function WavyBackgroundDemo() { | [instructions.md](landing/heros/wavy-background-accernity-ui/instructions.md) |
| `landing/testimonials/infinite-moving-cards-accernity-ui` | export function InfiniteMovingCardsDemo() { | [instructions.md](landing/testimonials/infinite-moving-cards-accernity-ui/instructions.md) |
| `navigation/menus/branched-menu-react-bits` | export default BranchedMenu; | [instructions.md](navigation/menus/branched-menu-react-bits/instructions.md) |
| `navigation/menus/flowing-menu-react-bits` | export default FlowingMenu; | [instructions.md](navigation/menus/flowing-menu-react-bits/instructions.md) |
| `navigation/navbars/navbar-menu` | export default NavigationMenuDemo | [instructions.md](navigation/navbars/navbar-menu/instructions.md) |
| `navigation/navbars/pill-nav-react-bits` | export default PillNav; | [instructions.md](navigation/navbars/pill-nav-react-bits/instructions.md) |
| `navigation/navbars/simple-nav-bar-shadcn-ui` | export default MenuBarMixedDemo | [instructions.md](navigation/navbars/simple-nav-bar-shadcn-ui/instructions.md) |
| `navigation/sidebars/line-sidebar-react-bits` | export default LineSidebar; | [instructions.md](navigation/sidebars/line-sidebar-react-bits/instructions.md) |
| `navigation/sidebars/sidebar-accernity-ui` | export function SidebarDemo() {; export const Logo = () => {; export const LogoIcon = () => { | [instructions.md](navigation/sidebars/sidebar-accernity-ui/instructions.md) |
| `navigation/tabs/icon-tab-shadcn-ui` | export default TabsWithIconDemo | [instructions.md](navigation/tabs/icon-tab-shadcn-ui/instructions.md) |
| `navigation/tabs/notification-with-tab-shadcn-ui` | export default TabsWithBadgeDemo | [instructions.md](navigation/tabs/notification-with-tab-shadcn-ui/instructions.md) |
| `navigation/tabs/simple-tab-shadcn-ui` | export default TabsOutlinedDemo | [instructions.md](navigation/tabs/simple-tab-shadcn-ui/instructions.md) |
| `reusable/buttons/go-to-settings-shadcn-ui` | export default ButtonGhostDemo | [instructions.md](reusable/buttons/go-to-settings-shadcn-ui/instructions.md) |
| `reusable/buttons/notifications-button-shadcn-ui` | export default ButtonNotificationsBadgeDemo | [instructions.md](reusable/buttons/notifications-button-shadcn-ui/instructions.md) |
| `reusable/buttons/shadcn-ui-buttons` | export default ButtonActionsDemo | [instructions.md](reusable/buttons/shadcn-ui-buttons/instructions.md) |
| `reusable/buttons/specular-button-react-bits` | export default SpecularButton; | [instructions.md](reusable/buttons/specular-button-react-bits/instructions.md) |
| `reusable/buttons/star-border-react-bits` | export default StarBorder; | [instructions.md](reusable/buttons/star-border-react-bits/instructions.md) |
| `reusable/buttons/tailwind-css-buttons-accernity-ui` | export function TailwindcssButtons() {; export const buttons = [ | [instructions.md](reusable/buttons/tailwind-css-buttons-accernity-ui/instructions.md) |
| `reusable/calender/book-your-appointment-shadcn-ui` | export default CalendarAppointmentBookingDemo | [instructions.md](reusable/calender/book-your-appointment-shadcn-ui/instructions.md) |
| `reusable/calender/normal-usage-calender-shadcn-ui` | export default CalendarAppointmentBookingDemo; export default CalendarWeekNumberDemo | [instructions.md](reusable/calender/normal-usage-calender-shadcn-ui/instructions.md) |
| `reusable/cards/apple-cards-carousel-accernity-ui` | export function AppleCardsCarouselDemo() { | [instructions.md](reusable/cards/apple-cards-carousel-accernity-ui/instructions.md) |
| `reusable/cards/bounce-cards-react-bits` | export default function BounceCards({ | [instructions.md](reusable/cards/bounce-cards-react-bits/instructions.md) |
| `reusable/cards/decent-plain-card-shadcn-ui` | export default CardTopImageDemo | [instructions.md](reusable/cards/decent-plain-card-shadcn-ui/instructions.md) |
| `reusable/cards/focus-cards-accernity-ui` | export function FocusCardsDemo() { | [instructions.md](reusable/cards/focus-cards-accernity-ui/instructions.md) |
| `reusable/cards/pixel-cards-react-bits` | export default function PixelCard({ | [instructions.md](reusable/cards/pixel-cards-react-bits/instructions.md) |
| `reusable/cards/profile-card-react-bits` | export default memo(ProfileCard); | [instructions.md](reusable/cards/profile-card-react-bits/instructions.md) |
| `reusable/cards/titled-card-react-bits` | export const TiltedCardLayer = ({; export default TiltedCard; | [instructions.md](reusable/cards/titled-card-react-bits/instructions.md) |
| `reusable/cards/wobble-cards-accernity-ui` | export function WobbleCardDemo() { | [instructions.md](reusable/cards/wobble-cards-accernity-ui/instructions.md) |
| `reusable/dialog-boxes-or-menu-shadcn-ui` | export default DialogFullScreenDemo | [instructions.md](reusable/dialog-boxes-or-menu-shadcn-ui/instructions.md) |
| `reusable/galleries/accordian-gallery-react-bits` | export default AccordionGallery; | [instructions.md](reusable/galleries/accordian-gallery-react-bits/instructions.md) |
| `reusable/galleries/circular-gallery-react-bits` | export default CircularGallery; | [instructions.md](reusable/galleries/circular-gallery-react-bits/instructions.md) |
| `reusable/galleries/flex-carousel-react-bits` | export default FlexCarousel; | [instructions.md](reusable/galleries/flex-carousel-react-bits/instructions.md) |
| `reusable/galleries/gradual-blur-react-bits` | export default GradualBlur; | [instructions.md](reusable/galleries/gradual-blur-react-bits/instructions.md) |
| `reusable/galleries/Masonry-react-bits` | export default Masonry; | [instructions.md](reusable/galleries/Masonry-react-bits/instructions.md) |
| `reusable/lists/animated-list-react-bits` | export default AnimatedList; | [instructions.md](reusable/lists/animated-list-react-bits/instructions.md) |
| `typographies/h1-shadcn-ui` | export default TypographyH1Demo | [instructions.md](typographies/h1-shadcn-ui/instructions.md) |
| `typographies/h2-shadcn-ui` | export default TypographyH2Demo | [instructions.md](typographies/h2-shadcn-ui/instructions.md) |
| `typographies/h3-shadcn-ui` | export default TypographyH3Demo | [instructions.md](typographies/h3-shadcn-ui/instructions.md) |
| `typographies/h4-shadcn-ui` | export default TypographyH4Demo | [instructions.md](typographies/h4-shadcn-ui/instructions.md) |
| `typographies/italic-decent-shadcn-ui` | export default TypographyBlockQuoteDemo | [instructions.md](typographies/italic-decent-shadcn-ui/instructions.md) |

## Individual component inventory — reviewed subset

Continuation checkpoint: 11 of 65 local instruction bundles reviewed; 13 independent renderers/providers identified in that subset; 54 bundles pending. Exact paths, hashes, findings and pending status are saved in `../ui-catalog-audit.checkpoint.json`. IDs assigned here must remain stable. Repeated copies of a demo within a bundle count once; column callbacks are subordinate implementation, not separate reusable components. Implementations are embedded in the linked instruction files, not standalone TSX files. Imported primitives are not included locally.

Domain codes: A CRM; B AI; C finance; D healthcare; E automation; F enterprise; G analytics; H SaaS; I commerce; J education. P = primary fit; S = secondary fit; L = limited fit; N = not applicable. These are design recommendations, not implemented product features. A neutral heading is secondary across domains, not a specialized domain solution.

| ID | Component / implementation | Observed purpose and limitations | Domain fit |
|---|---|---|---|
| COMP-001 | [PlotMetricToolUI](charts/chart-assistant-ui/instructions.md) | AI tool metric renderer; area variant receives label, value, delta and points. Actual Chart source absent. | P: B; S: G; L: A C E F H; N: D I J |
| COMP-002 | [MyRuntimeProvider](charts/chart-assistant-ui/instructions.md) | Nonvisual runtime/provider wiring with toolkit; toolkit absent. | P: B; S: —; L: A E F H; N: C D G I J |
| COMP-003 | [DialogSignInDemo](dashboards/data-showcase/data-table-shadcn-ui/instructions.md) | Sky-tinted sign-in dialog, labeled email/password, social icon buttons; nested forms and no submit/OAuth handlers. | P: H; S: A B F I J; L: C D E G; N: — |
| COMP-004 | [DataTableDemo](dashboards/data-showcase/data-table-shadcn-ui/instructions.md) | Bordered selectable payment table; right-aligned USD amounts; sorting/filtering/pagination models have no exposed controls. | P: A C F; S: E G I; L: B D H J; N: — |
| COMP-005 | [DataTableDensityDemo](dashboards/data-showcase/data-table-with-search-shadcn-ui/instructions.md) | Selectable payment table with three row-density settings; no search input despite folder name. Compact touch targets require review. | P: A C F G; S: E I; L: B D H J; N: — |
| COMP-006 | [TableWithVerticalLinesDemo](dashboards/data-tables/data-table-option-2-shadcn-ui/instructions.md) | Static four-column invoice table with vertical dividers, caption and footer; sample total is wrong ($2500 versus row sum $1750). | P: C I; S: A F G; L: B D E H J; N: — |
| COMP-007 | [TableDemo](dashboards/data-tables/simple-data-table-shadcn-ui/instructions.md) | Static four-column invoice table, caption and footer; sample total is wrong ($2500 versus row sum $1750). | P: C I; S: A F G; L: B D E H J; N: — |
| COMP-008 | [TypographyH1Demo](typographies/h1-shadcn-ui/instructions.md) | Page heading: text-3xl, extrabold, balanced wrapping, md:text-4xl. | P: —; S: A B C D E F G H I J; L: —; N: — |
| COMP-009 | [TypographyH2Demo](typographies/h2-shadcn-ui/instructions.md) | Section heading: text-3xl semibold. | P: —; S: A B C D E F G H I J; L: —; N: — |
| COMP-010 | [TypographyH3Demo](typographies/h3-shadcn-ui/instructions.md) | Subsection heading: text-2xl semibold, max-sm:w-full. | P: —; S: A B C D E F G H I J; L: —; N: — |
| COMP-011 | [TypographyH4Demo](typographies/h4-shadcn-ui/instructions.md) | Minor heading: text-xl semibold. | P: —; S: A B C D E F G H I J; L: —; N: — |
| COMP-012 | [TypographyBlockQuoteDemo](typographies/italic-decent-shadcn-ui/instructions.md) | Editorial blockquote with left border, pl-6, italics and max-w-2xl. | P: H J; S: —; L: A B C D E F G I; N: — |
| COMP-013 | [DrawerCart](dashboards/drawers/cart-drawer-shadcn-ui/instructions.md) | Right-side cart with product images, scrollable item summaries, totals and footer actions. Remove and Checkout lack handlers; totals are hardcoded even when items change. | P: I; S: —; L: H J; N: A B C D E F G |

### DrawerCart verification (COMP-013)

The complete bundle contains two copies of one component. Its embedded source is named `drawer-13.tsx`; `components/shadcn-studio/drawer/drawer-13.tsx` is a suggested integration destination, not an existing implementation path. Source attribution: shadcn Studio via the registry and destination. Product images come from the supplied shadcn Studio CDN URLs. Original component URL, author, attribution obligations and commercial restrictions are not specified; **License requires verification**.

| Dimension | Verified observation / integration decision |
|---|---|
| Purpose and placement | Cart review overlay on a store or marketplace; opens from a Cart button. Limited fit for paid SaaS add-ons or course purchases; not recommended for operational CRM, AI, finance, healthcare, automation, enterprise or analytics screens. |
| Visual character | Medium intensity: neutral stacked content, bordered rounded product thumbnails, muted descriptions, separators, destructive outline Remove buttons, primary Checkout action. |
| Interaction | `items` prop supplies rows; primitive-managed trigger and Continue Shopping close action. No item-removal handler, checkout handler, quantity control or explicit empty state. |
| Totals | Default prices sum correctly to $247.99; shipping $10 and total $257.99 are literals. Supplying different items does not update totals. Use numeric prices and computed totals in the application copy. |
| Motion | No explicit animation library, loop or scroll-triggered animation. Hover/focus classes change Remove colors. Right-side direction is configured, but transition timing and reduced-motion behavior require the absent drawer primitive. |
| Mobile/accessibility | Scrollable body, full-width Remove buttons, image alt text and DrawerTitle are supplied. No responsive breakpoints in this snippet. Drawer sizing, keyboard focus, Escape dismissal, touch behavior and reduced motion remain unverified. Hidden scrollbars may reduce overflow discoverability. |
| Performance/assets | Every item renders; no virtualization or explicit image lazy-loading policy. Remote asset availability and usage rights require verification. `no-scrollbar` styling is referenced but not supplied. |
| Dependencies | Required imported `lucide-react` (version/installation command not specified); declared React ^19, Tailwind CSS ^4, TypeScript ^5. Local button/drawer/separator implementations are missing, not npm package names. No optional dependency documented; installed-project status unverified. |
| Original commands | `npx shadcn@latest add @ss-components/drawer-13`; `npx shadcn@latest add button drawer separator`. Already preserved in the bundle command index. |
| Composition | Product page heading [TypographyH1Demo](typographies/h1-shadcn-ui/instructions.md) → Cart trigger → DrawerCart review → application checkout. The product listing and checkout must be implemented separately. Match font, radius, spacing and destructive colors; avoid stacking a sign-in dialog over the open cart. |

### Design situation and motion findings — reviewed subset

- COMP-001: in-conversation metric result, not a chat interface or financial charting system. Visual intensity, axes, keyboard behavior, animations and reduced-motion support cannot be verified without the imported Chart implementation. The snippet contains Markdown `>` artifacts that need repair in the application copy.
- COMP-002: nonvisual provider, not a dashboard component. No local animation; actual runtime compatibility requires verification.
- COMP-003: medium-intensity, sky-accented authentication overlay. User-input and click interaction; no local motion implementation. Dialog transition, focus trap, dismissal and reduced-motion support depend on absent primitives. Social logo images are remote shadcn Studio CDN assets.
- COMP-004/005: low-intensity, data-centric application tables. State-driven row selection; COMP-005 adds density selection and a CSS hover text-color change on its attribution link. No explicit animation loop, scroll animation or motion dependency. Large-dataset performance and mobile overflow require verification. Selection controls have aria-labels; primitive keyboard behavior is unverified.
- COMP-006/007: low-intensity, static report tables. No local animation, input handlers or responsive breakpoint behavior; overflow behavior depends on the imported table primitive. Prefer COMP-006 where column separation assists scanning, COMP-007 for less visual density.
- COMP-008–011: low-intensity static heading hierarchy. No animation or interaction; no continuous or scroll work; reduced-motion handling is unnecessary for the shown code. Use semantic heading order rather than choosing a tag solely for its size.
- COMP-012: low-intensity static editorial quote. No animation or interaction. Use for sourced testimonials or learning excerpts; not for operational records.

### Compatibility and small compositions — reviewed subset

- Invoice report: [TypographyH1Demo](typographies/h1-shadcn-ui/instructions.md) → [TypographyH2Demo](typographies/h2-shadcn-ui/instructions.md) → [TableDemo](dashboards/data-tables/simple-data-table-shadcn-ui/instructions.md). Neutral typography and aligned amounts support scanning. Replace demo data and calculate totals; normalize fonts and spacing. Use TableWithVerticalLinesDemo as an alternative, not a duplicate report.
- CRM customer list: [TypographyH1Demo](typographies/h1-shadcn-ui/instructions.md) → [DataTableDensityDemo](dashboards/data-showcase/data-table-with-search-shadcn-ui/instructions.md). Adapt payment fields to actual customer data. Add required search/pagination controls; they are not implemented by the existing folder's claimed search name. Use comfortable density for touch.
- AI metric integration: [MyRuntimeProvider and PlotMetricToolUI](charts/chart-assistant-ui/instructions.md) require retrieved Chart/toolkit implementations and a separately implemented conversation surface. This is an integration fragment, not a complete AI application recipe.
- Do not combine the two table variants' competing border treatments within the same report. Keep density, currency formatting and selection behavior consistent. Sky-colored authentication accents need approved token adaptation before combining with neutral enterprise tables.

### Dependency and source findings — reviewed subset

| Package / requirement | Components | Evidence / version / requirement |
|---|---|---|
| `@assistant-ui/react` | COMP-001/002 | Imported types and runtime APIs; version not specified; required for supplied integration |
| `@assistant-ui/ai-sdk` | COMP-002 | Imported useChatRuntime; version not specified; required |
| `@tanstack/react-table` | COMP-004/005 | Runtime import; shared required dependency; explicit `npm install @tanstack/react-table` in COMP-005 bundle; version not specified |
| `lucide-react` | COMP-003/005 | Runtime icon import; shared required dependency; exact package installation command not specified in reviewed bundles |
| `react` | COMP-004/005 and JSX components | useState imported by tables; ^19 declared in COMP-005–012 instructions; not a verified universal requirement |
| `tailwindcss`, `typescript` | COMP-005–012 | Tailwind CSS ^4 and TypeScript ^5 explicitly declared; styling/build requirements, not animation dependencies |
| Local table/checkbox/select/dialog/button/input/label and `cn` | COMP-003–007 as applicable | Aliased source requirements, not npm package names; implementations missing locally; do not assume Radix/Base UI API interchangeability |

No optional package is explicitly identified in these reviewed bundles. Existing-project dependency status is unverified. Preserve original commands in the dependency evidence table; do not infer packages from alias names.

Assistant UI attribution is explicit in its setup command and package imports. shadcn Studio attribution is supported by destination paths and registry identifiers. COMP-005 additionally embeds a Shadcn UI Blocks source link (`https://www.shadcnui-blocks.com/components/table`); this records supplied attribution, not independently verified provenance. Original component URLs are otherwise not specified in this reviewed subset. Author, attribution obligations and commercial restrictions are not specified. **License requires verification** for every reviewed component.


## Completion additions: COMP-102 to COMP-109

These eight records complete the 109-component ledger. Their exact source, stable ID, package evidence, and domain-fit values are also preserved in the checkpoint.

| ID | Component | Exact implementation | Purpose / intensity | Recommended fit |
|---|---|---|---|---|
| COMP-102 | MagicBento | [grids/magic-bento-react-bits](grids/magic-bento-react-bits/instructions.md) | Responsive linked feature bento; pointer glow, optional tilt/particles; high when all effects are enabled. | AI, automation, SaaS marketing feature section; adapt to neutral cards for enterprise. |
| COMP-103 | Hyperspeed | [landing/heros/hyperspeed-react-bits](landing/heros/hyperspeed-react-bits/instructions.md) | Three.js procedural road hero with hold-to-boost. Experimental. | Futuristic AI/SaaS landing page only. Never use behind dense app UI, healthcare, finance, or administration. |
| COMP-104 | SplashCursor | [landing/heros/splash-cursor](landing/heros/splash-cursor/instructions.md) | WebGL2 fluid cursor overlay. Experimental and GPU-intensive. | Single playful customer-facing campaign/landing page only; never operational UI. |
| COMP-105 | FlowingMenu | [navigation/menus/flowing-menu-react-bits](navigation/menus/flowing-menu-react-bits/instructions.md) | Editorial full-height menu and marquee reveal. Prominent. | Portfolio, product/brand navigation; avoid data-heavy product navigation. |
| COMP-106 | PillNav | [navigation/navbars/pill-nav-react-bits](navigation/navbars/pill-nav-react-bits/instructions.md) | Responsive compact nav with a collapsed menu. Moderate. | Marketing and lightweight SaaS top navigation; use solid/no-glass surface for business apps. |
| COMP-107 | CircularGallery | [reusable/galleries/circular-gallery-react-bits](reusable/galleries/circular-gallery-react-bits/instructions.md) | WebGL2 curved image carousel with keyboard fallback. Experimental. | Portfolio, visual learning, product discovery; not operational dashboards. |
| COMP-108 | FlexCarousel | [reusable/galleries/flex-carousel-react-bits](reusable/galleries/flex-carousel-react-bits/instructions.md) | OGL lens-distorted image carousel. Experimental. | Editorial/product showcase and commerce discovery; not work surfaces. |
| COMP-109 | Masonry | [reusable/galleries/Masonry-react-bits](reusable/galleries/Masonry-react-bits/instructions.md) | Responsive image masonry with optional lightbox/reorder. Moderate–prominent. | Catalogs, media, learning galleries and visual research; disable drag/parallax in business use. |

## Domain-based recommendations

Use **primary** first, then secondary only with the noted adaptation. The complete per-component P/S/L/N matrix is maintained in the checkpoint; this is the fast selection layer.

| Domain | Primary starting components | Secondary / conditional | Do not lead with |
|---|---|---|---|
| CRM / business management | LineSidebar, professional Kanban, data tables, profile drawer | PillNav, AnimatedList | Hyperspeed, SplashCursor, visual galleries |
| Agentic AI / AI products | Assistant UI metric renderer/runtime, MagicBento, LineSidebar | PillNav, ChromaGrid, Hyperspeed for a separate marketing page | Fluid cursor or gallery effects in agent workspaces |
| Finance / FinTech | DataTableDemo, DataTableDensityDemo, invoice tables, tabs | Plain cards, PillNav with solid surface | All WebGL heroes/galleries and glass navigation |
| Healthcare / medical | Appointment calendars, labeled sign-in forms, plain cards, neutral tables | Profile drawer, tabs | Hyperspeed, SplashCursor, FlowingMenu, distorted carousels |
| Automation / workflow | Professional Kanban, MagicBento automation visual, drawers, LineSidebar | AnimatedList, data tables | Decorative hero effects in execution screens |
| Enterprise / administration | Sidebar, data tables, tabs, drawers, Kanban | PillNav in solid mode | Marquees, fluid/glass overlays, experimental galleries |
| Data analytics / intelligence | PlotMetricToolUI, tables, ChromaGrid/MagicBento feature summaries | AnimatedList, tabs | Image-led effects as data visualizations |
| SaaS / customer-facing | Auth forms, PillNav, MagicBento, FAQ, standard cards | Masonry / carousels for a visual marketing page | Multiple competing animated backgrounds |
| E-commerce / marketplace | DrawerCart, invoice table, Masonry, FlexCarousel | Apple/Focus cards, appointment calendar only when relevant | Hyperspeed or SplashCursor at checkout |
| Education / learning | Calendars, typography, FAQ, Masonry/CircularGallery for course media | Tabs and cards | Motion-heavy decorative navigation in learner workflows |

## Design situation and motion index

| Situation | Preferred components | Motion policy |
|---|---|---|
| Operational navigation | LineSidebar, shadcn sidebar, simple tabs, PillNav (solid) | One subtle active-state system; do not pair with FlowingMenu. |
| Marketing navigation | PillNav or FlowingMenu | Choose one; FlowingMenu is the page’s dominant movement. |
| Product/AI marketing hero | MagicBento feature section; Hyperspeed as a background only | Hyperspeed must be the sole prominent animation and must have a static/reduced-motion fallback. |
| Business dashboard | Data tables, professional Kanban, drawers, tabs, plain cards | No continuous background, marquee, or cursor effect. |
| AI conversation / metrics | Assistant UI metrics/runtime plus application-built conversation surface | Metrics are a tool fragment, not a complete chat experience. |
| Visual catalog / editorial | Masonry, CircularGallery, or FlexCarousel | Pick one gallery pattern per page; never nest them or autoplay beside a marquee. |
| Authentication / settings | Sign-in or card forms, dialog/drawer primitives | Functional validation, focus handling, and native semantics take priority over animation. |

### Motion safety rules

- `Hyperspeed`, `SplashCursor`, `CircularGallery`, and `FlexCarousel` are GPU/WebGL effects. Feature-detect, lazy-load, provide static fallbacks, test low-end mobile, and never stack more than one on a route.
- `MagicBento`, `FlowingMenu`, `PillNav`, and `Masonry` have reduced-motion branches, but source inspection is not a browser accessibility test. Verify `prefers-reduced-motion` after integration.
- Do not combine a continuous hero/background with a marquee, scroll-reveal grid, and a moving gallery. Choose one prominent motion system plus subtle state feedback.

## Component composition recipes

| Product structure | Exact components / sequence | Why it works and required adaptation |
|---|---|---|
| CRM operations | [LineSidebar](navigation/sidebars/line-sidebar-react-bits/instructions.md) → [KanbanDemo](dashboards/kanbans/professional-karban-shadcn-ui/instructions.md) → [DataTableDensityDemo](dashboards/data-showcase/data-table-with-search-shadcn-ui/instructions.md) → [DrawerProfile](dashboards/drawers/profile-drawer-shadcn-ui/instructions.md) | Shared operational density. Replace demo data and add real search/pagination; use one neutral token system; omit decorative motion. |
| AI agent platform | [PillNav](navigation/navbars/pill-nav-react-bits/instructions.md) or LineSidebar → [PlotMetricToolUI](charts/chart-assistant-ui/instructions.md) → [MagicBento](grids/magic-bento-react-bits/instructions.md) | Separates navigation, agent output and feature overview. Build the actual conversation/execution UI separately; use MagicBento with tilt/particles disabled in the app. |
| Finance overview | [TypographyH1Demo](typographies/h1-shadcn-ui/instructions.md) → [DataTableDemo](dashboards/data-showcase/data-table-shadcn-ui/instructions.md) → [TabsWithBadgeDemo](navigation/tabs/notification-with-tab-shadcn-ui/instructions.md) | Scannable and restrained. Replace payment samples, calculate totals, add real filtering, and do not use glass/continuous motion. |
| Learning catalog | [PillNav](navigation/navbars/pill-nav-react-bits/instructions.md) → [Masonry](reusable/galleries/Masonry-react-bits/instructions.md) → [CollapsibleShowMoreDemo](landing/faqs/faq-shadcn-ui/instructions.md) | Supports discovery and help content. Use image alt text, disable mouse-only reorder, and keep the lightbox keyboard-tested. |
| Commerce discovery | [PillNav](navigation/navbars/pill-nav-react-bits/instructions.md) → [Masonry](reusable/galleries/Masonry-react-bits/instructions.md) **or** [FlexCarousel](reusable/galleries/flex-carousel-react-bits/instructions.md) → [DrawerCart](dashboards/drawers/cart-drawer-shadcn-ui/instructions.md) | Uses one discovery surface and a functional cart review. Never pair both galleries; cart totals/removal/checkout must be wired to real state. |

## Dependency, source, and license completion notes

| Dependency | Components | Status |
|---|---|---|
| `@hugeicons/react`, `@hugeicons/core-free-icons` | COMP-102, 105, 109 and other React Bits bundles | Required imports where used; versions absent. |
| `three` | COMP-103 Hyperspeed | Required import; package version absent. |
| `ogl` | COMP-108 FlexCarousel | Required import; package version absent. |
| Browser WebGL2 | COMP-104 SplashCursor; COMP-107 CircularGallery | Runtime platform requirement, not an npm package. |
| `react-dom` | COMP-109 Masonry | Required for `createPortal`; version absent. |

Every reviewed source is attributed to its instruction bundle and named ecosystem. Original component URLs, authors, explicit attribution requirements, commercial restrictions, and license terms are absent or insufficient in local materials: **License requires verification** for every selected component before production use. Registry commands (`npx shadcn ... add`) are installation evidence, not license evidence.

## Category index

- [charts](charts/): 1 instruction bundles.
- [dashboards](dashboards/): 10 instruction bundles.
- [forms](forms/): 5 instruction bundles.
- [grids](grids/): 2 instruction bundles.
- [landing](landing/): 9 instruction bundles.
- [navigation](navigation/): 10 instruction bundles.
- [reusable](reusable/): 23 instruction bundles.
- [typographies](typographies/): 5 instruction bundles.

## Dependency evidence

The following commands are copied from standalone command lines in the source instructions. They are evidence, not commands executed during this audit. Registry identifiers are not npm dependencies. This extraction does not capture all inline commands, imports, versions, optional dependencies, or transitive requirements. For example, the Assistant UI chart includes the inline command `npx assistant-ui@latest setup --products elements/chart` and imports `@assistant-ui/react` and `@assistant-ui/ai-sdk`.

Install dependencies selectively only after inspecting a chosen implementation and the target project. `latest` is not a pinned version. Package compatibility, optionality, and licenses require verification. Some typography instructions explicitly specify React ^19, Tailwind CSS ^4, and TypeScript ^5; do not apply those requirements indiscriminately to every bundle.

| Instructions | Verbatim standalone command evidence |
|---|---|
| [charts/chart-assistant-ui](charts/chart-assistant-ui/instructions.md) | Not found by standalone-line extraction; inspect inline instructions |
| [dashboards/data-showcase/data-table-shadcn-ui](dashboards/data-showcase/data-table-shadcn-ui/instructions.md) | `npx shadcn@latest add @ss-components/data-table-01` |
| [dashboards/data-showcase/data-table-with-search-shadcn-ui](dashboards/data-showcase/data-table-with-search-shadcn-ui/instructions.md) | `npm install @tanstack/react-table`<br>`npx shadcn@latest add checkbox select table utils`<br>`npx shadcn@latest add @ss-components/data-table-02` |
| [dashboards/data-tables/data-table-option-2-shadcn-ui](dashboards/data-tables/data-table-option-2-shadcn-ui/instructions.md) | `npx shadcn@latest add @ss-components/table-04`<br>`npx shadcn@latest add table` |
| [dashboards/data-tables/simple-data-table-shadcn-ui](dashboards/data-tables/simple-data-table-shadcn-ui/instructions.md) | `npx shadcn@latest add table`<br>`npx shadcn@latest add @ss-components/table-01` |
| [dashboards/drawers/cart-drawer-shadcn-ui](dashboards/drawers/cart-drawer-shadcn-ui/instructions.md) | `npx shadcn@latest add @ss-components/drawer-13`<br>`npx shadcn@latest add button drawer separator` |
| [dashboards/drawers/nooverlay-scrollable-content-drawer-shadcn-ui](dashboards/drawers/nooverlay-scrollable-content-drawer-shadcn-ui/instructions.md) | `npx shadcn@latest add @ss-components/drawer-06`<br>`npx shadcn@latest add button drawer` |
| [dashboards/drawers/profile-drawer-shadcn-ui](dashboards/drawers/profile-drawer-shadcn-ui/instructions.md) | `npx shadcn@latest add @ss-components/drawer-14`<br>`npx shadcn@latest add button drawer separator avatar` |
| [dashboards/drawers/scrollable-content-drawer-shadcn-ui](dashboards/drawers/scrollable-content-drawer-shadcn-ui/instructions.md) | `npx shadcn@latest add button drawer`<br>`npx shadcn@latest add @ss-components/drawer-03` |
| [dashboards/kanbans/professional-karban-shadcn-ui](dashboards/kanbans/professional-karban-shadcn-ui/instructions.md) | `npm install @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities @base-ui/react react-dom`<br>`npx shadcn@latest add button badge utils`<br>`npx shadcn@latest add @ss-components/kanban-01` |
| [dashboards/kanbans/simple-kanban-shadcn-ui](dashboards/kanbans/simple-kanban-shadcn-ui/instructions.md) | `npx shadcn@latest add navigation-menu`<br>`npx shadcn@latest add @ss-components/kanban-03` |
| [forms/drawer-signin-shadcn-ui](forms/drawer-signin-shadcn-ui/instructions.md) | `npx shadcn@latest add @ss-components/drawer-05`<br>`npx shadcn@latest add button drawer input label textarea` |
| [forms/login-card-form-shadcn-ui](forms/login-card-form-shadcn-ui/instructions.md) | `npx shadcn@latest add @ss-components/card-01`<br>`npx shadcn@latest add button card input label` |
| [forms/sign-in-form-shadcn-ui](forms/sign-in-form-shadcn-ui/instructions.md) | `npx shadcn@latest add button checkbox dialog input label`<br>`npx shadcn@latest add @ss-components/dialog-14` |
| [forms/signup-form-accernity-ui](forms/signup-form-accernity-ui/instructions.md) | `npx shadcn@latest add @aceternity/signup-form-demo` |
| [forms/signup-form-shadcn-ui](forms/signup-form-shadcn-ui/instructions.md) | `npx shadcn@latest add @ss-components/dialog-13`<br>`npx shadcn@latest add button checkbox dialog input label` |
| [grids/chroma-grids-react-bits](grids/chroma-grids-react-bits/instructions.md) | `npx shadcn@latest add @react-bits/ChromaGrid-TS-TW` |
| [grids/magic-bento-react-bits](grids/magic-bento-react-bits/instructions.md) | `npx shadcn@latest add @react-bits/MagicBento-TS-TW` |
| [landing/faqs/faq-shadcn-ui](landing/faqs/faq-shadcn-ui/instructions.md) | `npx shadcn@latest add collapsible`<br>`npx shadcn@latest add @ss-components/collapsible-06` |
| [landing/footer-components/github-globe-accernity-ui](landing/footer-components/github-globe-accernity-ui/instructions.md) | `npx shadcn@latest add @aceternity/globe-demo` |
| [landing/heros/cloud-shader-accernity-ui](landing/heros/cloud-shader-accernity-ui/instructions.md) | `npx shadcn@latest add @aceternity/cloud-shader`<br>`npx shadcn@latest add @aceternity/cloud-shader-hero-demo` |
| [landing/heros/hyperspeed-react-bits](landing/heros/hyperspeed-react-bits/instructions.md) | `npx shadcn@latest add @react-bits/Hyperspeed-TS-TW` |
| [landing/heros/scroll-explained-react-bits](landing/heros/scroll-explained-react-bits/instructions.md) | `npx shadcn@latest add @react-bits/ScrollExpand-TS-TW` |
| [landing/heros/splash-cursor](landing/heros/splash-cursor/instructions.md) | `npx shadcn@latest add @react-bits/SplashCursor-TS-TW` |
| [landing/heros/threads-react-bits](landing/heros/threads-react-bits/instructions.md) | `npx shadcn@latest add @react-bits/Threads-TS-TW` |
| [landing/heros/wavy-background-accernity-ui](landing/heros/wavy-background-accernity-ui/instructions.md) | `npx shadcn@latest add @aceternity/wavy-background-demo` |
| [landing/testimonials/infinite-moving-cards-accernity-ui](landing/testimonials/infinite-moving-cards-accernity-ui/instructions.md) | `npx shadcn@latest add @aceternity/infinite-moving-cards-demo` |
| [navigation/menus/branched-menu-react-bits](navigation/menus/branched-menu-react-bits/instructions.md) | `npm install @hugeicons/react @hugeicons/core-free-icons` |
| [navigation/menus/flowing-menu-react-bits](navigation/menus/flowing-menu-react-bits/instructions.md) | `npx shadcn@latest add @react-bits/FlowingMenu-TS-TW` |
| [navigation/navbars/navbar-menu](navigation/navbars/navbar-menu/instructions.md) | `npx shadcn@latest add @ss-components/navigation-menu-01`<br>`npx shadcn@latest add navigation-menu` |
| [navigation/navbars/pill-nav-react-bits](navigation/navbars/pill-nav-react-bits/instructions.md) | `npx shadcn@latest add @react-bits/PillNav-TS-TW` |
| [navigation/navbars/simple-nav-bar-shadcn-ui](navigation/navbars/simple-nav-bar-shadcn-ui/instructions.md) | `npx shadcn@latest add menubar`<br>`npx shadcn@latest add @ss-components/menubar-08` |
| [navigation/sidebars/line-sidebar-react-bits](navigation/sidebars/line-sidebar-react-bits/instructions.md) | `npx shadcn@latest add @react-bits/LineSidebar-TS-TW` |
| [navigation/sidebars/sidebar-accernity-ui](navigation/sidebars/sidebar-accernity-ui/instructions.md) | `npx shadcn@latest add @aceternity/sidebar-demo` |
| [navigation/tabs/icon-tab-shadcn-ui](navigation/tabs/icon-tab-shadcn-ui/instructions.md) | `npx shadcn@latest add tabs`<br>`npx shadcn@latest add @ss-components/tabs-03` |
| [navigation/tabs/notification-with-tab-shadcn-ui](navigation/tabs/notification-with-tab-shadcn-ui/instructions.md) | `npx shadcn@latest add badge tabs`<br>`npx shadcn@latest add @ss-components/tabs-04` |
| [navigation/tabs/simple-tab-shadcn-ui](navigation/tabs/simple-tab-shadcn-ui/instructions.md) | `npx shadcn@latest add tabs`<br>`npx shadcn@latest add @ss-components/tabs-02` |
| [reusable/buttons/go-to-settings-shadcn-ui](reusable/buttons/go-to-settings-shadcn-ui/instructions.md) | `npx shadcn@latest add @ss-components/button-16` |
| [reusable/buttons/notifications-button-shadcn-ui](reusable/buttons/notifications-button-shadcn-ui/instructions.md) | `npx shadcn@latest add @ss-components/button-25` |
| [reusable/buttons/shadcn-ui-buttons](reusable/buttons/shadcn-ui-buttons/instructions.md) | `npx shadcn@latest add @ss-components/button-06` |
| [reusable/buttons/specular-button-react-bits](reusable/buttons/specular-button-react-bits/instructions.md) | `npx shadcn@latest add @react-bits/SpecularButton-TS-TW` |
| [reusable/buttons/star-border-react-bits](reusable/buttons/star-border-react-bits/instructions.md) | `npx shadcn@latest add @react-bits/StarBorder-TS-TW` |
| [reusable/buttons/tailwind-css-buttons-accernity-ui](reusable/buttons/tailwind-css-buttons-accernity-ui/instructions.md) | `npx shadcn@latest add @aceternity/tailwindcss-buttons-demo` |
| [reusable/calender/book-your-appointment-shadcn-ui](reusable/calender/book-your-appointment-shadcn-ui/instructions.md) | `npx shadcn@latest add @ss-components/calendar-24`<br>`npx shadcn@latest add button calendar card scroll-area` |
| [reusable/calender/normal-usage-calender-shadcn-ui](reusable/calender/normal-usage-calender-shadcn-ui/instructions.md) | `npx shadcn@latest add button calendar card scroll-area`<br>`npx shadcn@latest add @ss-components/calendar-17` |
| [reusable/cards/apple-cards-carousel-accernity-ui](reusable/cards/apple-cards-carousel-accernity-ui/instructions.md) | `npx shadcn@latest add @aceternity/apple-cards-carousel-demo` |
| [reusable/cards/bounce-cards-react-bits](reusable/cards/bounce-cards-react-bits/instructions.md) | `npx shadcn@latest add @react-bits/BounceCards-TS-TW` |
| [reusable/cards/decent-plain-card-shadcn-ui](reusable/cards/decent-plain-card-shadcn-ui/instructions.md) | `npx shadcn@latest add button card`<br>`npx shadcn@latest add @ss-components/card-05` |
| [reusable/cards/focus-cards-accernity-ui](reusable/cards/focus-cards-accernity-ui/instructions.md) | `npx shadcn@latest add @aceternity/focus-cards-demo` |
| [reusable/cards/pixel-cards-react-bits](reusable/cards/pixel-cards-react-bits/instructions.md) | `npx shadcn@latest add @react-bits/PixelCard-TS-TW` |
| [reusable/cards/profile-card-react-bits](reusable/cards/profile-card-react-bits/instructions.md) | `npx shadcn@latest add @react-bits/ProfileCard-TS-TW` |
| [reusable/cards/titled-card-react-bits](reusable/cards/titled-card-react-bits/instructions.md) | `npx shadcn@latest add @react-bits/TiltedCard-TS-TW` |
| [reusable/cards/wobble-cards-accernity-ui](reusable/cards/wobble-cards-accernity-ui/instructions.md) | `npx shadcn@latest add @aceternity/wobble-card-demo` |
| [reusable/dialog-boxes-or-menu-shadcn-ui](reusable/dialog-boxes-or-menu-shadcn-ui/instructions.md) | `npx shadcn@latest add @ss-components/dialog-07`<br>`npx shadcn@latest add button dialog scroll-area` |
| [reusable/galleries/accordian-gallery-react-bits](reusable/galleries/accordian-gallery-react-bits/instructions.md) | `npm install gsap` |
| [reusable/galleries/circular-gallery-react-bits](reusable/galleries/circular-gallery-react-bits/instructions.md) | `npx shadcn@latest add @react-bits/CircularGallery-TS-TW` |
| [reusable/galleries/flex-carousel-react-bits](reusable/galleries/flex-carousel-react-bits/instructions.md) | `npx shadcn@latest add @react-bits/FlexCarousel-TS-TW` |
| [reusable/galleries/gradual-blur-react-bits](reusable/galleries/gradual-blur-react-bits/instructions.md) | `npx shadcn@latest add @react-bits/GradualBlur-TS-TW` |
| [reusable/galleries/Masonry-react-bits](reusable/galleries/Masonry-react-bits/instructions.md) | `npx shadcn@latest add @react-bits/Masonry-TS-TW` |
| [reusable/lists/animated-list-react-bits](reusable/lists/animated-list-react-bits/instructions.md) | `npx shadcn@latest add @react-bits/AnimatedList-TS-TW` |
| [typographies/h1-shadcn-ui](typographies/h1-shadcn-ui/instructions.md) | `npx shadcn@latest add @ss-components/typography-01` |
| [typographies/h2-shadcn-ui](typographies/h2-shadcn-ui/instructions.md) | `npx shadcn@latest add @ss-components/typography-02` |
| [typographies/h3-shadcn-ui](typographies/h3-shadcn-ui/instructions.md) | `npx shadcn@latest add @ss-components/typography-03` |
| [typographies/h4-shadcn-ui](typographies/h4-shadcn-ui/instructions.md) | `npx shadcn@latest add @ss-components/typography-04` |
| [typographies/italic-decent-shadcn-ui](typographies/italic-decent-shadcn-ui/instructions.md) | `npx shadcn@latest add @ss-components/typography-06` |

## Mandatory implementation workflow

1. Read the official theme/problem statement, `documents/idea.md`, `documents/design.md`, `documents/ARCHITECTURE.md`, `documents/planning.md`, and applicable frontend requirements. Identify users, workflows, domain, and approved visual direction.
2. Read this README before opening component folders. Until the domain and design situation recommendations are completed, use this inventory only as a location and evidence index.
3. Shortlist a small coherent selection by functional needs, hierarchy, visual direction, motion budget, dependency cost, and compatibility. The library is optional; use only components that improve the product.
4. Open every selected `instructions.md`. Read all embedded implementations, original prompts, commands, usage examples, and configuration. Never implement solely from this catalog or a folder name.
5. Check existing dependencies and installed versions. Install only missing required dependencies; verify aliases, registry setup, primitive APIs, and version compatibility. Never install the entire collection.
6. Adapt application copies to approved fonts, tokens, spacing, radii, responsive layout, accessibility, and architecture. Preserve the library originals. Do not combine competing hero backgrounds or multiple intensive effects. Normalize density and interaction behavior across components.
7. Verify actual behavior, visual appearance, responsiveness, reduced-motion handling, keyboard operation, console errors, and performance. Demo data and controls are not working authentication, payment, healthcare, or AI services.

## Limitations and outstanding analysis

This historical section predates completion of the source review. Statements that component/domain review is incomplete or that 54 bundles are pending are superseded by the 65-bundle, 109-record checkpoint. The remaining limitations below still apply: no browser run, no dependency installation, no license confirmation, and imported primitives unavailable locally.

- Individual-component boundaries remain unverified. The data-showcase/data-table bundle contains both `DialogSignInDemo` and `DataTableDemo`; the simple-kanban bundle also exports `NavigationMenuDemo`. The normal-calendar bundle includes booking and week-number demos. Preserve these distinctions during deeper review.
- Domain recommendations for CRM, AI, finance, healthcare, automation, enterprise, analytics, SaaS, commerce, and education remain **Not inspected** at the required implementation depth.
- Design situation and animation indexes, composition recipes, per-component metadata, and consolidated dependency/version/optional-requirement mappings remain incomplete. No unverified recipes are presented as approved compositions.
- Original source URLs, prompt availability, license terms, missing local primitives, external assets, and framework compatibility require per-bundle review. Registry commands do not establish license permission.
- Full collection review is incomplete. The continuation reviewed 11 local bundles (13 independent renderers/providers); 54 remain pending. The reviewed-subset section supersedes the earlier blanket uninspected labels for those entries. Referenced Chart, toolkit and UI primitives are unavailable locally. The checkpoint records exact pending paths and source hashes.
- Filename standardization renamed 14 `instruction.md` files and one `usage-instructions.md` file to `instructions.md`. No target collisions were found. Original byte hashes were recorded for preservation validation.
- The existing frontend rules file ends mid-sentence in its Browser Verification section. That pre-existing incomplete text was preserved.

