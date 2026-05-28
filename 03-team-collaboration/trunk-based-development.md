# Trunk-Based Development

Trunk-Based Development 强调短分支、快合入、主干持续稳定。

它适合工程纪律较强、CI 反馈较快、发布自动化较成熟的团队。

## 核心思想

团队尽量围绕一个主干分支协作，开发分支生命周期很短，避免长期分支积累大量冲突。

典型流程：

```text
short-lived branch -> main -> CI -> deploy
```

## 适合场景

- CI 快且稳定
- 测试覆盖较好
- 团队能接受频繁小变更
- 可以用 feature flag 控制未完成能力
- 服务端或 Web 产品可以高频发布

## 核心规则

- 分支生命周期短
- 尽快合入主干
- 主干必须随时可发布
- 大功能拆小步推进
- 未完成能力用 feature flag 隔离
- 出问题优先 revert

## 和 Gitflow 的区别

Gitflow 更强调 `develop`、`release`、`hotfix` 等多分支角色，适合版本发布节奏明确的产品。

Trunk-Based Development 更强调主干稳定和频繁集成，适合高频交付的服务型团队。

## 常见失败模式

### 1. CI 太慢

主干开发依赖快速反馈。

CI 如果经常排队几十分钟，团队会开始绕过流程。

### 2. 没有 feature flag

大功能无法一次完成时，需要用 feature flag 隔离未完成能力。

否则主干会出现半成品功能。

### 3. 分支仍然长期存在

如果 feature 分支存在几周，本质上已经偏离 trunk-based 的核心实践。

## 企业实践参考

[Google 主干开发与版本控制实践](../09-resources/company-practices/google-trunk-based-development.md) 的核心启发是，主干开发依赖一组工程能力：小变更、快速 CI、代码所有权、feature flag 和快速回滚。

普通团队落地时，不要只追求“分支少”，要先把这些支撑能力建起来。

## 延伸阅读

- [Trunk Based Development](https://trunkbaseddevelopment.com)
- [Feature Flags](https://trunkbaseddevelopment.com/feature-flags/)
- [Google 主干开发与版本控制实践](../09-resources/company-practices/google-trunk-based-development.md)
- [团队 Git 工作流指南](team-git-workflow-guide.md)
- [推荐阅读索引](../09-resources/recommended-reading.md)
