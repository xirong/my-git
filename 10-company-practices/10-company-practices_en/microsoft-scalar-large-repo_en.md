# Microsoft Scalar and Large Repository Git Practice

English | [中文](../microsoft-scalar-large-repo.md)

Original links:

- [The Story of Scalar](https://github.blog/open-source/git/the-story-of-scalar/)
- [The largest Git repo on the planet](https://devblogs.microsoft.com/bharry/the-largest-git-repo-on-the-planet/)
- [Get up to speed with partial clone and shallow clone](https://github.blog/open-source/git/get-up-to-speed-with-partial-clone-and-shallow-clone/)
- [Git partial clone documentation](https://git-scm.com/docs/partial-clone)
- [Git sparse-checkout documentation](https://git-scm.com/docs/git-sparse-checkout)

## 1. The Real Problems of Large Repositories

As a repository grows larger, what developers notice first is typically:

- clone is too slow
- fetch is too slow
- checkout is too slow
- `git status` is too slow
- Too many files in the working directory
- Historical objects and large files slow down local operations

The story of Microsoft Scalar illustrates that optimizing large repositories cannot rely solely on "getting a faster computer"; it requires combining multiple Git capabilities.

## 2. The Windows Repository Case

Microsoft publicly shared the extreme scale of the Windows team after migrating to Git: millions of files, a repository in the hundreds of gigabytes, thousands of engineers, and a massive daily volume of PRs, builds, and Reviews.

The inspiration from this case is that enterprise-level Git problems often do not lie in Git's version control semantics, but in the costs of these foundational operations:

- clone
- fetch
- checkout
- status
- Build systems reading the working directory
- Automation systems repeatedly pulling the repository

Therefore, Microsoft's evolutionary path from VFS for Git to Scalar centers on keeping Git usable under massive repositories.

## 3. Core Ideas of Scalar

Scalar combines multiple configurations suitable for large repositories:

- partial clone, reducing the download of historical objects
- sparse checkout, checking out only the currently needed directories
- background maintenance, preserving repository performance in the background
- File system monitoring, reducing the cost of status scanning
- Default configurations tuned for large repositories

For regular teams, the focus is to understand why these capabilities need to be used together, without necessarily requiring everyone to use Scalar right away.

## 4. Partial clone

Partial clone is useful for reducing the data downloaded during the initial clone and subsequent fetches.

Common approach:

```bash
git clone --filter=blob:none <url>
```

This kind of blobless clone downloads commits and trees first, downloading blob content on demand when needed.

Suitable for:

- Developers using large repositories daily
- Massive amount of file content in history
- Need to retain normal historical operation capabilities

Note:

- Accessing historical file content for the first time will trigger additional downloads
- The server must support partial clone
- Team documentation is needed to explain which commands might trigger on-demand downloads

## 5. Shallow clone

Shallow clone pulls only a portion of the commit history:

```bash
git clone --depth 1 <url>
```

Suitable for:

- One-off CI builds
- Temporary inspections
- Automated tasks that do not require history analysis

Not suitable for:

- Long-term developer workspaces
- Scenarios requiring `git blame`, complex merge-bases, or history tracing
- Workspaces that require long-term fetching subsequently

## 6. Sparse checkout

Sparse checkout keeps only a portion of the directories in the working area:

```bash
git sparse-checkout init --cone
git sparse-checkout set service-a service-b
```

Suitable for:

- Being responsible for only a few services in a Monorepo
- Build systems that can explicitly specify which paths are dependencies
- The number of files in the workspace already impacts IDE and Git performance

In Microsoft Scalar's experience, cone mode sparse checkout is a critical optimization direction, because selecting by directory yields more stable performance than arbitrary patterns.

## 7. Adoption Sequence for Large Repository Teams

Recommended sequence:

1. Identify where the repository is slow first; look at clone, fetch, status, and checkout separately
2. CI uses shallow clone or treeless/blobless clone for targeted optimization
3. Developer workspaces prioritize trying blobless partial clone
4. Enable sparse checkout in Monorepos, defining directory sets by team or service
5. Enable repository maintenance capabilities, such as `git maintenance`
6. Clean up large files and generated artifacts that shouldn't enter Git

## 8. Key Takeaways

Large repository optimization must avoid single-point thinking:

- partial clone solves object downloads
- sparse checkout solves workspace scale
- maintenance solves local repository maintenance
- LFS solves large binary files
- CODEOWNERS solves path responsibilities
- CI caching and build systems solve build costs

These capabilities need to be combined to form truly actionable large repository practices.
