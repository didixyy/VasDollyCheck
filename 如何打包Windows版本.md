# 如何打包Windows版本

## 方案1：使用GitHub Actions自动构建（推荐）

### 步骤：

1. **将代码推送到GitHub**
```bash
cd /Users/yuepeng/Documents/work/channel
git add .
git commit -m "准备打包Windows版本"
git push
```

2. **触发构建**

有两种方式触发构建：

**方式A：手动触发（推荐）**
- 访问你的GitHub仓库
- 点击 `Actions` 标签
- 选择 `Build VasDolly Tool` workflow
- 点击 `Run workflow` 按钮
- 等待构建完成（大约10-15分钟）
- 下载生成的Windows和macOS版本

**方式B：创建Tag触发**
```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```
这会自动构建并创建GitHub Release

3. **下载构建产物**
- 在Actions页面找到完成的workflow run
- 下载 `VasDollyTool-Windows` 和 `VasDollyTool-macOS` 压缩包

---

## 方案2：在Windows机器上手动打包

如果你有Windows电脑，可以按以下步骤操作：

### 在Windows上：

1. **安装Python 3.8+**
   - 从 python.org 下载安装

2. **复制项目到Windows机器**
   - 将整个 `channel` 文件夹复制到Windows

3. **安装依赖**
```cmd
cd channel
pip install pyinstaller
```

4. **下载VasDolly.jar**（如果还没有）
```cmd
mkdir resources
# 手动下载 https://github.com/Tencent/VasDolly/releases/download/v3.0.6/VasDolly.jar
# 放到 resources 文件夹
```

5. **运行打包脚本**
```cmd
python build.py
```

6. **获取exe文件**
   - 打包完成后，exe文件在 `dist/VasDollyTool.exe`

---

## 方案3：使用虚拟机或云服务

### 使用Windows虚拟机：
- Parallels Desktop (Mac上运行Windows)
- VirtualBox
- VMware Fusion

### 使用云服务：
- AWS Windows实例
- Azure Windows虚拟机
- 阿里云Windows ECS

---

## 打包参数说明

当前的打包配置（在 `build.py` 中）：

```python
--windowed      # 无控制台窗口
--onefile       # 单文件exe
--clean         # 清理临时文件
```

**包含内容：**
- ✅ VasDolly.jar
- ✅ Windows JRE（如果存在）
- ✅ 所有Python依赖

**预计文件大小：**
- 不含JRE: ~15-20MB
- 含JRE: ~60-80MB

---

## 推荐方案对比

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| GitHub Actions | 全自动、支持多平台、无需本地环境 | 需要GitHub账号 | ⭐⭐⭐⭐⭐ |
| Windows机器 | 完全控制、可调试 | 需要Windows环境 | ⭐⭐⭐⭐ |
| 虚拟机 | 可在Mac上操作 | 占用资源、配置复杂 | ⭐⭐⭐ |

---

## 快速开始（推荐）

**最简单的方式：**

1. 推送代码到GitHub
2. 访问 Actions 页面
3. 点击 "Run workflow"
4. 等待10分钟
5. 下载Windows版本

就这么简单！🎉

