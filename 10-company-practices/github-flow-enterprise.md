# GitHub Flow 企业化实践

原文链接：

- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- [About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [Managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)

## 1. GitHub Flow 的基础形态

GitHub Flow 的基础路径很简单：

```text
main -> branch -> pull request -> review -> merge -> deploy
```

它的价值在于学习成本低，天然适合 PR、Review、状态检查和持续发布。

但企业团队不能只停留在“开分支、提 PR、合并”。

## 2. 企业化之后长什么样

企业团队里的 GitHub Flow 通常会增加这些能力：

| 能力 | 解决的问题 |
| --- | --- |
| Protected branches | 保护 `main`，避免直接 push、强推、未检查合入 |
| CODEOWNERS | 按路径自动找 owner Review |
| Rulesets | 在仓库或组织层统一规则 |
| Required status checks | CI、lint、安全检查必须通过 |
| Merge Queue | 验证 PR 排队后的组合结果 |
| Actions | 构建、测试、发布自动化 |
| Security features | secret、依赖、代码安全问题前移发现 |

此时 GitHub Flow 已经从轻量流程升级成一套平台化协作链路。

## 3. 和主干开发的关系

GitHub Flow 更像平台上的工作流表达。

Trunk-Based Development 更像组织层面的工程原则。

当 GitHub Flow 满足这些条件时，它就很接近 trunk-based：

- 分支生命周期短
- PR 足够小
- 主分支持续可发布
- 必需 CI 稳定
- feature flag 管住未完成功能
- Merge Queue 保护合入顺序
- 出问题优先 revert

## 4. 适合什么团队

适合：

- Web / SaaS 服务
- 文档站和平台配置仓库
- 内部工具仓库
- 发布频率较高的业务服务
- 已有基础 CI 的中小团队

需要加强后再使用：

- PR 吞吐很高的团队，需要 Merge Queue
- 多团队共用仓库，需要 CODEOWNERS
- 多仓库组织，需要 Rulesets 和 reusable workflows
- 安全要求高的仓库，需要 code scanning、secret scanning、Dependabot

## 5. 常见误区

### 把 GitHub Flow 当成无规则流程

GitHub Flow 本身很轻，规则需要靠 GitHub 平台能力补齐。

### 合入后没有发布闭环

GitHub Flow 强调主分支可发布，但企业团队还要保证 tag、release note、部署、验证和回滚可追溯。

### 不处理大 PR

GitHub Flow 依赖 reviewer 能快速理解 diff。大功能应拆成堆叠 PR 或多个小 PR。

## 6. 对本仓库的启发

写 GitHub Flow 时，不要只写“流程简单”。

更有价值的写法是把它放进企业配置栈：

```text
short branch
-> PR
-> CODEOWNERS
-> CI
-> security checks
-> Merge Queue
-> protected main
-> release
```
