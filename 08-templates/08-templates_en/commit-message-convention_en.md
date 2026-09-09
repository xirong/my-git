# Commit Message Convention

English | [中文](../commit-message-convention.md)

## Format

```text
<type>(<scope>): <subject>
```

## Types

- `feat`: new feature
- `fix`: bug fix
- `docs`: documentation
- `style`: formatting only
- `refactor`: code change without behavior change
- `test`: add or update tests
- `chore`: tooling or maintenance
- `perf`: performance improvement
- `ci`: CI/CD change

## Examples

```text
feat(auth): add GitHub OAuth login
fix(api): handle empty response correctly
docs(git): add troubleshooting guide
refactor(order): simplify pricing calculation
test(auth): cover expired token case
```

## Rules

- The subject should use the imperative mood or a clear action description
- A single commit should express only one intent
- Do not use vague titles like `update`, `misc`, or `wip` for final commits

## AI Collaboration and `Co-authored-by`

When a team requires AI tool participation to be recorded, leave one blank line after the commit body and add the team-approved attribution trailer:

```text
Co-authored-by: <name or approved tool identity> <email>
```

GitHub supports one or more `Co-authored-by` trailers for recording co-authors. Its required format and email guidance are in [GitHub Docs: Creating a commit with multiple authors](https://docs.github.com/en/pull-requests/how-tos/commit-changes/creating-a-commit-with-multiple-authors).

- Record the tool or model, participation scope, and affected files in the PR's AI collaboration record; do not infer these details from a trailer.
- A `Co-authored-by` trailer records declared commit authorship or tool-participation provenance. It does not state that a person reviewed every file or prove that the change is correct.
- Do not fabricate a real person's name or email, and do not promise that GitHub will recognize a tool identity as an account or co-author.
- Record files actually reviewed by a person and the review focus separately in the PR's Human Review section, and clearly state when review has not happened.
