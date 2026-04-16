---
name: context-management-optimizer
description: 用于优化上下文管理的 skills（project-context-initializer, project-context-updater, project-context-enforcer）。当用户发现这些 skills 没有正确识别上下文（如遗漏了约束、未添加新文档到索引等）时，使用这个 skill 来收集反馈、诊断问题、并迭代改进相关的 skills。通过与用户对话不断优化上下文管理能力。
---

# Context Management Optimizer

这个 skill 用于优化项目的上下文管理 skills，包括 `project-context-initializer`、`project-context-updater` 和 `project-context-enforcer`。

## 何时使用

当用户发现以下情况时使用这个 skill：
- 上下文的 skills 没有正确识别需要更新的内容
- 约束没有被添加到约束文档中
- 新文档没有被添加到索引中
- 技能没有按预期触发或工作

## 工作流程

### 步骤 1：诊断问题

首先了解发生了什么问题：
1. 询问用户具体遇到了什么问题
2. 询问在什么场景下问题出现了
3. 询问用户期望的行为是什么

示例问题：
- "在什么情况下 skill 没有正确识别？"
- "你是希望系统自动发现这个约束吗？"
- "你希望 skill 在什么时候触发？"

### 步骤 2：分析相关 Skill

读取相关的 skills 文件，分析当前实现：
- `~/.agents/skills/project-context-initializer/SKILL.md`
- `~/.agents/skills/project-context-updater/SKILL.md`
- `~/.agents/skills/project-context-enforcer/SKILL.md`

### 步骤 3：确定改进方向

根据问题分析，确定需要改进的方面：

**如果问题是"没有检测到约束"：**
- 检查 `project-context-updater` 中对约束的检测逻辑
- 考虑：是否需要扩大检测关键词范围？
- 考虑：是否需要添加更多触发条件？

**如果问题是"没有添加到索引"：**
- 检查询问用户的环节是否正确
- 考虑：是否需要改进提示文案？

**如果问题是"没有触发 skill"：**
- 检查 description 是否足够"pushy"
- 考虑：是否需要优化触发条件描述？

### 步骤 4：提出改进建议

向用户解释发现的问题和可能的改进方案：
> 特别注意：对于 skill 的修改，不要打太多的补丁，要有总结归纳

```
我分析了问题，发现可能的原因有：
1. [原因1]
2. [原因2]

建议的改进方案：
- [方案1]
- [方案2]

您觉得哪个方案更符合您的预期？
```

### 步骤 5：实施改进

在用户确认后，更新相应的 skill 文件。

### 步骤 6：验证改进

告诉用户如何测试改进后的 skill：
- "请在下次遇到类似场景时注意观察"
- "如果还有问题，请再次使用这个 optimizer skill"

## 改进策略

### 扩大检测范围

如果 skill 没有检测到某些内容，考虑：
- 添加更多同义词和变体
- 添加更多触发模式
- 使用更宽松的匹配条件

### 改进触发描述

如果 skill 没有被正确触发：
- 在 description 中添加更多具体的触发场景
- 使用更"pushy"的语言
- 添加反面例子（什么情况下不应该触发）

### 添加兜底逻辑

如果不确定用户意图：
- 添加更多的询问确认步骤
- 提供默认行为但明确告知用户

## 重要提示

- 这个 skill 是迭代改进的工具，需要多次使用才能完善
- 每次用户反馈都是改进的机会
- 保持 skill 简洁，避免过度复杂化
- 记录每次改进的原因，便于后续维护
