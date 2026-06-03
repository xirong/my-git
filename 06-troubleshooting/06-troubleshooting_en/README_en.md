# Troubleshooting

English | [中文](../README.md)

This directory is used for handling high-frequency Git accidents. First, determine the state, then choose a recovery plan; do not copy dangerous commands right away.

## Answer Three Questions First

1. Has the code been committed?
2. Has the commit been pushed?
3. Has anyone continued development based on these commits?

The answers to these three questions determine whether you can rewrite history, whether you should use revert or reset, and whether you need to confirm with the team first.

## Choose a Plan Based on State

| Current State | Recommended Entry |
| --- | --- |
| Code not yet committed | [Undo Anything](undo-anything_en.md) |
| Committed, not yet pushed | [Git Troubleshooting Playbook](git-troubleshooting-playbook_en.md) |
| Pushed | [Git Troubleshooting Playbook](git-troubleshooting-playbook_en.md), [Revert Merge Commit](revert-merge-commit_en.md) |
| Used as a base for further development by others | [Git Troubleshooting Playbook](git-troubleshooting-playbook_en.md) |
| Secret has been committed | [Remove Secret from History](remove-secret-from-history_en.md) |
| Force push overwrote remote | [Recover Force Push](recover-force-push_en.md) |

## First Aid Entries

| Problem I'm Facing | Recommended Reading |
| --- | --- |
| Unsure how to recover | [Git Troubleshooting Playbook](git-troubleshooting-playbook_en.md) |
| Committed to the wrong branch | [Committed to Wrong Branch](committed-to-wrong-branch_en.md) |
| Want to undo an operation | [Undo Anything](undo-anything_en.md) |
| Cannot find a commit | [Recover Lost Commit](recover-lost-commit_en.md) |
| Force push overwrote remote | [Recover Force Push](recover-force-push_en.md) |
| Discovered an incorrect merge | [Revert Merge Commit](revert-merge-commit_en.md) |
| Conflict resolution is messed up | [Resolve Conflicts](resolve-conflicts_en.md) |
| Secret committed into history | [Remove Secret from History](remove-secret-from-history_en.md) |

## Handling Principles

- When unsure, start with `git status`, `git log --oneline -10`, `git reflog -10`
- Prioritize using `revert` on public branches
- Local unpushed errors are easier to clean up
- When secrets are involved, first revoke and rotate keys, then clean up history
- When collaborators are involved, first confirm if anyone is continuing development based on the old commits

## Related Content

- [Everyday Git Commands](../../02-daily-workflow/02-daily-workflow_en/everyday-git-commands_en.md)
- [AI Change Review Example](../../05-ai-native-development/05-ai-native-development_en/ai-change-review-example_en.md)
- [Hotfix Process](../../08-templates/08-templates_en/hotfix-process_en.md)
