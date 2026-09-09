# v2.2.0: Git Learning, Command Repairs, and AI Collaboration Practices

English | [中文](../release-notes-v2.2.0.md) | [Changelog](changelog_en.md)

This document defines the authorized v2.2.0 release scope. It was prepared on 2026-09-09; [GitHub Releases](https://github.com/xirong/my-git/releases) records publication status.

## Highlights

- [PR #67](https://github.com/xirong/my-git/pull/67) completed ten paired Git mental-model topics, interactives, and disposable repository labs, and added the knowledge map, engineering change course, CI for AI-generated changes, background agent tasks, agent incident recovery, and engineering cases.
- [PR #68](https://github.com/xirong/my-git/pull/68) repaired displayed commands that omitted recovery-ref creation and storage output snapshots. Its regression executes all four displayed command paths and checks object state and snapshot content independently.
- Updated the [PR template](../../08-templates/08-templates_en/pull-request-template_en.md), the repository's actual template, and the [commit convention](../../08-templates/08-templates_en/commit-message-convention_en.md) to record AI participation, task boundaries, human-verified files, validation gaps, and commit attribution.
- Updated [Agent governance](../../04-github-engineering/04-github-engineering_en/ai-agent-governance_en.md) for untrusted task content, data supplied to agents, and instruction or permission changes that alter agent behavior; the security and CODEOWNERS articles provide linked guidance.
- Added [AI Collaboration Metrics](../../05-ai-native-development/05-ai-native-development_en/ai-collaboration-metrics_en.md), defining measurement rules, observation windows, data sources, and a reproducible synthetic example that separates waiting, active review effort, and pre-/post-merge rework.
- Aligned bilingual navigation, roadmaps, the changelog, and these release notes.

## Why v2.2.0

v2.1.0 established agent governance and collaboration conventions. v2.2.0 connects those conventions to usable learning material, command regressions, fillable collaboration templates, and reproducible measurement examples, helping teams assess course learning, change evidence, and collaboration outcomes separately.

## Validation and evidence boundaries

- Documentation checks cover `python3 scripts/check-docs.py`, `python3 scripts/check-links.py --no-external`, and `git diff --check`.
- PR #67 and PR #68 are merged. On 2026-09-08, the Pages build and hosted interactive script were verified against PR #68's merged revision, `42ae30897b09a1b9f8bb147298b0d75204448ddf`. This fact covers that merged revision only.
- A real-reader session still needs to run; the tasks and recording criteria are in the [roadmap](roadmap_en.md). Automated documentation checks, command regressions, and agent-simulated reading do not establish course learning or improved team efficiency.
- This version introduces no metrics collection service or dashboard. Each team needs separate evidence for governance adoption, effective platform configuration, and real collaboration outcomes.
