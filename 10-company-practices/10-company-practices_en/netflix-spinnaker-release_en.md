# Netflix Spinnaker and Release Pipeline Practice

English | [中文](../netflix-spinnaker-release.md)

Original links:

- [Netflix's New Spinnaker Open Source Tool Makes It Easy to Use Amazon's Cloud-And Google's](https://www.wired.com/2015/11/netflixs-new-tool-makes-it-easy-to-use-amazons-cloud-and-googles)
- [Spinnaker](https://spinnaker.io/)

## 1. Why This Case Still Has Value

Some public company materials focus more on release controls, with branching models merely acting as supporting information.

This illustrates a real problem: for many teams, the true risk is not "how many branches to use," but "how to safely release code after it is merged."

The value of continuous delivery platforms like Spinnaker lies in breaking the release process into an observable, approvable, and rollback-capable pipeline.

## 2. Relationship with Git Workflow

Git is responsible for recording the facts of changes:

- commit
- PR
- tag
- release note
- changelog

The release platform is responsible for controlling the delivery process:

- Build
- Deployment
- Advancement across environments
- Manual approval gates
- Rollback
- Release status tracking

The two must be traceable to each other. Production versions should be able to link back to Git commits, tags, PRs, and release tickets.

## 3. Inspiration for Teams

If a team already has relatively mature PRs and CI, the next step shouldn't just be adding more branch rules, but adding release governance:

- Every release is associated with a commit or tag
- Every release has a release note
- Clear checkpoints exist before production release
- High-risk releases require manual approval gates
- Rollback commands and rollback owners are explicit
- Post-release validation results are written back into the release record

## 4. Suitable Scenarios

Suitable for:

- Multi-environment deployments
- Multi-cloud or multi-cluster deployments
- High release risks
- Strict rollback requirements
- Need for release auditing

Not suitable for:

- Small documentation repositories
- Teams without automated build and deployment foundations
- Processes still stuck on manually copying files for release

## 5. Key Takeaways

Git workflow articles cannot just stop before the merge.

A complete enterprise collaboration pipeline should cover:

```text
branch -> PR -> CI -> merge -> tag -> release -> deploy -> verify -> rollback
```
