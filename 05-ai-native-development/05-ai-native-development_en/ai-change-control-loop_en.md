# Accepting an Agent Change, from Intent to Evidence

English | [中文](../ai-change-control-loop.md)

An agent fixes a timeout bug and returns code, tests, and a completion message. You need to decide whether to accept the change and what can be recovered if it fails.

This article owns the auditable contract linking intent, scope, candidate SHA, and acceptance evidence. For the continuous `SERVICE_TIMEOUT` lab case through isolation, Index, review, integration SHA, artifact, and recovery, start with [One Engineering Change, from Task Contract to Recovery](engineering-change-course_en.md). For day-to-day commands, use [AI Native Git Workflow](ai-native-git-workflow_en.md).

Connect **intent → scope → commit → verification evidence → integration decision → release outcome**. A mismatch between adjacent steps can make “tests passed” irrelevant.

## 1. Define acceptable behavior

State the existing failure, expected result, behavior that must remain unchanged, and how to verify it. For a timeout fix, clarify whether defaults, error codes, and retry policy may change. A small task may need only a few sentences.

Ask the agent to identify its baseline commit and changed paths. The baseline distinguishes task changes from pre-existing differences.

## 2. Inspect the starting state and isolation

```bash
git status --short
git branch --show-current
git rev-parse HEAD
git worktree list
```

These are read-only checks. Record existing edits and their ownership. Branches separate lines of history; worktrees separate working directories and their indexes. Switching branches in a shared directory does not provide concurrent isolation. See [Worktree for AI Agents](worktree-for-ai-agents_en.md).

## 3. Define the accepted draft with the index

```bash
git diff --stat
git diff
git diff --cached
```

Plain diff compares the working tree with the index; cached diff compares the index with HEAD. Inspect untracked files too. Stage explicit paths after confirming scope, or use partial staging when one file mixes intentions. Follow repository authorization rules for committing.

Do not remove unrelated edits just to simplify the view. Establish ownership and commit only the relevant scope. See [The index draft](../../01-getting-started/01-getting-started_en/git-mental-model-03-index_en.md) and [AI Commit Splitting](ai-commit-splitting_en.md).

## 4. Bind verification to the actual revision

Working-tree tests can consume unstaged edits. Running tests does not alone prove the draft is correct. Once authorized to commit, record the commit ID and preferably run the required validation in a clean checkout of that revision. Describe dependencies, environment, and test data where relevant.

```bash
git rev-parse HEAD
git status --short
git show --stat --oneline HEAD
```

These commands identify the revision and state; they are not business tests. If source, tests, or configuration change during verification, reassess earlier evidence. A merge result can differ from the branch revision: validate what will actually ship.

Without an automated test suite, record repeatable manual steps, observed outcomes, and uncovered areas. Do not call this comprehensive verification.

## 4.1 Runnable exercise: make the evidence name one candidate revision

The [Agent Change Control Lab](../../labs/ai-change-control/README.md) connects this section's decisions through a temporary Git repository, minimal Python service, real tests, artifacts, and loopback HTTP requests. It does not alter the current repository's commits or working tree.

Run from the repository root:

~~~bash
python3 labs/ai-change-control/lab.py
bash labs/ai-change-control/test.sh
~~~

The lab intentionally starts with a negative case: the application repair remains in the dirty working tree while only the new test enters the candidate commit. The test passes in the current directory, then the same test fails in a clean worktree with exit code <code>1</code> and a specific timeout error. After the repair is committed, the lab records the actual candidate SHA tested in a clean worktree and builds an artifact from that commit with <code>git archive</code>.

An external artifact manifest records the commit SHA, artifact SHA-256, source SHA-256, and version. The lab first copies and tampers with the artifact, reuses its startup-preflight SHA-256 check, and asserts an explicit checksum mismatch. It then recomputes the original artifact's SHA-256 and checks the manifest, Git source, and embedded build metadata. The HTTP response also returns the candidate SHA and version as supporting evidence that the runtime result corresponds to the artifact.

The final <code>git revert</code> restores the code but does not automatically delete the temporary events written by the earlier service. That boundary means code recovery, artifact switching, and external-state compensation need separate handling. The exercise runs only in a temporary directory on <code>127.0.0.1</code>; it is not evidence of a real CI run, production release, signature, or supply-chain claim.

## 5. Give reviewers evidence for a decision

Replace the placeholders with observed values:

```text
Intent: <problem and behavior that must stay unchanged>
Baseline / candidate: <base SHA> / <head SHA>
Scope: <paths and behavioral differences>
Evidence: <commands, results, tested revision, relevant environment>
Not covered: <remaining unknowns>
Recovery: <code recovery; data and external effects>
Responsibility: <person or policy owning integration and release>
```

A PR supports discussion and review. Its title, author identity, and green checks do not prove business correctness. See [GitHub Pull requests](https://docs.github.com/en/pull-requests/reference/pull-requests) and [AI Reviewer and Human Reviewer](ai-reviewer-and-human-reviewer_en.md).

## 6. Verify integration, release, and recovery separately

Integration accepts code history. Release puts an artifact into an environment. Business verification checks the intended behavior. They must refer to matching versions, with evidence appropriate to each step.

If a timeout policy creates duplicate orders, revert can produce a commit that reverses code changes, but the orders need business compensation. Understand the impact and use the incident process. Do not substitute shared-history rewriting for coordinated recovery.

Continue with [Undo Anything](../../06-troubleshooting/06-troubleshooting_en/undo-anything_en.md) and [Release Management](../../04-github-engineering/04-github-engineering_en/release-management_en.md).

## What understanding looks like

With a different agent or repository, you can still identify:

- Which changes belong to the intent.
- Which revision passed which verification.
- Who or what accepted the change, using which evidence.
- Which effects can be recovered through code, and which cannot.

This is one complete exercise in applying Git’s design to engineering judgment.
