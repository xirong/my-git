# One Engineering Change, from Task Contract to Recovery

English | [中文](../engineering-change-course.md) | [local exercise](../../labs/ai-change-control/README.md)

An agent changes an empty `SERVICE_TIMEOUT` into a default of `30`. It looks like a small fix, but an engineering team still needs answers: what may change? Which revision did a passing dirty-worktree test actually test? What diff did a reviewer accept? How do the integrated code, artifact, and runtime result correspond? If recovery is needed, which effects remain outside Git?

This course follows the same temporary repository in the [Agent Change Control Lab](../../labs/ai-change-control/README.md) through those decisions. The script really uses Git, Python unit tests, `git archive`, SHA-256 calculations, and a `127.0.0.1` HTTP request. It does not contact real CI, GitHub, production, or an external service. “Verified by the lab” below means only that local temporary environment; it is not a production claim.

This article owns the continuous case and the acceptance decision at each handoff. [Accepting an Agent Change, from Intent to Evidence](ai-change-control-loop_en.md) goes deeper on the evidence contract and its limits. [AI Native Git Workflow](ai-native-git-workflow_en.md) is the day-to-day command reference for inspection, branches, and worktrees. The three articles connect, without duplicating the same long procedure.

## Course map: the output of each handoff

```text
task contract
  -> existing edits and isolation
  -> candidate diff in the Index
  -> review and candidate SHA
  -> CI / integration result
  -> artifact and local runtime identity
  -> code recovery and business compensation
```

| Handoff | Decision now | Acceptable evidence | When to reject or reassess |
| --- | --- | --- | --- |
| Task contract | Does an empty value default to `30`, and what remains unchanged? | Explicit inputs, outputs, invariants, and validation | Scope is vague, or defaulting, error semantics, and caller impact are unstated |
| Isolation | Do existing edits belong to this task? | Status, baseline SHA, and path ownership | A shared directory has unknown edits but someone still plans to switch, clean, or partially commit |
| Candidate commit | Which paths make up the reviewable version? | Index, commit diff, and candidate SHA | A test passed only in a dirty worktree, or an unrelated note was included |
| Review and CI | Who accepts which version, and which SHA did checks run on? | Review decision, commands, results, and tested SHA | A branch test is used as evidence for a different integration result |
| Artifact and runtime | Do the running bytes come from the accepted revision? | Artifact SHA-256, manifest, build metadata, and runtime response | A hash is presented as a signature, trusted build, or production-release proof |
| Recovery | Which code and external effects need separate handling? | Post-revert code check, event records, and compensation record | A Git revert is treated as automatic rollback of data, messages, or external calls |

## Write the task contract first: make a small fix judgeable

The lab's baseline service raises `SERVICE_TIMEOUT must be set` when `SERVICE_TIMEOUT` is missing or empty. The task changes a missing value and an empty string to `30`. An explicit positive integer still wins; non-integers and non-positive values retain their errors. Those invariants give “the test passed” a concrete meaning and stop a defaulting fix from quietly becoming an error-handling, API, or retry-policy rewrite.

The task contract can be as small as this. Angle brackets are facts to fill in for the actual project; never substitute a sample SHA for a measured one.

```text
Goal: use 30 when SERVICE_TIMEOUT is missing or empty.
Keep: explicit positive integers; invalid values still fail; no API, event-format, or retry-policy change.
Scope: app.py and tests/test_timeout.py; notes/agent-scratch.md is out of scope.
Acceptance: target test passes in a clean worktree of the candidate commit; runtime response reports that candidate SHA.
Recovery: if defaulting is wrong, recover code and assess written events or other external effects.
```

The decision at this point is the behavioral boundary, not the command. If empty and missing values need different business semantics, or environment configuration and caller compatibility can change the meaning of the default, complete the contract and gather those facts before changing code. A source-code default describes source-visible behavior only; environment variables, configuration services, and deployment parameters still need verification in the target environment.

## Preserve the starting state, then choose isolation

Each lab run creates a marked temporary root with an `agent-worktree`. It commits a baseline, then lets the agent edit three things at once:

- `app.py` implements the empty-value default of `30`;
- `tests/test_timeout.py` adds the target test;
- `notes/agent-scratch.md` receives an unrelated local note.

The note belongs to a human and is outside the timeout fix. This models a shared workspace: `git status` says that a path changed, not who owns it or whether it can be discarded.

Start a real repository with read-only observation:

```bash
git status --short
git branch --show-current
git rev-parse HEAD
git worktree list
```

When staged, unstaged, or untracked content has an unknown owner, the acceptance condition is to record ownership and continue in a separate clean worktree. Do not make room with `switch`, `restore`, `clean`, or a broad `reset`. Once the directory is confirmed clean and repository rules allow it, it can host the task branch. Parallel tasks need their own directories and Indexes. See [AI Native Git Workflow](ai-native-git-workflow_en.md) and [Worktree for AI Agents](worktree-for-ai-agents_en.md) for the operating details.

