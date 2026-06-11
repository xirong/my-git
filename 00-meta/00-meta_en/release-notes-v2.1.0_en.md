# v2.1.0: AI Agent Governance and Conventions

English | [中文](../release-notes-v2.1.0.md)

This release covers AI agents as governed, first-class repository participants: how to govern them, and how to write conventions for them.

## Highlights

- Added the [AI Agent Governance guide](https://github.com/xirong/my-git/blob/v2.1.0/04-github-engineering/04-github-engineering_en/ai-agent-governance_en.md), covering three agent identity models, permission scoping, PR approval rules, CI triggers with secrets isolation, and traceability, with hosted agent restrictions grounded in the official GitHub documentation
- Added the [AGENTS.md template](https://github.com/xirong/my-git/blob/v2.1.0/08-templates/08-templates_en/agents-md-template_en.md), copyable into team repositories, with setup commands, required verification, boundary rules, commit conventions, and a mapping table to tool-specific instruction files
- This repository now follows its own recommendations: a root [AGENTS.md](https://github.com/xirong/my-git/blob/v2.1.0/AGENTS.md), AI-assisted contribution rules in the contributing guides, and documentation checks that include AGENTS.md
- Expanded [Multi-Agent Branch Strategy](https://github.com/xirong/my-git/blob/v2.1.0/05-ai-native-development/05-ai-native-development_en/multi-agent-branch-strategy_en.md) with executable workflows: comparing experiment branches, integrating the winning solution, handling same-file collisions, and cleaning up losing branches
- Expanded [Stacked PR for AI-Generated Changes](https://github.com/xirong/my-git/blob/v2.1.0/05-ai-native-development/05-ai-native-development_en/stacked-pr-for-ai-generated-changes_en.md) with native Git stack operations (`--update-refs`, `rebase --onto`, `--force-with-lease`) and Graphite CLI core commands
- All content above is maintained as Chinese and English pairs

## Why This Release

v2.0 set the direction toward AI-native development workflows, but agent governance and collaboration conventions were still missing.

AI agents are already creating branches, opening PRs, and triggering CI. v2.1.0 upgrades them from diff generators to governed participants: maintainers get a governance configuration checklist, teams get a copyable AGENTS.md template, and developers get executable commands for multi-agent work and PR stacks.

## Validation

- `python3 scripts/check-docs.py`
- `python3 scripts/check-links.py --no-external`
- `git diff --check`
