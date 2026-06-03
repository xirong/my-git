# Recommended Reading

English | [中文](../recommended-reading.md)

This page collects official documentation, classic articles, and well-known materials referenced during subsequent writing.

Principles:

- Prioritize official documentation and primary sources
- Then choose classic materials long-cited by the industry
- Chinese articles can be added as supplements but should not replace official statements
- After new articles are written, attach the reference materials to the end of the text to make it convenient for readers to dig deeper

## Git Basics and Mental Model

| Material | Where it's suitable to add | Description |
| --- | --- | --- |
| [Pro Git](https://git-scm.com/book/en/v2) | `01-getting-started/`, `02-daily-workflow/` | System learning material recommended by the official Git site |
| [Git Official Documentation](https://git-scm.com/docs) | All command-related articles | Command behavior is subject to official documentation |
| [Git Cheat Sheet](https://git-scm.com/cheat-sheet.pdf) | `01-getting-started/git-basic-commands.md` | Use for quick command reference |
| [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) | `02-daily-workflow/commit-message.md` | Common reference for commit message specifications |
| [How to Write a Git Commit Message](https://cbea.ms/git-commit/) | `02-daily-workflow/commit-message.md` | Classic commit message writing article |

## Team Workflow

| Material | Where it's suitable to add | Description |
| --- | --- | --- |
| [Atlassian Git tutorials](https://www.atlassian.com/git) | `03-team-collaboration/` | Covers Centralized, Feature Branch, Gitflow, Forking, Pull Request, and other workflows |
| [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow) | `03-team-collaboration/github-flow.md` | GitHub's official lightweight branch workflow |
| [GitHub Flow Enterprise Practice](../../10-company-practices/10-company-practices_en/github-flow-enterprise_en.md) | `03-team-collaboration/github-flow.md`, `04-github-engineering/enterprise-github-workflow-stack.md` | How GitHub Flow coordinates with platform governance capabilities to upgrade to an enterprise collaboration workflow |
| [GitLab Flow](../../03-team-collaboration/03-team-collaboration_en/gitlab-flow_en.md) | `03-team-collaboration/team-git-workflow-guide.md` | Best for teams that require a production / stable branch |
| [Trunk Based Development](https://trunkbaseddevelopment.com) | `03-team-collaboration/trunk-based-development.md` | Classic material for trunk-based development, short branches, and feature flags |
| [Feature Flags](https://trunkbaseddevelopment.com/feature-flags/) | `03-team-collaboration/trunk-based-development.md` | Key practice for isolating unfinished features in trunk-based development |
| [A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/) | `03-team-collaboration/gitflow.md` | The classic original article on Gitflow |
| [Google Engineering Practices: Code Review](https://google.github.io/eng-practices/review/) | `03-team-collaboration/code-review-best-practices.md` | Google's public code review practices |
| [Google Code Review Practice](../../10-company-practices/10-company-practices_en/google-code-review_en.md) | `03-team-collaboration/code-review-best-practices.md` | Review standards, long-term code health, and categorizing comments |
| [Alibaba AoneFlow Branch Management Practice](../../10-company-practices/10-company-practices_en/alibaba-aoneflow_en.md) | `03-team-collaboration/team-git-workflow-guide.md`, `03-team-collaboration/gitflow.md` | Multiple features in parallel, combining release branches according to release scope |
| [Tencent Cloud Community Gitflow Branch Specification Practice](../../10-company-practices/10-company-practices_en/tencent-gitflow_en.md) | `03-team-collaboration/gitflow.md` | Gitflow-style team specification reference |
| [ByteDance Git Workflow and R&D Infrastructure Practice](../../10-company-practices/10-company-practices_en/bytedance-git-workflow_en.md) | `03-team-collaboration/team-git-workflow-guide.md`, `04-github-engineering/` | How large-scale R&D infrastructure supports Git workflows |
| [Google Trunk-Based Development and Version Control Practice](../../10-company-practices/10-company-practices_en/google-trunk-based-development_en.md) | `03-team-collaboration/trunk-based-development.md` | Trunk-based development, large-scale collaboration, small changes, and fast CI |
| [Microsoft Release Flow](../../10-company-practices/10-company-practices_en/microsoft-release-flow_en.md) | `03-team-collaboration/team-git-workflow-guide.md`, `04-github-engineering/release-management.md` | Team practice of trunk-based development combined with release branches |
| [Big Tech Engineering Practice Decision Map](../../10-company-practices/10-company-practices_en/company-practices-decision-map_en.md) | `10-company-practices/` | Linking public cases and theme articles according to team problems |

## GitHub Engineering Governance

| Material | Where it's suitable to add | Description |
| --- | --- | --- |
| [Protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) | `04-github-engineering/branch-protection.md` | Branch protection, required checks, review, Merge Queue |
| [Rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets) | `04-github-engineering/rulesets.md` | Repository and organization-level rule governance |
| [Issue and pull request templates](https://docs.github.com/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates) | `.github/`, `08-templates/` | Standardizing community contribution information |
| [Pull request reviews](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-request-reviews) | `03-team-collaboration/code-review-best-practices.md` | PR review, CODEOWNERS automatically requesting review |
| [Secret scanning](https://docs.github.com/github/administering-a-repository/about-secret-scanning) | `04-github-engineering/security-and-secret-scanning.md` | Credential scanning and leak alerts |
| [Push protection](https://docs.github.com/code-security/secret-scanning/protecting-pushes-with-secret-scanning) | `04-github-engineering/security-and-secret-scanning.md` | Intercepting secrets during the push phase |
| [GitHub Actions Docs](https://docs.github.com/en/actions) | `04-github-engineering/github-actions-ci.md` | GitHub Actions official documentation |
| [Reusable workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows) | `04-github-engineering/reusable-workflows.md` | Reusing CI templates across multiple repositories |
| [Gerrit Access Controls](https://gerrit-review.googlesource.com/Documentation/access-control.html) | `09-resources/gerrit-code-review-governance.md` | Gerrit permissions, labels, and Submit model |
| [Managing releases in a repository](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository) | `04-github-engineering/release-management.md` | GitHub Release official documentation |
| [Semantic Versioning](https://semver.org/) | `04-github-engineering/release-management.md` | Semantic versioning specification |
| [Merge Queue Practice](../../10-company-practices/10-company-practices_en/merge-queue-practices_en.md) | `04-github-engineering/merge-queue.md` | How teams with high PR concurrency protect main branch stability |
| [Shopify Merge Queue Practice](../../10-company-practices/10-company-practices_en/shopify-merge-queue_en.md) | `04-github-engineering/merge-queue.md` | Experience of large-scale teams using merge queues to protect the main branch |
| [Enterprise GitHub Collaboration Configuration Stack](../../04-github-engineering/04-github-engineering_en/enterprise-github-workflow-stack_en.md) | `04-github-engineering/` | Combination plan of GitHub Flow, CODEOWNERS, Rulesets, Actions, security scanning, and Merge Queue |
| [GitOps and Config as Code](../../04-github-engineering/04-github-engineering_en/gitops-and-config-as-code_en.md) | `04-github-engineering/github-engineering-governance.md` | How configuration, infrastructure, and release strategies enter the PR, review, and CI pipeline |
| [Slack Deploys Practice](../../10-company-practices/10-company-practices_en/slack-deploys_en.md) | `04-github-engineering/release-management.md` | How high-frequency deployment teams reduce daily release risks |

## Engineering Empirical Research

| Material | Where it's suitable to add | Description |
| --- | --- | --- |
| [Do Small Code Changes Merge Faster?](https://arxiv.org/abs/2203.05045) | `03-team-collaboration/pull-request-best-practices.md` | Empirical research on the relationship between small changes and merge time |
| [The Impact of a Continuous Integration Service on the Delivery Time of Merged Pull Requests](https://arxiv.org/abs/2305.16365) | `04-github-engineering/github-actions-ci.md` | Research on CI's impact on merge decisions, delivery times, and developer confidence |
| [Git Workflow Empirical Research Notes](empirical-git-workflow-research_en.md) | `03-team-collaboration/`, `04-github-engineering/` | Turning research conclusions into writing boundaries |

## AI Programming and Code Review

| Material | Where it's suitable to add | Description |
| --- | --- | --- |
| [Responsible use of GitHub Copilot code review](https://docs.github.com/en/copilot/responsible-use/code-review) | `05-ai-native-development/ai-generated-code-review.md` | GitHub's official statement on the boundaries of AI Review capabilities |
| [Review AI-generated code](https://docs.github.com/en/enterprise-cloud@latest/copilot/tutorials/review-ai-generated-code) | `05-ai-native-development/ai-generated-code-review.md` | Official tutorial for the review process of AI-generated code |
| [OpenAI Codex](https://openai.com/codex/) | `05-ai-native-development/codex-claude-code-git-practices.md` | Codex official product page, including multi-agent workflows and worktrees instructions |
| [OpenAI Codex Web](https://developers.openai.com/codex/cloud) | `05-ai-native-development/ai-coding-tools-git-integration.md` | Codex Web, GitHub integration, and remote task entries |
| [OpenAI Codex Sandboxing](https://developers.openai.com/codex/concepts/sandboxing) | `05-ai-native-development/ai-coding-tools-git-integration.md` | Codex sandbox and permission model |
| [Claude Code Worktrees](https://code.claude.com/docs/en/worktrees) | `05-ai-native-development/codex-claude-code-git-practices.md` | Claude Code's official instructions for parallel worktree sessions |
| [Claude Code Common Workflows](https://code.claude.com/docs/en/common-workflows) | `05-ai-native-development/codex-claude-code-git-practices.md` | Claude Code's official common workflows |
| [GitHub Copilot Cloud Agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent) | `05-ai-native-development/ai-coding-tools-git-integration.md` | Asynchronous Agent workflow from Issue to PR |
| [Aider Git Integration](https://aider.chat/docs/git.html) | `05-ai-native-development/ai-coding-tools-git-integration.md` | git-first local AI pair programming practice |
| [Cursor 2.0 and Composer](https://cursor.com/blog/2-0) | `05-ai-native-development/ai-coding-tools-git-integration.md` | Multi-Agent, Composer, and aggregated diff entry |
| [AI Change Review Action Example](../../05-ai-native-development/05-ai-native-development_en/ai-change-review-example_en.md) | `05-ai-native-development/ai-native-git-workflow.md`, `05-ai-native-development/ai-generated-code-review.md` | Complete example of AI diff review, cleaning, splitting commits, and writing PRs |
| [Stacked PR for AI-Generated Changes](../../05-ai-native-development/05-ai-native-development_en/stacked-pr-for-ai-generated-changes_en.md) | `05-ai-native-development/ai-native-git-workflow.md`, `05-ai-native-development/ai-commit-splitting.md` | How to split AI's large diffs into reviewable small PRs |

## Open Source Project Governance

| Material | Where it's suitable to add | Description |
| --- | --- | --- |
| [Kubernetes OWNERS Files](https://www.kubernetes.dev/docs/guide/owners/) | `04-github-engineering/codeowners.md`, `03-team-collaboration/code-review-best-practices.md` | OWNERS, reviewer / approver two-stage review |
| [Kubernetes Pull Request Process](https://www.kubernetes.dev/docs/guide/pull-requests/) | `03-team-collaboration/pull-request-best-practices.md` | PR process, automated checks, and maintainer collaboration |
| [Linux Kernel Pull Requests](https://docs.kernel.org/maintainer/pull-requests.html) | `09-resources/open-source-governance-practices.md` | Maintainer tree model and pull request specifications |
| [Go Contribution Guide](https://go.dev/doc/contribute) | `09-resources/open-source-governance-practices.md` | Gerrit, Review permissions, and contribution process |
| [Rust RFCs](https://github.com/rust-lang/rfcs) | `09-resources/open-source-governance-practices.md` | Major change RFC model |

## Troubleshooting and Recovery

| Material | Where it's suitable to add | Description |
| --- | --- | --- |
| [Git Flight Rules](https://github.com/k88hudson/git-flight-rules) | `06-troubleshooting/` | High-frequency Git incident handling checklist |
| [git reflog](https://git-scm.com/docs/git-reflog.html) | `06-troubleshooting/recover-lost-commit.md` | Core command to recover lost commits |
| [git restore](https://git-scm.com/docs/git-restore.html) | `06-troubleshooting/undo-anything.md` | Undo changes in the working tree and staging area |
| [How to undo almost anything with Git](https://github.blog/open-source/git/how-to-undo-almost-anything-with-git/) | `06-troubleshooting/undo-anything.md` | GitHub's classic undo guide |
| [Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) | `06-troubleshooting/remove-secret-from-history.md` | GitHub's official instructions for clearing sensitive data |
| [git filter-repo](https://github.com/newren/git-filter-repo) | `06-troubleshooting/remove-secret-from-history.md` | Common tool for cleaning Git history |

## Large Repositories and Monorepos

| Material | Where it's suitable to add | Description |
| --- | --- | --- |
| [Partial clone](https://git-scm.com/docs/partial-clone.html) | `07-large-repo/partial-clone.md` | Reduce object downloads |
| [Sparse checkout](https://git-scm.com/docs/sparse-checkout) | `07-large-repo/sparse-checkout.md` | Keep only parts of the worktree paths |
| [git worktree](https://git-scm.com/docs/git-worktree) | `02-daily-workflow/worktree.md`, `05-ai-native-development/worktree-for-ai-agents.md` | Multi-branch parallel worktrees |
| [Git LFS](https://git-lfs.com) | `07-large-repo/git-lfs.md` | Git large file management tool |
| [Pro Git: Submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) | `07-large-repo/submodule-vs-subtree.md` | Submodule system explanation |
| [git maintenance](https://git-scm.com/docs/git-maintenance) | `07-large-repo/repo-maintenance.md` | Repository maintenance commands |
| [Microsoft Scalar and Large Repository Git Practice](../../10-company-practices/10-company-practices_en/microsoft-scalar-large-repo_en.md) | `07-large-repo/large-repo-git-practices.md` | Combination practice of partial clone, sparse checkout, and maintenance |
| [Meta Sapling and Stacked Commits Practice](../../10-company-practices/10-company-practices_en/meta-sapling-stacked-commits_en.md) | `03-team-collaboration/pull-request-best-practices.md`, `07-large-repo/` | Stacked commits and massive repository development experience |
| [Uber GitFarm and Git as a Service Practice](../../10-company-practices/10-company-practices_en/uber-gitfarm_en.md) | `07-large-repo/large-repo-git-practices.md` | Git as a large-scale monorepo infrastructure service |
| [Git Version Upgrade Notes](git-version-upgrade-notes_en.md) | `07-large-repo/large-repo-git-practices.md`, `09-resources/` | Capabilities worth engineering teams' attention in Git 2.45 to 2.54 |
