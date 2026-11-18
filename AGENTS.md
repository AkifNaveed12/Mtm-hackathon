# AGENTS.md — GLOBAL PROJECT DEVELOPMENT INSTRUCTIONS

## 1. PURPOSE

This file defines the global development rules, project context, documentation authority, engineering standards, and collaboration requirements for every AI coding agent operating in this repository.

Every agent must read and follow these instructions before performing project work.

These instructions apply to:

- Project Lead
- Architect
- Frontend
- Backend
- AI Engineer
- Integration
- QA/Security
- Deployment

Specialized agent instructions and applicable rules provide additional responsibilities and implementation-specific guidance.

If an instruction conflicts with a higher-priority system or safety requirement, follow the higher-priority requirement.

---

# 2. PROJECT DEVELOPMENT PHILOSOPHY

The objective is to build a complete, functional, professional-quality hackathon product within a strict development window.

The application must solve the actual problem described in the official hackathon theme.

Prioritize:

1. Correct understanding of the problem.
2. Complete implementation of the approved MVP.
3. Reliable frontend/backend integration.
4. Working AI/ML functionality where required.
5. Real data persistence.
6. Professional UI/UX.
7. Security and reliability.
8. Testing and deployment.

Do not optimize for the quantity of generated code.

Optimize for working functionality, product quality, and demonstrable results.

Avoid unnecessary abstraction, over-engineering, speculative features, and fake implementations.

---

# 3. DOCUMENTATION AUTHORITY

The project has exactly eight approved Markdown documents under `documents/`.

```text
documents/
├── official-theme.md
├── idea.md
├── REQUIREMENTS.md
├── ARCHITECTURE.md
├── API-CONTRACT.md
├── DESIGN.md
├── MASTER-PLAN.md
└── PLANNING.md
```

Do not create additional project documents under `documents/` unless the user explicitly approves a change to this documentation policy.

## Authority of each document

### official-theme.md

The authoritative extracted source of the hackathon challenge.

Use it to understand the official problem, constraints, judging criteria, and mandatory deliverables.

### idea.md

The primary product knowledge source and source of truth for what must be built.

It defines:

- Product concept.
- Problem and proposed solution.
- Target users.
- Product modules.
- MVP functionality.
- AI/ML capabilities.
- Model and provider responsibilities.
- External integrations.
- User workflows.
- Scope boundaries.

Do not independently invent or expand the product scope.

### REQUIREMENTS.md

Defines functional and nonfunctional requirements, priorities, and acceptance criteria.

### ARCHITECTURE.md

Defines the approved technical architecture, system boundaries, technologies, and data flow.

### API-CONTRACT.md

Defines the communication contracts between frontend, backend, AI services, and external integrations.

### DESIGN.md

Defines the visual identity, design system, typography, layout, responsive behavior, and interaction direction.

### MASTER-PLAN.md

Defines the high-level development strategy, milestones, integration checkpoints, and overall execution direction.

### PLANNING.md

Defines the detailed implementation roadmap.

It breaks approved product modules into phases and executable tasks, including dependencies, agent ownership, deliverables, and verification.

## Mandatory interpretation

The relationship between these documents is:

- `idea.md` defines WHAT to build.
- `PLANNING.md` defines HOW to divide and implement it.
- `MASTER-PLAN.md` defines the overall execution direction.
- `REQUIREMENTS.md` defines WHAT must be satisfied.
- `ARCHITECTURE.md` defines HOW the system is structured.
- `API-CONTRACT.md` defines HOW system components communicate.
- `DESIGN.md` defines HOW the product looks and behaves.
- `official-theme.md` defines the original challenge.

Do not create competing product definitions, alternative plans, or duplicate technical documentation.

If a genuine inconsistency is discovered, identify it, inform the Project Lead, and update the appropriate authoritative document after the decision is resolved.

---

# 4. EXISTING AGENT INFRASTRUCTURE

The project uses a specialized multi-agent architecture.

The existing agent configuration is located in:

```text
.agents/
```

The available specialists are:

| Agent        | Responsibility                                                                                         |
| ------------ | ------------------------------------------------------------------------------------------------------ |
| Project Lead | Overall execution authority, planning, delegation, prioritization, integration decisions, and delivery |
| Architect    | System architecture, technical decisions, and architectural consistency                                |
| Frontend     | Complete frontend implementation and UI/UX                                                             |
| Backend      | APIs, database, business logic, authentication, and server-side infrastructure                         |
| AI Engineer  | AI/ML, LLMs, RAG, models, tool calling, and agentic workflows                                          |
| Integration  | Cross-system integration and contract consistency                                                      |
| QA/Security  | Independent testing, defect identification, and security verification                                  |
| Deployment   | Vercel, Render, configuration, and production verification                                             |

