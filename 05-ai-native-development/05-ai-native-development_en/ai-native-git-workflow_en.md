# AI Native Git Workflow

English | [中文](../ai-native-git-workflow.md)

AI makes writing code cheaper. It makes verifying code more expensive.

Git's new role in the AI era is slicing large AI-generated changes back into engineering units that humans can understand, review, and roll back.

For one continuous timeout-fix case that follows a task contract through candidate SHA, integration, artifact, and recovery, start with [One Engineering Change, from Task Contract to Recovery](engineering-change-course_en.md). This article remains the day-to-day reference for branches, worktrees, diffs, and commits.

## 1. New Risks

AI-generated code tends to share a few characteristics:

- Diffs are larger, touching more files.
- Code looks reasonable, but behavioral boundaries may shift quietly.
- Tests often cover only the happy path.
- Abstractions and naming can drift from project conventions.
- Dependencies, configs, and generated files sneak in as side effects.
- With multiple agents running in parallel, branches and workspaces contaminate each other easily.

The goal of a Git workflow in the AI era is to make changes small, clear, and verifiable again — not just fast to commit.

Different AI tools integrate with Git differently, but the objective is the same: keep AI modifications inside reviewable, rollback-ready engineering units. Codex emphasizes remote environments and sandboxes; Claude Code emphasizes worktree isolation; Copilot Cloud Agent follows an Issue-to-PR model; Aider treats local Git commits and reverts as a first-class experience. See [Git Integration Practices for AI Coding Tools](ai-coding-tools-git-integration_en.md) for a detailed comparison.

## 2. Core Principles

### Small Commits

Each commit expresses one complete intent.

If an AI touches 20 files at once, review the diff first, then split it into multiple commits.

### Isolated Branches

One branch per task.

AI exploratory changes should never land directly on `main`, `master`, `develop`, or any long-lived maintenance branch.

### Reviewable Diffs

Before committing, inspect:

```bash
git status
git diff
git diff --stat
```

If you can't explain in a few minutes why this diff exists, don't commit it yet.

### Reproducible Validation

Every AI change must leave behind a way to verify it:

- Unit tests
- Integration tests
- Compilation
- Static analysis
- Local manual regression
- Pre-production verification steps

### Humans Own the Merge Decision

AI can generate code, explain diffs, and run an initial review pass — but the final merge decision belongs to a human.

### Fast Rollback

Every PR must answer:

- How do you roll back if something breaks?
- Is `git revert` enough?
- Does this touch databases, configs, message queues, or external dependencies?
- Does a rollback require data backfill or compensation?

## 3. Recommended Workflow

### Step 1: Confirm the Baseline and Create an Isolated Branch

`<integration-branch>` is the integration branch selected by the team, such as `main`, `master`, or `develop`. Confirm its name from repository rules and the PR target; `main` is not a safe default for every repository.

The following flow requires a workspace with no pending edits. If `git status --porcelain` prints anything, stop, preserve the state, or continue in a separate clean worktree. Do not use switch, pull, reset, restore, or clean in this workspace to remove someone else's edits.

```bash
git status --porcelain
git branch --show-current
git switch <integration-branch>
git pull --rebase origin <integration-branch>
git switch -c feat/ai-assisted-short-task
```

### Step 2: Use Worktrees for Complex Tasks

Use worktrees when running multiple AI tools on different tasks in parallel:

```bash
git worktree add ../my-project-task-a -b feat/task-a
git worktree add ../my-project-task-b -b feat/task-b
```

