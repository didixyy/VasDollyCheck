"""
VasDolly渠道解析工具 - 主程序入口

简洁的APK渠道信息解析工具
支持Windows和Mac平台，无需配置Java环境
"""
import sys
import os
import tkinter as tk
from tkinter import messagebox

# 添加src目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow
from utils.logger import logger


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
        error_msg = f"程序启动失败: {str(e)}"
        logger.critical(error_msg)
        
        # 显示错误对话框
        try:
            root = tk.Tk()
            root.withdraw()  # 隐藏主窗口
            messagebox.showerror("错误", error_msg)
        except Exception:
            print(error_msg)
        
        sys.exit(1)


if __name__ == '__main__':
    main()

