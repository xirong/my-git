# Fork and Pull Request Workflow

English | [中文](../fork-and-pr-workflow.md)

Fork + PR is suited for open-source projects and external contributor scenarios.

Its core principle is: contributors develop in their own forks, then request maintainers to merge via PRs, eliminating the need for direct write access to the main repository.

## Process

```text
fork upstream -> create branch -> commit -> open PR -> maintainer review -> merge
```

## Suitable Scenarios

- Open-source projects
- Many external contributors
- Do not want to grant write access to the main repository to all contributors
- Maintainers need unified control over merge quality
- InnerSource common foundation repositories
- Ecosystem repositories with significant participation from external partners

## Contributor Process

```bash
git clone git@github.com:your-name/project.git
cd project
git remote add upstream git@github.com:owner/project.git
git switch -c docs/update-guide
```

Sync with upstream:

```bash
git fetch upstream
git rebase upstream/main
```

Push to your own fork:

```bash
git push -u origin docs/update-guide
```

Then open a PR from the GitHub page.

## Maintainer Checklist

- Provide contribution guidelines
- Provide Issue templates
- Provide PR templates
- Configure basic CI
- Clarify review standards
- Mark tasks suitable for newcomers
- Provide closing explanations for long-unresponsive PRs

## Common Issues

### 1. Fork falls too far behind upstream

Contributors should sync `upstream/main` regularly.

### 2. PR scope is too large

Maintainers can ask contributors to split the PR.

### 3. CI permissions and secret risks

PRs from forks require attention to CI permissions and secret exposure risks, especially when automated scripts execute code from external contributors.

## How to Use Internally in Enterprises

If all enterprise members are within the same organization, defaulting to the Forking Workflow is usually unnecessary.

However, in these scenarios, forks still hold value:

- Platform teams maintaining common core libraries
- Participation from external vendors or partners
- Wanting to isolate write access from untrusted contributors
- Core repositories only allowing maintainers to perform the final merge

For purely internal business services, feature branch + protected main is often simpler.

## Extended Reading

- [GitHub Docs: Fork a repo](https://docs.github.com/en/get-started/quickstart/fork-a-repo)
- [GitHub Docs: Creating a pull request from a fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork)
- [Atlassian: Forking Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/forking-workflow)
- [Recommended Reading Index](../../09-resources/09-resources_en/recommended-reading_en.md)
