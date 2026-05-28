# Slack Deploys 发布实践

原文链接：

- [Deploys at Slack](https://slack.engineering/deploys-at-slack/)

Slack 的发布实践适合补充“merge 之后发生什么”。

很多 Git 教程写到 PR 合并就结束了，但企业协作链路真正的风险常常在发布阶段。

## 关键链路

可以把 Slack 这类发布实践抽象成：

```text
PR
-> review
-> tests
-> merge
-> release branch
-> staging
-> dogfood
-> canary
-> percentage rollout
-> rollback / hotfix
```

不同团队的工具不同，但核心目标一致：发布要可控、可观察、可回滚。

## Git 和发布的关系

Git 负责记录变更事实：

- commit
- PR
- tag
- release branch
- changelog

发布系统负责控制变更进入用户环境：

- staging 验证
- 灰度
- 监控
- 回滚
- hotfix

这两套系统必须能互相追溯。

## 适合写进团队规范的规则

- 每个发布版本有明确 commit 或 tag
- 发布前必须知道本次包含哪些 PR
- staging 和生产环境的差异要可解释
- 灰度失败时能快速停止
- 回滚路径提前写清
- hotfix 后必须同步回主线

## 对本手册的启发

Release Management 不能只写 GitHub Release 和 tag。

还要写发布过程里的验证、灰度、回滚、hotfix 和发布记录。
