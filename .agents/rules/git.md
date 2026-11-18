---
trigger: always_on
---

---

trigger: always_on
description: Repository-wide Git, GitHub, collaboration, change management, commit safety, and multi-agent coordination rules.

---

# Git and Team Collaboration Rules

## 1. Core Principles

GitHub is the shared source of truth for the project.

The repository is shared by multiple agents and potentially multiple human contributors.

Every agent must:

- Inspect the repository before making significant changes.
- Preserve existing work.
- Make focused changes.
- Avoid conflicting edits.
- Keep the application runnable.
- Never commit secrets.
- Verify important changes before committing.
- Coordinate changes affecting other agents.

Git operations must be safe, deliberate, and reversible wherever possible.

## 2. Branch Strategy

This project uses a single-branch strategy.

The only project branch is:

```text
main
```

Rules:

- Do not create feature branches.
- Do not create development branches.
- Do not create temporary branches unnecessarily.
- Do not introduce GitFlow or another branching strategy.
- Perform approved project work on the existing `main` branch.
- Do not switch to an unexpected branch without understanding why it exists.
- Do not rewrite shared branch history.

If a task requires isolation from other ongoing work, coordinate through file ownership and task sequencing rather than creating unnecessary branches.

The Project Lead coordinates changes across agents.

## 3. Before Making Changes

Before significant modifications, inspect:

```bash
git status
git branch --show-current
git log -5 --oneline
```

Understand:

- Current branch
- Modified files
- Untracked files
- Deleted files
- Recent commits
- Existing changes from other agents

Never assume the working tree is clean.

Do not overwrite files merely because their contents differ from an expected version.

## 4. Protect Other Agents' Work

Before editing a file:

1. Inspect its current contents.
2. Check whether another agent owns or is modifying it.
3. Understand existing changes.
4. Avoid overlapping modifications.
5. Coordinate when ownership is unclear.

Ownership should generally follow:

| Agent        | Primary ownership                                  |
| ------------ | -------------------------------------------------- |
| Project Lead | Coordination and approved project planning         |
| Architect    | Architecture and technical decisions               |
| Frontend     | Frontend implementation                            |
| Backend      | Backend implementation                             |
| AI Engineer  | AI/ML implementation                               |
| Integration  | Cross-domain integration                           |
| QA/Security  | Testing and security verification                  |
| Deployment   | Deployment configuration and production operations |

Shared files require coordination.

Examples include:

- `AGENTS.md`
- `.agents/rules/`
- `documents/`
- `documents/API-CONTRACT.md`
- Environment examples
- Root configuration files
- Docker configuration
- Deployment configuration

Do not allow two agents to independently rewrite the same shared document or configuration.

If a conflict occurs, report it to the Project Lead.

## 5. Commits

Create focused commits with meaningful imperative messages.

Examples:

```text
feat: implement user authentication
feat: add document processing API
feat: integrate AI response workflow
fix: resolve frontend API connection
fix: correct database authorization
test: add core user journey tests
refactor: simplify backend service layer
docs: update API contract
chore: configure deployment environment
```

Avoid meaningless messages such as:

```text
update
changes
final
test
asdf
```

Rules:

- Do not mix unrelated changes in one commit.
- Do not commit incomplete unrelated work.
- Do not create empty commits.
- Do not create unnecessary commits for every tiny operation.
- Follow the existing repository commit conventions.

Only commit when appropriate for the assigned task or explicitly requested by the Project Lead/user.

## 6. Before Committing

Run:

```bash
git status
```

Review:

- Modified files
- Untracked files
- Deleted files
- Unexpected changes
- Generated files
- Environment files
- Sensitive information

Review the intended changes before staging.

Prefer explicitly staging relevant files:

```bash
git add path/to/file
```

Avoid blindly staging the entire repository when unrelated work may be present.

Do not commit:

- `.env`
- `.env.local`
- Real API keys
- Passwords
- Private keys
- Access tokens
- Database credentials
- Service-role keys
- Generated secrets
- Large unnecessary datasets
- Machine-specific configuration

Verify `.gitignore` covers sensitive and generated files.

## 7. Before Pushing

Before pushing to GitHub:

- Confirm the current branch is `main`.
- Confirm the intended files are staged.
- Review the commit.
- Check that no secrets are included.
- Run relevant tests or build checks where practical.
- Ensure no unrelated work is included.
- Check whether the local branch is behind the remote branch.

Use the existing GitHub connection.

