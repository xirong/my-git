# Trunk-Based Development

English | [中文](../trunk-based-development.md)

Trunk-Based Development emphasizes short branches, fast merges, and continuous trunk stability.

It is suited for teams with strong engineering discipline, fast CI feedback, and mature release automation.

## Core Philosophy

Teams collaborate primarily around a single trunk branch, with very short lifecycles for development branches to avoid accumulating massive conflicts in long-lived branches.

Typical Process:

```text
short-lived branch -> main -> CI -> deploy
```

## Suitable Scenarios

- Fast and stable CI
- Good test coverage
- Team can tolerate frequent small changes
- Can use feature flags to control unfinished capabilities
- Server-side or Web products capable of high-frequency releases

## Core Rules

- Short branch lifecycles
- Merge into trunk as quickly as possible
- Trunk must be deployable at any time
- Break large features into small incremental steps
- Isolate unfinished capabilities with feature flags
- Prioritize reverting when issues occur

## Differences from Gitflow

Gitflow emphasizes multiple branch roles like `develop`, `release`, and `hotfix`, making it suitable for products with clear version release cadences.

Trunk-Based Development emphasizes trunk stability and frequent integration, making it suitable for service-oriented teams with high-frequency delivery.

## Common Failure Modes

### 1. CI is Too Slow

Trunk development relies on fast feedback.

If CI frequently queues for tens of minutes, the team will start bypassing the process.

### 2. No Feature Flags

When large features cannot be completed at once, feature flags are needed to isolate unfinished capabilities.

Otherwise, half-finished features will appear in the trunk.

### 3. Branches are Still Long-Lived

If feature branches persist for weeks, you have essentially drifted away from the core practices of trunk-based development.

## Enterprise Practice References

The core insight from [Google Trunk-Based Development and Version Control Practices](../../10-company-practices/10-company-practices_en/google-trunk-based-development_en.md) is that trunk development relies on a set of engineering capabilities: small changes, fast CI, code ownership, feature flags, and fast rollbacks.

When typical teams adopt it, don't just chase "fewer branches"; build these supporting capabilities first.

## Extended Reading

- [Trunk Based Development](https://trunkbaseddevelopment.com)
- [Feature Flags](https://trunkbaseddevelopment.com/feature-flags/)
- [Google Trunk-Based Development and Version Control Practices](../../10-company-practices/10-company-practices_en/google-trunk-based-development_en.md)
- [Team Git Workflow Guide](team-git-workflow-guide_en.md)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
