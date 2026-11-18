# HACKATHON EXECUTION PROTOCOL

## 1. PURPOSE

This document defines the operational workflow for executing the hackathon project using the existing multi-agent development team.

The objective is to transform the finalized product idea and implementation plan into a complete, functional, tested, deployed, and demonstration-ready application within a strict time window.

The expected execution window is approximately 3.5 hours (210 minutes), unless the actual hackathon schedule specifies otherwise.

This protocol governs:

- Project execution.
- Agent coordination.
- Task delegation.
- Parallel development.
- Technical decision-making.
- Frontend/backend coordination.
- AI/ML implementation.
- Continuous integration.
- Testing.
- Deployment.
- GitHub synchronization.
- Final demonstration readiness.

The Project Lead is responsible for enforcing this protocol.

---

# 2. EXECUTION AUTHORITY AND TEAM STRUCTURE

The Project Lead is the single execution authority.

All specialist agents operate under the Project Lead's coordination.

## Agent responsibilities

| Agent        | Responsibilities                                                                                                            |
| ------------ | --------------------------------------------------------------------------------------------------------------------------- |
| Project Lead | Overall execution, task planning, delegation, prioritization, conflict resolution, integration oversight and final delivery |
| Architect    | Technical architecture, technical decisions, system boundaries and architectural consistency                                |
| Frontend     | Complete frontend, responsive UI, component integration and user experience                                                 |
| Backend      | Backend, APIs, database, business logic, authentication and server-side services                                            |
| AI Engineer  | Models, LLMs, AI/ML workflows, RAG, vision, tool calling and agentic functionality                                          |
| Integration  | Frontend/backend/AI/database/external service integration                                                                   |
| QA/Security  | Functional testing, browser testing, regression, security and defect reporting                                              |
| Deployment   | Vercel, Render, environment configuration, deployment and production verification                                           |

Use the existing agent definitions under `.agents/`.

Do not create duplicate agents.

Do not assign conflicting responsibilities without explicit coordination.

## Project Lead responsibilities

The Project Lead must:

1. Read all approved project documentation.
2. Understand the complete MVP.
3. Establish the execution task board.
4. Assign tasks to specialist agents.
5. Identify parallelizable work.
6. Establish shared technical contracts.
7. Monitor progress.
8. Resolve blockers.
9. Coordinate integration.
10. Verify completion.
11. Manage deployment readiness.
12. Make the final delivery decision.

The Project Lead must remain actively involved throughout the hackathon.

---

# 3. AUTHORITATIVE PROJECT DOCUMENTS

The project uses exactly eight approved documents under `documents/`.

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

## Document responsibilities

- `official-theme.md`: Original challenge and evaluation requirements.
- `idea.md`: Complete product definition and source of truth.
- `REQUIREMENTS.md`: Functional and nonfunctional acceptance requirements.
- `ARCHITECTURE.md`: Approved technical architecture.
- `API-CONTRACT.md`: Shared frontend/backend/API contracts.
- `DESIGN.md`: Visual identity and UI/UX direction.
- `MASTER-PLAN.md`: High-level execution milestones.
- `PLANNING.md`: Detailed phased tasks and dependencies.

## Execution hierarchy

```text
Official Hackathon Theme
          |
          v
       idea.md
          |
          v
  REQUIREMENTS.md
          |
          v
 ARCHITECTURE.md
          |
          v
 API-CONTRACT.md + DESIGN.md
          |
          v
    MASTER-PLAN.md
          |
          v
     PLANNING.md
          |
          v
    Development
```

`idea.md` defines what must be built.

`PLANNING.md` defines how implementation is divided into executable tasks.

Do not generate alternative planning documents or additional documentation files under `documents/`.

---

# 4. EXECUTION PRINCIPLES

The entire team must follow these principles.

## A. MVP First

Build the smallest complete implementation that satisfies the mandatory hackathon requirements.

Do not sacrifice core functionality for optional enhancements.

## B. Vertical Slices

Prefer implementing complete user-facing workflows over building disconnected frontend and backend pieces.

A vertical slice should include:

- Required interface.
- Backend functionality.
- Database interaction.
- AI functionality where applicable.
- Integration.
- Verification.

## C. Parallelize Independent Work

Run independent tasks simultaneously.

Do not parallelize work with unresolved dependencies or shared-file conflicts.

## D. Continuous Integration

Integrate stable work as soon as it becomes available.

Do not wait until all agents finish.

## E. Continuous Testing

