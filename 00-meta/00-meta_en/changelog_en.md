# Changelog

English | [中文](../changelog.md)

## v2.2.0: Git learning, repairs, and AI collaboration practices

[中文发布说明](../release-notes-v2.2.0.md) | [English release notes](release-notes-v2.2.0_en.md)

This section defines the v2.2.0 release scope. The documentation was prepared on 2026-09-09; [GitHub Releases](https://github.com/xirong/my-git/releases) records its publication status.

### Merged course and fixes

- [PR #67](https://github.com/xirong/my-git/pull/67) completed ten bilingual conceptual topics, interactives, and isolated labs, together with the [knowledge map](../../01-getting-started/01-getting-started_en/knowledge-map_en.md), [engineering change course](../../05-ai-native-development/05-ai-native-development_en/engineering-change-course_en.md), CI, background tasks, incident recovery, and engineering cases.
- [PR #68](https://github.com/xirong/my-git/pull/68) fixed displayed commands missing recovery-ref creation and storage snapshots, added regression coverage that executes all four displayed paths, and prepared real-reader acceptance tasks.
- PR #68's merged revision `42ae30897b09a1b9f8bb147298b0d75204448ddf` was built to Pages; on 2026-09-08, the hosted interactive script matched the corrected revision. This establishes deployment of that revision only; [GitHub Releases](https://github.com/xirong/my-git/releases) records the v2.2.0 publication status.

### v2.2.0 governance and collaboration material

- The [PR template](../../08-templates/08-templates_en/pull-request-template_en.md) and the repository's actual template record AI participation, task boundaries, human-verified files, and validation gaps. The [commit convention](../../08-templates/08-templates_en/commit-message-convention_en.md) distinguishes attribution from review evidence.
- [Agent governance](../../04-github-engineering/04-github-engineering_en/ai-agent-governance_en.md) adds scenarios for untrusted task content, data supplied to agents, and changes to agent instructions and permission configuration. Security and CODEOWNERS articles link to the relevant guidance.
- [AI Collaboration Metrics](../../05-ai-native-development/05-ai-native-development_en/ai-collaboration-metrics_en.md) defines measurement rules, observation windows, data sources, and a reproducible synthetic example, separating waiting, active review effort, and pre-/post-merge rework. AI code share or PR counts alone do not establish outcomes.
- Bilingual navigation, the [roadmap](roadmap_en.md), and the release notes are aligned; the original historical assessment, `2.x-ai-native-待办.md`, is preserved.

### Acceptance and adoption boundaries

Documentation acceptance includes local links, forbidden text, diff checks, bilingual review, recomputing the measurement example, and checking official sources for new platform descriptions. Repository commands are listed in [AGENTS.md](../../AGENTS.md). These documentation checks do not establish that governance rules were applied to a team's platform configuration or that an agent improved real-team productivity.

A real participant still needs to run the reader session; tasks and recording criteria are in the [roadmap](roadmap_en.md). v2.2.0 introduces no metrics collection service or dashboard and does not change historical release-note files.

## v2.1.0

- Added the AI agent governance guide.
- Added the AGENTS.md template.
- Added this repository's own AGENTS.md and AI-assisted contribution rules.
- Expanded the multi-agent branch strategy and stacked PR guides with executable workflows.
- Added the [v2.1.0 release notes](release-notes-v2.1.0_en.md).

## Early structure record

The following preserves early entries formerly labeled Unreleased, so established structure is not presented as new in this batch. Consult each release's notes for its formal scope.

- Updated the project positioning as a practical Git and GitHub handbook for modern engineering teams and AI-native development workflows.
- Added the first version of the v2.0 content structure.
- Added AI-native development guides.
- Added team collaboration and GitHub engineering governance guides.
- Added troubleshooting playbook.
- Added reusable templates for PRs, code review, commits, releases, hotfixes, branches, and AI code review.
- Added company practice notes and reference indexes.
- Added a legacy content migration checklist.
- Added a v2.0.0 release notes draft.
