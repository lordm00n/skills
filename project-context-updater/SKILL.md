---
name: project-context-updater
description: 在每轮对话结束时/用户显式指定时调用这个 skill，扫描所有对话信息的内容，对比 AGENTS.md、.agents/local-docs-index.md、.agents/remote-docs-index.md、.agents/constraints.md 文件， 检测是否有上下文需要更新。
---

## 工作流程

### Step1: 分析对话的消息记录
- 检查用户与 Agent 的对话记录
- 分析对话中是否有提供了远程上下文的 URL
- 分析对话中是否包含项目中的文档/目录路径
    - ！需要特别注意这部分：你只需要提取“总结/归档”类型的文档的路径，如果是针对某个需求的设计文档，就需要排除
- 分析对话中是否提到了某些约束/要求/规范
    - ！需要特别注意这部分：因为这部分的内容不像文档路径那么直接，你需要仔细地推敲用户的提示词，提炼出涉及到“约束/要求/规范”的内容
- 将以上分析的内容用列表的形式列出来

### Step2: 读取 .agents/remote-docs-index.md
- 读取 .agents/remote-docs-index.md 中有哪些远端文档
- 通过 Step1 获取到的列表，判断对话中是否有远端上下文没有被 .agents/remote-docs-index.md 包含，如果没有被包含，则向用户提问是否需要将这些远端上下文添加到 remote-docs-index.md 中

### Step3：读取 .agents/local-docs-index.md
- 读取 .agents/remote-docs-index.md 中包含了哪些项目中的文档目录
- 通过 Step1 获取到的列表，判断对话中是否有本地上下文目录没有被 .agents/remote-docs-index.md 包含，如果没有被包含，则向用户提问是否需要将这些本地上下文目录添加到 local-docs-index.md 中

### Step4: 读取 .agents/constraints.md
- 读取 .agents/constaints.md 中说明了哪些约束/规范
- 通过 Step1 获取到的列表，判断对话中是否有约束/规范/要求没有被 .agents/constraints.md 包含，如果没有被包含，则向用户提问是否将这些约束/规范/要求添加到 constraints.md 中