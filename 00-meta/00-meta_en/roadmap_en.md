# Roadmap

English | [中文](../roadmap.md)

## Current delivery: understanding, experiments, and change control

The handbook explains its purpose through the [philosophy](../../01-getting-started/01-getting-started_en/why-learn-git_en.md) and connects paired Chinese and English articles, interactives, and temporary-repository labs for ten topics through the [learning path](../../01-getting-started/01-getting-started_en/git-learning-path_en.md). Existing directories remain a reference index; folder numbers do not dictate reading order.

### Merged material

- [x] Add the [knowledge map](../../01-getting-started/01-getting-started_en/knowledge-map_en.md), organized as “understand the design → complete an engineering change → manage collaboration,” with prerequisites, problem entry points, and the next decision.
- [x] Clarify that [tool integration practices](../../05-ai-native-development/05-ai-native-development_en/ai-coding-tools-git-integration_en.md) own tool facts and sources, while [Codex / Claude Code Git Practices](../../05-ai-native-development/05-ai-native-development_en/codex-claude-code-git-practices_en.md) own stable Git workflow across tools.
- [x] Add the [engineering change course](../../05-ai-native-development/05-ai-native-development_en/engineering-change-course_en.md), [CI for AI-generated changes](../../05-ai-native-development/05-ai-native-development_en/ci-for-ai-generated-changes_en.md), [background agent tasks](../../05-ai-native-development/05-ai-native-development_en/background-agent-workflow_en.md), and [AI agent incident recovery](../../06-troubleshooting/06-troubleshooting_en/ai-agent-incident-recovery_en.md) for the acceptance chain, checked revision, asynchronous handoff, and incident scene.
- [x] Add [two AI Agent engineering cases](../../10-company-practices/10-company-practices_en/ai-native-engineering-cases_en.md), separating first-party public reports from local-pilot decisions.

