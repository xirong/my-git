# Reclaiming Background Agent Tasks: From Dispatch to Decision

English | [中文](../background-agent-workflow.md)

A background agent can keep working after its requester leaves. When it reports “complete,” an engineering team still needs answers: which repository and baseline did it use, what is the candidate version, which evidence applies, and who may accept it? Treat the result as an engineering handoff that must be reclaimed, not as a completion notification.

This applies to any asynchronous coding agent. The process is platform-neutral. The GitHub Copilot cloud agent section is one verified mapping only; this article did not start a cloud agent or present an example as a cloud execution record.

The minimum task contract, attempt, expiry state, scene preservation, and acceptance decision in this article are handbook recommendations for a team to adopt. An agent platform may not store these fields natively, prevent duplicate execution, or reclaim a result automatically at its deadline. Teams implement them in a task system, PR template, orchestration configuration, or human process. The GitHub section states only GitHub behavior verified here; it does not present these rules as platform guarantees.

## The problem: completion does not decide acceptance

An agent completion state only says that an attempt reached a terminal state. It does not establish that the candidate still has the right baseline, that tests ran against the candidate, or that the diff meets the business intent. A background task needs this full path:

```text
dispatch -> execution and records -> reclaim result -> human decision
                                                      -> accept
                                                      -> reject
                                                      -> rework
                                                      -> expire
```

The object of acceptance is a bounded change plus evidence. Rejection, rework, and expiry are useful outcomes when they preserve a checkable starting point for the next attempt.

## 1. Write a minimum task contract before dispatch

The task ID is the correlation key for the handoff. A natural-language title cannot reliably join a task, branch, logs, and pull request after retries or similar requests. The following fields let a receiver identify the exact result to reclaim.

| Field | Required content |
| --- | --- |
| Task ID | Unique ID, attempt number, idempotency key; retries retain the parent task and add an attempt |
| Repository and target | Canonical repository identifier, target branch or integration ref, task directory |
| Confirmed base and candidate | `base SHA` at dispatch; `candidate SHA` at reclaim, or an explicit statement that no commit exists |
| Allowed scope | Writable paths, allowed actions, files and behavior that must remain unchanged |
| Expected behavior | Inputs, outputs, error semantics, compatibility, and preserved constraints |
| Validation | Required commands, manual steps, data or environment, and the SHA to which evidence must bind |
| Permissions | Minimum read, write, network, secret, PR, CI, and release authority |
| Owners | Dispatcher, receiver, integrator; who can stop, accept, request rework, or expire it |
| Budget and deadline | Token, concurrency, cost, or run-time limits, plus preservation rules at expiry |

Even a small fix can use a concise contract. The `orders-api`, `main`, and `8d21...` below are fictional placeholders: a real task must name the actual repository, integration ref, and full SHA.

```text
Task: AGT-184, attempt 1
Repository / target: orders-api, main
Base: 8d21...; candidate: pending reclaim
Allowed: src/timeout/**, tests/timeout/**; no deployment configuration or dependency manifest
Behavior: an empty timeout returns 30; invalid values preserve the existing error
Validation: npm test -- timeout in a clean directory at the candidate SHA
Permissions: write only the task branch; no merge, release, or production-data access
Receiver: on-call engineer; expire after 45 minutes and preserve the scene
```

Example SHAs cannot identify a baseline that later moved.

## 2. Record reclaimable facts while work is running

The execution platform should tie the task ID to the repository, starting ref, runtime, tool permissions, every attempt, branch or worktree, log location, and terminal reason. An agent’s test claim also needs the command, exit code, time, working directory, and tested SHA.

Further instructions belong in the same task record and identify the attempt they changed. A new session gets a new attempt number and a newly confirmed base, so two executions cannot claim each other’s edits.

Long tasks need an observable heartbeat and deadline. A missing heartbeat, exhausted budget, or broken environment produces `expired` or `failed`; it is not an empty result. A late commit can be input to a new attempt, though it cannot silently replace an integration state that a person already accepted.

## 3. Reclaim by checking version, scope, then evidence

Use this order to avoid trusting a green result before discovering it tested the wrong version.

1. Match task ID, repository, target ref, base SHA, candidate SHA, and attempt.
2. Compare the current target-ref SHA with the recorded base. A difference means the integration base moved and the candidate needs a new decision in that combination.
3. Inspect paths and diff in `base..candidate` to confirm the allowed scope.
4. Check whether the candidate commit is complete. Uncommitted edits, untracked files, and an undelivered patch are scene evidence, not a candidate commit.
5. Match every validation item to its command, result, environment, and SHA. Missing evidence requires rework or rejection.
6. Review the diff against the contract, then let an authorized receiver accept, reject, request rework, or expire it.

