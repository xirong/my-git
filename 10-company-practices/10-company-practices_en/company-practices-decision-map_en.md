# Engineering Practices Decision Map

English | [中文](../company-practices-decision-map.md)

Use this page to map your team's current pain points to public engineering case studies and actionable guidance.

## Start with Your Problem

| Team Problem | Reference Cases | Corresponding Thematic Articles |
| --- | --- | --- |
| PRs are too large, review costs are high | [Google Code Review](google-code-review_en.md), [Meta Sapling](meta-sapling-stacked-commits_en.md) | [Pull Request Best Practices](../../03-team-collaboration/03-team-collaboration_en/pull-request-best-practices_en.md), [Stacked PR](../../05-ai-native-development/05-ai-native-development_en/stacked-pr-for-ai-generated-changes_en.md) |
| AI generates large diffs, needs splitting | [Google Code Review](google-code-review_en.md), [Meta Sapling](meta-sapling-stacked-commits_en.md) | [AI Commit Splitting](../../05-ai-native-development/05-ai-native-development_en/ai-commit-splitting_en.md), [AI Generated Code Review Example](../../05-ai-native-development/05-ai-native-development_en/ai-change-review-example_en.md) |
| Many PRs, main branch easily broken by combined changes | [Shopify Merge Queue](shopify-merge-queue_en.md), [Merge Queue Practice](merge-queue-practices_en.md) | [Merge Queue](../../04-github-engineering/04-github-engineering_en/merge-queue_en.md) |
| Fixed release windows, release branches, hotfix backporting | [Microsoft Release Flow](microsoft-release-flow_en.md), [Tencent Gitflow](tencent-gitflow_en.md) | [Release Management](../../04-github-engineering/04-github-engineering_en/release-management_en.md), [Gitflow](../../03-team-collaboration/03-team-collaboration_en/gitflow_en.md) |
| High-frequency deployment, need to break risks into daily releases | [Slack Deploys](slack-deploys_en.md), [Netflix Spinnaker](netflix-spinnaker-release_en.md) | [Release Management](../../04-github-engineering/04-github-engineering_en/release-management_en.md) |
| Repository is large, clone, checkout, status are very slow | [Microsoft Scalar](microsoft-scalar-large-repo_en.md), [Uber GitFarm](uber-gitfarm_en.md) | [Large Repository Git Practices](../../07-large-repo/07-large-repo_en/large-repo-git-practices_en.md) |
| Trunk-based development supporting large-scale collaboration | [Google Trunk-Based Development](google-trunk-based-development_en.md), [GitHub Flow Enterprise Practice](github-flow-enterprise_en.md) | [Trunk-Based Development](../../03-team-collaboration/03-team-collaboration_en/trunk-based-development_en.md), [GitHub Flow](../../03-team-collaboration/03-team-collaboration_en/github-flow_en.md) |
| Multiple features in parallel, need to flexibly combine release scopes | [Alibaba AoneFlow](alibaba-aoneflow_en.md) | [Team Git Workflow Guide](../../03-team-collaboration/03-team-collaboration_en/team-git-workflow-guide_en.md), [Gitflow](../../03-team-collaboration/03-team-collaboration_en/gitflow_en.md) |

## Four Core Takeaways

### 1. Google's Small CLs — Applied to Large AI Diffs

Google Code Review enforces small changes, clear intent, and long-term code health.

For AI-assisted development, the principle worth borrowing is how to split changes:

- Separate tests, behavioral changes, refactoring, and documentation into distinct CLs
- Each change should have a goal you can state in one sentence
- Reviewers can assess risk without needing to hold the full context in their heads
- Large features ship as a sequence of small, reviewable steps

Corresponding reading:

- [AI Commit Splitting](../../05-ai-native-development/05-ai-native-development_en/ai-commit-splitting_en.md)
- [AI Generated Code Review Example](../../05-ai-native-development/05-ai-native-development_en/ai-change-review-example_en.md)
- [Pull Request Best Practices](../../03-team-collaboration/03-team-collaboration_en/pull-request-best-practices_en.md)

### 2. Shopify's Merge Queue — Applied to High-Volume PR Teams

When PR volume is high, a single PR passing CI in isolation is not enough. The real risk is the combined state after several PRs land in quick succession.

Shopify's experience shows where a Merge Queue earns its keep:

- Validating the combined state before it touches the main branch
- Reducing the chance of a broken `main`
- Giving developers visibility into failure reasons, queue position, and retry options
- Surfacing flaky tests and slow CI before they become everyone's problem

Corresponding reading:

- [Merge Queue](../../04-github-engineering/04-github-engineering_en/merge-queue_en.md)
- [Enterprise GitHub Workflow Stack](../../04-github-engineering/04-github-engineering_en/enterprise-github-workflow-stack_en.md)

### 3. Microsoft Release Flow — Applied to Teams with Fixed Release Windows

Most business teams cannot ship to production on every merge. For them, release branches remain useful.

Microsoft Release Flow offers a clear model:

- The mainline absorbs daily development
- Release branches own the release window
- Only stability fixes go into a release branch — no new features
- Every fix must be backported to the mainline
- Every release must be traceable to a commit, tag, and release note

Corresponding reading:

- [Release Management](../../04-github-engineering/04-github-engineering_en/release-management_en.md)
- [Team Git Workflow Guide](../../03-team-collaboration/03-team-collaboration_en/team-git-workflow-guide_en.md)

### 4. Meta Sapling — Applied to Stacked PRs

Large features, monorepos, and large AI diffs share a common failure mode: once a single change grows too large, reliable human review breaks down.

Meta Sapling's approach to commit stacks translates into four practical rules:

- Use a commit stack to represent a sequence of small, incremental changes
- Every layer in the stack must be explainable on its own
- Later commits may depend on earlier ones — make those dependencies explicit
- Tooling should show developers the dependency graph and the history at a glance

Corresponding reading:

- [Stacked PR for AI-Generated Changes](../../05-ai-native-development/05-ai-native-development_en/stacked-pr-for-ai-generated-changes_en.md)
- [AI Commit Splitting](../../05-ai-native-development/05-ai-native-development_en/ai-commit-splitting_en.md)
- [Large Repository Git Practices](../../07-large-repo/07-large-repo_en/large-repo-git-practices_en.md)

## Adoption Guidance

Don't copy any single company's workflow end-to-end.

A more reliable approach: answer these five questions first, then pull only the practices that fit.

1. What is the team's sharpest pain point right now — review cost, release rhythm, main branch stability, large-repo performance, or AI-generated change risk?
2. Is CI fast enough to run on every PR?
3. Does the main branch need to be shippable at any time?
4. Are there fixed release windows?
5. Are there clear owners and a tested rollback path?

The clearer your answers, the easier it is to identify which practices from these case studies will actually land.
