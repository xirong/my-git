# Shallow Clone

English | [中文](../shallow-clone.md)

Shallow clone only fetches partial history.

Use for CI, temporary checks, and quickly downloading repositories. Avoid using it when complete historical analysis is required.

## Basic Usage

Only pull the latest commit:

```bash
git clone --depth 1 <url>
```

Only pull shallow history for a specific branch:

```bash
git clone --depth 1 --branch main <url>
```

## Suitable Scenarios

- CI only needs the current version's source code
- Temporarily reviewing a project
- Reducing fetch time when building images
- Repository history is huge, but the current task does not require history

## Unsuitable Scenarios

- Need `git blame`
- Need `git bisect`
- Need to generate a complete changelog
- Need to analyze historical commits
- Need to switch between many historical branches or tags

## Converting to a Complete Repository

If full history is needed later:

```bash
git fetch --unshallow
```

## Differences from Partial Clone

Shallow clone reduces history depth.

Partial clone reduces object downloads.

They solve different problems and can be used in combination, but verify support from your Git version and hosting platform.

## Further Reading

- [git clone official documentation](https://git-scm.com/docs/git-clone)
- [Partial Clone](partial-clone_en.md)
- [Large Repository Git Practices](large-repo-git-practices_en.md)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
