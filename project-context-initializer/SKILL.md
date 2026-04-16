---
name: project-context-initializer
description: 在项目的根目录下使用，用于初始化项目的上下文目录结构。在用户要求“初始化项目上下文”时使用。
metadata: 
   - name: baseDir
     description: 指的是当前 skill 的 SKILL.md 所在的目录路径
---

## 工作流程

### Step1: 创建 .agents 目录
- 如果不存在 .agents/ 目录，则直接新建

### Step2: 创建 .agents/local-docs-index.md
- 使用 {baseDir}/references/local-docs-index.template.md 模板文件
- 同时必须询问用户，有哪些项目内的存放文档的目录是需要包含在索引文件中的，例如 docs/archieves、docs/summary 等目录，用户回答后，把用户需要的目录写入到索引文件中

### Step3: 创建 .agents/remote-docs-index.md
- 使用 {baseDir}/references/remote-docs-index.template.md 模板文件
- 需要保留 {baseDir}/references/remote-docs-index.template.md 中的条目示例内容

### Step4: 创建 .agents/constraints.md
- 使用 {baseDir}/references/constraints.template.md 模板文件
- 需要保留 {baseDir}/references/constraints.template.md 中的条目示例内容

### Step5: 询问用户本地知识库的索引文件路径
- 必须要询问用户，本地知识库的索引文件路径是什么

### Step6: 创建 AGENTS.md 文件
- 使用 {baseDir}/references/AGENTS.template.md 文件的格式
- 参考 {baseDir}/references/AGENTS.template.md 文件格式，把 Step2 - Step5 创建/得到的文件路径写入到 AGENTS.md 中
- 创建的 AGENTS.md 需要把 {baseDir}/references/AGENTS.template.md 中的注释给去掉，只保留必要的内容
