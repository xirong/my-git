# Two AI Agent Engineering Cases: Turn Public Reports into Team Decisions

English | [中文](../ai-native-engineering-cases.md)

Public cases can help a team ask better questions. They cannot replace the team’s own permission, Git, CI, and review rules. This article covers two first-party reports only: Ramp’s description of its internal background coding platform, Inspect, and Cursor’s account of long-running concurrent-agent experiments. Their purpose, environment, and strength of evidence differ, so they must be read separately.

Each case separates “what the authors report,” “team practices we can infer,” and “what remains unproven.” Numbers retain their publication date and self-reported status. They are not independent quality measures or evidence of a repeatable benefit for another team.

## Distinguish the two kinds of evidence first

| Case | Original source and date | Kind of report | Question it helps answer |
| --- | --- | --- | --- |
| Ramp Inspect | [Ramp Builders: Why We Built Our Own Background Agent](https://builders.ramp.com/post/why-we-built-our-background-agent), 2026-01-12, Zach Bruggeman, Jason Quense, and Rahul Sengottuvelu | Company description of an internal platform | Why a background agent needs an isolated execution environment, tools, and validation context, and how its result returns to GitHub collaboration |
| Cursor long-running agents | [Cursor Research: Scaling long-running autonomous coding](https://cursor.com/blog/scaling-agents), 2026-01-14, Wilson Lin | Company research experiment report | How to divide parallel work, why coordination locks become bottlenecks, and how planning, worker, and evaluation responsibilities can differ |

Both sources are first-party accounts. They describe design choices and self-reported observations. Neither supplies an independent reproduction, complete costs, defect rates, or results from ordinary-team migration.

## Case one: Ramp Inspect centers on returning validation context with the result

### What the authors report

Ramp introduces Inspect, its internal background coding agent: backend work can use tests, telemetry, and feature flags, while frontend work can visually verify changes and produce screenshots and previews. Its public architecture mentions an isolated sandbox per session, prebuilt images, file-system snapshots, repository synchronization, and a user GitHub token for pull-request creation.

At publication, the authors reported that about 30% of merged PRs in their frontend and backend repositories were written by Inspect after a few months. This is Ramp’s internal usage report, not an independent measurement of defect rate, review quality, cost, or external reproducibility. The source also does not disclose a specific repository’s permissions, network policy, or production-data boundary.

### Practices a team can infer

1. Put both “what the agent may do” and “what it may establish” in the task contract. Tests, telemetry, feature flags, and screenshots need minimum permissions, input provenance, runtime, and output location before the results become reviewable.
2. Give every task an attributable isolated directory, branch, or runtime. Isolation reduces overwriting opportunities; it does not determine allowed paths or confirm business meaning.
3. Join the PR, candidate SHA, test output, and session record. Tool output without a command, time, environment, and SHA is a lead, not evidence.
4. Plan review, CI, and integration capacity together with concurrency. When production of candidate changes outpaces review capacity, narrow task scope or limit concurrency instead of accumulating an unlimited review queue.

These practices connect to the task contract, candidate SHA, and scene preservation in [Reclaiming Background Agent Tasks](../../05-ai-native-development/05-ai-native-development_en/background-agent-workflow_en.md). [CI for AI-Generated Changes](../../05-ai-native-development/05-ai-native-development_en/ci-for-ai-generated-changes_en.md) continues with binding check output to the candidate version.

### What remains unproven

- The source does not provide independent success rates, human-review time, rework rate, or security-incident data for Inspect tasks.
- The roughly 30% number does not state the complexity mix, team baseline, or counting method for all PRs, so it cannot set a local KPI.
- Whether image snapshots and remote sandboxes fit a codebase depends on build time, dependency licensing, network isolation, data classification, and budget. A local pilot must establish that fit.

## Case two: Cursor centers on defining responsibilities and convergence points before parallelism

### What the authors report

Cursor Research records long-running autonomous-coding experiments. When peer agents claimed tasks from a shared file using locks, the authors report that roughly twenty agents fell to effective throughput of two or three. They then split responsibilities among planners that create tasks, workers focused on assigned tasks, and a judge that decides whether each cycle continues.

The post also reports a browser project that ran for close to a week and produced more than one million lines across one thousand files, plus a Solid-to-React migration with `+266K/-193K` edits over more than three weeks. It says that migration still needed careful review while passing its CI and early checks. These observations were self-reported by Cursor’s authors on 2026-01-14; they do not establish quality, maintainability, or a repeatable gain.

### Practices a team can infer

1. Cut boundaries before increasing concurrency. Divide work by directory, component, service, or crisp behavior, and give each task an owner, base SHA, allowed paths, and validation. Shared state files and global locks easily become new serial points.
2. Planning, implementation, and acceptance can be different responsibilities. A planner creates executable boundaries, a worker returns a candidate, and a judge checks whether to continue. The judge does not replace a human receiver who has business and merge authority.
3. Convergence has capacity. Every candidate consumes CI, conflict handling, and review attention. Concurrency should be bounded by that capacity, task independence, and risk.
4. Begin every cycle from a confirmed integration state. This exposes moved bases, duplicate execution, and same-path conflicts, and makes old output an explicit input instead of a hidden change in the next cycle.

Together, [Multi-Agent Branch Strategy](../../05-ai-native-development/05-ai-native-development_en/multi-agent-branch-strategy_en.md), [Accepting an Agent Change](../../05-ai-native-development/05-ai-native-development_en/ai-change-control-loop_en.md), and [AI Agent Incident Recovery](../../06-troubleshooting/06-troubleshooting_en/ai-agent-incident-recovery_en.md) provide the isolation, candidate-evidence, and failure-scene links for this workflow.

### What remains unproven

- The source gives no controlled comparison of the lock approach and separated responsibilities on the same codebase and task set.
- A report of hundreds of agents pushing to one branch does not recommend a shared branch for ordinary teams. Without explicit isolation and integration rules, that choice increases conflict and incorrect-attribution risk.
- The post’s model comparisons and claims are not model-selection guidance in this handbook. Teams need their own evidence on task fit, permission, latency, cost, tests, and review outcome.

## Use the two cases to design a pilot

The transferable constraints differ. Ramp emphasizes the runtime and validation information of one background session. Cursor emphasizes division and coordination of many tasks. Their shared minimum is that tasks can be bounded, candidates resolve to a SHA, validation produces reviewable output, and humans have clear review and integration ownership.

Start with one low-risk, reversible path:

1. Choose work with stable tests and no production writes, secrets, or highly sensitive data.
2. Use [Reclaiming Background Agent Tasks](../../05-ai-native-development/05-ai-native-development_en/background-agent-workflow_en.md) to record task ID, base, allowed paths, permissions, candidate, evidence, and receiving decision.
3. Limit concurrency to the number of changes the team can review and integrate, while recording base movement, conflicts, rework, validation failure, and human handling time.
4. Review those local records after several tasks before expanding tool permissions, path scope, or concurrency.

Public reports supply hypotheses and design signals. Whether a team benefits has to be established from its own repository, data classification, CI, review capacity, and delivery results.
