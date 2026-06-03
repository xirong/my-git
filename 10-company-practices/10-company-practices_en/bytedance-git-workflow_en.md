# ByteDance Git Workflow and R&D Infrastructure Practice

English | [中文](../bytedance-git-workflow.md)

Original links:

- [Git Workflow under ByteDance's R&D Infrastructure](https://www.infoq.cn/article/9dotsvlwscznbxjpxfqe)

## 1. The Value of This Practice

The Git workflow of a large team is often not purely an issue of the branching model.

As the scale of R&D grows, the real challenge is to connect these things together:

- Permission management
- Code review
- CI checks
- Merge strategies
- Release processes
- Multi-repository collaboration
- R&D platform experience

The focus of infrastructure practices like ByteDance's is that the Git process needs to be supported by a platform. What developers see daily are MRs, checks, permissions, and release tickets, with branches and repositories lying underneath.

## 2. Typical Pain Points for Large-Scale R&D Teams

### Branch conventions rely on word of mouth

When a team is small, everyone can collaborate by just mentioning it in a chat group.

When the team grows, without platform rules, branch naming, review requirements, merge methods, and release processes will gradually fragment.

### High cost of multi-repository collaboration

A single requirement might simultaneously modify the client, backend, platform tools, and configuration repositories.

If each repository has different rules, cross-repository debugging and releasing become uncontrollable.

### Review and CI easily become superficial

As long as the merge button can be clicked on a PR / MR, teams will lean towards rapid integration.

If CI results, code ownership, and risk warnings do not enter the merge path, Code Review can easily become nothing more than a rubber-stamp approval.

## 3. Transferable Practices

### Productize the Git workflow

Team conventions should not just stay in documents; they should be turned into platform actions as much as possible:

- Automatically include requirement or task information when creating branches
- Automatically bring up the scope of changes when creating an MR
- Automatically request reviewers based on directories or modules
- Automatically run basic checks before merging
- The release system can trace back to commits, tags, and MRs

### Express organizational boundaries with permissions

Large teams need to distinguish:

- Who can push directly
- Who can approve
- Who can merge
- Who can release
- Who can bypass rules

These permissions should ideally be bound to code ownership, service owners, and on-call roles.

### Let check results inform merge decisions

CI, lint, unit tests, security scans, package size, and compatibility checks should not just be for "taking a quick look."

They must become explicit gatekeeping rules before merging, and when they fail, it should be possible to pinpoint the person responsible.

### Establish shared context for cross-repository requirements

Cross-repository changes should at least have a unified requirement ID, release ticket, or change ticket to link multiple MRs together.

In this way, during review, testing, release, and rollback, it is clear that these changes belong to the same initiative.

## 4. Guidance for Tech Leads

When a team exceeds dozens of people, the success or failure of the Git workflow mainly depends on three things:

1. Whether the branch strategy matches the release strategy
2. Whether permissions and code ownership can be mapped down to directories, modules, and services
3. Whether CI and the release system can trace commits back to production versions

Just saying "we use Gitflow" or "we use trunk-based development" is not enough.

## 5. Key Takeaways

Practices like ByteDance's are suitable to be placed in the team collaboration and GitHub engineering governance chapters, acting as a reminder:

- The branching model is just the entry point
- True engineering capability comes from rules, platforms, and automation
- Multi-repository teams must first unify collaboration metadata
- Code review, CI, release, and rollback must form a closed loop