These read-only commands do not contact a remote. They inspect an existing base and candidate:

```bash
git rev-parse <integration-ref>
git merge-base --is-ancestor <base-sha> <candidate-sha>
git diff --name-status <base-sha>..<candidate-sha>
git diff --check <base-sha>..<candidate-sha>
git show --stat --oneline <candidate-sha>
```

`merge-base --is-ancestor` only proves that the candidate descends from the recorded base. It does not prove that the target ref stayed still, and it cannot replace diff review or testing. When the integration ref moved, validation must address the combination about to be accepted, not continue to cite a green result from the old candidate.

## 4. Reclaim common failure modes

| Observation | Receiver action | Avoid |
| --- | --- | --- |
| Base moved | Record the new ref SHA; update the candidate against the new combination and validate again | Presenting old-base test output as integration evidence |
| Edits were not committed | Preserve status, diff, untracked paths, and ownership; request a candidate commit or ask its owner to decide disposition | Using `clean`, `restore`, or a broad `reset` on unknown edits |
| Wrong branch or target | Compare candidate ancestry, PR target, and allowed paths; state the correct base/ref in rework | Accepting because a commit message sounds plausible |
| No reviewable evidence | State the missing command, output, version, or environment; request a rerun or reject | Treating “the agent said it passed” as evidence |
| Duplicate task run | Deduplicate on task ID, attempt, repository, base, and target paths; keep one active attempt | Letting multiple executions write unordered changes to one branch |
| Timeout or failure | Mark `expired`/`failed`; preserve final SHA, state, logs, and uncommitted diff before releasing platform resources | Marking a timed-out task successful or deleting its isolation before preservation |

Preserve the minimum incident scene: task contract, branch or candidate SHA, `git status --porcelain`, changed-path list, diff summary, validation output, runtime identifier, and terminal reason. Redact logs that contain secrets, user data, or internal addresses before sharing them.

Clean up after the decision. First record the retained location and owner, then act only on a worktree, temporary directory, or branch demonstrably exclusive to the task. Keep directories with unknown edits intact and escalate to their owner. A rejected candidate must remain locatable for the team’s audit-retention period; storage and compliance rules set that period.

## 5. Platform-neutral handoff and reclaim example

Place this record in an issue, task system, or pull-request description. Replace every angle-bracket field with a fact.

```text
Task ID: AGT-184 / attempt 2
Repository and target: orders-api / main
Dispatch base: <base SHA>
Candidate: <candidate SHA>; branch: agent/AGT-184
Allowed scope: src/timeout/**, tests/timeout/**
Behavior: empty timeout returns 30; invalid input retains its existing error
Evidence: npm test -- timeout, exit <n>, run at <candidate SHA> in <environment>
Uncovered: <real configuration source, concurrent calls, or another boundary>
Permissions and deadline: task-branch write only; no merge/release; expire at <time>
Recommendation: accept / rework, reason <fact tied to the contract>
```

A reclaim decision needs more than “received”:

```text
Decision: rework
Reason: main advanced from <base SHA> to <new SHA>; tests only name the old candidate.
Next: create a new candidate from <new SHA> and rerun the specified test in a clean directory.
Preserve: attempt 2 branch, diff summary, and test log at <location>.
Owner: <person or role>; deadline: <time>.
```

## 6. Runnable local version check

The following example creates a temporary Git repository with a `background-agent-demo.` prefix under `/tmp`. It simulates an agent candidate followed by advancement of `main`, then checks a candidate file in a separate worktree. It never accesses a remote, creates a pull request, or invokes a paid service. Read every line first and never substitute a real workspace for the example directory.

