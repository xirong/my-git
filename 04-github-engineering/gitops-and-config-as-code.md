# GitOps and Config as Code

原文链接：

- [Airbnb: Safeguarding Dynamic Configuration Changes at Scale](https://airbnb.tech/infrastructure/safeguarding-dynamic-configuration-changes-at-scale/)
- [Spotify Fleet Management Part 2: The Path to Declarative Infrastructure](https://engineering.atspotify.com/2023/05/fleet-management-at-spotify-part-2-the-path-to-declarative-infrastructure)
- [Spotify Fleet Management Part 3: Fleet-wide Refactoring](https://engineering.atspotify.com/2023/05/fleet-management-at-spotify-part-3-fleet-wide-refactoring)

Git 的边界已经从代码扩展到配置、基础设施、发布和组织流程。

对工程团队来说，Git 既保存源码，也记录配置、基础设施和发布策略的变更轨迹。

## 1. 配置为什么要进入 Git

配置变更如果只存在管理后台里，很容易出现这些问题：

- 谁改了不清楚
- 为什么改不清楚
- 改动有没有 Review 不清楚
- 出问题怎么回滚不清楚
- 哪些服务受影响不清楚

把配置纳入 Git 工作流后，可以复用已有能力：

- PR
- Review
- CODEOWNERS
- CI 校验
- 发布记录
- rollback
- 变更审计

## 2. Airbnb Sitar 的启发

Airbnb Sitar 这类配置管理实践说明，动态配置也需要工程化治理。

关键点：配置文件进入仓库后，配置变更也要经过：

```text
PR -> validation -> review -> staged rollout -> monitoring -> rollback
```

这和代码发布非常相似。

## 3. Spotify Declarative Infrastructure 的启发

Spotify 把基础设施配置和源码一起管理，通过 GitOps workflow 获得 peer review 和 audit trail。

它的关键点：

- 基础设施配置进入仓库
- 变更通过 PR 审查
- CI 做 dry run 或轻量校验
- 运行时状态可被平台查询
- 紧急情况下保留 break-glass 机制

## 4. 自动化变更也要走 PR

Spotify fleet-wide refactoring 这类案例提醒我们，自动化改造不能绕开协作流程。

大规模自动变更应该：

- 自动创建 PR
- 通过 checks
- 限速合并
- 工作时间合并
- 留下审计记录
- 出问题能快速停止

这对 AI 时代也有直接启发。AI 生成变更、本地脚本批量变更、平台自动修复，都应该回到 PR、Review、CI 和发布记录里。

## 5. 团队落地建议

1. 先把高风险配置纳入 Git 管理
2. 配置仓库启用 CODEOWNERS
3. 配置变更必须走 PR
4. CI 校验格式、语义和风险
5. 发布系统能追踪配置版本
6. 保留紧急变更路径，但要有审计记录

## 6. 适合什么场景

适合：

- 业务开关
- 动态配置
- 基础设施配置
- Kubernetes manifest
- 权限配置
- 发布策略

不适合：

- 高频实时运营数据
- 必须毫秒级生效的临时状态
- 不能暴露到仓库权限体系内的敏感值
