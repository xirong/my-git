# Contributing

English | [中文贡献说明](00-meta/contributing.md)

Thank you for helping improve My Git Handbook.

This project is a practical Git/GitHub handbook for modern engineering teams and AI-native development workflows. Contributions are most valuable when they solve real problems for developers, team leads, maintainers, or AI coding users.

## What to Contribute

Good contributions include:

- Broken link fixes
- Typo and wording fixes
- Clearer Git command examples
- Troubleshooting cases from real development work
- Team workflow practices
- GitHub governance examples
- AI coding and code review workflows
- Reusable templates for PRs, reviews, releases, and hotfixes

Please avoid adding link lists without context. A useful guide should explain when to use a practice, when to avoid it, what risks exist, and how to verify the result.

## Contribution Workflow

1. Open an issue for larger changes.
2. Fork the repository.
3. Create a focused branch.
4. Keep each pull request limited to one topic.
5. Run the documentation checks before submitting.
6. Open a pull request with a clear summary and validation notes.

```bash
python3 scripts/check-docs.py
git diff --check
```

## Writing Guidelines

- Prefer practical judgment over abstract theory.
- Explain the problem before listing commands.
- Mark risky Git operations clearly.
- Include safe checks before destructive commands.
- Link to official documentation when describing Git or GitHub behavior.
- Keep examples copyable and easy to adapt.
- Keep bilingual navigation intact when editing translated files.

## Pull Request Checklist

- [ ] The change is focused and reviewable.
- [ ] Local Markdown links still work.
- [ ] Dangerous commands include context and warnings.
- [ ] New content is placed in the right section.
- [ ] Related English or Chinese files are updated when needed.
- [ ] `python3 scripts/check-docs.py` passes.
- [ ] `git diff --check` passes.

## Issue Types

Useful issues include:

- Broken links
- Outdated Git/GitHub behavior
- Missing workflow cases
- Unclear commands
- Translation quality problems
- New company practice references
- Template improvement requests

If you are unsure where a topic belongs, open an issue first.