These materials were merged through [PR #67](https://github.com/xirong/my-git/pull/67), with documentation and link CI passing. On 2026-09-08, the GitHub Pages build was verified at `7fcc238fad2e3aaca0f0d2196d62951833951fbb`; the hosted interactive script matched that revision, and the knowledge map, engineering-change course, and sampled course entry points were accessible. This does not establish deployment of later local fixes or reader learning.

### Closeout and remaining work

- [x] Locally fix the missing recovery-ref creation and storage output snapshots. `node scripts/test-curriculum-commands.mjs` executes all four displayed command paths and independently checks object state and snapshot content. Targeted checks against the old source catch the original missing-ref and missing-snapshot errors.
- [ ] Submit and merge these fixes, then verify the actual Pages revision; the hosted check above still refers to PR #67.
- [ ] Run a real-reader session using the tasks below.
- [ ] Add AI tool, task-scope, and human-verified file fields to the reusable PR template, and AI provenance guidance to the commit convention. Repository contribution rules do not replace reusable templates.
- [ ] Evaluate an AI collaboration metrics article and specific Agent scenario gaps in chapter 04; defer additional articles until reader feedback.
- [ ] Create public roadmap issues only when requested; choose a version and release notes if a versioned release is wanted. This merge record does not establish a tag or GitHub Release.

The historical assessment's governance, AGENTS.md template, repository conventions, multi-agent and stacked PR operations, incident recovery, CI, background tasks, engineering cases, and tool-article responsibilities are covered. Preserve the original assessment; use these concrete gaps for new work.

### Real-reader acceptance tasks

Invite an engineer who did not author the course to start from the [knowledge map](../../01-getting-started/01-getting-started_en/knowledge-map_en.md). The facilitator records predictions, actual actions, the number of hints, and stumbling points without explaining answers first. Run Git commands only in the disposable repositories created by the course labs.

1. In recovery, predict what happens to C2 and C3 after reflog expiration and cleanup, then run the lab and explain the difference with ref and object checks.
2. In storage, compare content before and after maintenance, explain what unchanged content establishes, and why it does not establish a performance improvement.
3. Transfer the model to an Agent scenario involving committed files, unstaged edits, and an external database. Explain which evidence to preserve, what Git can recover, and what needs separate handling.
4. Navigate from article to interactive and lab, then switch language; record broken links, terminology obstacles, and points needing help.

Record each task as “independent / completed with hints / incomplete,” with differences between prediction and observation. One session establishes only that participant's behavior on that revision. No participant is scheduled yet; automated checks and Agent-simulated reading do not count as a passing reader session.

### Material and evidence boundaries

| Code and material visible | Scope covered | Evidence still needed separately |
| --- | --- | --- |
| Ten paired conceptual articles, ten labs, and ten interactive entry points are linked in one order from 01 through 10 | Snapshots, objects, index, refs, recovery, merge, rebase, remotes, worktrees, and storage | There is no behavior data establishing whether readers can predict, reproduce, and transfer the ideas |
| The interactive entry keeps the three existing topics for 01 through 03 and adds seven topics for 04 through 10 | Every topic can lead from article to interactive and lab; deployment of the merged revision above was verified | Browser behavior across all paths, deployment of later fixes, and real reader experience need separate verification |
| The [engineering change course](../../05-ai-native-development/05-ai-native-development_en/engineering-change-course_en.md) and [acceptance loop](../../05-ai-native-development/05-ai-native-development_en/ai-change-control-loop_en.md) have a local artifact and HTTP-service exercise | Intent, candidate commit, clean-checkout test, artifact, loopback runtime response, and code recovery are observable under a temporary root | It does not contact real CI, a hosting platform, production, or an external service, and does not establish supply-chain trust |
| The [command-safety regression](../../labs/git-command-safety/README.md) rechecks four named old command patterns | Stop on a dirty workspace, commit owned paths, reset before partial staging after a soft reset, and substitute the integration branch | Other historical examples, remote authorization, branch protection, hooks, and team rules are outside this regression |
| `bash scripts/run-git-learning-labs.sh` runs ten course labs, three reading experiments, and three Agent/command regression entry points in sequence | Scripted local Git scenarios, including Agent incident recovery, can be rechecked | Passing runs do not establish reader learning, performance benchmarks, or production state |

### Course order and verification

1. **01 through 03: snapshots, objects, and index.** First observe how an edit appears separately in HEAD, the index, and the working tree; then follow the object graph and the next-commit draft.
2. **04 through 05: references and recovery.** Branches, tags, and HEAD precede reachability, reflogs, and GC retention limits.
3. **06 through 09: history and collaboration.** Three-way merge, rebase replay, remote-tracking refs, and worktrees explain divergence, integration, and isolation in order.
4. **10: storage and maintenance.** After the object model, distinguish logical snapshots, packs, GC, and commit-graph. The lab observes only a controlled temporary repository; performance conclusions require separate measurement.
5. **Agent-change acceptance.** The local artifact-and-service exercise connects commit, test, and runtime evidence while preserving the boundary that Git cannot automatically reverse external state.

### Teaching contract

Each chapter needs a causal question, a stable diagram, one adjustable condition, a temporary-repository lab, expected output, a misconception and recovery boundary, and an agent-oriented judgment exercise. Motion must explain change. Identify whether timing, counters, and hashes are real or illustrative.

Learning is demonstrated through prediction, reproduction, and transfer. Enjoying an animation is useful feedback, but cannot alone establish mastery.

### Boundaries to maintain

- Git does not capture all engineering state: ignored files, secrets, LFS objects, submodules, databases, dependencies, and environments require separate treatment.
- Content hashes, signatures, CI results, and business correctness provide different evidence.
- Agent concurrency can shift bottlenecks to integration and review capacity.
- Maintain diagram assumptions, keyboard access, reduced motion, and no-JavaScript reading.
- Date and source tool integration guidance separately from stable principles.

The goal of v2.0 is to bridge the gap in practical content for modern engineering teams regarding Git / GitHub collaboration, AI programming, incident handling, and engineering governance.

## v2.0 Goals

v2.0 aims to accomplish one primary task: establish a clear content structure and complete the first batch of core articles and templates that are ready for immediate use.

## Phase 1: 30-Day Version

### Week 1: Positioning Upgrade

- [x] Update README
- [x] Add main entry point descriptions
- [x] Establish new directory structure
- [x] Add Content Style Guide
- [x] Add GitHub Issue / PR templates
- [x] Organize legacy content migration checklist

### Week 2: AI Differentiation

- [x] Add `ai-native-git-workflow.md`
- [x] Add `ai-generated-code-review.md`
- [x] Add `codex-claude-code-git-practices.md`
- [x] Add AI Code Review template
- [x] Add `worktree-for-ai-agents.md`
- [x] Add `ai-commit-splitting.md`
- [x] Add `multi-agent-branch-strategy.md`

### Week 3: Team Engineering Practices

- [x] Add `team-git-workflow-guide.md`
- [x] Add `github-engineering-governance.md`
- [x] Add PR and Review templates
- [x] Add full version of `branch-protection.md`
- [x] Add `release-management.md`
- [x] Add `codeowners.md`

### Week 4: Incident Playbook and Release

- [x] Add `git-troubleshooting-playbook.md`
- [x] Add `undo-anything.md`
- [x] Add `recover-lost-commit.md`
- [x] Add `remove-secret-from-history.md`
- [x] Repository-wide link validation
- [x] The `v2.0.0` release notes file is present in the repository

## Content Principles

1. Fewer link piles, more engineering judgment.
2. Fewer command lists, more scenario explanations.
3. Less pursuit of exhaustive completeness, more actionable paths.
4. Every article must answer "When to use this, and when not to."

## v2.0 Release Narrative

AI programming is changing the way software is developed, and the value of Git is evolving accordingly.

v2.0 will systematically add practical Git / GitHub content around team collaboration, GitHub engineering governance, AI code review, incident recovery, and large repository practices.

## Recent Optimization Checklist

- [x] README: Add "Find answers by problem"
- [x] Add practical AI change review examples
- [x] Add legacy content migration checklist
- [x] Complete the decision table for `07-large-repo/`
- [x] Verify that the `v2.0.0` release notes file exists