```bash
set -euo pipefail
demo_dir=$(mktemp -d /tmp/background-agent-demo.XXXXXX)
case "$demo_dir" in /tmp/background-agent-demo.*) ;; *) exit 1 ;; esac

git init -q -b main "$demo_dir"
git -C "$demo_dir" config user.name "Background Agent Demo"
git -C "$demo_dir" config user.email "background-agent-demo@example.invalid"
printf 'timeout=10\n' > "$demo_dir/config.txt"
git -C "$demo_dir" add config.txt
git -C "$demo_dir" commit -qm "base timeout"
base_sha=$(git -C "$demo_dir" rev-parse main)

git -C "$demo_dir" switch -q -c agent/AGT-42 "$base_sha"
printf 'timeout=30\n' > "$demo_dir/config.txt"
git -C "$demo_dir" add config.txt
git -C "$demo_dir" commit -qm "agent timeout change"
candidate_sha=$(git -C "$demo_dir" rev-parse HEAD)

git -C "$demo_dir" switch -q main
printf 'release_note=keep\n' > "$demo_dir/release.txt"
git -C "$demo_dir" add release.txt
git -C "$demo_dir" commit -qm "integration moved"
integration_sha=$(git -C "$demo_dir" rev-parse main)

test "$base_sha" != "$integration_sha"  # detects a moved base
git -C "$demo_dir" merge-base --is-ancestor "$base_sha" "$candidate_sha"
git -C "$demo_dir" diff --check "$base_sha".."$candidate_sha"
git -C "$demo_dir" worktree add --detach "$demo_dir/verify" "$candidate_sha"
test "$(sed -n '1p' "$demo_dir/verify/config.txt")" = 'timeout=30'
git -C "$demo_dir" worktree remove --force "$demo_dir/verify"
```

The final `worktree remove` targets the fixed `verify` directory created by the prior command. After recording the result, dispose of the temporary root using the operating system’s recoverable deletion method. Real-repository worktrees, branches, and directories with unknown contents do not fit this example.

## 7. A concrete GitHub Copilot cloud agent mapping

As of 2026-09-07, GitHub’s documentation describes cloud agent as one implementation of this protocol. This mapping only covers publicly documented GitHub capabilities. Preview status and repository settings can change the observed behavior.

GitHub Issues, sessions, branches, and PRs can carry task records. They do not automatically gain the task ID, allowed paths, budget, expiry conclusion, or acceptance decision from this article’s template. After a team records these fields in an issue, PR, external task system, or automation configuration, its own rules and authorized people still perform reclaim.

| Reclaim stage | GitHub documentation establishes | The team still decides |
| --- | --- | --- |
| Dispatch | A person with repository write access can assign Copilot to an issue; this starts work, raises a PR, then requests review on completion | The issue must still state contract, especially base, scope, tests, and receiver |
| Agent identity and execution | API docs identify the assignable actor as `copilot-swe-agent`; cloud agent works in a GitHub Actions-powered ephemeral environment | Record actual issue, session, branch, PR, and candidate SHA for later audit |
| Result and validation | The agent can run tests and linters; built-in code-quality, security, and second-Copilot-review tools are configurable | These tools and the agent report are evidence inputs; the receiver still checks behavior, scope, execution SHA, and gaps |
| Workflow trigger | By default GitHub Actions workflows do not run automatically after agent pushes to a PR; a person can approve a run in the PR merge box. An administrator can enable automatic runs | Inspect the workflow, permissions, and secrets before approval; record the SHA for every green result |
| Acceptance | The agent requests a reviewer at completion; human PR review, branch rules, and merge authority continue to follow repository configuration | A person with merge authority accepts or requests rework from the contract, not from an automatic terminal state |

GitHub also states that repository administrator permission is needed to change cloud-agent validation tools and automatic Actions settings. Enabling Actions without approval can give unreviewed code repository write access or Actions-secret access. Validate team rules first in a low-risk repository with minimum permissions before expanding automation.

The following sources were read-only verified for this article: [Using Copilot cloud agent on GitHub](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-on-github), [Configuring settings for GitHub Copilot cloud agent](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/configuring-agent-settings), [Using Copilot cloud agent via the API](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-via-the-api), and [Assigning issues and pull requests](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/assigning-issues-and-pull-requests-to-other-github-users). This article did not verify whether a particular repository has enabled the feature, its paid plan, permissions, branch rules, workflows, or secrets.

## Further reading

- [Accepting an Agent Change: From Intent to Evidence](ai-change-control-loop_en.md)
- [CI for AI-Generated Changes: Bind Checks to the Candidate Version](ci-for-ai-generated-changes_en.md)
- [AI Agent Incident Recovery: Preserve the Scene Before Deciding Code Handling](../../06-troubleshooting/06-troubleshooting_en/ai-agent-incident-recovery_en.md)
- [Two AI Agent Engineering Cases: Turn Public Reports into Team Decisions](../../10-company-practices/10-company-practices_en/ai-native-engineering-cases_en.md)
