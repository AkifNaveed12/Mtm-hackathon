---
trigger: glob
globs: frontend/**/*.{js,jsx,ts,tsx}, frontend/**/*.{css,scss}, frontend/**/*.html
---

# Frontend Engineering Rules

## 1. Core Principles

The frontend must prioritize:

1. Correct implementation of official hackathon requirements.
2. Functional user journeys.
3. Clear and deliberate user experience.
4. Consistent visual design.
5. Responsive behavior.
6. Accessibility.
7. Performance.
8. Maintainability.
9. Reliable backend integration.

Build a complete working product, not merely a landing page or visual prototype.

Do not over-engineer the frontend during the hackathon.

## 2. Source of Truth

Before implementation, inspect:

- `AGENTS.md`
- Applicable `.agents/rules/`
- Relevant `.agents/skills/`
- Finalized documentation inside `documents/`
- `documents/idea.md`, if present
- `documents/planning.md`, if present
- `documents/design.md`, if present
- `documents/API-CONTRACT.md`, if present
- `documents/ARCHITECTURE.md`, if present
- Existing frontend implementation
- Root `ui-library/`, if present
- Supplied fonts and assets

The official hackathon theme and its extracted mandatory requirements take precedence over design preferences.

The approved `documents/design.md` is the visual design source of truth when available.

Do not invent requirements or contradict finalized project decisions.

## 3. Technology and Architecture

Use the existing approved frontend stack.

The default project direction is:

- Next.js
- TypeScript
- React
- CSS or the styling system selected by the Architect
- Vercel for frontend deployment

Rules:

- Inspect the existing project before choosing or changing frameworks.
- Use the existing Next.js routing architecture.
- Do not migrate App Router to Pages Router or vice versa without approval.
- Keep components modular and reusable.
- Separate UI, application logic, API communication, and state management appropriately.
- Respect React server/client component boundaries.
- Use client components only when browser-side interactivity is required.
- Avoid unnecessary global state.
- Avoid unnecessary abstractions and dependencies.

Do not introduce another frontend framework.

## 4. Mandatory UI/UX Compliance

The official hackathon theme document is authoritative for mandatory UI/UX requirements.

Before implementation:

1. Read the extracted UI requirements.
2. Identify mandatory screens and components.
3. Identify required navigation and layouts.
4. Identify required colors, typography, branding, and visual restrictions.
5. Identify mandatory interactions.
6. Implement those requirements.
7. Verify the final UI against them.

Never replace an explicit hackathon requirement with personal design preference.

If a requirement is ambiguous, report it to the Project Lead.

## 5. Design Quality

The interface must look deliberately designed rather than generated from a generic template.

Prioritize:

- Strong visual hierarchy
- Consistent typography
- Intentional whitespace
- Balanced layouts
- Clear navigation
- Appropriate content density
- Consistent component sizing
- Carefully selected colors
- Meaningful visual elements
- Professional interaction states

Avoid generic AI-generated UI patterns:

- Default blue/purple gradients
- Random gradients without a design reason
- Excessive glassmorphism
- Glowing cards everywhere
- Unnecessary blur effects
- Generic dashboard layouts
- Repeated identical card grids
- Excessive rounded containers
- Decorative elements without purpose
- Fake statistics and fabricated metrics
- Placeholder buttons that do nothing
- Unnecessary filler copy

Do not use a gradient simply because it looks modern. Use one only when the approved design explicitly requires it or when it has a clear design purpose.

Do not sacrifice usability to add visual complexity.

## 6. Design System

Create or follow the approved design system.

Keep consistent:

- Color tokens
- Typography scale
- Font weights
- Line heights
- Spacing scale
- Border radius
- Shadows
- Borders
- Button variants
- Input styles
- Card styles
- Icon sizing
- Breakpoints
- Animation behavior
- Focus and interaction states

Avoid introducing arbitrary colors, spacing, radii, or shadows in individual components.

Use shared design tokens where practical.

Do not create a new design system when an approved one already exists.

## 7. UI Library Integration

The user manually collects reusable components in the root `ui-library/` directory.

This directory is a source library, not an instruction to install or render every component.

Before using a component:

1. Inspect the actual `ui-library/` contents.
2. Understand the component's purpose.
3. Inspect its source code.
4. Identify dependencies.
5. Check styling assumptions.
6. Check required icon or animation libraries.
7. Check compatibility with the current frontend stack.
8. Decide whether it genuinely improves the required interface.

