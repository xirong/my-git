# Reusable Workflows

English | [中文](../reusable-workflows.md)

Original Links:

- [GitHub Docs: Reuse workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows)
- [GitHub Docs: Reusing workflow configurations](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations)

## 1. What Problems It Solves

Multi-repository teams are most prone to CI fragmentation:

- A copy-pasted workflow in every repository
- Inconsistent checking methods for Node, Java, Go, and Python
- Security scanning exists in some repositories but not in others
- Ununified job names make branch protection difficult to configure
- Changing a template once requires manually updating dozens of repositories

Reusable workflows extract common CI logic using `workflow_call`, allowing business repositories to call a unified template.

## 2. Basic Structure

Public repository:

```text
org/.github
  .github/workflows/
    java-ci.yml
    node-ci.yml
    security-scan.yml
```

Public workflow:

```yaml
name: java-ci

on:
  workflow_call:
    inputs:
      java-version:
        required: false
        type: string
        default: "17"

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: ${{ inputs.java-version }}
      - run: mvn test
```

Business repository call:

```yaml
name: ci

on:
  pull_request:
  push:
    branches: [main]

jobs:
  java-ci:
    uses: org/.github/.github/workflows/java-ci.yml@v1
    with:
      java-version: "21"
```

## 3. Multi-Repository Governance Recommendations

### Pin Versions

When business repositories call public workflows, do not use `@main` long-term.

Recommended:

```yaml
uses: org/.github/.github/workflows/java-ci.yml@v1
```

This ensures that upgrades to the public template do not suddenly affect all repositories.

### Stable Job Names

Branch protection relies on status check names.

The job names in public workflows should be as stable as possible to avoid renaming that causes main branch protection to fail.

### Least Privilege

Explicitly declare permissions in public workflows:

```yaml
permissions:
  contents: read
```

Elevate permissions individually only when writing PR comments, uploading security results, or publishing packages is required.

### Layered Language Templates

Do not write a super workflow to handle all languages.

Split them by language and responsibility:

- `java-ci.yml`
- `node-ci.yml`
- `go-ci.yml`
- `docs-ci.yml`
- `security-scan.yml`
- `release.yml`

## 4. Rollout Sequence

1. Select 1 low-risk repository for a pilot first
2. Extract the minimal common checks
3. Stabilize job names and outputs
4. Tag the templates
5. Rollout to similar repositories
6. Then incorporate security scanning, releases, and image builds into the templates

## 5. Common Risks

### A single public template upgrade affects too many repositories

Solution: Use tags or releases for layered upgrades.

### Business repositories completely lose flexibility

Solution: Public templates provide a small number of input parameters, but do not parameterize every detail.

### Chaotic secrets management

Solution: Even when `secrets: inherit` can be used, define clear boundaries; high-risk secrets should be restricted to necessary repositories and environments.

## 6. Implications for This Repository

When 40+ microservice teams implement GitHub engineering governance, Reusable workflows, Rulesets, and CODEOWNERS are three essential pieces of infrastructure.

They resolve the following respectively:

- How to unify CI rules
- How to unify branching and merging rules
- How to unify code responsibilities
