---
name: project-context-initializer
description: 在项目的根目录下使用，用于初始化项目的上下文目录结构。在用户要求“初始化项目上下文”时使用。
---

## 工作流程

### Step1: 创建 .agents 目录
- 如果不存在 .agents/ 目录，则直接新建

### Step2: 创建 .agents/local-docs-index.md
- 使用 ./references/local-docs-index.template.md 模板文件

### Step3: 创建 .agents/remote-docs-index.md
- 使用 ./references/remote-docs-index.template.md 模板文件

### Step4: 创建 .agents/constraints.md
- 使用 ./references/constraints.template.md 模板文件

### Step5: 询问用户本地知识库的索引文件路径
- 必须要询问用户，本地知识库的索引文件路径是什么

### Step6: 创建 AGENTS.md 文件
- 使用 ./references/AGENTS.template.md 文件的格式
- 参考 ./references/AGENTS.template.md 文件格式，把 Step2 - Step5 创建/得到的文件路径写入到 AGENTS.md 中
