# Index of Tech Giant Engineering Practices

English | [中文](../README.md)

This directory collects Git, branch management, code review, CI, Monorepo, and engineering governance practices from public resources.

It does not aim to merely list materials, but focuses on clearly explaining the engineering judgments in these public cases: what the problem is, what the approach is, which teams it suits, and what to pay attention to when migrating.

## Organized Cases

If you don't know which one to read first, start with the [Tech Giant Engineering Practices Decision Map](company-practices-decision-map_en.md). It connects cases and thematic articles based on team problems.

| Case | Suitable Reading Scenario |
| --- | --- |
| [Tech Giant Engineering Practices Decision Map](company-practices-decision-map_en.md) | Select cases based on team problems, and understand which thematic articles the cases can be migrated to |
| [Alibaba AoneFlow Branch Management Practice](alibaba-aoneflow_en.md) | Multiple features in parallel, organize release branches by environment, need to flexibly adjust release scope |
| [Tencent Gitflow Branch Convention Practice](tencent-gitflow_en.md) | Client, SDK, enterprise delivery products, need stable release / hotfix processes |
| [ByteDance Git Workflow and R&D Infrastructure Practice](bytedance-git-workflow_en.md) | Large-scale R&D organizations, need to connect Git processes, permissions, CI, and release platforms |
| [GitHub Flow Enterprise Practice](github-flow-enterprise_en.md) | How GitHub Flow works with branch protection, CODEOWNERS, Rulesets, and Merge Queue to become an enterprise collaboration pipeline |
| [Google Trunk-Based Development and Version Control Practice](google-trunk-based-development_en.md) | Want to understand why trunk-based development can support large-scale collaboration |
| [Google Code Review Practice](google-code-review_en.md) | Want to establish team review standards, and avoid PRs being slowed down by low-value comments |
| [Microsoft Scalar and Large Repository Git Practice](microsoft-scalar-large-repo_en.md) | Large repository clone, status, checkout, and historical object download are too slow |
| [Meta Sapling and Stacked Commits Practice](meta-sapling-stacked-commits_en.md) | Break down large features into commit stacks, split large AI diffs, development experience in massive repositories |
| [Uber GitFarm and Git as a Service Practice](uber-gitfarm_en.md) | Frequent clone / checkout by Monorepo automation systems becomes an infrastructure bottleneck |
| [Netflix Spinnaker and Release Pipeline Practice](netflix-spinnaker-release_en.md) | Beyond branching models, how to turn the release process into a traceable, approvable, and rollback-capable pipeline |
| [Merge Queue Practice](merge-queue-practices_en.md) | Many PRs, busy main branch, individual PRs pass CI but combined merging carries high risk |
| [Microsoft Release Flow](microsoft-release-flow_en.md) | Trunk-based development combined with release branches, suitable for product teams with fixed release windows |
| [Shopify Merge Queue Practice](shopify-merge-queue_en.md) | How large-scale teams use merge queues to protect main branch stability |
| [Slack Deploys Practice](slack-deploys_en.md) | How high-frequency deployment teams use small batches, automated checks, and quick rollbacks to reduce release risks |
