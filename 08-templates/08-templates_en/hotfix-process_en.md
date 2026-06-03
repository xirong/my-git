# Hotfix Process

English | [中文](../hotfix-process.md)

## When to Use Hotfix

Only use a hotfix when the production environment is already affected, and the fix cannot wait for the regular release process.

## Steps

1. Create hotfix branch from production tag
2. Apply minimal fix
3. Add test or verification note
4. Open emergency PR
5. Get required approval
6. Merge and release
7. Tag the release
8. Back-merge to main branch
9. Write postmortem note

## Rules

- Keep the diff small
- Do not include refactoring
- Do not mix unrelated changes
- Always document rollback plan
