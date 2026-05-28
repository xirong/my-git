# Netflix Spinnaker 与发布流水线实践

原文链接：

- [Netflix's New Spinnaker Open Source Tool Makes It Easy to Use Amazon's Cloud-And Google's](https://www.wired.com/2015/11/netflixs-new-tool-makes-it-easy-to-use-amazons-cloud-and-googles)
- [Spinnaker](https://spinnaker.io/)

## 1. 为什么这个案例仍然有价值

有些公司公开资料更关注发布控制，分支模型只是配套信息。

这说明一个现实问题：很多团队真正的风险不在“用几个分支”，而在“代码合入后如何安全发布”。

Spinnaker 这类持续交付平台的价值在于，把发布过程拆成可观察、可审批、可回滚的流水线。

## 2. 和 Git 工作流的关系

Git 负责记录变更事实：

- commit
- PR
- tag
- release note
- changelog

发布平台负责控制交付过程：

- 构建
- 部署
- 分环境推进
- 人工审批点
- 回滚
- 发布状态追踪

两者要能互相追溯。线上版本应该能回到 Git commit、tag、PR 和发布单。

## 3. 对团队的启发

如果团队已经有比较成熟的 PR 和 CI，下一步不要只继续加分支规则，还要补发布治理：

- 每次发布关联 commit 或 tag
- 每次发布有 release note
- 生产发布前有明确检查点
- 高风险发布需要人工审批点
- 回滚命令和回滚责任人明确
- 发布后验证结果写回发布记录

## 4. 适合什么场景

适合：

- 多环境部署
- 多云或多集群部署
- 发布风险高
- 回滚要求高
- 需要发布审计

不适合：

- 小型文档仓库
- 没有自动构建和部署基础的团队
- 仍停留在手工复制文件上线的流程

## 5. 对本仓库的启发

Git 工作流文章不能只停留在 merge 之前。

企业协作完整链路应该覆盖：

```text
branch -> PR -> CI -> merge -> tag -> release -> deploy -> verify -> rollback
```
