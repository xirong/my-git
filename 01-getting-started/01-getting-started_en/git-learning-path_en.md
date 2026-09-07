# Learning Git: from Understanding to Judgment

English | [中文](../git-learning-path.md)

Read [why learn Git in the AI era](why-learn-git_en.md), then follow **understand the design → verify a decision → manage change**. Look up commands as needed. Each stage should help you explain behavior and predict the effect of changing a condition.

This page arranges only the ten Git conceptual topics. When you need to choose between conceptual learning, one engineering change, and team collaboration, use the [knowledge map](knowledge-map_en.md).

## Part one: understand the design

The table below is the unified order for ten topics. Each topic has paired Chinese and English articles, an interactive page, and a runnable temporary-repository lab. Topics 01 through 03 are the existing interactive topics; topics 04 through 10 are the seven added in this delivery. Available material and passing scripts do not establish that a reader has mastered it; that still needs evidence from prediction, reproduction, and transfer.

| Order | Core question | Article, interactive, and lab | Judgment exercise |
| --- | --- | --- | --- |
| 01 Snapshots and state | What do editing, staging, and committing record? | [Article](git-mental-model-01-snapshots_en.md) · [Interactive](../../interactive/git-mental-model/snapshots-and-state.html?lang=en) · [Lab](../../labs/git-mental-model/01-snapshots-and-state/README.md) | After editing again after add, which version is committed? |
| 02 Object graph | What belongs to commits, trees, and blobs? | [Article](git-mental-model-02-object-graph_en.md) · [Interactive](../../interactive/git-mental-model/object-graph.html?lang=en) · [Lab](../../labs/git-mental-model/02-object-graph/README.md) | Why can two paths share a blob? |
| 03 Index | What is the next commit draft? | [Article](git-mental-model-03-index_en.md) · [Interactive](../../interactive/git-mental-model/index-as-draft.html?lang=en) · [Lab](../../labs/git-mental-model/03-index/README.md) | How can one file contribute only some edits? |
| 04 References and HEAD | How do branches, tags, HEAD, and detached HEAD relate? | [Article](git-mental-model-04-refs_en.md) · [Interactive](../../interactive/git-mental-model/refs-and-head.html?lang=en) · [Lab](../../labs/git-mental-model/04-refs/README.md) | Does moving a branch change the old commit? |
| 05 Reachability and recovery | Can an unnamed commit be recovered? | [Article](git-mental-model-05-recovery_en.md) · [Interactive](../../interactive/git-mental-model/reachability-and-recovery.html?lang=en) · [Lab](../../labs/git-mental-model/05-recovery/README.md) | Why is reflog not a permanent backup? |
| 06 Merging and ancestry | How does Git understand divergent histories? | [Article](git-mental-model-06-merge_en.md) · [Interactive](../../interactive/git-mental-model/three-way-merge.html?lang=en) · [Lab](../../labs/git-mental-model/06-merge/README.md) | Does a conflict-free merge imply compatible behavior? |
| 07 Replay and rewriting | Why does rebase produce new commits? | [Article](git-mental-model-07-rebase_en.md) · [Interactive](../../interactive/git-mental-model/rebase-and-replay.html?lang=en) · [Lab](../../labs/git-mental-model/07-rebase/README.md) | Why does rewriting shared history need coordination? |
| 08 Remotes and synchronization | How does origin/main differ from remote main? | [Article](git-mental-model-08-remote_en.md) · [Interactive](../../interactive/git-mental-model/remote-and-fetch.html?lang=en) · [Lab](../../labs/git-mental-model/08-remote/README.md) | Does fetch necessarily change working files? |
| 09 Worktrees and concurrency | Which state is shared and which is isolated? | [Article](git-mental-model-09-worktree_en.md) · [Interactive](../../interactive/git-mental-model/worktree-and-isolation.html?lang=en) · [Lab](../../labs/git-mental-model/09-worktree/README.md) | Why can agents with separate branches still interfere? |
| 10 Storage and maintenance | How are snapshots stored and queried efficiently? | [Article](git-mental-model-10-storage_en.md) · [Interactive](../../interactive/git-mental-model/storage-and-maintenance.html?lang=en) · [Lab](../../labs/git-mental-model/10-storage/README.md) | Do graph edges describe physical disk layout? |