Test during implementation.

Do not leave all testing until the final minutes.

## F. Early Deployment

Deploy a stable foundation early.

Do not postpone all deployment activity until the end.

## G. Preserve Working Functionality

Do not replace a working implementation with an untested alternative near the deadline.

## H. Evidence-Based Completion

A task is complete only after its acceptance criteria have been verified.

Agent reports alone are not sufficient evidence.

---

# 5. PRIORITY SYSTEM

All tasks must be prioritized.

## P0 — Mandatory

P0 tasks are required for a working MVP.

Examples:

- Mandatory theme requirements.
- Core user workflows.
- Required frontend screens.
- Required backend operations.
- Database persistence.
- Essential AI functionality.
- Required external integrations.
- Authentication and authorization where required.
- Working demonstration.
- Production deployment where feasible.

## P1 — Important

P1 tasks improve reliability and product quality.

Examples:

- Additional validation.
- Better error handling.
- Responsive refinements.
- Improved security.
- Additional edge cases.
- Better performance.
- Additional test coverage.

## P2 — Optional

P2 tasks are enhancements beyond the required MVP.

Examples:

- Additional animation effects.
- Decorative improvements.
- Nonessential features.
- Advanced capabilities outside the approved scope.

P0 always takes precedence over P1 and P2.

The Project Lead may downgrade or defer optional tasks when time becomes limited.

Do not downgrade mandatory theme requirements without explicitly reporting the impact.

---

# 6. TASK MANAGEMENT AND DELEGATION

The Project Lead must convert `PLANNING.md` into an actively maintained task board.

Each task must contain:

| Field               | Description                                  |
| ------------------- | -------------------------------------------- |
| Task ID             | Unique identifier from planning              |
| Task                | Implementation work                          |
| Agent               | Responsible specialist                       |
| Priority            | P0/P1/P2                                     |
| Dependencies        | Required preceding work                      |
| Status              | Pending/In Progress/Blocked/Review/Completed |
| Deliverable         | Expected result                              |
| Acceptance criteria | Conditions for completion                    |
| Verification        | How completion will be tested                |

## Delegation rules

- Give agents clear, bounded tasks.
- Include relevant documentation references.
- Identify expected files or interfaces where possible.
- Include dependencies.
- Define completion conditions.
- Avoid vague instructions such as "build the entire backend" without a task breakdown.

## Ownership rules

- Frontend owns frontend implementation.
- Backend owns backend implementation.
- AI Engineer owns AI/ML implementation.
- Architect owns architectural decisions.
- Integration owns cross-system integration.
- QA/Security owns independent verification.
- Deployment owns deployment operations.
- Project Lead coordinates all work.

Shared files require coordination before modification.

---

# 7. TIME-BASED EXECUTION FRAMEWORK

The following schedule is a target framework for a 210-minute hackathon.

It is not a reason to delay work that can begin earlier.

| Time        | Duration | Primary objective                                     |
| ----------- | -------: | ----------------------------------------------------- |
| 00–20 min   |   20 min | Repository validation, foundation and task delegation |
| 20–95 min   |   75 min | Parallel core module development                      |
| 95–140 min  |   45 min | Integration, AI workflows and complete user journeys  |
| 140–175 min |   35 min | QA, bug fixing, security and regression               |
| 175–210 min |   35 min | Final deployment verification and demonstration       |

Deployment and integration must begin earlier whenever a stable implementation is available.

Do not wait until the assigned time window if the required work is ready.

---

# 8. PHASE 0 — INITIAL VALIDATION AND TASK DELEGATION

## Objective

Understand the finalized product and establish a stable development foundation.

## Required actions

Project Lead:

1. Read all eight approved documents.
2. Inspect `AGENTS.md`.
3. Inspect `.agents/` and relevant agent instructions.
4. Read this execution protocol.
5. Inspect the existing repository.
6. Check Git status and current branch.
7. Verify existing frontend/backend configuration.
8. Verify environment templates.
9. Inspect database configuration.
10. Identify required API keys.
11. Create the task board from `PLANNING.md`.
12. Identify parallel P0 tasks.
13. Delegate initial tasks.

Architect:

- Verify architecture against actual repository structure.
- Identify missing technical foundations.
- Resolve critical architecture ambiguity.

Backend:

- Prepare required backend foundation.
- Verify application startup and database connectivity.

Frontend:

- Read `ui-library/README.md`.
- Review `DESIGN.md`.
- Shortlist appropriate components.
- Prepare the frontend foundation.

