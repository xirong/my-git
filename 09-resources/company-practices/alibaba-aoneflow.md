# 阿里巴巴 AoneFlow 分支管理实践

原文链接：

- [How Do We Manage Code Branches at Alibaba?](https://www.alibabacloud.com/blog/how-do-we-manage-code-branches-at-alibaba_593834)
- [Evolved Branch Management with AoneFlow](https://www.alibabacloud.com/blog/evolved-branch-management-with-aoneflow_594903)

说明：本文是面向本仓库读者的改写版，保留原文核心思路，重新整理为团队选型和落地参考。

## 1. AoneFlow 解决什么问题

传统 Gitflow 分支角色清晰，但分支多、流程重，长期使用后容易出现 `develop`、`release`、`main` 多处分叉，回合成本高。

Trunk-Based Development 足够轻，但它要求 CI、测试覆盖、feature flag 和团队纪律都比较成熟，对于多个 feature 并行、上线范围经常调整的团队，直接用主干开发会有压力。

AoneFlow 想解决的是这个中间地带：

- 多个 feature 并行开发
- 每次上线要按需求组合功能
- 某个 feature 随时可能延期、撤下或替换
- release 分支要和测试、预发、生产环境联动
- 团队希望减少 Gitflow 的分支复杂度

## 2. 核心分支模型

AoneFlow 主要保留三类分支：

| 分支 | 作用 |
| --- | --- |
| `master` / `main` | 已发布代码的主线，用 tag 标记线上版本 |
| `feature/*` | 每个需求或任务对应一个 feature 分支 |
| `release/*` | 面向某个环境或某次发布的功能组合分支 |

它的关键点在于，`release/*` 可以从主线拉出后，再按发布计划合入一组 feature 分支，不必长期依赖 `develop` 演进。

```text
main
  \-> feature/a
  \-> feature/b
  \-> feature/c

main -> release/test  <- merge feature/a + feature/b
main -> release/prod  <- merge feature/a
```

这样做的好处是，发布分支表达的是“本次要上线哪些功能”，而不只是“当前集成分支上有什么代码”。

## 3. 三条关键规则

### 规则一：开发前从主线创建 feature 分支

每个任务先从主线创建 `feature/*` 分支，开发者不要直接改主线。

这能让每个需求天然成为一个可选择、可移除、可审查的单元。

### 规则二：release 分支由 feature 组合生成

需要测试或发布时，从主线创建 `release/*`，再把本次要发布的 feature 逐个合入。

如果某个 feature 临时不上线，可以重新生成 release 分支，只合入剩下的 feature，减少手工回滚和摘代码的风险。

### 规则三：发布后回合主线并清理分支

当某个 release 分支完成生产发布后，将它合入主线，打 tag，并删除已经发布的 feature 分支。

这样主线仍然代表已经发布过的事实，tag 代表可追溯的线上版本。

## 4. 可以借鉴的做法

### 用 release 分支表达环境

可以把 `release/test`、`release/staging`、`release/prod` 和部署环境绑定，让每个环境的代码来源清晰可查。

这适合业务系统里常见的“测试一批、预发一批、生产一批”。

### 用平台记录 feature 与 release 的关系

AoneFlow 的复杂点不在 Git 命令，而在“哪些 feature 被合入了哪个 release 分支”。

如果靠人工记忆，很容易出错。团队至少需要用 Issue、PR、项目管理平台或发布单记录这些关系。

### 保持构建可复现

原文特别强调，生产分支不能依赖只在本地或临时环境存在的 snapshot 包。

这点很重要，release 分支经常会重建，如果依赖不可复现，重建出的包就可能和上一次不一致。

## 5. 适合什么团队

适合：

- 多 feature 并行
- 发布范围经常变化
- 有测试、预发、生产多环境
- 需要按需求组合上线
- 不想维护长期 `develop` 分支

不适合：

- 小团队高频 Web 服务
- CI 很弱、测试很少
- 没有发布平台或发布单记录
- 团队无法维护 feature 和 release 的对应关系

## 6. 对本仓库的启发

AoneFlow 给团队的提醒是：

- 分支策略要服务发布策略
- release 分支最好表达明确的上线范围
- feature 要保持可选、可撤、可审查
- 分支关系需要工具或流程记录
- 发布完成后要及时回到主线事实

如果团队处在 Gitflow 太重、主干开发又太激进的阶段，可以参考 AoneFlow 做一个轻量版本。