See official documentation: [git worktree](https://git-scm.com/docs/git-worktree).

### Step 3: Give AI a Scoped Task

Keep prompts specific and bounded:

```text
Modify only the order validation logic, do not adjust interface signatures, and do not change irrelevant formatting.
Upon completion, list changed files, behavioral changes, validation methods, and potential risks.
```

### Step 4: Review the Diff Before Committing

```bash
git status
git diff --stat
git diff
```

Look for:

- Unrelated files in the diff.
- Formatting noise.
- Changes to configs, lock files, or generated files.
- Behavioral changes in public APIs.
- Tests changed without implementation changes, or implementation changed without test updates.

### Step 5: Split Commits

Use interactive staging to carve up changes. It belongs in a clean or isolated task worktree; inspect `git diff --cached` first and ensure the Index contains only the current intent:

```bash
git add -p
git commit -m "fix(auth): handle expired token"
```

If the AI already landed everything in one large commit, and that commit has not been pushed or used by collaborators, split it again. First confirm the current branch, last commit, and clean baseline:

```bash
git status --porcelain
git log --oneline --decorate -2
git reset --soft HEAD~1
git reset
git diff
git add -p
git diff --cached
```

`reset --soft` leaves every change from the original commit in the Index. Running `git add -p` immediately afterward has no unstaged hunk to choose, so a normal next commit includes everything. The second argument-free `git reset` returns the Index to the current `HEAD` while leaving the Working Tree intact. Only then can `git add -p` select hunks for the next commit.

If `git status --porcelain` prints anything, do not run either reset. Preserve existing staged, unstaged, or untracked content in a clean task worktree instead. See the runnable [Git command safety regression](../../labs/git-command-safety/README.md) for the counterexample and corrected flow.

When AI generates a large cross-layer feature, consider breaking it into a stack of smaller dependent PRs so that tests, implementation, cleanup, and docs each go through review separately. See [Stacked PR for AI-Generated Changes](stacked-pr-for-ai-generated-changes_en.md) for details.

### Step 6: Run Verification

Run the minimum necessary tests for your project type:

```bash
npm test
mvn test
go test ./...
pytest
```

If there are no tests, document the local verification steps explicitly.

### Step 7: Let AI Run the First Review Pass

Ask AI to check against a fixed list:

```text
Please perform a Review based on the current git diff.
Focus checks on: behavioral boundaries, error handling, compatibility, test validity, security risks, and irrelevant changes.
Do not provide vague summaries; list only specific risks and file locations.
```

### Step 8: Open a PR

The PR description must include at least:

- What changed
- Why
- How tested
- Risk
- Rollback plan

You can directly use the [PR Template](../../08-templates/08-templates_en/pull-request-template_en.md).

### Step 9: Merge Only After CI Passes

CI is the minimum quality bar for AI-generated code — treat it as non-negotiable.

If your team uses GitHub, enforce this with branch protection rules, required status checks, and review requirements. See [GitHub branch protection docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

## 4. Commit Strategy

### Recommended

```text
docs: explain the behavior
test: cover the failing case
fix: change the implementation
refactor: simplify local helper
```

### Avoid

```text
fix all ai changes
update files
misc
wip
```

### The Test for a Good Commit

A commit should independently answer:

- Why was it changed?
- What behavior changed?
- How do you verify it?
- How do you roll back if something breaks?

## 5. Branch Strategy

### Single Task

```text
feat/short-description
fix/bug-description
docs/topic-name
```

### AI Exploration

```text
ai/experiment-short-description
```

### Multi-Agent Parallelism

```text
ai/task-a
ai/task-b
ai/review-task-a
```

Pair multi-agent work with `git worktree` to prevent multiple tools from competing over the same files.

## 6. Human Review Checklist

- [ ] The diff is small enough to review carefully.
- [ ] No unrelated formatting changes or generated files.
- [ ] Behavioral changes are described clearly.
- [ ] Public API, config, and data structure changes are flagged.
- [ ] Tests cover the actual changes.
- [ ] Verification commands are reproducible.
- [ ] Rollback plan is documented.
- [ ] The human reviewer understands and accepts the change.

See [AI Code Review Checklist](../../08-templates/08-templates_en/ai-code-review-checklist_en.md) for the full template.

For large changes that cross layers or ownership boundaries, split into stacked PRs. A single PR shouldn't simultaneously carry requirement explanation, code understanding, test verification, and risk assessment.

## 7. Common Anti-Patterns

### Letting AI Rewrite an Entire Module at Once

Risk: The diff is too large to review effectively.

Fix: Ask AI to output a plan first, then execute incrementally in small, scoped tasks.

### Committing Immediately After AI Finishes

Risk: Unrelated files, debug code, and config changes get bundled in.

Fix: Always run `git diff` before staging anything.

### Asking AI to Fix Bugs, Refactor, Add Tests, and Update Docs in One Shot

Risk: Behavioral changes and structural changes are tangled together.

Fix: Split into multiple commits or separate PRs.

### Force-Pushing Over a Collaborator's Branch

Risk: Work that others built on top of old commits is lost.

Fix: On public branches, prefer new commits for corrections. If history rewriting is truly necessary, confirm with collaborators first.

## 8. Example Workflow

```bash
# <integration-branch> comes from team repository rules, for example main, master, or develop
git status --porcelain
# Expected: no output. Stop and preserve the state if there is output.
git switch <integration-branch>
git pull --rebase origin <integration-branch>
git switch -c fix/order-timeout-validation

# AI modifies files

git status
git diff --stat
git diff

git add -p
git commit -m "test(order): cover timeout validation"

git add -p
git commit -m "fix(order): reject expired timeout config"

mvn test -pl order-service -Dtest=OrderTimeoutValidatorTest

git push -u origin fix/order-timeout-validation
```

In the PR description:

```text
What changed:
Add validation for expired timeout config.

How tested:
mvn test -pl order-service -Dtest=OrderTimeoutValidatorTest

Risk:
Low. Only affects invalid timeout config path.

Rollback:
Revert this PR.
```

## Further Reading

- [git worktree](https://git-scm.com/docs/git-worktree)
- [AI Change Review Practice Example](ai-change-review-example_en.md)
- [Git Integration Practices for AI Coding Tools](ai-coding-tools-git-integration_en.md)
- [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- [Responsible use of GitHub Copilot code review](https://docs.github.com/en/copilot/responsible-use/code-review)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