## Let the Index expose the candidate: first make an acceptance attempt fail

The lab first runs the target test in a dirty worktree. The repaired `app.py` is already present there, so the test exits `0`. It then stages and commits only `tests/test_timeout.py`, producing a bad candidate commit; the repaired `app.py` and unrelated note remain in the worktree.

At this point, reject the conclusion “the local test passed, so the test commit is acceptable.” A clean worktree of that candidate contains the new test but the old application, which still rejects the empty value. The script asserts exit code `1` and this message:

```text
empty timeout must default to 30; got SERVICE_TIMEOUT must be set
```

The negative case has two different comparison objects: `git diff` observes the Working Tree relative to the Index, while `git diff --cached` observes the Index relative to `HEAD`. A test process reads the current filesystem; it does not automatically read only staged content. Before review, inspect at least:

```bash
git diff --stat
git diff
git diff --cached
git status --short
```

The lab then commits only the `app.py` repair. The candidate commit now contains the target test and implementation, while `notes/agent-scratch.md` stays uncommitted. A fresh clean worktree passes at the measured candidate SHA. The acceptable conclusion is “this command passed in a clean directory at this candidate SHA,” not “the whole workspace” or “the code is already integrated.”

When one file mixes intentions, a path-level commit cannot separate them. Move to a clean task worktree and use interactive staging; when that path already includes another owner's work, stop to clarify ownership. Go deeper with [Index: the draft of the next commit](../../01-getting-started/01-getting-started_en/git-mental-model-03-index_en.md) and [AI Commit Splitting](ai-commit-splitting_en.md).

## Review the candidate: accept behavior, not merely green output

With the candidate SHA defined, reviewers return to the task contract and inspect the diff. This case needs at least these questions:

- Do missing and empty values both return `30`, while explicit `15` still returns `15`?
- Do non-integers and non-positive values retain their contracted failures?
- Can target-environment configuration override the source default?
- Does the commit contain only the test and implementation change, with the unrelated note still in the worktree?
- Can the test fail before the repair and pass afterward, for the intended boundary?

A reviewer can accept “the candidate implements the contract and the evidence names this SHA,” or reject it for a missing invariant, mixed scope, or an uncovered configuration source. An AI risk scan may help locate files and counterexamples, but it cannot confirm business semantics for a person. GitHub pull-request reviews support comments, approval, and requested changes; whether approvals are required and who may provide them follows the repository's rules and permissions, as described in the [official GitHub documentation](https://docs.github.com/en/pull-requests/reference/pull-request-reviews).

Record the conclusion with its version:

```text
Candidate: <candidate SHA measured in this run>
Check: <command>, exit code <observed result>
Covered: empty default, explicit value, candidate scope
Not covered: <real configuration source, concurrent calls, other dependencies>
Review decision: accept / reject, because <specific behavior or diff>
```

For a full evidence template and a useful “not covered” statement, continue with [Accepting an Agent Change, from Intent to Evidence](ai-change-control-loop_en.md).

## CI and integration: a candidate SHA is not always the merged result

A clean-worktree test proves the candidate commit. Integrating can produce another SHA: merge commits, squash merges, and rebase merges can change final history, while the target branch may advance during review. Only a fast-forward integration whose final `HEAD` is the tested candidate SHA lets the candidate test directly describe that code version.

Make the decision by condition:

1. The integration-result SHA equals the tested candidate SHA: keep the candidate-test evidence and record the actual integrated SHA, review decision, and environment.
2. Integration creates a new SHA, or the target branch receives new commits after the check: the branch test does not directly represent the combined result. Run the necessary checks for that integration result and bind output to its new SHA.
3. CI offers a PR-merge or merge-queue result: record its triggering event, actual ref, and SHA before accepting it; do not attach only the agent branch SHA.

GitHub Actions needs an especially precise object label. For an open `pull_request`, default `GITHUB_REF` is the PR merge ref and `GITHUB_SHA` is the last merge commit on that ref; use `github.event.pull_request.head.sha` for the agent branch's last commit. `merge_group` has its own SHA and ref. When Actions checks are required for a merge queue, the workflow must listen for `merge_group`, or those checks will not report in the queue. The [GitHub Actions events documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows) defines these event and SHA semantics. This course requires only that evidence distinguish those objects; workflow configuration belongs in [CI for AI-generated changes](ci-for-ai-generated-changes_en.md).

Protected GitHub branches can require reviews and status checks; strict status checks require a branch to be current with its base, and a merge queue runs required checks when the pull request is applied to the newest target branch and queued changes. The actual capability and repository configuration follow the [GitHub protected branches documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches). The lab creates no pull request and runs no CI, so its local exit code cannot be reported as a GitHub check.

