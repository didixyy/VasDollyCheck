# Resources 目录说明

本目录用于存放应用所需的资源文件。

## 📁 目录结构

```
resources/
├── VasDolly.jar          # VasDolly命令行工具（必需）
├── jre/                  # Java运行时环境（可选）
│   ├── windows/          # Windows JRE
│   └── macos/            # macOS JRE
└── icons/                # 应用图标（可选）
    ├── app_icon.ico      # Windows图标
    └── app_icon.icns     # macOS图标
```

## 🔧 VasDolly.jar（必需）

### 下载地址
https://github.com/Tencent/VasDolly/releases

### 安装步骤
1. 访问上述地址
2. 下载最新版本的 `VasDolly.jar`
3. 将jar文件放到本目录（resources/）

### 验证
确保文件路径为：`resources/VasDolly.jar`

## ☕ JRE - Java运行时环境（可选）

### 为什么需要？
- 如果打包时包含JRE，用户无需单独安装Java
- 提升用户体验，开箱即用
- 缺点：会增加打包体积（约40-60MB）

### 不包含JRE的方案
如果不包含JRE，需要提示用户自行安装Java：
- 下载地址: https://adoptium.net/
- 要求版本: JRE 8 或更高

### 包含JRE的方案

#### Windows平台
1. 下载OpenJDK JRE (Windows x64)
   - 推荐: https://adoptium.net/
   - 选择: JRE 8/11/17 (x64)

2. 解压到指定目录
   ```
   resources/jre/windows/
   └── bin/
       └── java.exe
   ```

3. 确保目录结构正确
   ```
   resources/jre/windows/bin/java.exe
   ```

#### macOS平台
1. 下载OpenJDK JRE (macOS)
   - 推荐: https://adoptium.net/
   - 选择: JRE 8/11/17 (macOS)

2. 解压到指定目录
   ```
   resources/jre/macos/
   └── bin/
       └── java
   ```

3. 确保目录结构正确
   ```
   resources/jre/macos/bin/java
   ```

### 精简JRE（高级）

如果想要更小的体积，可以使用jlink创建精简JRE：

```bash
# 创建只包含必要模块的JRE
jlink --add-modules java.base,java.desktop \
      --output jre-minimal \
      --strip-debug \
      --compress=2 \
      --no-header-files \
      --no-man-pages
```

体积对比：
- 完整JRE: 约200MB
- 标准JRE: 约40-60MB
- 精简JRE: 约30MB

## 🎨 应用图标（可选）

### Windows图标 (.ico)
1. 准备图标文件: `app_icon.ico`
2. 建议尺寸: 256x256 或包含多种尺寸
3. 放置路径: `resources/icons/app_icon.ico`

### macOS图标 (.icns)
1. 准备图标文件: `app_icon.icns`
2. 建议尺寸: 512x512
3. 放置路径: `resources/icons/app_icon.icns`

### 制作图标
- 在线工具: https://convertio.co/zh/
- 本地工具: 
  - Windows: IcoFX
  - macOS: Image2Icon

## 📋 检查清单

打包前检查：

- [ ] `VasDolly.jar` 已放置 ✅ 必需
- [ ] Windows JRE 已配置（可选）
- [ ] macOS JRE 已配置（可选）
- [ ] Windows图标已配置（可选）
- [ ] macOS图标已配置（可选）

## 🔍 故障排除

### 问题：程序提示"未找到VasDolly.jar"
**解决**：
1. 确认jar文件在正确位置
2. 检查文件名拼写
3. 确认文件有读取权限

### 问题：程序提示"未找到Java环境"
**解决**：
- 方案1: 安装系统Java环境
- 方案2: 配置内置JRE并重新打包

### 问题：打包后文件太大
**解决**：
1. 不包含JRE（减少40MB+）
2. 使用精简JRE（减少10-20MB）
3. 排除不需要的Python模块

## 📚 相关链接

- VasDolly官方: https://github.com/Tencent/VasDolly
- OpenJDK下载: https://adoptium.net/
- Java官网: https://www.java.com/

---

**提示**: 如果只是开发测试，可以只准备 `VasDolly.jar`，其他资源文件在实际打包发布时再配置。

