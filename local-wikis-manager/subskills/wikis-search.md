# Wikis Search - 查找文档规范

本 subskill 规范如何在 wikis 目录中查找文档。

## 查找方式

### 1. 目录浏览

先查看 wikis 根目录的 `index.md`，了解整体结构：

```bash
cat ~/wikis/index.md
```

### 2. 子目录浏览

进入子目录，查看 `index.md` 获取该分类下的文档列表：

```bash
cat ~/wikis/env/index.md
```

### 3. 文件搜索

#### 按文件名搜索

```bash
# 查找包含关键词的文件名
find ~/wikis -name "*关键词*"

# 列出所有 md 文件
find ~/wikis -name "*.md"
```

#### 按内容搜索

```bash
# 在所有 md 文件中搜索关键词
grep -r "关键词" ~/wikis --include="*.md"

# 显示文件名和匹配行
grep -rn "关键词" ~/wikis --include="*.md"
```

#### 忽略 index.md 的搜索

index.md 通常是索引文件，如果想搜索具体文档内容：

```bash
grep -r "关键词" ~/wikis --include="*.md" | grep -v "index.md"
```

## 查找结果呈现

找到文档后，向用户呈现：

1. **文档路径** - 相对于 wikis 的路径
2. **文档说明** - 从文档中提取的简要描述
3. **匹配内容** - 如果是内容搜索，显示匹配的行

## 示例

### 示例 1: 浏览目录结构

**场景**: 用户想了解 wikis 中有哪些内容

**操作**:
```bash
cat ~/wikis/index.md
```

**结果呈现**:
```
文档结构:
- env/ - 环境配置
- notes/ - 学习笔记
- tools/ - 工具手册
```

### 示例 2: 搜索特定主题

**场景**: 用户想找关于 Python 的配置文档

**操作**:
```bash
grep -r "python" ~/wikis --include="*.md"
```

**结果呈现**:
```
找到 2 个匹配:
- env/python.md: 包含 "python"
- env/index.md: 包含 "Python 环境"
```

### 示例 3: 查找特定文件

**场景**: 用户想找 golang 相关的文档

**操作**:
```bash
find ~/wikis -name "*golang*"
```

**结果呈现**:
```
找到: ~/wikis/env/golang.md
```

## 检查清单

查找完成后，确认：

- [ ] 向用户清晰展示文档位置
- [ ] 提供文档内容的简要说明
- [ ] 如果有多个匹配项，列出所有选项
