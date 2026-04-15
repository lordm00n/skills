---
name: local-wikis-manager
description: 管理本地 wikis 文档库的新增、查找、修改操作。当你需要对本机 wikis 目录进行文档操作时使用，包括：总结内容输出到 wikis 目录、查找 wikis 中的文档、修改 wikis 中的文档内容、创建新的文档分类。请务必使用此 skill 来管理 wikis 文档，用户可以通过指定路径来指定 wikis 目录位置，格式如 `~/wikis` 或 `/path/to/wikis`。
---

# Local Wikis Manager

本 skill 用于管理本地 wikis 文档库，支持新增、查找、修改文档等操作。

## 使用方式

用户调用时需要提供：
1. **wikis 目录路径** - 通过参数或指令中指定，如 `~/wikis`、`/Users/name/wikis`
2. **操作类型** - 新增、查找、修改
3. **具体内容** - 根据操作类型提供相应信息

## 调用示例

```
/local-wikis-manager 将当前对话总结输出到 ~/wikis 目录
/local-wikis-manager 在 ~/wikis 中搜索包含 "python" 的文档
/local-wikis-manager 修改 ~/wikis 中的 golang.md 添加新内容
```

## 参数解析

当用户给出指令后，需要解析：

1. **wikis 路径**: 从指令中提取路径。如果用户没有说明知识库的路径，**必须询问用户**确认路径，不能使用默认值。
2. **操作类型**: 
   - 包含"初始化"、"新建知识库" → wikis-init
   - 包含"新增"、"创建"、"输出"、"总结" → wikis-create
   - 包含"搜索"、"查找" → wikis-search
   - 包含"修改"、"编辑"、"更新" → wikis-edit

## Subskills

根据解析的操作类型，加载对应的 subskill：

| 操作 | Subskill |
|------|----------|
| 初始化知识库 | `subskills/wikis-init.md` |
| 新增文档 | `subskills/wikis-create.md` |
| 查找文档 | `subskills/wikis-search.md` |
| 修改文档 | `subskills/wikis-edit.md` |

## 工作流程

1. 解析用户指令，提取 wikis 路径和操作类型
2. 根据操作类型加载对应的 subskill
3. 按照 subskill 的规范执行操作
4. 返回操作结果

## 目录结构示例

wikis 目录结构示例：
```
wikis/
├── index.md          # 文档索引
├── env/              # 环境配置 (一层子目录)
│   └── index.md      # env 目录索引
├── notes/            # 笔记 (一层子目录)
│   └── index.md
└── ...               # 其他分类 (一层子目录)
```

**重要约束**：
- wikis 目录下最多只允许一层子目录
- 每个子目录必须包含 `index.md` 作为索引
- 在根目录 index.md 中添加新分类说明
