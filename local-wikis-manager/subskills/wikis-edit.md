# Wikis Edit - 修改文档规范

本 subskill 规范如何在 wikis 目录中修改文档。

## 修改前准备

1. **确认 wikis 路径** - 用户指定或默认 `~/wikis`
2. **定位目标文件** - 根据用户描述找到要修改的文档
3. **读取现有内容** - 先阅读文档内容再修改

## 修改流程

### Step 1: 定位文档

如果用户没有指定完整路径，需要搜索定位：

```bash
# 按文件名查找
find ~/wikis -name "*.md" | grep -i "关键词"

# 按内容查找
grep -r "关键词" ~/wikis --include="*.md"
```

### Step 2: 读取文档

使用 Read 工具读取文件内容：

```
读取: ~/wikis/env/golang.md
```

### Step 3: 理解现有结构

在修改前，先理解文档的组织方式：

- 文档使用什么格式？
- 有哪些可识别的章节？
- 修改是追加内容还是替换部分？

### Step 4: 执行修改

使用 Edit 工具进行修改：

- **追加内容**: 使用 `oldString` 匹配文档末尾或合适的插入点
- **替换内容**: 精确匹配要替换的段落
- **删除内容**: 替换为空字符串

### Step 5: 验证修改

修改后：
1. 确认文件内容正确
2. 检查格式是否一致
3. 确认 index.md 不需要更新（通常 index.md 不需要修改）

## 修改类型

### 1. 追加新内容

追加到文档末尾或特定章节：

```
oldString: (文档末尾或章节末尾)
newString: (原有内容 + 新增内容)
```

### 2. 修改现有内容

精确匹配要修改的段落：

```
oldString: (需要修改的原始内容)
newString: (修改后的内容)
```

### 3. 删除内容

移除不需要的内容：

```
oldString: (要删除的内容)
newString: (空)
```

### 4. 重命名/移动文件

如果需要重命名文档：

1. 移动文件到新位置
2. 更新所在目录的 `index.md`
3. 如果移动到新目录，更新原目录的 `index.md`

```bash
mv ~/wikis/old-name.md ~/wikis/new-name.md
```

## 注意事项

### 保持格式一致

- 使用相同的 Markdown 格式
- 保持标题层级一致
- 表格格式保持统一风格

### 不要轻易修改 index.md

- `index.md` 通常不需要频繁修改
- 只有在新增/删除子目录时才需要修改

### 备份意识

对于大量修改，可以先用 Bash 确认：

```bash
# 修改前备份
cp ~/wikis/doc.md ~/wikis/doc.md.bak
```

## 示例

### 示例 1: 追加内容

**场景**: 在 golang.md 末尾添加新命令说明

**操作**:
```bash
cat >> ~/wikis/env/golang.md << 'EOF'

## 常用命令

```bash
go version  # 查看版本
go env      # 查看环境变量
```
EOF
```

### 示例 2: 修改现有内容

**场景**: 修正 golang.md 中的版本号

**操作**:
```
oldString: | 版本 | go1.22.12 |
newString: | 版本 | go1.23.0 |
```

### 示例 3: 重命名文件

**场景**: 将 `golang.md` 重命名为 `go-basics.md`

**操作**:
1. 移动文件: `mv ~/wikis/env/golang.md ~/wikis/env/go-basics.md`
2. 更新 `env/index.md` 中的链接
3. 验证修改

## 检查清单

修改完成后，确认：

- [ ] 文件内容正确
- [ ] Markdown 格式一致
- [ ] 相关 index.md 已更新（如有必要）
- [ ] 向用户说明做了哪些修改
