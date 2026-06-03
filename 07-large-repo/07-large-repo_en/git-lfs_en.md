# Git LFS

English | [中文](../git-lfs.md)

Git LFS is used to manage large files.

Git itself is well-suited for managing text and small files. If large binary files frequently enter regular Git history, they will make the repository increasingly slow and raise the costs of clone, fetch, and diff operations.

## Suitable Scenarios

- Images
- Audio and video
- Design assets
- Model files
- Large binary files that must follow versioning

## Content Unsuitable for Committing to Git

- Logs
- Temporary files
- Build artifacts
- Database dumps
- Local caches
- Regeneratable intermediate files

These contents should ideally be placed in object storage, artifact repositories, or CI caches.

## Basic Usage

Enable after installation:

```bash
git lfs install
```

Track a specific type of file:

```bash
git lfs track "*.psd"
git add .gitattributes
git add design.psd
git commit -m "chore(lfs): track design assets"
```

## Team Rules

- First, define which files must use LFS
- Commit `.gitattributes` into the repository
- Do not put generated artifacts into LFS
- Verify that Git LFS is installed in the CI environment
- Regularly check for large files mistakenly committed to regular Git history

## What to do if large files were already mistakenly committed

History needs to be cleaned up, typically using `git filter-repo` or BFG Repo-Cleaner.

Cleaning up history affects collaborators; the team must be notified in advance.

## Further Reading

- [Git LFS Official Site](https://git-lfs.com)
- [GitHub Docs: About Git Large File Storage](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage)
- [Large Repository Git Practices](large-repo-git-practices_en.md)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
