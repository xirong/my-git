# 大厂工程实践索引

这个目录收录公开资料中的 Git、分支管理、代码评审、CI、Monorepo 和工程治理实践。

每篇资料页都采用同一结构：

1. 头部保留原文链接
2. 正文按本仓库读者的使用场景重新组织
3. 提炼可复用做法、适合场景和注意事项
4. 在相关手册章节中补充引用

## 已整理案例

| 案例 | 适合阅读场景 |
| --- | --- |
| [阿里巴巴 AoneFlow 分支管理实践](alibaba-aoneflow.md) | 多 feature 并行、按环境组织 release 分支、需要灵活调整上线范围 |
| [腾讯 Gitflow 分支规范实践](tencent-gitflow.md) | 客户端、SDK、企业交付产品，需要稳定的 release / hotfix 流程 |
| [字节跳动 Git 工作流与研发设施实践](bytedance-git-workflow.md) | 大规模研发组织，需要把 Git 流程、权限、CI、发布平台串起来 |
| [Google 主干开发与版本控制实践](google-trunk-based-development.md) | 想理解主干开发为什么能支撑大规模协作 |
| [Microsoft Scalar 与大仓库 Git 实践](microsoft-scalar-large-repo.md) | 大仓库 clone、status、checkout、历史对象下载太慢 |
| [Merge Queue 合并队列实践](merge-queue-practices.md) | PR 多、主分支繁忙、单个 PR CI 通过但组合合入风险高 |

