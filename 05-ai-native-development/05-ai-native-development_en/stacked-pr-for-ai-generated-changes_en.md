# Stacked PR for AI-Generated Changes

English | [中文](../stacked-pr-for-ai-generated-changes.md)

Original links:

- [Google Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)
- [GitHub Stacked PRs](https://github.github.com/gh-stack/)
- [GitHub Stacked PRs Overview](https://github.github.com/gh-stack/introduction/overview/)
- [Sapling ReviewStack](https://sapling-scm.com/docs/addons/reviewstack/)
- [Graphite: Stacked Diffs](https://graphite.com/guides/stacked-diffs)

AI easily generates a large PR that looks complete but is actually hard to review.

The value of Stacked PRs lies in splitting a large change into a set of PRs with dependencies, allowing each step to be understood, verified, and rolled back.

## 1. What is a Stacked PR

Ordinary PR:

```text
main <- big-pr
```

Stacked PR:

```text
main <- pr-1 <- pr-2 <- pr-3
```

`pr-1` is merged into the main line first, `pr-2` is based on `pr-1`, and `pr-3` is based on `pr-2`.

Each PR solves a smaller problem.

## 2. Why it is Suitable for AI-Generated Code

Common problems with AI-generated code:

- Too many files modified at once.
- Behavioral changes, refactoring, tests, and documentation are mixed together.
- Reviewers need to reconstruct intent.
- It is hard to roll back only the risky parts.

Stacked PRs can split it into:

```text
PR 1: add tests
PR 2: change implementation
PR 3: remove old helper
PR 4: update docs
```

This way, reviewers can gradually understand intent, and CI can verify layer by layer.

## 3. Ways to Split

### Split by Layer

```text
data model -> service -> API -> UI
```

Suitable for features with clear architectural layering.

### Split by Behavior

```text
support feature A -> support feature B -> enable flag
```

Suitable for multiple sub-capabilities.

### Split by Risk

```text
test only -> refactor no behavior change -> behavior change -> cleanup
```

Suitable for AI refactoring or incident fixes.

## 4. Operational Rules

- Each PR must be independently explainable.
- Each PR must clearly state its dependencies.
- Downstream PRs must be rebased promptly after upstream PR changes.
- Do not mix generated files and behavioral changes in one PR.
- Merge order must be clear.
- Rollback prioritized from top of the stack downwards.

## 5. Operating a Stack with Native Git

Create a two-level stack:

```bash
git switch -c pr-1 main
# commit the content of pr-1
git switch -c pr-2 pr-1
# commit the content of pr-2

gh pr create --base main --head pr-1
gh pr create --base pr-1 --head pr-2
```

The downstream PR's base points to the upstream branch, so reviewers only see `pr-2`'s own changes in `pr-2`.

Update downstream after upstream changes:

```bash
git switch pr-2
git rebase pr-1
git push --force-with-lease origin pr-2
```

For deeper stacks, update the whole chain at once from the top (Git 2.38+):

```bash
git switch pr-3
git rebase main --update-refs
git push --force-with-lease origin pr-1 pr-2 pr-3
```

`--update-refs` moves the pointers of the other branches in the stack during the rebase, so you skip the per-level manual rebase.

After `pr-1` merges into the main line, remove the already-merged commits from `pr-2`'s history:

```bash
git switch pr-2
git rebase --onto main pr-1
git push --force-with-lease origin pr-2
```

GitHub automatically retargets the downstream PR's base to `main` after the base branch is deleted, but the rebase is still on you.

Risk note: force push only your own stack branches, always with `--force-with-lease`, and never force push the main branch.

## 6. Stack Management Tools

When the stack grows beyond two or three levels, or several people on the team work with stacks, bring in tooling to replace manual rebasing. Taking the Graphite CLI as an example:

```bash
gt create -am "add tests"    # create a new stack branch on top of the current one
gt modify -a                 # amend the current branch and restack the branches above
gt submit --stack            # push the whole chain and create or update PRs
gt sync                      # pull the main line, clean up merged branches, restack
```

Sapling's ReviewStack offers a similar stack-oriented review view.

Learn the mechanics with native commands first, then decide whether to adjust the team workflow around a tool.

## 7. Relationship with Commit Splitting

Commit splitting is suitable for keeping history clear within a PR.

Stacked PRs are suitable for splitting a large feature into multiple review units.

They can be used in combination:

```text
stacked PR
  -> each PR has small logical commits
```

Meta Sapling's public practice indicates that commit stacks are suitable for expressing a set of continuous small changes. After AI generates a large diff, you can borrow this idea to transform "large chunks of results" into "reviewable sequences of changes." For more case comparisons, see [Enterprise Git Workflow Stack Decision Map](../../10-company-practices/10-company-practices_en/company-practices-decision-map_en.md).

## 8. Suitable Scenarios

Suitable for:

- AI generating a large diff at once.
- Large features landing incrementally.
- Cross-layer changes.
- Behavioral changes following refactoring.
- Changes requiring review from multiple owners.

Not suitable for:

- Very small bugfixes.
- Multiple independent tasks without dependencies.
- Teams that do not yet have stable PR Review habits.

## Extended Reading

- [git rebase documentation](https://git-scm.com/docs/git-rebase)
- [Graphite CLI Command Cheatsheet](https://graphite.dev/docs/cheatsheet)
- [Meta Sapling and Stacked Commits Practice](../../10-company-practices/10-company-practices_en/meta-sapling-stacked-commits_en.md)
- [Google Code Review Practice](../../10-company-practices/10-company-practices_en/google-code-review_en.md)
- [Enterprise Git Workflow Stack Decision Map](../../10-company-practices/10-company-practices_en/company-practices-decision-map_en.md)