This course establishes the judgment chain from evidence to version. [Background Agent Workflow](background-agent-workflow_en.md) covers version, environment, and recovery evidence for background or remote agents.

## Before release: connect commit, bytes, and runtime identity

The lab takes source from the passing candidate commit with `git archive` and packages a tar.gz artifact. It writes a JSON manifest outside the artifact with:

- the candidate commit SHA;
- SHA-256 of the complete tar.gz;
- SHA-256 of extracted `app.py`;
- source version and build metadata written into the artifact.

The script also asserts that the note in the artifact is the baseline committed version, excluding the uncommitted `notes/agent-scratch.md`. It copies and tampers with the artifact, then rejects the copy with a SHA-256 preflight before extraction and service start; the error includes `artifact checksum mismatch`. This proves that the preflight detects “the bytes of this copy differ from the record in this manifest.”

After the original artifact passes preflight, the script compares the manifest, `app.py` from the recorded Git commit, and the artifact's build metadata. It then starts the service with empty `SERVICE_TIMEOUT` on a system-assigned port. The real `/health` HTTP response reports default timeout `30`, version, candidate commit, and event count. That gives a local evidence chain: tested SHA → artifact record → runtime response.

Hash capability depends on its object. Artifact SHA-256 checks that the complete artifact bytes match a trusted manifest record. Source SHA-256 checks that the `app.py` bytes recorded in the manifest were not substituted. Neither identifies who generated or signed the manifest, proves a trustworthy build machine or dependency source, proves deployment, or proves production behavior. A production release still needs real build provenance, authorization, deployment records, and target-environment verification.

## Retain local evidence: write a judgment, then explain the wrong answers

The following commands run only the temporary exercise supplied by this repository; they do not commit, switch, or clean the host repository. First run retained mode and copy the actual path printed after `kept lab root:`. Do not treat an example path or SHA as a result.

```bash
python3 labs/ai-change-control/lab.py --keep

# Replace with the actual path from the final line above.
lab_path=/printed/lab/root

python3 -m json.tool "$lab_path/evidence/exercise-evidence.json"
git -C "$lab_path/agent-worktree" log --oneline --decorate --all --graph
git -C "$lab_path/agent-worktree" status --short
cat "$lab_path/external-state/events.jsonl"
```

Before viewing the output, write a decision and reason for each:

1. Does “the test commit includes the new test” imply that the candidate contains the repair?
2. Does a matching SHA-256 in the manifest imply a trusted build and safe release?
3. After two `git revert` commits, should the event file automatically return to zero records?

After the run, the first two answers are no for different reasons: the test commit lacks the application repair that remained in the worktree, and a recomputable hash only compares bytes with a record. The third answer is no because the two HTTP requests wrote temporary events outside Git. The script verifies that reverted code accepts explicit `15`, that the rollback artifact reports event count `2`, and that the event file retains one record from the repaired version and one from the rollback version.

After inspection, clean only the marked temporary root printed by the script:

```bash
python3 labs/ai-change-control/lab.py --cleanup "$lab_path"
```

The script refuses unmarked directories, the repository root, the user's home directory, the filesystem root, and paths outside the temporary directory. Stop if the variable is not a path emitted by the script.

## Verify after integration; recover code and business effects separately

In the lab, the candidate artifact writes the first event. The script then makes two `git revert` commits, restores the baseline application and test, and builds and runs a rollback artifact. Reverted code accepts explicit `SERVICE_TIMEOUT=15`, yet the event file contains two records: one from the repaired version and one from the rollback version.

The acceptance decision has two parts. At the code layer, the rollback SHA's clean-worktree test and artifact response obey the earlier rule. At the business layer, the team has assessed whether external events need stopping, deduplication, compensation, or notification. If events represent orders, charges, messages, or third-party calls, `git revert` only creates a reverse code commit; it cannot replace those actions. Do not rewrite history that others already depend on to recover a shared branch.

The lab writes events only to a temporary JSONL file, so it does not demonstrate resolution of a real incident. For real severity, communication, compensation, and evidence retention, continue with [AI Agent Incident Recovery](../../06-troubleshooting/06-troubleshooting_en/ai-agent-incident-recovery_en.md).

## After this course, judge the next repository too

With another agent or repository, you should not need these exact filenames, language, or tools. You should be able to identify:

- what the task permits and which behavior must remain unchanged;
- which existing edits have an owner, and what the Index and candidate commit actually contain;
- which SHA ran which command, and whether the integration SHA is still that version;
- how the artifact and runtime response lead back to that SHA, and which trust assumptions hashes still lack;
- which data or external effects require a business process after code recovery.

That judgment chain puts Git principles into a repeatable engineering narrative. Return to [AI Native Git Workflow](ai-native-git-workflow_en.md) for commands, [Accepting an Agent Change, from Intent to Evidence](ai-change-control-loop_en.md) for the evidence contract, then select CI, background-agent, and incident-recovery topics according to project risk.
