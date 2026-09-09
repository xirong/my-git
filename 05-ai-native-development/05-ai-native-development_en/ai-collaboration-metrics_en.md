# Does Agent Adoption Improve Delivery? Reconstructible Collaboration Metrics

English | [中文](../ai-collaboration-metrics.md)

After a team adopts agents, PR volume and the percentage of AI-generated code may rise quickly. These numbers show a change in activity. On their own, they cannot establish that tasks ship faster, review costs fall, or production quality improves.

This article defines a compact measurement plan for a short trial. The five measures below are **local definitions for this article**, not official DORA or SPACE metrics. DORA examines software delivery performance through throughput and instability, recommends multiple measures, and warns that application context matters. The SPACE paper likewise states that developer productivity cannot be measured by one metric or dimension.

## Fix the comparison rules first

Write these rules before the trial and do not change them after seeing the results:

- **Unit:** Use a task with explicit acceptance criteria as the primary unit. Multiple PRs for one task still count as one task.
- **Window and cohort:** For example, fix the cohort as tasks entering `In progress` during April and measure completion through April 30. Extend the data cutoff to May 7 for a seven-day post-merge problem observation period.
- **Attribution:** Record `none`, `assist`, or `agent-led`. Keep mixed human-agent work as mixed attribution; do not describe it as autonomous agent output. Disclose any grouping rule used when the sample is too small.
- **Comparability:** At minimum, stratify by task complexity, repository, work type, and reviewer load. Record simultaneous changes in staffing, release cadence, test coverage, or demand mix as confounders.
- **Reporting:** Show numerators, denominators, and distributions. Prefer adjacent windows for the same team or matched cohorts. A small sample can reveal investigation targets; it cannot establish causality.

Do not use these measures to rank individuals. Rankings encourage PR splitting, hidden rework, and avoidance of risky tasks, while assigning a collaborative outcome to one person.

## Five useful measures

### 1. Window completion rate

**Definition:** Tasks reaching the agreed acceptance state within the window ÷ all tasks in the fixed cohort.

Open tasks stay in the denominator. Closed but undelivered tasks must not silently disappear. A business cancellation unrelated to implementation may be excluded only under a rule fixed in advance; report the count and reasons separately.

**Limitation:** Loose acceptance criteria inflate the result. Tasks with materially different complexity should not be compared without stratification.

### 2. Delivery lead time

**Definition:** For each completed task, `accepted_at - work_started_at`. Report the median beside the window completion rate.

An incomplete task has no complete duration; do not invent one using the window end. Mark it as right-censored or represent it only in completion rate. If merge is the only available endpoint, use `merged_at` and call the measure “merge lead time” so that merge is not presented as production acceptance.

**Limitation:** Completed tasks alone introduce survivor bias. Decide in advance whether time blocked on external dependencies remains included.

### 3. First-review wait and actual reviewer effort

**Wait definition:** Calculate each PR first. The start is when the PR enters its first valid reviewable interval: use the PR's `created_at` when it opens as non-draft; when it changes from draft to ready, use the `created_at` of the REST timeline's `ready_for_review` event. If a `convert_to_draft` event occurs before the first human review, discard that interval and restart at the next `ready_for_review` event. The endpoint is the first substantive human review's `submitted_at` within that interval. Report a review earlier than the selected start as a data anomaly.

For a task with several PRs, take the median of its valid PR waits as the task value, then report the cohort median of task values. A PR without a substantive human review has no wait value. Report missing PRs and affected tasks rather than silently dropping them.

**Effort definition:** The sum of active minutes recorded by reviewers across all review sessions and PRs for the task. GitHub timestamps can reconstruct waiting; they cannot reveal how long a reviewer actively read the change. Report the median among tasks with effort records and the record-coverage rate. A shorter wait with higher effort means the queue improved while review cost may have risen.

**Limitation:** Exclude bot reviews from substantive human review. Define in advance whether a human “LGTM”-only response counts as substantive. Active minutes usually require sampled self-reporting or an existing time record.

### 4. Pre-merge rework incidence

**Definition:** Reviewed and merged tasks with at least one author code update explicitly linked to review feedback after the first substantive human review ÷ all reviewed and merged tasks. The link may come from a review thread, commit description, or an existing team change record.

