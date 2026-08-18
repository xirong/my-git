# My Git Handbook

English | [中文](README.md)

A practical Git/GitHub handbook for modern engineering teams and AI-native development workflows.

## Why Maintain This Repository

This repository started as a collection of Git learning materials and has helped many Chinese developers get started with Git.

Today, a link collection is no longer enough. The core challenges of Git have expanded from "how to use commands" to more practical questions:

1.  How individual developers understand Git's mental model.
2.  How to handle conflicts, rollbacks, and accidental commits in daily development.
3.  How teams choose the right branch and PR workflows.
4.  How engineering leads establish collaboration standards using GitHub.
5.  How to review, split, verify, and revert AI-generated code changes in AI-native development workflows.

Therefore, v2.0 upgrades this repository into:

> A practical Git/GitHub handbook for modern engineering teams and AI-native development workflows.

## Who Is This For?

- **Git beginners** looking to build the right mental model.
- **Practicing developers** who frequently need to handle conflicts, rollbacks, and accidental commits.
- **Senior developers** focused on PRs, Review, CI, and release collaboration.
- **Technical leads** who need to design team Git workflows and GitHub governance standards.
- **AI coding users** who need to control the risks of code changes brought by tools like Codex, Claude Code, Cursor, and Cline.

## Directory Navigation

| Directory | Problems Solved |
| --- | --- |
| [01-getting-started](01-getting-started/01-getting-started_en/git-learning-path_en.md) | Git basics, mental models, and the difference between Git and SVN |
| [02-daily-workflow](02-daily-workflow/02-daily-workflow_en/everyday-git-commands_en.md) | Daily commands, branching and merging, rebase, stash, and worktree |
| [03-team-collaboration](03-team-collaboration/03-team-collaboration_en/README_en.md) | Team workflows, PRs, Code Review, and selecting collaboration models |
| [04-github-engineering](04-github-engineering/04-github-engineering_en/README_en.md) | Branch protection, Rulesets, CODEOWNERS, CI, releases, and security |
| [05-ai-native-development](05-ai-native-development/05-ai-native-development_en/README_en.md) | Diff review, commit splitting, worktree, and multi-agent strategies for AI coding |
| [06-troubleshooting](06-troubleshooting/06-troubleshooting_en/README_en.md) | Recovering from Git mishaps, conflict resolution, secret cleaning, and force push recovery |
| [07-large-repo](07-large-repo/07-large-repo_en/README_en.md) | Large repositories, monorepos, partial clone, sparse checkout, and Git LFS |
| [08-templates](08-templates/08-templates_en/README_en.md) | Templates for PRs, Issues, Reviews, Hotfixes, Releases, and AI Reviews |
| [10-company-practices](10-company-practices/10-company-practices_en/README_en.md) | Enterprise engineering practice cases and decision maps |

## Learning Paths

### Beginner Path

1.  [Why Use Git](01-getting-started/01-getting-started_en/why-git_en.md)
2.  [Git Mental Model](01-getting-started/01-getting-started_en/git-mental-model_en.md)
3.  [Snapshots and State: HEAD, Index, and Working Tree](01-getting-started/01-getting-started_en/git-mental-model-01-snapshots_en.md)
4.  [Git Basic Commands](01-getting-started/01-getting-started_en/git-basic-commands_en.md)
5.  [Everyday Git Commands](02-daily-workflow/02-daily-workflow_en/everyday-git-commands_en.md)

### Daily Development Path

1.  [Branch and Merge](02-daily-workflow/02-daily-workflow_en/branch-and-merge_en.md)
2.  [Rebase vs. Merge](02-daily-workflow/02-daily-workflow_en/rebase-vs-merge_en.md)
3.  [Stash](02-daily-workflow/02-daily-workflow_en/stash_en.md)
4.  [Worktree](02-daily-workflow/02-daily-workflow_en/worktree_en.md)

### Team Collaboration Path

