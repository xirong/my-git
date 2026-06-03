# Uber GitFarm and Git as a Service Practice

English | [中文](../uber-gitfarm.md)

Original links:

- [GitFarm: Git as a Service for Large-Scale Monorepos](https://arxiv.org/abs/2604.11977)

## 1. Why Git Becomes an Infrastructure Problem

In massive monorepos, Git costs are not just incurred on developers' local machines.

A vast number of automated systems will also clone, fetch, checkout, and sync:

- CI
- Code search
- Build systems
- Static analysis
- Release systems
- Bulk change tools

When each of these systems maintains a complete local Git copy, cold start and synchronization costs become an infrastructure bottleneck.

## 2. Core Idea of GitFarm

GitFarm abstracts Git operations into remote services, allowing automation systems to request repository states and checkout results on demand, reducing the cost of full clones on every machine.

Its inspiration is: when a repository becomes large enough, Git is no longer just a developer tool; it becomes an underlying service that platform teams must operate.

## 3. What Inspiration Does This Have for Ordinary Teams

Most teams do not need to build their own GitFarm, but they can watch for these signals early on:

- CI cold starts are primarily consumed by clone and checkout
- Multiple automation systems repeatedly pull the same set of objects
- Monorepos pull the full history on every build
- Developers frequently complain that `status`, `fetch`, and `checkout` are slow
- Preparing workspaces on new machines takes over a dozen minutes or more

When these signals appear, don't rush to break up the repository; you can optimize in sequence:

1. CI uses shallow clone or partial clone
2. Developers use partial clone + sparse checkout
3. Large repositories enable `git maintenance`
4. Build systems determine the scope of impact based on paths
5. High-frequency automated tasks use caches or shared object pools
6. Then evaluate whether deeper platform-level solutions are needed

## 4. Reminders for Monorepo Decisions

The benefits of a Monorepo are unified dependencies, ease of cross-service changes, centralized code search, and governance.

The cost is an increase in toolchain complexity.

When teams make Monorepo decisions, they must evaluate simultaneously:

- Git performance
- Build performance
- CI concurrency
- Path ownership
- Release blast radius
- Repository access costs for automated systems

Merely discussing "one repository vs. multiple repositories" is insufficient.

## 5. Key Takeaways

Large repository practices should be written as a set of progressive strategies:

```text
clone optimization
-> workspace pruning
-> local maintenance
-> CI caching
-> path impact analysis
-> Git as a service
```

This way, readers can adopt them gradually according to their team size, avoiding blindly copying the solutions of mega-corporations right from the start.
