# AI Agent Governance

English | [中文](../ai-agent-governance.md)

When AI agents start creating branches, committing code, and opening PRs, the repository gains a new class of participants. Governance now covers agents as well as humans, and existing branch protection, review rules, and CI policies deserve a fresh look.

This guide answers five questions:

1. What identity do agents use to commit code?
2. How should agent permissions be scoped down?
3. Who approves PRs opened by agents?
4. How do agents trigger CI, and how are secrets isolated?
5. How do you trace a problem back to a specific agent session?

## Three Identity Models for Agents

### 1. Tools running locally under a human account

Claude Code, Codex CLI, and Aider run on a developer's machine, and commits appear under the developer's own identity.

Governance focus:

- Mark tool involvement in commit messages with a `Co-authored-by` trailer.
- Developers take full responsibility for all code pushed under their accounts.
- Write team rules into AGENTS.md so every member's agent follows the same boundaries.

```text
fix(order): handle empty timeout config

Co-authored-by: Claude <noreply@anthropic.com>
```

### 2. Platform-hosted agents

Agents such as GitHub Copilot cloud agent and Codex cloud run in platform sandboxes and commit under separate bot identities.

Taking Copilot cloud agent as an example, GitHub ships these built-in restrictions (see the official documentation at the end):

- Only users with write access can trigger the agent, and comments from users without write access are never passed to it.
- The agent can only push to its own `copilot/` branches and is still subject to branch protections and required checks.
- PRs opened by the agent are drafts. The agent cannot mark them ready for review, approve them, or merge them.
- The person who started the task cannot approve the resulting PR, so the Required approvals control is preserved.
- By default, Actions workflows do not run until a user with write access clicks Approve and run workflows.

Governance focus: confirm these defaults have not been loosened before deciding which repositories to open up to hosted agents.

### 3. Agents inside self-built automation

When teams run agents inside GitHub Actions or internal platforms, the identity is usually a GitHub App or a machine user.

Governance focus:

- Prefer a GitHub App over a personal access token. App permissions can be scoped per repository and per capability.
- One identity per purpose, which keeps auditing and revocation simple.
- Use fine-grained tokens limited to the repositories the task actually needs.

## Permission Design

Core principle: grant agents the smallest permission set that the task requires.

- Restrict write access to a dedicated branch prefix. Use branch name targeting in Rulesets so agents can only push to `ai/**` or `copilot/**`.
- Never grant agents any bypass. Agent identities should not appear in a Ruleset bypass list.
- Do not grant admin rights, and do not let agents change repository settings, webhooks, or Actions configuration.
- Use CODEOWNERS as the backstop for high-risk directories, and keep owners human.

## PR Approval Rules

- PRs opened by agents must be approved by a human. Enable Require approvals.
- Keep the task initiator and the approver separate. Hosted agent platforms usually build this in; self-built agents need a process rule to cover it.
- Enable Require review from Code Owners for high-risk paths.
- Treat AI review output as advisory input only. The approval action must come from a human.

## CI Triggers and Secrets Isolation

Once agent-authored code runs in CI, that code holds execution rights in the CI environment. Three control points:

- Keep the default behavior of human approval before workflows run, especially on public repositories.
- Move deployment secrets into environments with required reviewers, so agent branches cannot reach them.
- Be careful with `pull_request_target`, which runs code from external branches in a context that carries secrets.

Hosted agent environments restrict outbound network access through a firewall by default. Confirm the list of required domains before loosening it.

## Traceability

When something goes wrong, you need to answer: whose agent produced this code, in which session, started by whom.

- Commit authorship must distinguish humans from agents. Hosted agents commit under a bot identity with the initiator as co-author, and the commits are signed.
- Local tools should consistently add a `Co-authored-by` trailer.
- Keep a task or session link in the commit message.
- Retain platform session logs and audit logs for review.

## Minimal Setup

A small team needs only four things to start:

1. Agree on an agent branch prefix and write it into AGENTS.md and the branch naming convention.
2. Enable Require a pull request before merging and Require approvals on the main branch.
3. Agree on commit trailers that mark AI involvement.
4. Move deployment secrets into environments.

Growing teams can then add:

- Rulesets to unify agent branch rules across repositories.
- CODEOWNERS coverage for high-risk directories.
- A GitHub App identity for self-built agents.
- Periodic audits of agent identity permissions and activity.

## Common Mistakes

### 1. Granting agents the same permissions as humans

Agents do not need admin, do not need bypass, and do not need access to every repository. Oversized permissions make audits unable to tell humans and agents apart.

### 2. Sharing one token across all agents

A shared token means no accountability and no selective revocation. One identity per purpose.

### 3. Treating AI review as human approval

AI review can run a first pass, but Required approvals must be satisfied by a human.

### 4. No naming convention for agent branches

Without a unified prefix, auditing, cleanup, and Ruleset targeting all become impossible.

## Extended Reading

- [GitHub Docs: Risks and mitigations for Copilot cloud agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations)
- [Rulesets](rulesets_en.md)
- [Branch Protection](branch-protection_en.md)
- [CODEOWNERS](codeowners_en.md)
- [AI Reviewer and Human Reviewer](../../05-ai-native-development/05-ai-native-development_en/ai-reviewer-and-human-reviewer_en.md)
