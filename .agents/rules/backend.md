---
trigger: glob
globs: backend/**/*.{js,jsx,ts,tsx,py}
---

# Backend Engineering Rules

## 1. Core Principles

The backend must prioritize:

1. Correctness
2. Security
3. Reliability
4. Clear API contracts
5. Simple architecture
6. Fast integration
7. Testability
8. Deployment readiness

Build the smallest reliable backend that satisfies the approved requirements.

Do not over-engineer the backend during the hackathon.

## 2. Source of Truth

Before implementation, inspect:

- `AGENTS.md`
- Applicable `.agents/rules/`
- Relevant `.agents/skills/`
- `HACKATHON-EXECUTION-PROTOCOL.md`
- Finalized documentation inside `documents/`
- `documents/ARCHITECTURE.md`, if present
- `documents/API-CONTRACT.md`, if present
- `documents/idea.md`, if present
- `documents/planning.md`, if present
- Existing backend implementation
- Database schema and migrations
- Existing environment configuration
- Docker and deployment files

Follow the architecture approved by the Project Lead and Architect.

Do not invent endpoints, database tables, or requirements.

## 3. Technology Selection

The approved project direction allows:

- Python
- FastAPI
- Node.js
- Express
- TypeScript where appropriate
- Supabase PostgreSQL
- Other services only when justified by the requirements

Use the selected backend architecture.

Python/FastAPI is appropriate when Python-based AI/ML libraries or processing materially simplify implementation.

Node.js/Express may be appropriate for conventional application APIs and service integrations.

Do not introduce multiple backend frameworks unnecessarily.

Do not create a separate backend service if the approved architecture does not require one.

The Project Lead/Architect owns final architecture decisions.

## 4. Architecture and Code Organization

Keep backend code modular and understandable.

Separate responsibilities where appropriate:

- API routes
- Controllers
- Services
- Business logic
- Database access
- Schemas and validation
- Authentication and authorization
- External integrations
- AI/ML service interfaces
- Configuration
- Logging
- Tests

Use the existing repository structure.

Do not force an elaborate architecture onto a small hackathon application.

Avoid unnecessary microservices, message brokers, queues, distributed systems, and abstractions.

## 5. API Design

Every API endpoint should have:

- Clear purpose
- Correct HTTP method
- Defined request structure
- Defined response structure
- Input validation
- Appropriate status codes
- Error handling
- Authentication requirements where applicable
- Authorization requirements where applicable

Prefer predictable REST-style APIs unless the project requires another approach.

Example:

```text
GET    /api/resource
GET    /api/resource/{id}
POST   /api/resource
PUT    /api/resource/{id}
PATCH  /api/resource/{id}
DELETE /api/resource/{id}
```

The actual route format must follow the selected framework and approved API contract.

## 6. API Contract

Read `documents/API-CONTRACT.md` when it exists.

Do not independently invent or change API contracts.

When implementing an endpoint:

1. Follow the documented route.
2. Follow the documented method.
3. Validate the documented request.
4. Return the documented response.
5. Use the documented error structure.
6. Update the contract only through coordinated approval.
7. Inform Frontend and Integration agents about relevant changes.

If the contract is missing, coordinate with the Project Lead/Architect before defining interfaces that affect other agents.

Do not silently break existing API consumers.

## 7. Input Validation

Treat all external input as untrusted.

Validate:

- Request bodies
- Query parameters
- URL parameters
- Uploaded files
- Authentication data
- External API responses
- AI-generated structured outputs

Reject malformed input early.

Use Pydantic or an appropriate validation library when using FastAPI.

Use appropriate validation tools for Node.js/Express.

Never assume frontend validation is sufficient.

## 8. Error Handling

Every important endpoint must handle expected failures.

Return structured and consistent errors where practical.

Example:

```json
{
  "error": "INVALID_REQUEST",
  "message": "The required field is missing."
}
```

Do not expose to clients:

- Stack traces
- Internal database errors
- File paths
- API keys
- Tokens
- Internal implementation details
- Sensitive infrastructure information

Log useful debugging information server-side without exposing secrets.

Use appropriate HTTP status codes.

Do not hide failures with fake successful responses.

## 9. Authentication

If authentication is required:

- Use the selected authentication provider consistently.
- Validate authentication server-side.
- Never trust user identity supplied only by the client.
- Distinguish authentication from authorization.
- Protect privileged endpoints.
- Handle expired or invalid credentials.

If Supabase Auth is selected, follow the existing Supabase authentication architecture.

Do not create a second authentication system unnecessarily.

## 10. Authorization

Authentication does not automatically grant access to every resource.

For protected resources, verify:

- Who the user is.
- What the user is permitted to do.
- Whether the requested resource belongs to or is accessible by that user.
- Whether the requested operation requires elevated privileges.

Never rely exclusively on frontend authorization checks.

## 11. Database and Supabase

When Supabase is selected, use the approved Supabase architecture for:

- PostgreSQL
- Authentication
- Storage
- Realtime
- Edge Functions where appropriate

Before changing the schema:

1. Inspect the current schema.
2. Understand existing relationships.
3. Check current migrations.
4. Identify affected queries and consumers.
5. Avoid destructive changes.
6. Use migrations where appropriate.
7. Verify the result.

