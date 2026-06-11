# AGENTS.md Template

English | [中文](../agents-md-template.md)

AGENTS.md is a project guide written for AI coding agents. It is an open format read by tools such as Codex, GitHub Copilot cloud agent, Devin, Cursor, Aider, and Gemini CLI. README is for humans; AGENTS.md is for agents: how to set up the environment, what to run after a change, and which areas must never be touched.

Claude Code reads CLAUDE.md, which shares the same content structure. The two files can reference each other so you avoid maintaining two rule sets.

## Where to Place It

- One copy at the repository root.
- In a monorepo, sub-projects can carry their own copy. Agents generally prioritize the file closest to the changed code.

## Template

```markdown
# AGENTS.md

## Project Overview

One sentence on what this repository does, the tech stack, and service boundaries.

## Environment Setup

- Install dependencies: `pnpm install`
- Start local server: `pnpm dev`

## Required Verification After Changes

- Unit tests: `pnpm test`
- Type check: `pnpm typecheck`
- Lint: `pnpm lint`

Run at least the tests for the touched module; run the full suite when shared modules change.

## Code Style

- TypeScript strict mode.
- Match the naming and comment density of the surrounding file.
- Before adding a new dependency, check whether the repository already has one of the same kind.

## Repository Structure

- `src/api/`: external interface layer
- `src/service/`: business logic
- `src/infra/`: data access and external dependencies

## Boundaries

The following operations are forbidden:

- Changing CI configuration under `.github/workflows/`
- Changing historical database migration files
- Deleting or rewriting existing test assertions to make tests pass
- Force pushing to any shared branch
- Writing `.env` contents, keys, or tokens into any file

## Commit and PR Conventions

- Branch naming: `ai/task-<topic>`
- Commit format: `<type>(<scope>): <subject>`
- Commits with AI involvement carry a trailer: `Co-authored-by: <tool> <email>`
- The PR description states: task boundaries, files verified by a human, verification commands and results
```

## Writing Tips

- Write executable commands, keep prose short. An agent can do nothing with "please keep the code clean" but can run `pnpm lint` directly.
- Express constraints as allow and deny lists. The more specific, the more effective.
- Keep verification commands identical to CI. What the agent runs locally is what CI will run.
- Prune regularly. Outdated instructions keep misleading agents, which is worse than having none.
- Keep it within one or two screens. Agents read it on every session, and length dilutes the key constraints.

## Mapping to Tool-Specific Files

| Tool | File Read |
| --- | --- |
| Codex, Devin, Cursor, Aider, Gemini CLI, etc. | `AGENTS.md` |
| Claude Code | `CLAUDE.md`, which can reference AGENTS.md |
| GitHub Copilot | `AGENTS.md`, also supports `.github/copilot-instructions.md` |

For the supported tool list, refer to the official [agents.md](https://agents.md) page.

## Extended Reading

- [agents.md official guide](https://agents.md)
- [Codex / Claude Code Git Practices](../../05-ai-native-development/05-ai-native-development_en/codex-claude-code-git-practices_en.md)
- [AI Agent Governance](../../04-github-engineering/04-github-engineering_en/ai-agent-governance_en.md)
