# Partial Clone

English | [中文](../partial-clone.md)

Partial clone is used to reduce the number of Git objects downloaded during a clone.

In large repositories, history and object volumes can be massive. Partial clone allows Git to fetch essential metadata first, and download objects like blobs on demand.

## Examples

```bash
git clone --filter=blob:none <url>
```

Common meanings:

- `--filter=blob:none`: Do not download file content objects initially; fetch them later on demand.
- `--filter=tree:0`: Further reduce tree object downloads; suitable for more extreme large repository scenarios.

Specific support depends on the Git version and remote service capabilities.

## Suitable Scenarios

- Repository history is massive
- The current task only requires partial files
- CI wants to reduce network downloads
- Initial monorepo clone is too slow

## Considerations

- Accessing a missing object for the first time will still trigger a download
- Certain legacy tools might not understand partial clones
- The effect is more pronounced when paired with sparse checkout

## Recommended Combinations

```bash
git clone --filter=blob:none --sparse <url>
cd repo
git sparse-checkout set services/order
```

## Further Reading

- [Git partial clone official documentation](https://git-scm.com/docs/partial-clone.html)
- [git clone official documentation](https://git-scm.com/docs/git-clone)
- [Sparse Checkout](sparse-checkout_en.md)
- [Large Repository Git Practices](large-repo-git-practices_en.md)