## Agent collaboration rules

- Project Lead is the single execution authority.
- Specialist agents must respect their assigned responsibilities.
- Independent tasks should be executed in parallel where safe.
- Shared interfaces must be agreed upon before dependent implementation.
- Agents must avoid simultaneous conflicting edits.
- Integration must happen continuously.
- Every completed task must satisfy its acceptance criteria.
- Agents must report blockers rather than silently skipping tasks.

Do not recreate existing agents or duplicate their responsibilities.

Read the relevant agent definition and applicable rules before executing a specialized task.

---

# 5. UI COMPONENT LIBRARY — MANDATORY FRONTEND RESOURCE

The repository contains a curated UI component collection:

```text
ui-library/
```

The central component intelligence catalog is:

```text
ui-library/README.md
```

The Frontend Agent must read this README before selecting reusable components.

The catalog provides:

- Component inventory.
- Component locations.
- Product-domain compatibility.
- Design situation classification.
- Animation and interaction classification.
- Component composition recommendations.
- Dependencies.
- Implementation references.

## Component selection requirements

Select components based on:

1. Actual product domain.
2. Required screen and functionality.
3. Approved design direction.
4. Visual compatibility.
5. Animation requirements.
6. Component complementarity.
7. Existing project dependencies.

Do not select components randomly or merely because they look impressive.

For every selected component:

1. Open its actual component directory.
2. Read its `instructions.md`.
3. Inspect the original component code.
4. Review the original prompt and source information.
5. Check installation commands.
6. Identify required dependencies.
7. Verify compatibility with the existing project.
8. Adapt the component to the approved design system.

Install only the dependencies needed by selected components.

Do not install the entire UI library or every package listed in its catalog.

Preserve the original `ui-library/` contents.

Do not modify original component source files unless explicitly authorized.

The UI library is an implementation resource, not a mandatory collection of components that must all be used.

---

# 6. APPROVED TECHNOLOGY AND INFRASTRUCTURE

Follow the technology decisions in:

```text
documents/ARCHITECTURE.md
documents/idea.md
```

The existing project environment generally supports:

- Next.js.
- React.
- TypeScript.
- Python.
- FastAPI when a separate Python backend is justified.
- Supabase PostgreSQL where approved.
- AI/ML frameworks and model providers required by the product.
- Docker where justified.

Do not assume that every project requires every technology.

Do not introduce a new framework, database, provider, or infrastructure service without a genuine technical reason.

## Deployment platforms

Approved deployment targets:

- Frontend: Vercel.
- Backend: Render, when a separate backend is required.

Existing Vercel CLI and Render CLI connections should be reused.

GitHub is the source of truth.

Do not introduce Railway.

Do not unnecessarily recreate cloud resources, projects, or services.

---

# 7. ENVIRONMENT AND SECRET MANAGEMENT

Never hardcode:

- API keys.
- Passwords.
- Database credentials.
- Access tokens.
- Private keys.
- Authentication secrets.
- Service-role keys.

Use environment variables and approved server-side secret management.

Never expose private backend credentials through `NEXT_PUBLIC_` variables.

Never commit real environment files.

Use `.env.example` with safe placeholder values.

Do not print secrets in terminal output, logs, screenshots, or documentation.

If a required credential is missing:

1. Identify the exact environment variable.
2. Explain which service needs it.
3. Notify the Project Lead.
4. Continue independent tasks where possible.
5. Do not fabricate a successful integration.

Follow the security rules in:

```text
.agents/rules/security.md
```

---

# 8. CODE QUALITY AND IMPLEMENTATION STANDARDS

All agents must produce maintainable, readable, and testable code.

Requirements:

- Follow existing project conventions.
- Use appropriate types.
- Separate responsibilities.
- Validate external input.
- Handle errors explicitly.
- Avoid unnecessary duplication.
- Avoid unused dependencies.
- Avoid dead code.
- Avoid unnecessary abstractions.
- Preserve existing working functionality.
- Keep frontend and backend contracts consistent.

Do not rewrite stable project code without a clear reason.

Do not claim functionality exists merely because its interface has been created.

A feature is implemented only when its actual intended behavior works.

---

# 9. FRONTEND QUALITY STANDARDS

Follow:

```text
documents/DESIGN.md
```

The product must have a coherent visual identity.

Prioritize:

- Typography.
- Clear hierarchy.
- Deliberate whitespace.
- Consistent spacing.
- Responsive layouts.
- Accessible controls.
- Meaningful animations.
- Appropriate information density.
- Consistent component behavior.

Avoid:

- Generic AI-generated dashboards.
- Default purple/blue gradients.
- Excessive glassmorphism.
- Random glowing cards.
- Repetitive card grids.
- Unnecessary animation.
- Fake statistics.
- Placeholder functionality.
- Dead buttons.

