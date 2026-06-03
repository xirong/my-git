# Legacy Content Migration Checklist

English | [中文](../legacy-content-migration.md)

This checklist is used to track how legacy articles are integrated into the new learning paths.

Principles:

1. Content with long-term value is moved to new directories.
2. Content that still has reference value but is less timely is placed in the resource index.
3. Practices that are no longer recommended are placed in the archive with explanatory notes.
4. When entry points are kept in the root directory, they must point to more complete new articles.
5. During migration, prioritize adding scenarios, risks, recommended practices, and further reading.

## Root Directory Articles

| Legacy File | New Location | Status | Action Suggestion |
| --- | --- | --- | --- |
| `why-git.md` | `01-getting-started/why-git.md` | Migrated | README should prioritize the new directory |
| `useful-git-command.md` | `02-daily-workflow/everyday-git-commands.md` | Migrated | Add common scenarios and risk warnings later |
| `git-workflow-tutorial.md` | `03-team-collaboration/` | Partially Migrated | Split into GitHub Flow, Gitflow, Trunk-Based Development, and Team Workflow Guide |
| `how-to-use-github.md` | `04-github-engineering/` | Partially Migrated | Split into GitHub Engineering Governance, Branch Protection, Rulesets, Actions, and Release |
| `use-gitlab-github-together.md` | `03-team-collaboration/gitlab-flow.md`, `09-resources/` | Pending Evaluation | Retain GitLab / GitHub hybrid experience, add timeliness notes |
| `using-svn.md` | `01-getting-started/git-vs-svn.md`, `09-resources/deprecated-resources.md` | Pending Evaluation | Keep as historical migration reference, not as a main learning path |
| `ixirong.com.md` | `09-resources/resources-index.md` | Pending Evaluation | Retain only relevant project resource entries |

## Chinese Directory (`zh/`)

| Legacy File | Status | Action Suggestion |
| --- | --- | --- |
| `zh/readme.md` | Pending Evaluation | Retain historical entry point; redefine relationship with the main README later |
| `zh/why-git.md` | Pending Evaluation | Align with `01-getting-started/why-git.md` |
| `zh/useful-git-command.md` | Pending Evaluation | Align with `02-daily-workflow/everyday-git-commands.md` |
| `zh/git-workflow-tutorial.md` | Pending Evaluation | Split into the Team Collaboration directory |
| `zh/how-to-use-github.md` | Pending Evaluation | Split into the GitHub Engineering directory |

## Resource Content

| Content | New Location | Status | Action Suggestion |
| --- | --- | --- | --- |
| Books | `09-resources/books.md` | Entry Created | Regularly check link validity |
| Tools | `09-resources/tools.md` | Entry Created | Annotate recommended scenarios and maintenance status |
| Visual Learning | `09-resources/visual-learning.md` | Entry Created | Retain materials suitable for beginners |
| Company Practices | `10-company-practices/` | Independent Level-1 Directory | Each case should link back to the corresponding topic article |
| Deprecated Resources | `09-resources/deprecated-resources.md` | Entry Created | Annotate why they are not recommended as the main path |

## Next Steps

1. Add pointers from root directory legacy articles to new articles.
2. Split valuable content from `git-workflow-tutorial.md` into `03-team-collaboration/`.
3. Split valuable content from `how-to-use-github.md` into `04-github-engineering/`.
4. Check if legacy articles under `zh/` need to be retained, merged, or archived.
5. Clean up links in README that still point to legacy entry points.
