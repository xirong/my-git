# Sparse Checkout

English | [中文](../sparse-checkout.md)

Sparse checkout is used to keep only specific directories in the working tree.

It is suited for monorepos or large repositories: the repository contains many projects, but you currently only need a few directories.

## Examples

Initialize cone mode:

```bash
git sparse-checkout init --cone
```

Only checkout specified directories:

```bash
git sparse-checkout set services/order services/payment
```

View current rules:

```bash
git sparse-checkout list
```

Restore complete working tree:

```bash
git sparse-checkout disable
```

## Suitable Scenarios

- The monorepo is huge
- The current task only involves a few directories
- CI only requires partial paths
- Local disk space and checkout times need optimization

## Combining with Partial Clone

Sparse checkout controls which paths are present in the working tree.

Partial clone controls the object download strategy.

Using in combination:

```bash
git clone --filter=blob:none --sparse <url>
cd repo
git sparse-checkout set services/order
```

## Considerations

- Build scripts might implicitly depend on other directories
- IDE indexing might only see files within the sparse scope
- The team must clarify which directories can operate independently

## Further Reading

- [Git sparse checkout official documentation](https://git-scm.com/docs/sparse-checkout)
- [Partial Clone](partial-clone_en.md)
- [Large Repository Git Practices](large-repo-git-practices_en.md)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