AI Engineer:

- Identify required models and providers.
- Verify AI integration requirements.
- Prepare the necessary AI service architecture.

Deployment:

- Inspect existing Vercel and Render resources.
- Verify the current GitHub connection.
- Identify deployment prerequisites.

Integration:

- Review API contracts.
- Identify integration dependencies.

QA/Security:

- Review mandatory acceptance criteria.
- Identify critical security and testing requirements.

## Exit criteria

- Task ownership established.
- Critical dependencies identified.
- Initial foundation operational.
- Independent development tasks started.

---

# 9. PHASE 1 — PARALLEL CORE DEVELOPMENT

## Objective

Implement the approved MVP modules.

Use the task breakdown in `PLANNING.md`.

Launch independent tasks in parallel.

## Frontend execution

The Frontend Agent must:

1. Inspect the UI component intelligence catalog.
2. Select appropriate components based on the product domain.
3. Inspect selected component instructions.
4. Verify dependencies.
5. Implement the design system.
6. Build the required pages and navigation.
7. Connect stable backend interfaces.
8. Implement real interactions.
9. Add loading, empty, success and error states.
10. Verify responsive behavior.

Do not implement a landing page while leaving mandatory application screens incomplete.

## Backend execution

The Backend Agent must:

1. Initialize the approved backend.
2. Implement required data models.
3. Apply database migrations.
4. Implement business logic.
5. Implement API contracts.
6. Add validation and error handling.
7. Implement authentication and authorization where required.
8. Verify persistence.
9. Prepare integration-ready endpoints.

## AI Engineer execution

The AI Engineer must:

1. Implement approved AI/ML capabilities.
2. Configure model providers.
3. Implement actual model calls.
4. Implement required retrieval or data-processing workflows.
5. Validate structured outputs.
6. Implement tool execution where applicable.
7. Handle model errors and timeouts.
8. Test actual outputs.
9. Expose functionality through approved backend interfaces.

Do not introduce unnecessary AI features.

## Deployment execution

The Deployment Agent should prepare deployment configuration while core development is in progress.

## Exit criteria

- Critical modules have working implementations.
- Core API contracts are respected.
- Database foundation is operational.
- Frontend and backend are ready for vertical integration.
- Required AI functionality has a working implementation or a clearly reported external blocker.

---

# 10. PHASE 2 — CONTINUOUS INTEGRATION AND COMPLETE WORKFLOWS

## Objective

Turn individual implementations into a coherent working product.

The Integration Agent coordinates this phase continuously.

Integrate:

- Frontend and backend.
- Backend and database.
- Backend and AI services.
- Authentication.
- External APIs.
- File storage.
- Notifications.
- Other approved integrations.

## Integration workflow

For every module:

1. Inspect the frontend implementation.
2. Inspect the corresponding backend implementation.
3. Verify the API contract.
4. Connect the actual request and response flow.
5. Verify database persistence.
6. Verify AI behavior where applicable.
7. Test error handling.
8. Verify the user-facing result.
9. Report and fix failures.
10. Mark the module integration-ready only after verification.

## Vertical-slice priority

Complete the main user journey from beginning to end.

A typical vertical slice may contain:

```text
User Action
    |
    v
Frontend Interface
    |
    v
Backend API
    |
    v
Business Logic
    |
    v
Database / AI Service
    |
    v
Processed Result
    |
    v
Frontend Response
```

Use the actual application workflow.

Do not accept disconnected modules as a complete application.

## Exit criteria

- Mandatory user journeys work end-to-end.
- Frontend/backend integration is verified.
- Required database operations work.
- Required AI workflows work.
- Major integration defects are resolved.

---

# 11. PHASE 3 — QUALITY, TESTING AND SECURITY

## Objective

Verify the application independently and eliminate critical defects.

QA/Security owns independent verification.

## Functional testing

Test:

- Every mandatory page.
- Every important user journey.
- All required buttons.
- Forms and validation.
- Navigation.
- Tables and filtering.
- File operations.
- AI workflows.
- Authentication.
- Authorization.
- Database persistence.
- External integrations.

## API testing

Verify:

- HTTP methods.
- Request schemas.
- Response schemas.
- Status codes.
- Error responses.
- Authentication.
- Authorization.
- Validation.

## Browser testing

Use Chrome DevTools MCP where available.

Inspect:

- Actual rendered pages.
- Browser console.
- Network requests.
- Failed API calls.
- Responsive layouts.
- Interactive behavior.

## AI testing

Where applicable, verify:

- Actual provider calls.
- Valid output.
- Invalid input behavior.
- Model errors.
- Timeouts.
- Structured output validation.
- Retrieval quality.
- Tool execution restrictions.

## Security testing

Verify:

- No exposed secrets.
- Correct authorization.
- Appropriate database policies.
- Input validation.
- Safe file processing.
- Safe AI tool execution.
- No sensitive information leakage.

## Defect severity

| Severity | Meaning                                         | Action              |
| -------- | ----------------------------------------------- | ------------------- |
| Critical | Core application or mandatory workflow unusable | Fix immediately     |
| High     | Major functionality broken or unsafe            | Fix before release  |
| Medium   | Important defect with a workaround              | Fix if time permits |
| Low      | Minor visual or usability issue                 | Address after P0/P1 |

Every reported issue must include:

- Description.
- Affected module.
- Severity.
- Reproduction steps.
- Responsible agent.
- Fix status.
- Retest result.

## Exit criteria

- No known unresolved critical defects.
- Mandatory workflows verified.
- Major security issues addressed.
- Regression tests executed.

---

# 12. PHASE 4 — DEPLOYMENT AND PRODUCTION VERIFICATION

## Objective

Make the application available in a working production environment.

Approved deployment platforms:

- Frontend: Vercel.
- Backend: Render, if the approved architecture uses a separate backend.

Use existing Vercel CLI and Render CLI connections.

Reuse existing deployment resources.

Do not introduce Railway.

Do not create duplicate projects or services.

## Deployment checklist

- [ ] Correct GitHub repository connected.
- [ ] Correct `main` branch selected.
- [ ] Frontend build succeeds.
- [ ] Backend build/startup succeeds where applicable.
- [ ] Required environment variables configured.
- [ ] Database connection works.
- [ ] AI provider configuration works.
- [ ] CORS configuration is correct.
- [ ] Health checks work.
- [ ] Logs contain no critical errors.
- [ ] Production API responds.
- [ ] Production frontend loads.
- [ ] Frontend-to-backend communication works.
- [ ] Main production user journey is verified.

## Docker

Use Docker when required by the approved architecture.

Verify:

- Dockerfile.
- Build context.
- Dependencies.
- Runtime command.
- Ports.
- Environment variables.
- Health checks.
- `compose.yaml` where applicable.
- `render.yaml` where applicable.

## Deployment strategy

Deploy early when a stable vertical slice is available.

Do not postpone all deployment activity until the final phase.

Keep the deployed version synchronized with verified changes.

Do not claim successful deployment without checking the actual production result.

---

# 13. PHASE 5 — FINAL DEMONSTRATION PREPARATION

## Objective

Prepare a reliable demonstration of the actual product.

Verify:

- Production URL.
- Required routes.
- Main user journey.
- Authentication where required.
- Data persistence.
- AI workflows.
- Important integrations.
- Error handling.
- Browser responsiveness.

Create a short demonstration sequence based on the approved idea and official evaluation criteria.

The demonstration should clearly communicate:

1. The problem.
2. The proposed solution.
3. The main user workflow.
4. The core modules.
5. The AI/ML value where applicable.
6. The differentiating features.
7. The practical outcome.

Do not present incomplete or fabricated functionality as operational.

Keep a verified working state available for the final demonstration.

---

# 14. CONTINUOUS GIT AND GITHUB SYNCHRONIZATION

GitHub is the source of truth.

Use only the existing `main` branch.

The `.agents/` directory must remain tracked and pushed.

## Git rules

- Inspect changes before committing.
- Coordinate shared-file modifications.
- Use meaningful commits.
- Push verified changes frequently.
- Preserve teammate work.
- Never commit secrets.
- Never force push.
- Never rewrite shared history.
- Never use destructive Git commands without human approval.

Do not wait until the final minutes to synchronize all development work.

If conflicts occur, inspect and reconcile them safely.

---

# 15. AGENT COMMUNICATION AND HANDOFF FORMAT

Every specialist agent must provide a structured completion or progress report.

Use this format:

```text
TASK ID:
AGENT:
STATUS:

COMPLETED:
- Work actually implemented.

FILES CHANGED:
- Exact files.

DEPENDENCIES:
- Required or completed dependencies.

TESTS:
- Commands and actual results.

INTEGRATION:
- Interfaces or endpoints exposed.
- Integration status.

BLOCKERS:
- Missing credentials, dependencies or issues.

REMAINING WORK:
- Incomplete items.

HANDOFF:
- What the next agent needs to know.
```

