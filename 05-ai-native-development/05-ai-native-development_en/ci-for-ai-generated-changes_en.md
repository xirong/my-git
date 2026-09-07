# CI for AI-Generated Changes: Make Every Check Name the Tested Revision

English | [中文](../ci-for-ai-generated-changes.md) | [Agent Incident Recovery](../../06-troubleshooting/06-troubleshooting_en/ai-agent-incident-recovery_en.md)

AI lowers the cost of generating code and makes it easier for one pull request to include behavior, dependency, configuration, and workflow changes together. CI should turn those risks into executable checks and make every result answer: which SHA was checked, in what environment, and what remains unproven.

This article describes check design only. It does not enable this repository's GitHub Actions, secret scanning, dependency review, or branch rules. GitHub capabilities and plan prerequisites were checked against official documentation on **2026-09-07**. The target repository's plan, Actions settings, rulesets, required checks, and run evidence still need confirmation in that repository.

## Start with an auditable evidence chain

The smallest useful chain is:

```text
task intent → candidate SHA → clean checkout → change-type checks → project tests → integration-SHA checks → merge decision
```

Each link answers a different question:

| Risk | Executable check | Evidence to retain |
| --- | --- | --- |
| a working-tree test consumed an uncommitted repair | check out the candidate SHA in a clean environment, then run tests | candidate SHA, actual `git rev-parse HEAD`, test output |
| AI expanded behavior | choose unit, contract, integration, or migration tests from changed paths | paths, scenarios, passes, and uncovered areas |
| a `.env`, token, or private key entered the change | platform secret scanning, reviewed organization scanning policy, and human review | whether scanning is available and alert handling; never the secret text |
| manifest or lockfile changes were missed | dependency diff, license and vulnerability review, project build test | direct and transitive changes, approval reason, build result |
| a green PR fails with the newest base branch | rerun needed checks on the PR merge result or merge-queue SHA | integration SHA, event, check name, result |
| an untrusted PR obtains credentials or write access | least-privilege token, secret-free untrusted-code job, isolated privileged work | workflow permissions, trigger, and whether fork head runs |

[Accepting an Agent Change, from Intent to Evidence](ai-change-control-loop_en.md) establishes locally which commit a test result belongs to. CI carries that same decision into a repeatable clean environment. [AI Change Review Example](ai-change-review-example_en.md) examines diffs and business boundaries; the two practices support each other.

## Candidate SHA and clean checkout

For `pull_request`, GitHub sets `GITHUB_SHA` to the last merge commit on the PR merge branch. GitHub's documentation directs workflows that need the PR head to use `github.event.pull_request.head.sha`. Decide which object is being checked:

- **Candidate check**: check out `github.event.pull_request.head.sha` to answer whether the agent's commits pass on their own.
- **Integration check**: use the PR merge ref or merge-queue SHA to answer whether the change passes with the newest target branch.

Do not describe both results as simply “the PR was tested.” This minimal workflow skeleton is for instruction. Replace `<official-full-commit-SHA>` and the project-test steps before enabling it: choose a stable release in the action's official repository, verify the full commit SHA, repository owner, and release notes, then use that full SHA in `uses`. GitHub's security guidance identifies a full SHA as the immutable action reference.

```yaml
name: AI change evidence

on:
  pull_request:
    types: [opened, synchronize, reopened]
  merge_group:
    types: [checks_requested]

permissions:
  contents: read

jobs:
  agent-candidate:
    if: github.event_name == 'pull_request'
    name: ai-change-candidate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<official-full-commit-SHA>
        with:
          ref: ${{ github.event.pull_request.head.sha }}
          fetch-depth: 1
          persist-credentials: false
      - name: Record candidate SHA
        env:
          EXPECTED_SHA: ${{ github.event.pull_request.head.sha }}
        run: |
          actual_sha=$(git rev-parse HEAD)
          test "$actual_sha" = "$EXPECTED_SHA"
          printf 'candidate SHA: %s\n' "$actual_sha"
      - name: Replace with the project's focused tests before enabling
        run: |
          echo 'Replace this failing placeholder with the project test command.'
          echo 'Example selection: a changed API needs contract and negative-path tests.'
          exit 1

  integration:
    name: ai-change-integration
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<official-full-commit-SHA>
        with:
          fetch-depth: 1
          persist-credentials: false
      - name: Record tested integration SHA
        run: git rev-parse HEAD
      - name: Replace with integration tests before enabling
        run: |
          echo 'Replace this failing placeholder with an integration-appropriate command.'
          exit 1
```

The deliberately failing placeholder prevents a false-green workflow before a project test is selected. The `pull_request` job checks out the head SHA. The `integration` job uses the default merge ref for a PR and the `merge_group` SHA for a merge queue. GitHub documents that required Actions checks used with a merge queue must explicitly listen for `merge_group`, or the required check is not reported after enqueueing.

`permissions: contents: read` is an explicit low-permission setting in this example. It is not a claim about every repository's default token. GitHub allows enterprise, organization, and repository default workflow permissions, then lets a workflow or job use `permissions` to narrow or add access as needed. This example does not reference `secrets` or configure a privileged environment.

This is a configuration-parsing example and was not run in GitHub Actions. The local Git boundary is covered by the [Agent Change Control Lab](../../labs/ai-change-control/README.md) and the related incident-recovery lab. Actions triggers, platform scanning, and required-rule outcomes require target-repository run evidence.

## Choose business tests from the change

Generic `npm test` or `mvn test` cannot automatically cover the business contract an agent changed. Select tests from paths, callers, and data boundaries, then record the reason in the PR:

