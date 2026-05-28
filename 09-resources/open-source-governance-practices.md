# 开源项目 Git 治理实践

原文链接：

- [Kubernetes OWNERS Files](https://www.kubernetes.dev/docs/guide/owners/)
- [Kubernetes Pull Request Process](https://www.kubernetes.dev/docs/guide/pull-requests/)
- [Linux Kernel: Creating Pull Requests](https://docs.kernel.org/maintainer/pull-requests.html)
- [Go Contribution Guide](https://go.dev/doc/contribute)
- [Rust RFCs](https://github.com/rust-lang/rfcs)

说明：本文是面向本仓库读者的改写版，重点提炼开源项目治理方式对企业团队的启发。

## 1. 为什么看开源治理

成熟开源项目的协作问题和企业团队很像：

- 贡献者很多
- 模块边界复杂
- Review 资源有限
- 权限不能随便放开
- 变更需要可追溯
- 自动化要辅助维护者判断

它们的实践适合借鉴到企业内的多团队、多服务、多仓库治理。

## 2. Kubernetes：OWNERS 与两阶段评审

Kubernetes 使用 OWNERS 文件表达代码责任，并把 Review 拆成两个阶段：

| 角色 | 关注点 |
| --- | --- |
| reviewer | 代码质量、正确性、风格、局部实现 |
| approver | 整体接受标准、兼容性、依赖关系、API 和长期影响 |

这种设计的价值是把“看代码的人”和“对模块负责的人”分开。

企业团队可以借鉴：

- 核心目录必须有 owner
- reviewer 数量要多于 approver
- owner 文件要定期维护
- 离开岗位或不再活跃的人要移出 owner 列表
- 自动化可以负责分配 reviewer、检查标签、提示缺少审批

如果使用 GitHub，可以先用 CODEOWNERS 实现简化版。

## 3. Linux Kernel：维护者树状模型

Linux Kernel 的治理方式更像多层维护者网络。

贡献者把变更提交给子系统维护者，维护者验证、整理，再向更上层维护者发送 pull request。

企业团队可以借鉴：

- 大系统不要要求一个中心团队审所有代码
- 子系统负责人要承担第一层质量判断
- 上层负责人关注集成风险和版本节奏
- 关键合入最好有签名、tag、变更说明

这种模型适合特别大的平台或基础设施团队。

## 4. Go：Gerrit 与严格 Review 流程

Go 项目长期使用 Gerrit 做代码评审。

它的启发是：当项目对兼容性、代码质量和历史整洁要求很高时，Review 工具可以比普通 PR 模型更强约束。

企业里不一定要引入 Gerrit，但可以借鉴：

- 每个变更都要有清楚的 change 描述
- Review 权限分级
- 自动测试和人工 Review 结合
- 对公共 API 和标准库级代码保持更高审查标准

## 5. Rust：RFC 与重大变更流程

Rust 的 RFC 流程适合处理影响面大的设计变化。

企业团队可以把它简化成轻量 ADR 或设计评审：

```text
背景
目标
非目标
方案
影响范围
替代方案
风险
未决问题
上线与回滚
```

适合用 RFC/ADR 的场景：

- 改公共接口
- 改数据模型
- 改核心链路
- 改团队协作规则
- 引入新基础设施

不适合每个小需求都走 RFC，否则流程会变重。

## 6. 企业团队可直接落地的做法

1. 用 CODEOWNERS 或 OWNERS 表达模块责任
2. 把 reviewer 和 approver 职责拆开
3. 对高风险目录提高 Review 要求
4. 对重大变更使用轻量 ADR
5. 用自动化提示缺少 owner、缺少测试、缺少发布说明
6. 定期清理 owner 列表和长期无人处理的 PR

## 7. 对本仓库的启发

Git 治理的核心是责任边界。

分支保护、CODEOWNERS、PR 模板、CI、Rulesets 都只是工具，最终要回答：

- 谁理解这块代码
- 谁有权批准这次变更
- 谁负责合入后的风险
- 哪些变更需要更高层级评审