1.  [Team Git Workflow Guide](03-team-collaboration/03-team-collaboration_en/team-git-workflow-guide_en.md)
2.  [GitLab Flow](03-team-collaboration/03-team-collaboration_en/gitlab-flow_en.md)
3.  [Pull Request Best Practices](03-team-collaboration/03-team-collaboration_en/pull-request-best-practices_en.md)
4.  [Code Review Best Practices](03-team-collaboration/03-team-collaboration_en/code-review-best-practices_en.md)
5.  [GitHub Flow](03-team-collaboration/03-team-collaboration_en/github-flow_en.md)
6.  [Trunk-Based Development](03-team-collaboration/03-team-collaboration_en/trunk-based-development_en.md)
7.  [Gitflow](03-team-collaboration/03-team-collaboration_en/gitflow_en.md)

### GitHub Engineering Governance Path

1.  [GitHub Engineering Governance Manual](04-github-engineering/04-github-engineering_en/github-engineering-governance_en.md)
2.  [Enterprise GitHub Workflow Stack](04-github-engineering/04-github-engineering_en/enterprise-github-workflow-stack_en.md)
3.  [Branch Protection](04-github-engineering/04-github-engineering_en/branch-protection_en.md)
4.  [Rulesets](04-github-engineering/04-github-engineering_en/rulesets_en.md)
5.  [Merge Queue](04-github-engineering/04-github-engineering_en/merge-queue_en.md)
6.  [GitOps and Config as Code](04-github-engineering/04-github-engineering_en/gitops-and-config-as-code_en.md)
7.  [Release Management](04-github-engineering/04-github-engineering_en/release-management_en.md)
8.  [AI Agent Governance](04-github-engineering/04-github-engineering_en/ai-agent-governance_en.md)

### AI Native Development Path

1.  [AI Native Git Workflow](05-ai-native-development/05-ai-native-development_en/ai-native-git-workflow_en.md)
2.  [AI-Generated Code Review](05-ai-native-development/05-ai-native-development_en/ai-generated-code-review_en.md)
3.  [Codex / Claude Code Git Practices](05-ai-native-development/05-ai-native-development_en/codex-claude-code-git-practices_en.md)
4.  [Git Integration Practices for AI Coding Tools](05-ai-native-development/05-ai-native-development_en/ai-coding-tools-git-integration_en.md)
5.  [Worktree for AI Agents](05-ai-native-development/05-ai-native-development_en/worktree-for-ai-agents_en.md)
6.  [Stacked PR for AI-Generated Changes](05-ai-native-development/05-ai-native-development_en/stacked-pr-for-ai-generated-changes_en.md)
7.  [AI Reviewer and Human Reviewer](05-ai-native-development/05-ai-native-development_en/ai-reviewer-and-human-reviewer_en.md)

### Troubleshooting Path

1.  [Git Troubleshooting Playbook](06-troubleshooting/06-troubleshooting_en/git-troubleshooting-playbook_en.md)
2.  [Undo Anything](06-troubleshooting/06-troubleshooting_en/undo-anything_en.md)
3.  [Recover Lost Commit](06-troubleshooting/06-troubleshooting_en/recover-lost-commit_en.md)
4.  [Remove Secret from History](06-troubleshooting/06-troubleshooting_en/remove-secret-from-history_en.md)

## Find Answers by Problem

