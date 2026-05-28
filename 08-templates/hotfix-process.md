# Hotfix Process

## 什么时候使用 hotfix

只有当生产环境已经受影响，且修复不能等待常规发布流程时，才使用 hotfix。

## 步骤

1. Create hotfix branch from production tag
2. Apply minimal fix
3. Add test or verification note
4. Open emergency PR
5. Get required approval
6. Merge and release
7. Tag the release
8. Back-merge to main branch
9. Write postmortem note

## 规则

- Keep the diff small
- Do not include refactoring
- Do not mix unrelated changes
- Always document rollback plan