| Change category | Add at least | A green check does not establish |
| --- | --- | --- |
| API, error codes, serialization | contract tests, old-client or negative cases | every caller is compatible |
| authorization, identity, tenant scope | denial paths, cross-scope boundaries, audit fields | production permission configuration is correct |
| database or migration | empty-database upgrade, rollback feasibility, critical queries | production-data remediation completed |
| retry, queue, asynchronous task | idempotency, duplicate delivery, timeout, failure paths | external systems had no side effect |
| configuration, default, feature flag | default, override source, off path | every environment has the same final configuration |
| dependency or lockfile | build, affected tests, dependency review | runtime license and risk are accepted |

The project test entry must be a command that already fits the repository, such as a focused module test, contract suite, or migration rehearsal. Do not place tutorial commands unchanged into a production workflow. An exit code proves the scenarios it covered; remaining gaps belong in review material.

## Sensitive information and dependencies: confirm availability first

GitHub secret scanning searches the complete Git history on all repository branches for known hardcoded credential types and creates alerts for detected exposure. Per GitHub's [Secret scanning documentation](https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning), it is automatically free for public repositories. Organization-owned private and internal repositories need GitHub Secret Protection enabled on GitHub Team or GitHub Enterprise Cloud. User-owned repositories have separate constraints. No alert does not prove the repository has no secret, and it does not replace credential invalidation and rotation.

Organization custom patterns can cover organization-specific private-key, connection-string, or API-key forms. A security owner should maintain rules from actual credential formats, false-positive handling, and log-exposure risk. Do not use a tutorial regular expression as a production secret scanner, and do not place a real secret in CI samples.

Dependency review exposes direct and transitive manifest and lockfile changes, vulnerabilities, licenses, dependents, and release dates. Per GitHub's [Dependency review documentation](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review), the feature is available to public GitHub.com repositories and organization-owned GitHub Team repositories with GitHub Code Security enabled. The dependency review action is available to public repositories and private repositories with GitHub Code Security or GitHub Advanced Security. Confirm the dependency graph, supported ecosystem, and organization license before enabling it; this tutorial does not assume every plan can use it.

## Required-check names, sources, and merge queues

Before making a CI job required, identify its actual GitHub UI check name, source App, trigger event, and target branches. A protected branch can require checks or commit statuses. GitHub warns that the same job name across workflows creates ambiguous results that can block a pull request. Give every required job a stable, unique `name`, such as `ai-change-candidate` and `ai-change-integration`, then configure the target repository's branch protection or ruleset from the observed name.

The existing [Docs Check workflow](../../.github/workflows/docs-check.yml) in this repository uses the `docs-check` job ID. Whether it is a required check, its full UI check name, and its branch coverage must be confirmed from a current PR and repository settings; this article changes none of them.

A merge queue composes a PR with the newest target branch and preceding queued changes into a merge group. GitHub provides a distinct `merge_group` SHA. Required checks must run again on this SHA; a green PR-head result cannot replace it.

## Permissions and secrets for untrusted PRs

Treat a fork or unknown PR head as untrusted code. Jobs that run it need minimum `GITHUB_TOKEN` permissions and must not receive deployment, cloud, package-registry, or other long-lived secrets. The example's `contents: read` and `persist-credentials: false` are enforced source-reading boundaries in this YAML. Another project can need different permissions, but each one should be explicit in the workflow and reviewed.

Keep platform policy, repository settings, and the example separate. GitHub currently documents that a fork-triggered `pull_request` does not pass ordinary secrets to a runner and, when write tokens are not allowed, adjusts write permissions to read-only. Enterprise, organization, and repository settings can set default workflow permissions. Private-repository fork policies can also allow a write token, secrets and variables, and manual approval. Inspect the target repository's Actions settings. This example does not rely on those defaults: it explicitly sets `GITHUB_TOKEN` to `contents: read`, does not reference secrets, and does not run head code in a privileged job. Even under these restrictions, untrusted scripts can read files, caches, and environment made visible to their job and can affect its output.

`pull_request_target` runs in default-branch context and can serve limited labeling or commenting actions. A metadata-only job can receive only the write permission needed for its label or comment; that job must never check out or execute an untrusted PR head. GitHub warns that a privileged trigger combined with untrusted checkout permits cache poisoning, secret exposure, or expanded write access. Jobs that execute untrusted code must stay isolated from privileged metadata handling. Release, signing, and deployment also belong on a trusted integration SHA or an approval-controlled isolated flow. Self-hosted runners need a separate review of host, network, and residual data.

## Official basis and next step

- [GitHub Actions secure use reference](https://docs.github.com/en/actions/reference/security/secure-use): least privilege, full-SHA action pinning, and risks from `pull_request_target` with untrusted checkout.
- [Events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows): PR head SHA, merge ref, and `merge_group` trigger conditions.
- [Secret scanning](https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning): scan scope and availability for public, organization private, and user-owned repositories.
- [Dependency review](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review): dependency differences, the action, and plan prerequisites.
- [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches): required checks, name ambiguity, and merge-queue behavior.
- [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax): `permissions` calculation and the fork-PR write-token exception.
- [Managing GitHub Actions settings for a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository): private-repository fork settings for write tokens, secrets, and approval.

Map the table's checks to the repository's actual test entries, GitHub plan, and branch rules using stable job names and explicit candidate/integration SHAs. For recovery, use [Agent Incident Recovery](../../06-troubleshooting/06-troubleshooting_en/ai-agent-incident-recovery_en.md); the [engineering change course entry](engineering-change-course_en.md) organizes the course sequence.
