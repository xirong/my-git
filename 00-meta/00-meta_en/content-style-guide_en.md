# Content Style Guide

English | [中文](../content-style-guide.md)

This document governs all subsequent new articles to prevent the repository content from remaining a mere collection of links.

## Questions Each Article Must Answer

1. What practical problem does this solve?
2. In what situations should it be used?
3. In what situations should it be avoided?
4. What is the safe practice?
5. What are the high-risk operations?
6. What is the underlying mental model?

## Recommended Structure

```text
# Title

## Problem

## Suitable Scenarios

## Recommended Practices

## Commands

## Examples

## Common Errors

## Further Reading
```

## Writing Principles

- Organize content with engineering judgment; do not just pile up resource links.
- Explain the scenario first, then provide the commands.
- When involving operations like `reset --hard`, `push --force`, or history rewriting, risks must be clearly stated.
- When involving team collaboration, a distinction must be made between "local uncommitted," "committed but not pushed," "pushed," and "already used by others for development."
- When involving GitHub features, prioritize referencing official documentation.
- Do not package a specific workflow as a "standard answer" applicable to all teams.
- Legacy materials can be retained but must be marked with their timeliness/relevance.

## Template Writing

### Incident Handling

```md
## Scenario: I did a certain operation incorrectly

### Symptoms

### Initial Checks

### Safe Handling

### High-Risk Handling

### What to Avoid

### Why It Works
```

### Team Processes

```md
## Problem

## Suitable Teams

## Unsuitable Scenarios

## Process

## Team Rules

## Common Failure Modes
```

### AI Programming

```md
## New Risks

## Git Control Strategy

## Review Checklist

## Commit Strategy

## Rollback Strategy
```