Integration rules:

- Select only components relevant to the product.
- Do not install every component or library in the directory.
- Do not assume a component exists without inspecting it.
- Do not blindly copy code with incompatible dependencies.
- Install only the dependencies required by selected components.
- Avoid duplicate or conflicting packages.
- Adapt components to the approved design system.
- Ensure responsiveness and accessibility.
- Preserve the original `ui-library/` source files.
- Do not overwrite or reorganize the source library unless explicitly requested.

Integrate selected components into the application's actual component structure.

Do not make the application depend on unused or unnecessary UI packages.

## UI Library Intelligence and Component Selection

Always read `documents/idea.md`, the approved `documents/DESIGN.md`, and `ui-library/README.md` before selecting reusable UI components. Infer the product domain and required user journeys from the idea, then use the catalog's domain matrix, design situation index, and composition recipes to select a coherent screen-by-screen set. Distinguish operational screens from marketing pages: an AI landing effect is not an AI workflow interface. Respect missing-source and untested-runtime labels.

For every selection, verify the actual folder exists and read its `instructions.md`, including implementation code. Reuse the original prompt, installation command, and source where appropriate. Never implement from the catalog description alone or assume a component exists.

Check project dependencies and component-specific requirements before installing anything. Install only missing required packages with compatible versions; never install all library dependencies indiscriminately.

Adapt selections to the approved design system, typography, colors, spacing, responsive layouts, accessibility, and architecture. Avoid conflicting visual languages, competing backgrounds, excessive animation, and decorative effects. Preserve all original `ui-library/` source files.

**Use `ui-library/` as the exclusive source of reusable UI components for this project.** Select only relevant components; never import unrelated templates, UI kits, or components from external catalogs. Original installation commands may supply dependencies and missing primitives explicitly referenced by a selected local bundle; this does not authorize adding unrelated components.

Compose and adapt application copies, wire real data and interactions, and implement necessary layout and business logic using those selections. Preserve the original library. If a required UI capability cannot be composed from the collection, report the exact gap to the Project Lead and request a scoped exception from the user; do not silently substitute an external component or omit a required workflow. Continue independent work while the gap is resolved.

Record selected component IDs, source paths, placement, required adaptations, and unresolved gaps in the existing `documents/PLANNING.md`; keep approved tokens and visual decisions in `documents/DESIGN.md`. Do not create a competing design-system document. Apply the same typography, semantic colors, spacing, radii, icon treatment, density, focus states, breakpoints, and motion policy to every application copy. Prefer primary domain fits, use secondary fits with the recorded adaptations, and avoid limited/not-applicable fits unless the user approves the specific placement.

Use the composition and motion indexes to prevent competing heroes, stacked marquees, incompatible overlay behavior, and excessive continuous effects. Verify mobile/touch behavior, keyboard operation, reduced motion, and actual functionality after integration; source inspection alone is not a browser test. Demo labels, counters, calendars, payments, and AI tool wrappers must never be presented as implemented services.

## 8. Fonts and Typography

Inspect the fonts supplied with the project.

Use the supplied fonts when they are intended for the product.

Verify:

- Font family
- Available weights
- File formats
- Italic variants, if required
- Correct font loading
- Fallback behavior

For local font files, use the appropriate Next.js font-loading approach, such as `next/font/local`, when compatible with the project.

Do not reference font files that do not exist.

Do not invent font weights or claim that a font has been integrated without verifying it.

Typography must remain consistent across headings, body text, labels, buttons, forms, and navigation.

## 9. Images and Visual Assets

Use assets that support the product's actual requirements.

Prefer:

- Relevant product imagery
- Appropriate illustrations
- SVG assets
- Transparent-background graphics where useful
- Optimized images
- Meaningful icons
- Carefully selected background imagery

Rules:

- Do not fabricate product screenshots or statistics.
- Do not use irrelevant stock imagery as decoration.
- Do not introduce copyrighted assets without appropriate permission.
- Do not create unnecessary image assets.
- Optimize large images.
- Use `next/image` where appropriate.
- Provide meaningful alternative text for informative images.
- Treat decorative images appropriately for accessibility.

## 10. Animation and Motion

