# GitHub Actions CI

CI 是 GitHub 协作流程里的最低质量验收。

它不能保证代码一定正确，但可以防止明显的编译失败、测试失败、格式错误和基础安全问题直接进入主分支。

CI 的价值不只体现在“更快上线”，更重要的是让合入决策更可靠，让 reviewer 和作者对变更质量更有信心。相关研究整理见 [Git 工作流经验研究笔记](../09-resources/empirical-git-workflow-research.md)。

## 最小 CI

一个正式团队至少应该有：

- lint
- test
- build

示例：

```yaml
name: ci

on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm test
      - run: npm run build
```

不同语言的命令不同，但原则一致：PR 合入前必须能自动验证最关键路径。

## 推荐实践

- job 名称保持稳定，方便分支保护引用
- 快速失败，不让明显错误浪费队列
- 缓存依赖，降低 CI 时间
- 对大仓库按路径触发重任务
- 主分支和 PR 都跑必要检查
- flaky test 要尽快治理，不要让团队习惯忽略红灯

## 和分支保护结合

在 GitHub 分支保护中，可以把 CI job 配成 required status checks。

这样 PR 没通过 CI 时不能合入主分支。

## 多仓库团队

多仓库团队不要在每个仓库复制粘贴一份 workflow。

推荐把公共检查抽成 reusable workflows，再由业务仓库按版本调用。这样可以统一 job 名称、权限、缓存策略和基础检查，也更容易配合组织级规则推广。

详细见 [Reusable Workflows](reusable-workflows.md)。

## AI 编程场景

AI 生成代码后，CI 是最低质量保障。

建议至少检查：

- 编译是否通过
- 单元测试是否通过
- lint 是否通过
- 依赖锁文件是否符合预期
- 生成文件是否符合仓库规范

## 延伸阅读

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [企业 GitHub 协作配置栈](enterprise-github-workflow-stack.md)
- [Reusable Workflows](reusable-workflows.md)
- [Git 工作流经验研究笔记](../09-resources/empirical-git-workflow-research.md)
- [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub 工程治理手册](github-engineering-governance.md)
- [推荐阅读索引](../09-resources/recommended-reading.md)
