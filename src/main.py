"""
VasDolly渠道解析工具 - 主程序入口

简洁的APK渠道信息解析工具
支持Windows和Mac平台，无需配置Java环境
"""
import sys
import os
import traceback
import tkinter as tk
from tkinter import messagebox

# 添加项目根目录到Python路径
if getattr(sys, 'frozen', False):
    # 打包后的环境
    base_path = sys._MEIPASS
else:
    # 开发环境
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, base_path)
sys.path.insert(0, os.path.join(base_path, 'src'))

try:
    from src.gui.main_window import MainWindow
    from src.utils.logger import logger
except ImportError:
    # 备用导入方式
    from gui.main_window import MainWindow
    from utils.logger import logger


def write_error_log(error_msg: str):
    """将错误写入日志文件"""
    try:
        log_file = os.path.join(os.path.expanduser('~'), 'VasDollyTool_error.log')
        with open(log_file, 'a', encoding='utf-8') as f:
            import datetime
            f.write(f"\n{'='*60}\n")
            f.write(f"时间: {datetime.datetime.now()}\n")
            f.write(f"错误: {error_msg}\n")
            f.write(f"{'='*60}\n")
        return log_file
    except:
        return None


def main():
    """主函数"""
    try:
        # 创建主窗口
        root = tk.Tk()
        
        # 设置图标（如果存在）
        try:
            # 这里可以添加图标设置
            pass
        except Exception:
            pass
        
        # 创建应用
        app = MainWindow(root)
        
        logger.info("VasDolly工具已启动")
        
        # 运行主循环
        root.mainloop()
        
    except Exception as e:
        error_msg = f"程序启动失败: {str(e)}\n\n详细信息:\n{traceback.format_exc()}"
        
        # 写入日志文件
        log_file = write_error_log(error_msg)
        
        try:
            logger.critical(error_msg)
        except:
            pass
        
        # 显示错误对话框
        try:
            root = tk.Tk()
            root.withdraw()  # 隐藏主窗口
            msg = f"程序启动失败: {str(e)}"
            if log_file:
                msg += f"\n\n详细日志已保存到:\n{log_file}"
            messagebox.showerror("错误", msg)
        except Exception:
            print(error_msg)
        
        sys.exit(1)


if __name__ == '__main__':
    main()

