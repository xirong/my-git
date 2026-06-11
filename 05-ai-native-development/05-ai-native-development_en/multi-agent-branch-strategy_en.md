# Multi-Agent Branch Strategy

English | [中文](../multi-agent-branch-strategy.md)

When developing with multiple agents in parallel, the core is isolating tasks, clarifying ownership, and finally having humans perform integration.

## Branch Naming

```text
ai/task-parser-refactor      # one clear task
ai/experiment-parser-a       # approach A to the same problem
ai/experiment-parser-b       # approach B to the same problem
ai/review-parser-refactor    # cleanup branch prepared for review
```

Before merging experimental branches, reorganize them into normal business branches:

```text
feat/parser-error-handling
fix/parser-empty-input
```

## Recommended Process

1. One branch per agent, paired with one worktree directory per branch.
2. One clear task per branch, with boundaries cut along directories or modules.
3. Independent commits and validation for each branch.
4. Humans compare the results and choose which solution to keep.
5. Organize commits before merging, and rename the experimental branch into a business branch.

## Comparing Experimental Branches

Two agents each produced a solution. First check what each branch changed relative to the main line:

```bash
git log --oneline main..ai/experiment-parser-a
git diff main...ai/experiment-parser-a    # three dots: only the branch's own changes
git diff main...ai/experiment-parser-b
```

Then compare the two solutions directly:

```bash
git diff ai/experiment-parser-a..ai/experiment-parser-b
git range-diff main ai/experiment-parser-a ai/experiment-parser-b
```

`git range-diff` aligns the two branches commit by commit, which works well when the two solutions have similar structure.

Do not decide on diffs alone. Run the same test commands on both branches and record the results in the task notes or PR description as the basis for the decision.

## Integrating the Winning Solution

When solution A wins as a whole, turn it into a business branch:

```bash
git switch -c feat/parser-error-handling ai/experiment-parser-a
git rebase main
```

When you only need part of solution B, pick by commit:

```bash
git cherry-pick <commit-sha>
```

Or pick by file:

```bash
git restore --source ai/experiment-parser-b -- src/parser/recover.ts
git add src/parser/recover.ts
git commit
```

## When Two Agents Touch the Same File

Prevention first: cut task boundaries so agent scopes do not overlap, and let only one task touch files such as route tables, dependency manifests, and shared configuration.

When a collision still happens, handle it in order:

1. Merge one branch first.
2. Rebase the other branch onto the latest main line: `git rebase main`.
3. Conflicts are decided by humans. You can ask the agents to explain the intent of each side, but a human picks the outcome.
4. After resolving conflicts, rerun the branch's validation before sending it to review.

## Cleaning Up Losing Branches

```bash
# Tag first if you want to preserve the state for later reference
git tag archive/ai-experiment-parser-b ai/experiment-parser-b

# Delete the local branch and its worktree
git branch -D ai/experiment-parser-b
git worktree remove ../wt-parser-b

# If it was pushed, delete the remote branch as well
git push origin --delete ai/experiment-parser-b
```

When closing the draft PR of a losing branch, state why it lost, so similar future tasks have a record to consult.

## Avoid

- Multiple agents writing to the same workspace.
- Multiple agents modifying the same set of files simultaneously.
- Letting agents merge public branches themselves.
- Accepting results without looking at the diff.
- Leaving experimental branches uncleaned until the repository fills up with dead `ai/` branches.

## Extended Reading

- [git worktree](https://git-scm.com/docs/git-worktree)
- [git range-diff](https://git-scm.com/docs/git-range-diff)
- [Worktree for AI Agents](worktree-for-ai-agents_en.md)
- [AI Native Git Workflow](ai-native-git-workflow_en.md)
- [AI Agent Governance](../../04-github-engineering/04-github-engineering_en/ai-agent-governance_en.md)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
