# Fork and Pull Request Workflow

Fork + PR 适合开源项目和外部贡献者场景。

它的核心是：贡献者在自己的 fork 中开发，再通过 PR 请求维护者合入，不需要直接拥有主仓库写权限。

## 流程

```text
fork upstream -> create branch -> commit -> open PR -> maintainer review -> merge
```

## 适合场景

- 开源项目
- 外部贡献者很多
- 不希望给所有贡献者主仓库写权限
- 维护者需要统一把控合入质量
- InnerSource 公共基础仓库
- 外部合作方参与较多的生态仓库

## 贡献者流程

```bash
git clone git@github.com:your-name/project.git
cd project
git remote add upstream git@github.com:owner/project.git
git switch -c docs/update-guide
```

同步上游：

```bash
git fetch upstream
git rebase upstream/main
```

推送到自己的 fork：

```bash
git push -u origin docs/update-guide
```

然后从 GitHub 页面发起 PR。

## 维护者清单

- 提供贡献指南
- 提供 Issue 模板
- 提供 PR 模板
- 配置基础 CI
- 明确 Review 标准
- 标记适合新手的任务
- 对长期无人响应的 PR 做关闭说明

## 常见问题

### 1. fork 落后上游太多

贡献者要定期同步 `upstream/main`。

### 2. PR 范围太大

维护者可以要求贡献者拆分 PR。

### 3. CI 权限和 secret 风险

来自 fork 的 PR 需要注意 CI 权限和 secret 暴露风险，尤其是自动化脚本会执行外部贡献者代码时。

## 企业内部怎么用

企业内部如果所有成员都在同一个组织里，通常不必默认使用 Forking Workflow。

但在这些场景里，fork 仍然有价值：

- 平台团队维护公共基础库
- 外部供应商或合作伙伴参与
- 希望隔离不可信贡献者写权限
- 核心仓库只允许维护者最终合入

对纯内部业务服务，feature branch + protected main 往往更简单。

## 延伸阅读

- [GitHub Docs: Fork a repo](https://docs.github.com/en/get-started/quickstart/fork-a-repo)
- [GitHub Docs: Creating a pull request from a fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork)
- [Atlassian: Forking Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/forking-workflow)
- [推荐阅读索引](../09-resources/recommended-reading.md)