Use animation to improve understanding and interaction, not merely to make the interface move.

Approved options may include:

- Framer Motion
- GSAP

Use only when justified by the design and existing project architecture.

Suitable use cases:

- Page transitions
- Component entrance animations
- Meaningful hover interactions
- Scroll-triggered reveals
- Horizontal scroll sections
- Vertical scroll storytelling
- Navigation transitions
- Interactive feedback

Rules:

- Do not introduce both animation libraries without a clear need.
- Avoid excessive motion.
- Avoid animation that delays important interactions.
- Respect `prefers-reduced-motion`.
- Ensure animations work on mobile.
- Avoid expensive scroll handlers.
- Avoid layout shifts.
- Keep animation behavior consistent with the design system.

Do not add horizontal or vertical scroll animation simply for decoration.

## 11. Functional Screens and Interactions

Implement every required screen and interaction from the approved requirements.

Examples, when required:

- Landing page
- Authentication
- User dashboard
- Forms
- Data submission
- Search and filtering
- File upload
- AI interaction
- Results and reports
- Settings
- User profile
- Administrative interfaces

Every visible interactive element must have a meaningful action.

Never leave:

- Dead buttons
- Fake navigation
- Nonfunctional forms
- Decorative controls that appear interactive
- Hardcoded success messages
- Fake API responses

Implement the necessary states:

- Initial
- Loading
- Success
- Empty
- Validation error
- API error
- Disabled
- Authentication-required

## 12. API Integration

Read `documents/API-CONTRACT.md` when available.

Never invent:

- Endpoint paths
- HTTP methods
- Request fields
- Response fields
- Authentication behavior
- Error structures

Use the actual backend contract.

Create a consistent API communication layer when appropriate.

Requirements:

- Use environment-based API URLs.
- Handle HTTP errors.
- Handle network failures.
- Handle request timeouts where appropriate.
- Validate or safely parse responses.
- Handle loading and error states.
- Pass authentication correctly.
- Avoid unnecessary repeated requests.

Do not hardcode production or localhost URLs throughout components.

Never expose private credentials through `NEXT_PUBLIC_` variables.

If the API contract does not match the backend implementation, coordinate with the Project Lead and Integration Agent rather than silently changing it.

## 13. Forms and Data Handling

Forms must:

- Use appropriate input types.
- Provide clear labels.
- Validate user input.
- Display useful validation messages.
- Prevent accidental duplicate submissions.
- Show loading/submission states.
- Handle server-side validation errors.
- Display meaningful success or failure feedback.

Do not assume client-side validation replaces backend validation.

Do not fabricate submitted records or successful transactions.

## 14. Responsive Design

The interface must work across:

- Desktop
- Laptop
- Tablet
- Mobile

Use responsive layouts rather than fixed dimensions that only work at one resolution.

Verify:

- Navigation behavior
- Text wrapping
- Image scaling
- Grid and flex layouts
- Form usability
- Dialog and modal behavior
- Overflow
- Horizontal scrolling
- Touch interactions

Do not treat mobile responsiveness as a final optional polish task.

## 15. Accessibility

Use semantic HTML.

Interactive elements must be keyboard accessible.

Provide:

- Labels for form controls
- Useful button text
- Alternative text for meaningful images
- Visible focus states
- Appropriate heading hierarchy
- Accessible dialog behavior
- Sufficient contrast
- Keyboard-operable navigation

Do not rely exclusively on color to communicate important information.

Respect reduced-motion preferences.

## 16. Performance

- Avoid unnecessary network requests.
- Avoid unnecessary re-renders.
- Optimize large images and assets.
- Lazy-load expensive resources when appropriate.
- Avoid unnecessary client components.
- Avoid unnecessarily large dependencies.
- Avoid blocking the initial render with nonessential effects.
- Do not prematurely optimize simple components.

Use appropriate Next.js performance features when they fit the application.

## 17. Security

- Never expose secrets in client-side code.
- Never put private API keys in frontend environment variables.
- Never rely on frontend checks for authorization.
- Treat API responses as untrusted data.
- Avoid unsafe HTML rendering.
- Do not expose internal server errors.
- Do not store sensitive authentication data insecurely.
- Follow the repository's security rules.

## 18. Browser Verification

After significant UI or integration changes:

1. Start the application.
2. Open it in a browser.
3. Verify the affected scr
