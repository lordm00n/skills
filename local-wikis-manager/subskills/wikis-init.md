# Wikis Init - 初始化知识库

本 subskill 规范如何初始化一个新的本地 wikis 知识库。

## 初始化流程

### Step 1: 确认路径

用户需要指定 wikis 目录的父目录路径。例如：
- `~/wikis` → 初始化到 `/Users/name/wikis`
- `/Users/name/docs/wikis` → 初始化到 `/Users/name/docs/wikis`

如果用户未指定路径，询问用户。

### Step 2: 创建目录结构

初始化时只创建基础结构：

```
wikis/
└── index.md          # 文档总索引
```

执行命令：
```bash
mkdir -p <wikis-path>
```

### Step 3: 创建 index.md 文件

#### index.md 的作用

`index.md` 是目录的索引文件，用于：
1. **说明目录用途** - 告诉用户这个目录下存放什么内容
2. **提供文档导航** - 列出该目录下的文档列表和简要说明
3. **保持结构清晰** - 新增文档时更新索引，方便查阅

#### wikis/index.md 模板

```markdown
# Wiki 文档库

> 本目录用于存放个人知识库、笔记和文档，便于分类查阅和管理。

## 分类文档

本知识库采用一层目录结构，每个子目录都有独立的 index.md 索引。

| 目录 | 说明 |
|------|------|

> 暂无分类。创建子目录后，在本文件中添加对应的目录说明。

## 搜索文档

```bash
# 查找包含关键词的文档
grep -r "关键词" <wikis-path>/

# 列出所有文档
find <wikis-path> -name "*.md"
```
```

### Step 4: 验证结构

创建完成后，验证：

```bash
ls -la <wikis-path>/
```

确认包含：
- [ ] `wikis/index.md`

## 新增分类时的索引规范

当用户后续创建新的子目录时（如 `env/`、`notes/`），需要：

1. 在子目录中创建 `index.md`
2. 更新 `wikis/index.md` 中的分类表格

#### 子目录 index.md 模板

```markdown
# [分类名称]

> 本目录用于存放 [...简短说明...]。

## 文档列表

| 文档 | 说明 |
|------|------|

> 暂无文档。
```