This answers how many tasks required another change because of review; it does not measure rework size. Report newly requested scope separately and do not count it as review rework. Report unclassified code updates too. Follow-up commits, force-updated branches, and several PRs for one task require event aggregation by task ID. Because the link depends on recording discipline, this remains a proxy for rework.

### 5. Post-merge repair rate

**Definition:** Tasks linked to a revert, hotfix, or production incident within seven days after the task's final `merged_at` ÷ tasks with a complete seven-day post-merge observation period.

Exclude tasks without the full observation period from this denominator and report how many were excluded. Link through a task ID, PR link, deployed revision, or incident record; do not infer the relationship only from a commit title.

**Limitation:** Defects found after seven days are missed. A delayed release shortens the real exposure period after merge. Release policy, observability, and incident-record quality also influence this measure.

## A fully synthetic, reconstructible example

The following data demonstrates the arithmetic only; it is not a production result from any team. The cohort contains similarly complex work in one repository. Each task has one PR; every accepted task was merged and received a substantive human review, and every rework flag is linked to review feedback. `A5` remains open without a human review at the end of the window. Every merged task has a complete seven-day post-merge observation period.

| Cohort | Task | Status | Lead time (hours) | First-review wait (hours) | Review effort (minutes) | Pre-merge rework | Repair within 7 days |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| No agent | N1 | Accepted | 40 | 8 | 30 | No | No |
| No agent | N2 | Accepted | 48 | 12 | 45 | Yes | No |
| No agent | N3 | Accepted | 56 | 20 | 30 | Yes | Yes |
| No agent | N4 | Accepted | 72 | 24 | 60 | Yes | No |
| Agent-assisted | A1 | Accepted | 24 | 6 | 45 | Yes | Yes |
| Agent-assisted | A2 | Accepted | 30 | 10 | 60 | Yes | No |
| Agent-assisted | A3 | Accepted | 36 | 14 | 60 | Yes | Yes |
| Agent-assisted | A4 | Accepted | 42 | 18 | 75 | No | No |
| Agent-assisted | A5 | Open | - | - | - | - | - |

Reconstructed results:

- Completion rate: no agent is `4 / 4 = 100%`; agent-assisted is `4 / 5 = 80%`.
- Median lead time among completed tasks: no agent is `(48 + 56) / 2 = 52` hours; agent-assisted is `(30 + 36) / 2 = 33` hours.
- Median first-review wait: no agent is `(12 + 20) / 2 = 16` hours; agent-assisted is `(10 + 14) / 2 = 12` hours.
- Median review effort: no agent is `(30 + 45) / 2 = 37.5` minutes; agent-assisted is `(60 + 60) / 2 = 60` minutes.
- Task-record coverage for both first-review wait and review effort: no agent is `4 / 4 = 100%`; agent-assisted is `4 / 5 = 80%`, with the open task `A5` missing in both.
- Pre-merge rework incidence is `3 / 4 = 75%` in both cohorts. Seven-day repair rates are `1 / 4 = 25%` and `2 / 4 = 50%`, respectively.

The data supports only a description: completed agent-assisted tasks were faster and waited less for the first review, while reviewer effort was higher, completion was lower, and short-term repairs were more frequent. The sample is tiny and may still differ in task complexity, reviewer scheduling, or other confounders. It cannot establish that agents increased or decreased productivity.

## Start with existing records

You do not need a dashboard or a new collection service first. A task tracker usually supplies start, acceptance, complexity, and work type. GitHub's [Pull requests REST API](https://docs.github.com/en/rest/pulls/pulls), [Pull request reviews REST API](https://docs.github.com/en/rest/pulls/reviews), and [Timeline events REST API](https://docs.github.com/en/rest/issues/timeline) can supply PR, merge, review, and reviewable-state events. [Issue event types](https://docs.github.com/en/rest/using-the-rest-api/issue-event-types) documents the `ready_for_review` and `convert_to_draft` names and their `created_at` field. Deployment and incident systems own accepted revisions, hotfixes, and incident links. Manually extract one fixed cohort, preserve the mapping from task IDs to PRs, deployments, and incidents, and then decide whether automation is worth its cost.

## Further reading

- [DORA software delivery performance metrics](https://dora.dev/guides/dora-metrics/)
- [The SPACE of Developer Productivity](https://www.microsoft.com/en-us/research/publication/the-space-of-developer-productivity-theres-more-to-it-than-you-think/)
- [Accepting an Agent Change, from Intent to Evidence](ai-change-control-loop_en.md)
