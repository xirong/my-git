# AI Change Review Practice Example

English | [中文](../ai-change-review-example.md)

This article uses a simulated scenario to illustrate how humans use Git to reorganize changes into reviewable, verifiable, and rollback-ready engineering units after AI has modified the code.

## Scenario

You asked the AI to fix a problem:

```text
When the order timeout configuration is empty, the system should use the default timeout and should not throw an exception directly.
```

After the AI finishes, the workspace looks like this:

```bash
git status --short
```

```text
 M src/order/timeout.ts
 M src/order/validator.ts
 M src/order/index.ts
 M test/order/timeout.test.ts
 M package-lock.json
 M README.md
?? debug-output.log
```

At this point, do not directly `git add .`.

## Step 1: Check the Scale of Changes First

```bash
git diff --stat
```

Focus on three things:

1. Whether the number of files exceeds the task scope.
2. Whether there are generated files, logs, or lock files.
3. Whether documentation, formatting, or dependency upgrades are mixed in.

In this example, the task is to fix the order timeout configuration, but the following appeared:

- `src/order/index.ts`
- `package-lock.json`
- `README.md`
- `debug-output.log`

These all need to be confirmed for relevance first.

## Step 2: Clear Obviously Irrelevant Files

Process untracked logs first:

```bash
rm debug-output.log
```

If `package-lock.json` has no real dependency changes, restore it:

```bash
git restore package-lock.json
```

If `README.md` is just a vague description added by the AI, restore it first:

```bash
git restore README.md
```

Check again:

```bash
git status --short
git diff --stat
```

The target state should be more focused:

```text
 M src/order/timeout.ts
 M src/order/validator.ts
 M test/order/timeout.test.ts
```

## Step 3: Split Diffs by Intent

Look at the tests first:

```bash
git diff -- test/order/timeout.test.ts
```

If the tests indeed cover "use default timeout when config is empty," commit the tests separately first:

```bash
git add test/order/timeout.test.ts
git commit -m "test(order): cover empty timeout config"
```

Then look at the implementation:

```bash
git diff -- src/order/timeout.ts src/order/validator.ts
```

Confirm that the implementation only changed the default value handling and did not incidentally change error codes, interface signatures, or log formats.

```bash
git add src/order/timeout.ts src/order/validator.ts
git commit -m "fix(order): fallback to default timeout config"
```

This results in two final commits:

```text
test(order): cover empty timeout config
fix(order): fallback to default timeout config
```

## Step 4: Let AI Perform a Risk Scan

You can hand the current diff or commit range to an AI for review:

```text
Please review the changes in the current branch relative to main.
List only specific risks, do not provide vague summaries.
Key checks:
1. Whether behavioral boundaries have been expanded
2. Whether error handling has become weaker
3. Whether default values affect compatibility
4. Whether tests cover real business scenarios
5. Whether irrelevant changes are mixed in
```

If the AI's output lacks file paths and specific risks, and only says "looks good," this review round has very low value; push back with more specific prompts.

## Step 5: Manual Verification Focus

A human reviewer should at least confirm:

- How empty configurations, empty strings, and illegal numbers are handled respectively.
- Where the default values come from.
- Whether production configurations might override the code's default values.
- Whether error codes and logs have changed.
- Whether callers depend on the original exceptional behavior.
- Whether tests can fail before the fix and pass after the fix.

When production configurations are involved, static code can only describe default behavior. The final production values still need to be confirmed in conjunction with configuration centers, environment variables, or deployment parameters.

## Step 6: Run Verification

Run only the most relevant validations for this change:

```bash
npm test -- test/order/timeout.test.ts
```

If the project has lint or type checking, include those as well:

```bash
npm run lint
npm run typecheck
```

The PR should clearly state the actual commands executed and their results.

## Step 7: Write the PR

Recommended PR description:

```md
## What changed

- Add test coverage for empty timeout config
- Fallback to default timeout config when config is empty

## Why

Empty timeout config should not break order validation.

## How tested

- npm test -- test/order/timeout.test.ts
- npm run lint

## Risk

Low. The change only affects empty timeout config fallback.

## Rollback plan

Revert this PR.
```

## Step 8: If the Diff is Still Too Large

If the AI changed cross-layer capabilities at once—for example, model, service, API, UI, and documentation all changed—a single PR is still hard to review.

In this case, it can be split into stacked PRs:

```text
PR 1: add tests for timeout fallback
PR 2: implement timeout fallback
PR 3: update API response note
PR 4: update docs
```

See [Stacked PR for AI-Generated Changes](stacked-pr-for-ai-generated-changes_en.md) for details.

## Common Mistakes

### Committing All AI Output Directly

Risk: Irrelevant files, debug logs, and dependency changes will be mixed in.

Suggestion: Always look at `git diff --stat` first.

### Only Checking if Tests Pass

Risk: AI might write tests that only verify the current implementation.

Suggestion: Confirm whether tests cover business boundaries and try to confirm they fail before the fix.

### Mixing Refactoring and Behavioral Fixes Together

Risk: Reviewers cannot determine where the risk comes from.

Suggestion: Fix behavior first, then perform refactoring separately.

## Extended Reading

- [AI Native Git Workflow](ai-native-git-workflow_en.md)
- [How to Review AI-Generated Code](ai-generated-code-review_en.md)
- [AI Commit Splitting](ai-commit-splitting_en.md)
- [Stacked PR for AI-Generated Changes](stacked-pr-for-ai-generated-changes_en.md)
- [AI Code Review Checklist](../../08-templates/08-templates_en/ai-code-review-checklist_en.md)
