# AI Commit Splitting

English | [中文](../ai-commit-splitting.md)

When an AI modifies many files at once, split the commits before pushing.

## Dimensions for Judgment

- Behavioral fixes
- Test additions
- Documentation updates
- Refactoring and cleanup
- Dependency changes
- Configuration changes

## Commands

```bash
git diff --stat
git add -p
git commit -m "test(module): cover edge case"
git add -p
git commit -m "fix(module): handle edge case"
```

If already committed as one large commit, but not yet pushed:

```bash
git reset --soft HEAD~1
git add -p
```

Exercise caution when rewriting history after pushing; confirm first if anyone else is continuing development based on that branch.

## Splitting Suggestions

Prioritize splitting into these types:

- Test commits
- Behavioral fixes
- Documentation descriptions
- Local refactoring
- Configuration adjustments
- Dependency changes

Do not put "bug fix + large refactor + formatting + dependency upgrade" in the same commit.

## Borrowing from Stacked Commits

Meta Sapling's public practice uses a stack of commits as an important workflow, suitable for splitting large features into multiple continuous small changes.

After an AI generates a large diff, you can also organize it with this mindset:

```text
commit 1: add failing test
commit 2: change implementation
commit 3: update docs
commit 4: remove obsolete helper
```

Each commit should be independently explainable, and the sequence should be clear.

When a large diff exceeds the review capacity of a single PR, it can be further split into stacked PRs. Commit splitting solves the issue of clear history within a PR, while stacked PRs solve the issues of multi-person review and layered merging.

Both Google's small CLs and Meta Sapling show that making changes smaller first leads to more accurate reviews. When AI modifies code, the core value of splitting is cutting risks back to a judgeable range. For case comparisons, see [Enterprise Git Workflow Stack Decision Map](../../10-company-practices/10-company-practices_en/company-practices-decision-map_en.md).

## Extended Reading

- [git add official documentation](https://git-scm.com/docs/git-add)
- [git reset official documentation](https://git-scm.com/docs/git-reset)
- [AI Native Git Workflow](ai-native-git-workflow_en.md)
- [AI Change Review Practice Example](ai-change-review-example_en.md)
- [Commit Message](../../02-daily-workflow/02-daily-workflow_en/commit-message_en.md)
- [Meta Sapling and Stacked Commits Practice](../../10-company-practices/10-company-practices_en/meta-sapling-stacked-commits_en.md)
- [Stacked PR for AI-Generated Changes](stacked-pr-for-ai-generated-changes_en.md)
- [Enterprise Git Workflow Stack Decision Map](../../10-company-practices/10-company-practices_en/company-practices-decision-map_en.md)