Do not unnecessarily reconfigure GitHub authentication or recreate repository connections.

GitHub is the shared source of truth, so avoid pushing changes that may overwrite another contributor's work.

## 8. Forbidden Destructive Operations

Never execute these commands:

```bash
git reset --hard
git clean -fd
git clean -fdx
git push --force
git push --force-with-lease
git branch -D
```

Do not rewrite shared branch history.

Do not use commands that discard uncommitted changes without explicit human approval.

Human approval is required before any destructive Git operation.

## 9. Pull and Synchronization

Before synchronizing with GitHub:

- Inspect local changes.
- Check the current branch.
- Understand whether remote commits exist.
- Avoid overwriting local uncommitted work.
- Resolve divergence carefully.

If the local repository is behind:

1. Inspect the remote changes.
2. Identify files affected.
3. Preserve local work.
4. Synchronize using a safe approach.
5. Resolve conflicts carefully.
6. Run relevant tests.

Do not blindly pull or overwrite changes while multiple agents are working.

## 10. Conflict Handling

If a merge or synchronization conflict occurs:

1. Stop editing the affected files.
2. Inspect both versions.
3. Understand what each contributor changed.
4. Identify the intended final behavior.
5. Preserve necessary functionality from both sides.
6. Resolve the conflict.
7. Run relevant tests.
8. Inform the Project Lead.

Never blindly choose one side of a conflict.

Never discard another agent's implementation without understanding its purpose.

## 11. Multi-Agent Coordination

All agents share one repository and one `main` branch.

Rules:

- Respect the assigned task and ownership.
- Avoid simultaneous edits to the same files.
- Communicate before modifying shared configuration.
- Integrate changes frequently.
- Verify the application after major integrations.
- Report changed files.
- Report dependencies on other agents.
- Do not overwrite another agent's completed work.

Integration Agent should coordinate cross-domain changes.

Project Lead is responsible for resolving ownership conflicts and deciding task sequencing.

## 12. Documentation and Configuration

Treat finalized project documentation as shared project assets.

Do not casually rewrite:

- `documents/idea.md`
- `documents/planning.md`
- `documents/design.md`
- `documents/API-CONTRACT.md`
- `documents/ARCHITECTURE.md`
- `HACKATHON-EXECUTION-PROTOCOL.md`
- `AGENTS.md`
- `.agents/rules/`

Only modify them when the task requires it or the Project Lead approves the change.

Keep documentation consistent with the actual implementation.

Do not commit credentials in configuration examples.

## 13. Build and Test Before Important Pushes

Before pushing substantial changes, run relevant checks.

Examples:

Frontend:

```bash
npm run build
```

Backend:

Run the project's actual test and startup commands.

Python:

```bash
python -m pytest
```

These commands are examples. Use the scripts and tools defined by the actual repository.

Do not claim tests passed unless they were actually executed.

If a test cannot be executed, report why.

## 14. GitHub Deployment Workflow

GitHub is the source repository for the application.

The deployment targets are:

- Frontend: Vercel
- Backend: Render

Where continuous deployment is configured:

- Verify that the correct GitHub repository is connected.
- Verify that the intended `main` branch is selected.
- Avoid unnecessary deployment configuration changes.
- Check deployment status after relevant pushes.
- Investigate failed builds before claiming success.

Do not create duplicate deployments or cloud resources unnecessarily.

The Deployment Agent owns deployment operations.

## 15. Hackathon Time Management

During the short hackathon window:

1. Keep `main` stable.
2. Make small, focused changes.
3. Integrate frequently.
4. Verify critical flows after integration.
5. Avoid large unreviewed changes near the demo.
6. Avoid unnecessary Git operations.
7. Preserve a known working state.

A working simpler implementation is preferable to an unstable sophisticated implementation.

## 16. Human Approval

Always request human approval before:

- Destructive Git operations
- Discarding uncommitted work
- Rewriting shared history
- Deleting important repository content
- Changing repository ownership or permissions
- Changing GitHub access or security settings
- Force pushing
- Irreversible repository changes

Do not assume that an agent's command execution permission authorizes destructive actions.

## 17. Completion Report

After significant Git-related work, report:

- Current branch
- Files modified
- Files created
- Files deleted
- Commit created, if any
- Push status, if applicable
- Tests or builds executed
- Synchronization issues
- Conflicts resolved
- Remaining risks

Never claim a commit or push succeeded without checking its actual result.