The Project Lead must use these reports to coordinate the next tasks.

Do not accept vague reports such as "done" or "working perfectly" without evidence.

---

# 16. TIME MANAGEMENT AND SCOPE CONTROL

The expected hackathon window is approximately 210 minutes.

Prioritize work using P0/P1/P2.

When time is limited:

1. Protect mandatory functionality.
2. Complete the primary user journey.
3. Maintain a working application.
4. Fix critical defects.
5. Complete required integrations.
6. Verify deployment.
7. Defer optional enhancements.

Do not sacrifice core product functionality for unnecessary animations or decorative improvements.

Do not attempt to complete optional features while mandatory user journeys remain broken.

If a required feature is blocked by an unavailable external service, document the blocker and preserve the strongest feasible implementation without misrepresenting it.

---

# 17. FINAL ACCEPTANCE GATE

The Project Lead must compare the actual application against all eight approved documents.

## Product

- [ ] The official problem is addressed.
- [ ] The approved MVP is implemented.
- [ ] Mandatory modules exist.
- [ ] Required user workflows work.

## Frontend

- [ ] Required pages are implemented.
- [ ] Navigation works.
- [ ] Important interactions work.
- [ ] The UI follows `DESIGN.md`.
- [ ] The component catalog was consulted.
- [ ] Selected components were inspected before integration.
- [ ] Responsive behavior is verified.

## Backend

- [ ] Required APIs work.
- [ ] Business logic works.
- [ ] Database persistence is verified.
- [ ] Validation works.
- [ ] Authentication and authorization work where required.

## AI/ML

- [ ] Required models are configured.
- [ ] Actual AI functionality works.
- [ ] Output validation is implemented.
- [ ] Error handling works.
- [ ] Tool permissions are appropriate.

## Integration

- [ ] Frontend/backend communication works.
- [ ] Database integration works.
- [ ] AI integration works.
- [ ] Required external integrations work.

## Quality

- [ ] Critical defects are resolved.
- [ ] Mandatory workflows are tested.
- [ ] Security checks are completed.
- [ ] Browser verification is completed.

## Deployment

- [ ] Production frontend is available.
- [ ] Production backend is available where applicable.
- [ ] Environment configuration is correct.
- [ ] Production smoke tests pass.

## GitHub

- [ ] Only `main` is used.
- [ ] Latest changes are pushed.
- [ ] `.agents/` remains tracked.
- [ ] No secrets are committed.

A failed mandatory check prevents a READY decision.

---

# 18. FINAL DELIVERY REPORT

At the end of execution, provide:

## Product Status

- Project name.
- Product summary.
- Implemented MVP.
- Mandatory requirements completed.
- Remaining incomplete requirements.

## Development Status

- Tasks completed by phase.
- Agent contributions.
- Blocked tasks.
- Important implementation decisions.

## Frontend

- Pages and modules implemented.
- UI components selected.
- Functional interactions.
- Responsive verification.

## Backend

- APIs implemented.
- Database functionality.
- Business logic.
- Authentication and authorization.

## AI/ML

- Models and providers.
- Implemented workflows.
- Actual verification results.
- Known limitations.

## Integration

- Connected services.
- Verified user journeys.
- Remaining issues.

## QA/Security

- Tests executed.
- Critical issues.
- Fixes completed.
- Remaining risks.

## Deployment

- Vercel URL.
- Render URL where applicable.
- Production status.
- Smoke-test results.

## GitHub

- Current branch.
- Latest commit.
- Push verification.
- `.agents/` tracking confirmation.

## Final readiness

Choose one:

**READY:** Mandatory requirements and primary workflows have been implemented and verified.

**PARTIALLY READY:** The core product works but documented issues remain.

**BLOCKED:** A critical dependency prevents a working demonstration.

Never claim READY without evidence.

---

# 19. FINAL OPERATING DIRECTIVE

The Project Lead must maintain active execution throughout the hackathon.

Do not stop after generating the first implementation.

Do not stop after the agents report completion.

Do not stop after a successful build.

Do not stop after the first deployment.

Continue integrating, testing, debugging, fixing, and verifying.

The objective is to deliver a complete, coherent, functional, professional, and demonstration-ready product within the available time.

END OF HACKATHON EXECUTION PROTOCOL.
