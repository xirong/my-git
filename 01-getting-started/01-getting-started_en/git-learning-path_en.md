# Git Learning Path

English | [中文](../git-learning-path.md)

Git is not suitable for learning by memorizing commands.

A more effective way is to build capabilities based on real work scenarios.

## Phase 1: Establishing a Mental Model

First, understand the four areas:

```text
working tree -> index -> local repository -> remote repository
```

Recommended reading:

1. [Git Mental Model](git-mental-model_en.md)
2. [Snapshots and State: HEAD, Index, and Working Tree](git-mental-model-01-snapshots_en.md)
3. [Git Basic Commands](git-basic-commands_en.md)
4. [Why Use Git](why-git_en.md)

Mastery Goals:

- Understand `git status`.
- Know the relationship between `git add` and `git commit`.
- Distinguish different versions in HEAD, the index, and the working tree.
- Know the difference between local commit and remote push.

## Phase 2: Daily Development

Recommended reading:

1. [Everyday Git Commands](../../02-daily-workflow/02-daily-workflow_en/everyday-git-commands_en.md)
2. [Branch and Merge](../../02-daily-workflow/02-daily-workflow_en/branch-and-merge_en.md)
3. [Rebase vs Merge](../../02-daily-workflow/02-daily-workflow_en/rebase-vs-merge_en.md)
4. [Stash](../../02-daily-workflow/02-daily-workflow_en/stash_en.md)

Mastery Goals:

- Create a branch for every task.
- Check diff before committing.
- Know when to use stash.
- Know the risks of local rebase and public history.

## Phase 3: Team Collaboration

Recommended reading:

1. [Team Git Workflow Guide](../../03-team-collaboration/03-team-collaboration_en/team-git-workflow-guide_en.md)
2. [Pull Request Best Practices](../../03-team-collaboration/03-team-collaboration_en/pull-request-best-practices_en.md)
3. [Code Review Best Practices](../../03-team-collaboration/03-team-collaboration_en/code-review-best-practices_en.md)

Mastery Goals:

- Can write reviewable PRs.
- Can split commits and PRs into smaller pieces.
- Understand why different teams choose different workflows.

## Phase 4: Troubleshooting and Recovery

Recommended reading:

1. [Git Troubleshooting Playbook](../../06-troubleshooting/06-troubleshooting_en/git-troubleshooting-playbook_en.md)
2. [Undo Anything](../../06-troubleshooting/06-troubleshooting_en/undo-anything_en.md)
3. [Recover Lost Commit](../../06-troubleshooting/06-troubleshooting_en/recover-lost-commit_en.md)

Mastery Goals:

- Know what reflog can save.
- Prioritize revert for public commits.
- Preserve the current state before executing high-risk commands.

## Phase 5: Git in the AI Programming Era

Recommended reading:

1. [AI Native Git Workflow](../../05-ai-native-development/05-ai-native-development_en/ai-native-git-workflow_en.md)
2. [AI Generated Code Review](../../05-ai-native-development/05-ai-native-development_en/ai-generated-code-review_en.md)
3. [Worktree for AI Agents](../../05-ai-native-development/05-ai-native-development_en/worktree-for-ai-agents_en.md)

Mastery Goals:

- Review the diff first after AI modifications.
- Split large diffs into commits first.
- Use branches and worktrees to isolate multi-agent parallel work.

## Extended Reading

- [Pro Git](https://git-scm.com/book/en/v2)
- [Git Cheat Sheet](https://git-scm.com/cheat-sheet.pdf)
- [Atlassian Git tutorials](https://www.atlassian.com/git)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