Maintainers can run `bash scripts/run-git-learning-labs.sh` to regress the ten labs, three existing reading experiments, one local agent-change acceptance exercise, and one command-safety regression. It verifies only scripted temporary local scenarios; it does not measure reader learning or establish production state.

Predict, manipulate the diagram, read the chapter, reproduce it in a temporary repository, then change one condition. Recovery precedes history rewriting so dangerous operations arrive with the necessary context.

## Part two: apply the ideas to one real change

Start with the [engineering change course](../../05-ai-native-development/05-ai-native-development_en/engineering-change-course_en.md) and use one small repair to follow the task contract, candidate commit, CI, runtime evidence, and recovery:

1. Define expected behavior and the scope that must remain unchanged.
2. Identify existing edits and arrange branches and working directories.
3. Choose changes with the index and inspect the diff.
4. Record and verify a specific commit and assess test coverage.
5. Make a review decision and identify the actual release revision.
6. Explain the boundary between code recovery and business compensation.

Continue with [Accept an Agent Change](../../05-ai-native-development/05-ai-native-development_en/ai-change-control-loop_en.md), [CI for AI-Generated Changes](../../05-ai-native-development/05-ai-native-development_en/ci-for-ai-generated-changes_en.md), the [review example](../../05-ai-native-development/05-ai-native-development_en/ai-change-review-example_en.md), [commit splitting](../../05-ai-native-development/05-ai-native-development_en/ai-commit-splitting_en.md), and [AI Agent Incident Recovery](../../06-troubleshooting/06-troubleshooting_en/ai-agent-incident-recovery_en.md).

Use this question to check your explanation: when an agent says “finished,” can you identify the commit scope, evidence, and what remains unverified?

## Part three: turn judgment into team mechanisms

Choose for your constraints; a team does not need every workflow at once.

| Constraint | Reading | Decision to make |
| --- | --- | --- |
| Shared collaboration conventions | [Team Workflows](../../03-team-collaboration/03-team-collaboration_en/team-git-workflow-guide_en.md) | Integration frequency, branch lifetime, and ownership |
| Background or parallel agents increase integration pressure | [Background Agent Tasks](../../05-ai-native-development/05-ai-native-development_en/background-agent-workflow_en.md) → [Multi-Agent Strategy](../../05-ai-native-development/05-ai-native-development_en/multi-agent-branch-strategy_en.md) | How each result is reclaimed, and how isolated results are compared, tested, and integrated |
| Changes depend on each other | [Stacked PR](../../05-ai-native-development/05-ai-native-development_en/stacked-pr-for-ai-generated-changes_en.md) | Whether downstream evidence survives an upstream change |
| Acceptance requires enforceable rules | [GitHub Governance](../../04-github-engineering/04-github-engineering_en/github-engineering-governance_en.md) | Which permissions, checks, and approvals actually apply |
| Releases cause external effects | [Release Management](../../04-github-engineering/04-github-engineering_en/release-management_en.md) | How commits, artifacts, environments, and outcomes correspond |

Then read [two AI Agent engineering cases](../../10-company-practices/10-company-practices_en/ai-native-engineering-cases_en.md) and [company case studies](../../10-company-practices/10-company-practices_en/README_en.md) to compare sources, constraints, and tradeoffs. Public reports offer experience; a team still judges fit from its own repository and validation results.

## References to use as needed

- [Basic commands](git-basic-commands_en.md) for operations.
- [Troubleshooting](../../06-troubleshooting/06-troubleshooting_en/git-troubleshooting-playbook_en.md) for state and risk assessment.
- [Templates](../../08-templates/08-templates_en/README_en.md) after understanding their purpose.
- [Content roadmap](../../00-meta/00-meta_en/roadmap_en.md) for missing lessons and acceptance standards.
