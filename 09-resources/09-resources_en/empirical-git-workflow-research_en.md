# Git Workflow Empirical Research Notes

English | [中文](../empirical-git-workflow-research.md)

Original links:

- [Do Small Code Changes Merge Faster? A Multi-Language Empirical Investigation](https://arxiv.org/abs/2203.05045)
- [The Impact of a Continuous Integration Service on the Delivery Time of Merged Pull Requests](https://arxiv.org/abs/2305.16365)

## 1. Do Small PRs Definitely Merge Faster?

Avoid framing it this way.

Public research shows there is no stable, simple relationship between change size and merge time.

This doesn't mean small PRs have no value. Their true, stable value lies in being:

- Easier to understand
- Easier to review
- Easier to troubleshoot
- Easier to revert
- Better suited for stacked reviews
- Better suited for manual splitting of AI-generated code

Therefore, when the handbook recommends small PRs, the reasoning should focus on reviewability and revertability, rather than mechanically promising a definite increase in throughput speed.

## 2. Does CI Definitely Make Delivery Faster?

Avoid framing it this way either.

The value of CI is not only reflected in delivery time, but more importantly in:

- Improving the quality of merge decisions
- Increasing author and reviewer confidence in changes
- Discovering compilation, testing, formatting, and security issues early
- Providing an automated foundation for main branch stability

When CI becomes slow or unstable, it can even slow down the team's pace.

## 3. How to Express This When Writing

Write it like this instead:

- Small PRs improve understandability, reviewability, and revertability
- CI improves merge decision quality and developer confidence
- Merge Queue protects the combined results of the main branch
- CODEOWNERS lets people who truly understand the code participate in review
- Rulesets solidify organization-level rules into the platform

Avoid writing like this:

- Small PRs definitely merge faster
- Adopting CI definitely speeds up releases
- Fewer branches mean a more efficient team
- Turning on more tools means more mature governance

## 4. Inspiration for AI Programming

After AI generates code, small PRs and small commits become even more important, but the reasons remain reviewability, verifiability, and revertability.

Do not mistake AI generation speed for merge speed. Merge speed depends on:

- Whether the diff is understandable
- Whether the tests are trustworthy
- Whether CI is stable
- Whether the owner can quickly assess risks
- Whether reverting is simple
