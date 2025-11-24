"""
打包脚本 - 使用PyInstaller打包应用

使用方法：
    python build.py

输出：
    Windows: dist/VasDollyTool.exe
    macOS: dist/VasDollyTool.app
"""
import os
import sys
import platform
import shutil
from pathlib import Path

# 修复Windows控制台编码问题
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def clean_build():
    """清理构建目录"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['*.spec']
    
    print("清理旧的构建文件...")
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  删除目录: {dir_name}")
    
    for pattern in files_to_clean:
        import glob
        for file in glob.glob(pattern):
            os.remove(file)
            print(f"  删除文件: {file}")


def check_dependencies():
    """检查依赖"""
    print("检查依赖...")
    try:
        import PyInstaller
        print(f"  PyInstaller: {PyInstaller.__version__}")
    except ImportError:
        print("  错误: 未安装PyInstaller")
        print("  请运行: pip install pyinstaller")
        sys.exit(1)
    
    # 检查资源文件
    if not os.path.exists('resources/VasDolly.jar'):
        print("\n警告: 未找到 resources/VasDolly.jar")
        print("请从以下地址下载并放到 resources 目录：")
        print("https://github.com/Tencent/VasDolly/releases")
        print("\n继续打包将生成不包含VasDolly.jar的版本")
        input("按Enter继续...")


def build():
    """执行打包"""
    system = platform.system()
    print(f"\n开始打包 ({system})...")
    
    # PyInstaller命令参数
    args = [
        'src/main.py',
        '--name=VasDollyTool',
        # '--windowed',  # 暂时保留控制台窗口，方便调试
        '--onefile',   # 打包成单文件
        '--clean',     # 清理临时文件
        '--noconfirm', # 不确认覆盖
    ]
    
    # 添加资源文件
    if os.path.exists('resources/VasDolly.jar'):
        if system == 'Windows':
            args.append('--add-data=resources/VasDolly.jar;resources')
        else:
            args.append('--add-data=resources/VasDolly.jar:resources')
        print("  包含: VasDolly.jar")
    
    # 添加JRE（如果存在）
    if system == 'Windows' and os.path.exists('resources/jre/windows'):
        args.append('--add-data=resources/jre/windows;resources/jre/windows')
        print("  包含: Windows JRE")
    elif system == 'Darwin' and os.path.exists('resources/jre/macos'):
        args.append('--add-data=resources/jre/macos:resources/jre/macos')
        print("  包含: macOS JRE")
    
    # 添加图标（如果存在）
    if system == 'Windows' and os.path.exists('resources/icons/app_icon.ico'):
        args.append('--icon=resources/icons/app_icon.ico')
        print("  包含: 应用图标")
    elif system == 'Darwin' and os.path.exists('resources/icons/app_icon.icns'):
        args.append('--icon=resources/icons/app_icon.icns')
        print("  包含: 应用图标")
    
    # 添加隐藏导入（确保所有模块被打包）
    hidden_imports = [
        'src',
        'src.gui',
        'src.gui.main_window',
        'src.gui.components',
        'src.core',
        'src.core.java_runner',
        'src.core.channel_parser',
        'src.utils',
        'src.utils.logger',
        'src.utils.file_helper',
    ]
    for module in hidden_imports:
        args.append(f'--hidden-import={module}')
    
    # 排除不需要的模块（减小体积）
    exclude_modules = [
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'pytest',
    ]
    for module in exclude_modules:
        args.append(f'--exclude-module={module}')
    
    # 执行PyInstaller
    print("\n执行PyInstaller...")
    print(f"命令: pyinstaller {' '.join(args)}")
    
    import PyInstaller.__main__
    PyInstaller.__main__.run(args)
    
    print("\n打包完成！")
    
    # 输出结果
    if system == 'Windows':
        output = 'dist/VasDollyTool.exe'
    elif system == 'Darwin':
        output = 'dist/VasDollyTool.app'
    else:
        output = 'dist/VasDollyTool'
    
    if os.path.exists(output):
        size = os.path.getsize(output) if os.path.isfile(output) else get_dir_size(output)
        size_mb = size / (1024 * 1024)
        print(f"输出文件: {output}")
        print(f"文件大小: {size_mb:.2f} MB")
    else:
        print(f"警告: 未找到输出文件 {output}")


def get_dir_size(path):
    """获取目录大小"""
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += get_dir_size(entry.path)
    return total


def create_resources_structure():
    """创建资源目录结构"""
    print("\n创建资源目录结构...")
    
    dirs = [
        'resources',
        'resources/icons',
        'resources/jre',
        'config',
        'logs',
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"  创建目录: {dir_path}")
    
    # 创建README
    if not os.path.exists('resources/README.md'):
        with open('resources/README.md', 'w', encoding='utf-8') as f:
            f.write("""# Resources 目录说明

## VasDolly.jar
从官方下载VasDolly命令行工具：
https://github.com/Tencent/VasDolly/releases

下载后放到此目录

## JRE (可选)
如果要打包包含JRE的版本，需要：

### Windows
下载JRE并解压到: resources/jre/windows/

### macOS
下载JRE并解压到: resources/jre/macos/

### 推荐JRE
- OpenJDK JRE 8+ (轻量版约40MB)
- 下载地址: https://adoptium.net/

## Icons (可选)
应用图标：
- Windows: app_icon.ico
- macOS: app_icon.icns
""")
        print(f"  创建文件: resources/README.md")


def main():
    """主函数"""
    print("=" * 60)
    print("VasDolly工具 - 打包脚本")
    print("=" * 60)
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("错误: 需要Python 3.8或更高版本")
        sys.exit(1)
    
    # 创建资源目录
    create_resources_structure()
    
    # 检查依赖
    check_dependencies()
    
    # 清理旧文件
    clean_build()
    
    # 执行打包
    build()
    
    print("\n" + "=" * 60)
    print("打包流程完成！")
    print("=" * 60)
    print("\n下一步：")
    print("1. 测试运行打包后的程序")
    print("2. 如果需要JRE，请下载并放到resources/jre目录后重新打包")
    print("3. 如果需要自定义图标，请准备.ico/.icns文件后重新打包")


if __name__ == '__main__':
    main()

