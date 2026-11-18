---
trigger: always_on
---

---

trigger: always_on
description: Repository-wide security rules covering secrets, authentication, authorization, databases, APIs, AI/LLM systems, file processing, external services, and deployment.

---

# Hackathon Security Rules

## 1. Core Security Principle

Security requirements apply to every agent and every part of the application.

Treat all external input, user-provided content, uploaded files, external API responses, and AI-generated output as untrusted.

Do not weaken security merely to make a feature work.

Security must be practical and appropriate to the project's risk and hackathon constraints.

## 2. Secrets and Credentials

Never expose:

- API keys
- Access tokens
- Passwords
- Private keys
- Database credentials
- Supabase service-role keys
- Authentication secrets
- Provider credentials
- Session secrets
- Private connection strings

Rules:

- Never hardcode real secrets in source code.
- Never commit `.env` or `.env.local` files containing credentials.
- Never print secrets in terminal output.
- Never include secrets in logs, screenshots, responses, or documentation.
- Use environment variables or approved secret-management mechanisms.
- Keep backend-only credentials on the server.
- Never expose private credentials through `NEXT_PUBLIC_` variables.
- Never send secrets to an LLM.
- Never paste credentials into GitHub issues or public documentation.

`.env.example` may contain variable names and safe placeholder values only.

If a secret is accidentally exposed:

1. Stop further exposure.
2. Notify the Project Lead.
3. Recommend revoking or rotating the credential.
4. Do not attempt to hide the incident by deleting only the local evidence.
5. Obtain human approval for credential rotation or infrastructure changes when required.

## 3. Authentication

When authentication is required:

- Use the approved authentication provider.
- Validate credentials server-side.
- Handle expired and invalid sessions.
- Protect private routes and endpoints.
- Do not trust user identity supplied only by the frontend.
- Avoid exposing authentication tokens in URLs or logs.
- Do not create duplicate authentication systems unnecessarily.

If Supabase Auth is used, follow the approved Supabase architecture.

## 4. Authorization

Authentication does not automatically grant permission to access every resource.

Verify:

- User identity
- Resource ownership
- Resource access permissions
- Role and privilege requirements
- Permission to perform the requested operation

Rules:

- Enforce authorization on the server or through correctly configured database policies.
- Never rely only on frontend visibility checks.
- Prevent users from accessing other users' private records.
- Protect administrative and privileged operations.
- Apply least privilege.

## 5. Database Security

Treat all user input as untrusted.

Use:

- Parameterized queries
- Safe database client methods
- Input validation
- Appropriate authorization checks
- Row Level Security where applicable

When using Supabase:

- Never expose service-role keys to the browser.
- Do not disable RLS simply to bypass permission errors.
- Verify policies for sensitive tables.
- Use appropriate client credentials.
- Protect private storage buckets.
- Review access policies before changing them.

Before modifying database schemas:

- Inspect the existing schema.
- Understand relationships.
- Avoid destructive changes.
- Use migrations where appropriate.
- Test affected queries.

Human approval is required before destructive production database operations.

## 6. API Security

Every API must:

- Validate incoming data.
- Reject malformed or unexpected input.
- Authenticate protected operations.
- Authorize access to protected resources.
- Return safe error messages.
- Use appropriate HTTP status codes.
- Avoid leaking internal implementation details.

Never expose:

- Stack traces
- Credentials
- Internal paths
- Database details
- Private user data
- Sensitive infrastructure information

Protect against applicable risks such as:

- SQL injection
- Cross-site scripting (XSS)
- Cross-site request forgery (CSRF)
- Broken access control
- Insecure direct object references
- Excessive data exposure
- Unrestricted resource consumption
- Unsafe deserialization

Apply protections appropriate to the actual framework and architecture.

## 7. Frontend Security

Frontend code is public and must be treated accordingly.

Never place in browser-accessible code:

- Private API keys
- Database passwords
- Supabase service-role keys
- Backend provider credentials
- Signing secrets
- Private tokens

Rules:

- Never rely exclusively on client-side authorization.
- Avoid unsafe HTML rendering.
- Sanitize untrusted content when necessary.
- Do not expose internal server errors.
- Do not store sensitive data insecurely.
- Validate data on the backend even if the frontend already validates it.

## 8. File Upload Security

If file uploads are implemented:

- Validate file type and size.
- Do not trust file extensions alone.
- Do not trust client-provided MIME types alone.
- Prevent path traversal.
- Generate safe storage names where appropriate.
- Store uploaded files safely.
- Do not execute uploaded files.
- Restrict access to private files.
- Avoid exposing internal storage paths.
- Apply appropriate processing limits.

For image, video, audio, and document processing, consider memory usage, processing time, and malicious input.

## 9. AI / LLM Security

AI-generated output must be treated as untrusted.

Rules:

- Never send secrets or private credentials to an LLM.
- Validate structured model output before using it.
- Do not allow model output to directly execute arbitrary system commands.
- Do not allow LLM output to bypass authorization.
- Validate tool arguments before execution.
- Restrict tools to explicitly permitted operations.
- Avoid exposing internal prompts or secrets.
- Treat retrieved documents and user-provided content as untrusted.
- Defend against prompt injection where relevant.
- Do not assume model responses are factually correct.
- Apply output validation before using AI results in application logic.