Every required page, navigation item, form, interaction, and workflow must be implemented according to the approved product.

Do not deliver a landing-page-only prototype when the approved MVP requires a complete application.

---

# 10. BACKEND AND DATA STANDARDS

Backend functionality must follow:

```text
documents/ARCHITECTURE.md
documents/API-CONTRACT.md
documents/idea.md
```

Requirements:

- Implement the approved API contracts.
- Validate incoming requests.
- Enforce authentication and authorization where required.
- Use persistent storage where required.
- Handle database errors.
- Apply appropriate access controls.
- Protect private information.
- Handle external service failures.
- Maintain consistent response formats.

Do not use hardcoded or in-memory data as a substitute for required persistence.

Do not bypass security policies to make a feature work.

---

# 11. AI/ML ENGINEERING STANDARDS

Implement only the AI capabilities defined by the approved product.

Where applicable:

- Use the approved model/provider.
- Keep credentials server-side.
- Validate model inputs and outputs.
- Use structured output where appropriate.
- Handle rate limits and timeouts.
- Validate tool arguments.
- Protect against prompt injection.
- Validate retrieved content.
- Enforce authorization on AI-related operations.
- Handle provider failures.
- Test actual model behavior.

Never present a hardcoded response as a real AI result.

Never claim an AI workflow is complete without testing the actual integration or an appropriate verified test environment.

---

# 12. API AND INTEGRATION RULES

`documents/API-CONTRACT.md` is the shared interface authority.

Frontend and backend agents must not independently invent incompatible request or response structures.

The Integration Agent coordinates:

- Frontend/backend communication.
- Database integration.
- AI service integration.
- Authentication.
- File handling.
- External APIs.
- Notifications.
- Other approved services.

Any necessary API contract change must be coordinated with the Project Lead and documented in the existing API contract.

Do not create a separate competing contract document.

---

# 13. TESTING AND VERIFICATION

Testing is mandatory throughout development.

Use the existing QA/Security Agent.

Verify:

- Required user journeys.
- Frontend interactions.
- API behavior.
- Database persistence.
- Authentication.
- Authorization.
- AI workflows.
- External integrations.
- Error handling.
- Responsive layouts.
- Browser console.
- Network requests.
- Security boundaries.

Use Chrome DevTools MCP when available.

Do not assume a successful build proves the application works.

Do not claim tests passed unless they were actually executed.

Report:

- Tests executed.
- Results.
- Failures.
- Fixes.
- Remaining issues.

---

# 14. GIT AND COLLABORATION RULES

GitHub is the source of truth.

Use only the existing:

```text
main
```

branch.

The `.agents/` directory MUST be version controlled and pushed to GitHub.

Never add `.agents/` to `.gitignore`.

Before committing:

- Inspect Git status.
- Review changes.
- Avoid committing secrets.
- Preserve teammate work.
- Stage only intended files.
- Run relevant checks.

Use meaningful commit messages.

Push verified changes at sensible checkpoints.

Never force push.

Never rewrite shared history.

Never execute destructive Git commands that discard uncommitted work without explicit approval.

Follow:

```text
.agents/rules/git.md
```

---

# 15. HACKATHON EXECUTION

Follow:

```text
HACKATHON-EXECUTION-PROTOCOL.md
```

The expected execution window is approximately 3.5 hours when applicable.

Use the detailed task breakdown in:

```text
documents/PLANNING.md
```

Prioritize:

- P0: Mandatory MVP.
- P1: Important improvements.
- P2: Optional enhancements.

Work in parallel where safe.

Integrate continuously.

Deploy early.

Test continuously.

Fix failures.

Do not stop after initial implementation or after a successful build.

The goal is a complete, functional, verified, demonstration-ready product.

---

# 16. COMPLETION AND HONEST REPORTING

Never claim a task is complete without satisfying its acceptance criteria.

Never claim:

- A page works without testing it.
- An API works without testing it.
- A database operation works without verifying persistence.
- An AI feature works without verifying its behavior.
- A deployment succeeded without checking its actual status.

Report blockers, missing credentials, limitations, and unresolved bugs honestly.

Project Lead is responsible for the final readiness decision.

---

# 17. FINAL GLOBAL DIRECTIVE

Every agent must understand the approved product before implementing its assigned work.

Follow the existing documentation.

Respect the architecture.

Use the UI component intelligence catalog.

Protect existing repository work.

Collaborate through defined responsibilities.

Implement real functionality.

Test actual behavior.

Keep the project synchronized with GitHub.

The objective is to deliver a coherent, reliable, professional hackathon product — not merely a collection of independently generated components.

END OF GLOBAL PROJECT INSTRUCTIONS.
