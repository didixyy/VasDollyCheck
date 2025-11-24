# VasDolly渠道解析工具

简洁的APK渠道信息解析工具，基于VasDolly。

## 功能特点

- ✅ 极简界面，一键解析APK渠道信息
- ✅ 自动复制结果到剪贴板
- ✅ 支持Windows和macOS
- ✅ 内置JRE，无需安装Java
- ✅ 显示渠道名称、详细信息、长度等完整信息

## 快速开始

### 使用方法

1. 运行程序
2. 点击"选择 APK 文件"按钮
3. 选择要解析的APK文件
4. 自动弹出对话框显示渠道信息
5. 结果已自动复制到剪贴板

### 开发模式运行

```bash
# 安装依赖
pip install pyinstaller

# 运行程序
python3 src/main.py
```

## 打包可执行文件

### 本地打包

```bash
# 打包当前平台版本
python build.py

# 输出：
# macOS: dist/VasDollyTool.app
# Windows: dist/VasDollyTool.exe
```

### 使用GitHub Actions自动构建（推荐）

1. 推送代码到GitHub
2. 访问 Actions 页面
3. 运行 "Build VasDolly Tool" workflow
4. 下载生成的Windows和macOS版本

详见：[如何打包Windows版本.md](如何打包Windows版本.md)

## 项目结构

```
channel/
├── src/                    # 源代码
│   ├── main.py            # 程序入口
│   ├── gui/               # 图形界面
│   ├── core/              # 核心功能
│   └── utils/             # 工具函数
├── resources/             # 资源文件
│   ├── VasDolly.jar      # VasDolly工具
│   └── jre/              # JRE运行环境（可选）
├── .github/workflows/     # GitHub Actions配置
├── build.py               # 打包脚本
└── requirements.txt       # Python依赖
```

## 技术栈

- **Python 3.8+**
- **Tkinter** - GUI界面
- **PyInstaller** - 打包工具
- **VasDolly** - 渠道解析核心（腾讯开源）

## 相关链接

- [VasDolly官方](https://github.com/Tencent/VasDolly)

## 许可证

MIT License
