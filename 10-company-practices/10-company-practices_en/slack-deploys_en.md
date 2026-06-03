# Slack Deploys Practice

English | [中文](../slack-deploys.md)

Original links:

- [Deploys at Slack](https://slack.engineering/deploys-at-slack/)

Slack's deployment practice is an excellent addition to "what happens after merge."

Many Git tutorials end when the PR is merged, but the true risks of enterprise collaboration pipelines often lie in the release phase.

## Critical Pipeline

Slack's release practice can be abstracted as:

```text
PR
-> review
-> tests
-> merge
-> release branch
-> staging
-> dogfood
-> canary
-> percentage rollout
-> rollback / hotfix
```

Different teams use different tools, but the core goal is the same: releases must be controllable, observable, and rollback-capable.

## Relationship Between Git and Releases

Git is responsible for recording the facts of changes:

- commit
- PR
- tag
- release branch
- changelog

The release system is responsible for controlling changes entering the user environment:

- staging validation
- canary rollouts
- monitoring
- rollback
- hotfix

These two systems must be mutually traceable.

## Rules Suitable for Team Conventions

- Every release version has an explicit commit or tag
- Must know which PRs are included in this release before deploying
- Discrepancies between staging and production environments must be explainable
- Can quickly halt when a canary rollout fails
- Rollback paths are clearly written out in advance
- Hotfixes must be synchronized back to the mainline after completion

## Key Takeaways

Release Management cannot just cover GitHub Releases and tags.

It also needs to cover validation, canary rollouts, rollbacks, hotfixes, and release records during the release process.
