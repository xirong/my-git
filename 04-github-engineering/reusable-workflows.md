# Reusable Workflows

原文链接：

- [GitHub Docs: Reuse workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows)
- [GitHub Docs: Reusing workflow configurations](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations)

说明：本文是面向本仓库读者的改写版，重点整理多仓库团队如何统一 GitHub Actions CI 模板。

## 1. 解决什么问题

多仓库团队最容易出现 CI 分裂：

- 每个仓库一份复制粘贴的 workflow
- Node、Java、Go、Python 检查方式不一致
- 安全扫描有的仓库有，有的仓库没有
- job 名称不统一，分支保护很难配置
- 模板改一次，要手工改几十个仓库

Reusable workflows 用 `workflow_call` 把公共 CI 逻辑抽出来，让业务仓库调用统一模板。

## 2. 基本结构

公共仓库：

```text
org/.github
  .github/workflows/
    java-ci.yml
    node-ci.yml
    security-scan.yml
```

公共 workflow：

```yaml
name: java-ci

on:
  workflow_call:
    inputs:
      java-version:
        required: false
        type: string
        default: "17"

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: ${{ inputs.java-version }}
      - run: mvn test
```

业务仓库调用：

```yaml
name: ci

on:
  pull_request:
  push:
    branches: [main]

jobs:
  java-ci:
    uses: org/.github/.github/workflows/java-ci.yml@v1
    with:
      java-version: "21"
```

## 3. 多仓库治理建议

### 固定版本

业务仓库调用公共 workflow 时，不要长期使用 `@main`。

推荐：

```yaml
uses: org/.github/.github/workflows/java-ci.yml@v1
```

这样公共模板升级不会突然影响所有仓库。

### job 名称稳定

分支保护依赖 status check 名称。

公共 workflow 的 job 名称要尽量稳定，避免改名导致主分支保护失效。

### 权限最小化

公共 workflow 里显式声明权限：

```yaml
permissions:
  contents: read
```

需要写 PR 评论、上传安全结果、发布包时，再单独提高权限。

### 语言模板分层

不要写一个超级 workflow 处理所有语言。

建议按语言和职责拆：

- `java-ci.yml`
- `node-ci.yml`
- `go-ci.yml`
- `docs-ci.yml`
- `security-scan.yml`
- `release.yml`

## 4. 推广顺序

1. 先选 1 个低风险仓库试点
2. 抽出最小公共检查
3. 稳定 job 名称和输出
4. 给模板打 tag
5. 推广到同类仓库
6. 再把安全扫描、发布、镜像构建纳入模板

## 5. 常见风险

### 公共模板一次升级影响太多仓库

解决：用 tag 或 release 分层升级。

### 业务仓库完全失去灵活性

解决：公共模板提供少量输入参数，但不要把每个细节都参数化。

### secrets 管理混乱

解决：能用 `secrets: inherit` 时也要明确边界，高风险 secret 要限制在必要仓库和环境。

## 6. 对本仓库的启发

40+ 微服务团队做 GitHub 工程治理时，Reusable workflows、Rulesets、CODEOWNERS 是三件基础设施。

它们分别解决：

- CI 规则怎么统一
- 分支和合入规则怎么统一
- 代码责任怎么统一

