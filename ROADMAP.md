# Roadmap

English | [中文路线图](00-meta/roadmap.md)

This roadmap describes how My Git Handbook will continue evolving as a practical Git/GitHub handbook for modern engineering teams and AI-native development workflows.

## v2.0 Direction

The v2.0 line focuses on turning the repository into a maintained handbook with clear learning paths, operational playbooks, reusable templates, bilingual content, and documentation quality checks.

Core themes:

- Git fundamentals and mental models
- Daily developer workflows
- Team collaboration models
- GitHub engineering governance
- AI-native Git workflows
- Troubleshooting and recovery playbooks
- Large repository practices
- Reusable templates
- Company practice case studies

## v2.0.1

The v2.0.1 maintenance release focuses on open source project governance and maintainability.

- [x] Add a root license file
- [x] Add root contribution guidelines
- [x] Add a root roadmap
- [x] Add maintainer information
- [x] Keep documentation checks active
- [ ] Open public roadmap issues for upcoming maintenance work

## v2.1.0

The v2.1.0 release focuses on agent governance and agent-facing conventions, so the handbook covers AI agents as first-class repository participants.

- [x] Add an AI agent governance guide covering bot identity, permissions, PR approval, CI triggers, and secrets isolation
- [x] Add an AGENTS.md template for team repositories
- [x] Add this repository's own AGENTS.md and AI contribution guidelines
- [x] Expand the multi-agent branch strategy guide with executable comparison, integration, and cleanup workflows
- [x] Expand the stacked PR guide with native Git commands and stack tooling

## v2.2.0

The v2.2.0 release scope connects Git learning material, command-path repairs, and AI collaboration practices. Its [bilingual release notes](00-meta/00-meta_en/release-notes-v2.2.0_en.md) were prepared on 2026-09-09; [GitHub Releases](https://github.com/xirong/my-git/releases) records publication status.

- [x] Include the ten-topic bilingual Git mental-model course, interactives, labs, and engineering-change material merged in [PR #67](https://github.com/xirong/my-git/pull/67)
- [x] Include the displayed-command repairs and regression coverage merged in [PR #68](https://github.com/xirong/my-git/pull/68)
- [x] Add AI participation, task-boundary, human-review, validation-gap, and attribution guidance to reusable PR and commit templates
- [x] Add three concrete AI governance scenarios and cross-references from security and CODEOWNERS guidance
- [x] Add the AI collaboration metrics article with measurement definitions and a reproducible synthetic example
- [ ] Run a real-reader session; automated documentation and command checks do not establish reader learning or team efficiency

## Next Maintenance Areas

The current content sequence covers understanding, experiments, engineering-change acceptance, background-agent handoff, and incident recovery. The [detailed bilingual roadmap](00-meta/00-meta_en/roadmap_en.md) records the ten-topic material, its local regression entry points, and the remaining reader-learning, performance, deployment, and production evidence boundaries.

The detailed roadmap records PR #67's course material and PR #68's fixes, including the verified Pages build. It also records the v2.2.0 collaboration templates, three governance scenarios, metrics article, and reader-session plan. See the [v2.2.0 release notes](00-meta/00-meta_en/release-notes-v2.2.0_en.md) and [bilingual Changelog](00-meta/00-meta_en/changelog_en.md) for the scope; real-reader learning needs separate evidence.

### Documentation Quality

- Improve English prose in high-traffic guides
- Keep Chinese and English navigation aligned
- Expand link checking for external links where practical
- Review old resources and mark outdated material clearly

### AI-Native Development

- Refine AI-generated code review guidance
- Add more realistic AI diff review examples
- Improve stacked PR guidance for AI-generated changes
- Collect practices from Codex, Claude Code, Cursor, Aider, and GitHub Copilot workflows

### GitHub Engineering Governance

- Expand Rulesets examples
- Improve branch protection examples
- Add more reusable GitHub Actions patterns
- Add clearer release and rollback playbooks

### Community Contributions

- Label issues for broken links, wording fixes, and new guide requests
- Encourage small pull requests
- Review community examples before adding them as recommended practice
- Keep issue triage and release notes visible

## Maintenance Principles

- Prefer real-world problems over generic tutorials.
- Prefer safe recovery paths over command lists.
- Prefer small, reviewable pull requests.
- Prefer official documentation and primary sources.
- Keep historical resources available, but do not present outdated content as the primary path.