| The problem I'm facing | Suggested reading |
| --- | --- |
| Just committed to the wrong branch | [Committed to Wrong Branch](06-troubleshooting/06-troubleshooting_en/committed-to-wrong-branch_en.md) |
| Don't know how to recover after reset, rebase, or force push | [Git Troubleshooting Playbook](06-troubleshooting/06-troubleshooting_en/git-troubleshooting-playbook_en.md) |
| Team doesn't know whether to choose GitHub Flow, Gitflow, or Trunk-Based Development | [Team Git Workflow Guide](03-team-collaboration/03-team-collaboration_en/team-git-workflow-guide_en.md) |
| PR is too large, review is slow | [Pull Request Best Practices](03-team-collaboration/03-team-collaboration_en/pull-request-best-practices_en.md) |
| AI changed too many files at once, don't know how to review | [AI Change Review Examples](05-ai-native-development/05-ai-native-development_en/ai-change-review-example_en.md) |
| Large AI-generated diff needs to be split into commits or PRs | [AI Commit Splitting](05-ai-native-development/05-ai-native-development_en/ai-commit-splitting_en.md), [Stacked PR for AI-Generated Changes](05-ai-native-development/05-ai-native-development_en/stacked-pr-for-ai-generated-changes_en.md) |
| Want to protect the main branch | [Branch Protection](04-github-engineering/04-github-engineering_en/branch-protection_en.md) |
| AI agents are pushing code and opening PRs, and I don't know how to govern them | [AI Agent Governance](04-github-engineering/04-github-engineering_en/ai-agent-governance_en.md) |
| Want an agent collaboration convention for the team repository | [AGENTS.md Template](08-templates/08-templates_en/agents-md-template_en.md) |
| Too many PRs, main branch often broken after merge | [Merge Queue](04-github-engineering/04-github-engineering_en/merge-queue_en.md) |
| Clone, status, or checkout is slow in a large repository | [Large Repository Git Practices](07-large-repo/07-large-repo_en/large-repo-git-practices_en.md) |
| Want to directly copy team templates | [Templates](08-templates/08-templates_en/README_en.md) |

## Phase 1: Must-Read Articles

- [AI Native Git Workflow](05-ai-native-development/05-ai-native-development_en/ai-native-git-workflow_en.md)
- [Codex / Claude Code Git Practices](05-ai-native-development/05-ai-native-development_en/codex-claude-code-git-practices_en.md)
- [Git Integration Practices for AI Coding Tools](05-ai-native-development/05-ai-native-development_en/ai-coding-tools-git-integration_en.md)
- [AI Change Review Examples](05-ai-native-development/05-ai-native-development_en/ai-change-review-example_en.md)
- [Stacked PR for AI-Generated Changes](05-ai-native-development/05-ai-native-development_en/stacked-pr-for-ai-generated-changes_en.md)
- [Git Troubleshooting Playbook](06-troubleshooting/06-troubleshooting_en/git-troubleshooting-playbook_en.md)
- [Team Git Workflow Guide](03-team-collaboration/03-team-collaboration_en/team-git-workflow-guide_en.md)
- [GitHub Engineering Governance Manual](04-github-engineering/04-github-engineering_en/github-engineering-governance_en.md)
- [Enterprise Engineering Practice Case Library](10-company-practices/10-company-practices_en/README_en.md)
- [Decision Map for Enterprise Engineering Practices](10-company-practices/10-company-practices_en/company-practices-decision-map_en.md)
- [AI Code Review Checklist](08-templates/08-templates_en/ai-code-review-checklist_en.md)

## Recommended Resources

New content will prioritize official documentation and industry-standard materials:

- [Pro Git](https://git-scm.com/book/en/v2)
- [Git Official Documentation](https://git-scm.com/docs)
- [GitHub Docs](https://docs.github.com)
- [Atlassian Git tutorials](https://www.atlassian.com/git)
- [Trunk Based Development](https://trunkbaseddevelopment.com)
- [Git Flight Rules](https://github.com/k88hudson/git-flight-rules)

For a more complete index of materials, see [Recommended Reading](09-resources/09-resources_en/recommended-reading_en.md).

## v2.0 Maintenance Plan

See the [roadmap](00-meta/00-meta_en/roadmap_en.md) for detailed plans.

Existing content will be gradually incorporated into new learning paths. See the [legacy content migration](00-meta/00-meta_en/legacy-content-migration_en.md) for the migration list and the [resources index](09-resources/09-resources_en/resources-index_en.md) for the materials index.

## Project Governance

- [License](LICENSE)
- [Contributing](CONTRIBUTING.md)
- [Roadmap](ROADMAP.md)
- [Maintainers](MAINTAINERS.md)
- [Agent Conventions](AGENTS.md)

Original project content is licensed under the MIT License. Third-party materials, archived ebooks, external articles, linked resources, and quoted references remain under their original licenses and copyrights.

## Contributing

We welcome contributions of real-world problems, team practices, incident recovery experiences, AI programming workflows, and reusable templates.

Please follow the [Content Style Guide](00-meta/00-meta_en/content-style-guide_en.md) for new content.