Database operations must be explicit, validated, and safe.

Avoid:

- Unnecessary queries
- N+1 query patterns
- Unbounded data retrieval
- Unnecessary full-table scans
- Destructive queries during debugging

Use indexes when justified by actual access patterns.

Never expose Supabase service-role keys to frontend code.

Never weaken RLS policies just to make an API request work.

## 12. AI / ML Integration

When backend functionality communicates with an AI/ML service:

- Keep provider credentials server-side.
- Validate input before processing.
- Validate model output before using it.
- Handle provider failures.
- Handle timeouts.
- Handle rate limits.
- Handle malformed responses.
- Use structured outputs where appropriate.
- Provide useful fallback behavior where practical.

Do not assume AI providers are always available.

Do not trust generated content as application logic without validation.

For long-running AI or file-processing operations, consider appropriate request limits and resource usage.

Do not introduce queues or workers unless the workload and architecture justify them.

## 13. External API Integration

For third-party services:

- Store credentials in environment variables.
- Follow provider API documentation.
- Handle timeouts.
- Handle rate limits.
- Handle non-success responses.
- Validate external responses.
- Avoid unnecessary repeated requests.
- Use retries only where safe.
- Avoid duplicating operations that must be idempotent.

Do not invent provider capabilities or assume credentials are configured.

## 14. File Processing

If the application processes files:

- Validate file type and size.
- Do not trust client-provided filenames.
- Prevent path traversal.
- Store files safely.
- Avoid executing uploaded content.
- Clean temporary files where appropriate.
- Handle processing failures.
- Set appropriate timeouts.

For image, video, audio, and document processing, consider memory usage and execution time.

Do not load unnecessarily large files into memory.

## 15. Environment Variables

Use environment variables for:

- API keys
- Database URLs
- Authentication secrets
- Provider credentials
- Storage configuration
- Deployment-specific configuration

Maintain a safe `.env.example`.

Never commit real credentials.

Do not print secret values in logs or terminal output.

Ensure the actual application configuration matches the deployment configuration.

## 16. Logging

Logs should help diagnose problems without leaking sensitive information.

Never log:

- Passwords
- Access tokens
- API keys
- Session secrets
- Private credentials
- Sensitive personal data

Use appropriate log levels.

Avoid excessive production logging.

Include enough context to identify the failing operation without disclosing sensitive payloads.

## 17. CORS

Configure CORS deliberately.

- Allow the required frontend origin.
- Use the correct production Vercel origin.
- Support local development origins when needed.
- Do not use unrestricted origins in production without a justified reason.
- Verify credentials and allowed headers when authentication requires them.

Coordinate production origin changes with the Integration and Deployment agents.

## 18. API Testing

Test critical endpoints.

Verify:

- Successful requests
- Invalid requests
- Missing fields
- Unauthorized requests
- Forbidden requests
- Not-found cases
- Server failures
- External provider failures
- Database failures
- Edge cases

Use the existing automated test framework or appropriate API testing tools.

When an endpoint changes, update relevant tests and inform dependent agents.

## 19. Health Checks

Where appropriate, provide a simple health endpoint, such as:

```text
GET /health
```

It should allow developers and deployment infrastructure to determine whether the service is running.

Do not expose credentials, internal database details, or sensitive infrastructure information through health checks.

## 20. Docker

When Docker is part of the approved architecture:

- Keep the Dockerfile minimal.
- Use an appropriate base image.
- Avoid unnecessary packages.
- Do not place secrets inside Dockerfiles.
- Use runtime environment variables.
- Ensure reproducible builds.
- Prefer non-root execution where practical.
- Maintain `.dockerignore`.
- Verify the actual container startup command.

The expected configuration may include:

```text
backend/
  Dockerfile
  .dockerignore
  requirements.txt
  app/
```

or:

```text
backend/
  Dockerfile
  .dockerignore
  package.json
  src/
```

The actual structure must follow the selected stack.

Do not introduce Docker infrastructure if it is not required by the approved architecture.

## 21. Deployment

The approved deployment platform for the backend is Render.

Before declaring the backend deployable:

- Dependencies install successfully.
- Tests pass.
- Build succeeds where applicable.
- Runtime start command is correct.
- Required environment variables are identified.
- Database connectivity is verified.
- External API connectivity is verified where required.
- Health endpoint works where implemented.
- Port configuration is correct.
- CORS is configured.
- Critical endpoints are tested.

Use the existing Render configuration and CLI connection.

The Deployment Agent owns actual cloud deployment.

Do not create or delete cloud resources independently.

Do not introduce Railway.

## 22. Integration

When changing an API:

1. Identify frontend consumers.
2. Identify backend consumers.
3. Identify AI or external-service dependencies.
4. Check the approved API contract.
5. Coordinate changes with the Integration Agent.
6. Update relevant documentation after approval.
7. Update affected clients and tests.
8. Verify the complete user flow.

Do not silently break existing consumers.

## 23. Hackathon Time Constraint

Prioritize:

**P0**

- Required endpoints
- Core business logic
- Database connectivity
- Authentication w