For RAG systems:

- Treat retrieved content as untrusted input.
- Do not let retrieved instructions override system-level security controls.
- Enforce document-level access permissions.
- Avoid returning unauthorized source documents.
- Validate citations and source references where required.

For agentic systems:

- Use an explicit tool registry.
- Apply least privilege.
- Validate every tool call.
- Require human approval for sensitive or destructive operations.
- Do not permit unrestricted command execution through model-generated instructions.

## 10. External API Security

For third-party services:

- Store credentials securely.
- Keep private credentials server-side.
- Validate external responses.
- Handle timeouts and failures.
- Respect provider rate limits.
- Avoid leaking sensitive request data.
- Use secure HTTPS endpoints.
- Do not trust external API responses without validation.

Do not invent provider capabilities or claim an integration is secure without checking its actual behavior.

## 11. Environment and Configuration Security

Maintain safe configuration practices.

- Keep real credentials outside source control.
- Use `.env.example` for safe documentation.
- Verify production and development configurations.
- Do not expose backend secrets to the frontend.
- Avoid insecure default credentials.
- Avoid unrestricted CORS in production.
- Avoid debug mode in production.
- Disable unnecessary public endpoints.
- Keep sensitive configuration out of client-side bundles.

## 12. Logging and Error Messages

Logs must support debugging without exposing sensitive information.

Never log:

- Passwords
- API keys
- Authentication tokens
- Session secrets
- Private credentials
- Full sensitive user records

Client-facing errors must not expose:

- Stack traces
- Database internals
- Private file paths
- Environment variables
- Provider credentials
- Internal implementation details

Use meaningful error messages without disclosing sensitive context.

## 13. Dependencies and Supply Chain

Before adding dependencies:

- Check whether the feature already exists.
- Prefer maintained packages.
- Avoid unnecessary dependencies.
- Review installation and security warnings.
- Avoid packages with suspicious behavior.
- Do not ignore critical vulnerabilities without review.

Do not introduce dependencies solely for convenience when a safe existing solution is available.

## 14. Docker and Deployment Security

When Docker is used:

- Never place secrets inside Dockerfiles.
- Do not commit secret-bearing environment files.
- Avoid unnecessary packages.
- Prefer non-root execution where practical.
- Use appropriate base images.
- Keep `.dockerignore` updated.
- Avoid exposing unnecessary ports.
- Use runtime configuration for secrets.

For deployment:

- Verify production environment variables.
- Protect private backend endpoints.
- Configure CORS deliberately.
- Do not expose internal debugging endpoints.
- Verify health checks do not leak infrastructure information.
- Never claim security verification without actual testing.

The approved deployment platforms are Vercel for frontend and Render for backend.

## 15. Destructive and Sensitive Operations

Human approval is required before:

- Deleting production data
- Dropping database tables
- Performing destructive migrations
- Revoking or rotating important credentials
- Changing production authentication
- Removing critical infrastructure
- Deleting cloud resources
- Changing paid plans or enabling billing
- Force-pushing Git history
- Deleting major project directories
- Making irreversible production changes

When uncertain whether an operation is destructive, stop and ask.

## 16. Multi-Agent Security Responsibilities

All agents must follow these rules.

**Project Lead**

- Ensure security requirements are included in planning.
- Approve sensitive or destructive changes.

**Architect**

- Include security boundaries in architecture.
- Avoid unnecessary exposure of services and data.

**Frontend**

- Never expose private credentials.
- Implement safe UI data handling.

**Backend**

- Enforce validation, authentication, authorization, and secure data access.

**AI Engineer**

- Protect prompts, credentials, retrieved content, and tool execution.

**Integration**

- Verify secure communication between systems.
- Identify exposed credentials and unsafe interfaces.

**QA/Security**

- Test security-sensitive workflows.
- Report vulnerabilities and severity.

**Deployment**

- Protect production environment configuration.
- Verify deployment security.

## 17. Security Incident Reporting

If a security issue is discovered, report:

- Issue description
- Affected component
- Potential impact
- Severity
- Reproduction steps where safe
- Recommended fix
- Whether credentials or user data may be exposed
- Whether human action is required

Do not silently ignore or conceal security issues.

## 18. Final Security Checklist

Before final submission, verify:

- [ ] No real secrets are committed.
- [ ] No private credentials are exposed in frontend code.
- [ ] Authentication works where required.
- [ ] Authorization is enforced server-side.
- [ ] Database permissions are appropriate.
- [ ] Supabase RLS is not improperly bypassed.
- [ ] API inputs are validated.
- [ ] Client-facing errors do not leak internals.
- [ ] File uploads are validated where implemented.
- [ ] AI outputs and tool calls are validated where implemented.
- [ ] External integrations protect credentials.
- [ ] Production configuration is checked.
- [ ] Critical security issues are reported and addressed.

Security must be verified through actual implementation and testing, not assumed from documentation alone.
