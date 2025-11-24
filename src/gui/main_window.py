"""主窗口模块"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from pathlib import Path

from gui.components import FileSelectFrame
from core.channel_parser import ChannelParser
from utils.logger import logger
from utils.file_helper import FileHelper


class MainWindow:
    """主窗口类"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("VasDolly 渠道解析")
        self.root.geometry("400x150")
        self.root.minsize(350, 120)
        self.root.resizable(False, False)
        
        # 配置文件路径
        self.config_file = 'config/config.json'
        self.config = self._load_config()
        
        # 核心组件
        self.parser = None
        
        # 初始化UI
        self._init_ui()
        
        # 初始化核心组件（异步）
        self._init_core_async()
        
        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _init_ui(self):
        """初始化UI界面"""
        # 主框架（不使用标签页）
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)
        
        # 创建按钮
        self._create_main_button()
        
        # 状态栏
        self.status_bar = tk.Label(
            self.root,
            text="就绪",
            bd=1,
            relief='sunken',
            anchor='w'
        )
        self.status_bar.pack(side='bottom', fill='x')
    
    def _create_main_button(self):
        """创建主按钮"""
        # 使用place布局，让按钮精确居中
        self.select_button = tk.Button(
            self.main_frame,
            text="选择 APK 文件",
            command=self._select_and_parse_apk,
            font=('Arial', 16, 'bold'),
            bg='#4CAF50',
            fg='white',
            activebackground='#45a049',
            relief='raised',
            bd=3,
            cursor='hand2'
        )
        # 按钮位置：在垂直中间，高度为窗口的一半，四周留间距
        self.select_button.place(
            relx=0.5,      # 水平居中
            rely=0.5,      # 垂直居中
            relwidth=0.92, # 宽度占92%（左右各留4%间距）
            relheight=0.4, # 高度为40%（上下各留30%间距）
            anchor='center'
        )
    
    def _init_core_async(self):
        """异步初始化核心组件"""
        def init():
            self._update_status("正在初始化...")
            try:
                self.parser = ChannelParser()
                self._update_status("初始化完成，就绪")
                
                # 显示Java版本
                java_version = self.parser.runner.get_java_version()
                if java_version:
                    self._update_status(f"Java环境: {java_version}")
                
            except Exception as e:
                error_msg = str(e)
                self._update_status(f"初始化失败: {error_msg}")
                messagebox.showerror("初始化失败", error_msg)
                logger.error(f"初始化失败: {error_msg}")
        
        thread = threading.Thread(target=init, daemon=True)
        thread.start()
    
    def _select_and_parse_apk(self):
        """选择APK文件并自动解析"""
        from tkinter import filedialog
        
        initial_dir = self.config.get('last_apk_dir', os.path.expanduser("~"))
        file_path = filedialog.askopenfilename(
            title="选择APK文件",
            initialdir=initial_dir,
            filetypes=[("APK文件", "*.apk"), ("所有文件", "*.*")]
        )
        
        if file_path:
            logger.info(f"选择APK文件: {file_path}")
            # 保存目录到配置
            self.config['last_apk_dir'] = os.path.dirname(file_path)
            # 自动开始解析
            self._do_parse_apk(file_path)
    
    def _do_parse_apk(self, apk_path):
        """执行渠道解析"""
        if not self.parser:
            messagebox.showerror("错误", "工具尚未初始化完成")
            return
        
        # 更新状态和按钮
        self._update_status("正在解析...")
        self.select_button.configure(text="解析中...", state='disabled')
        logger.info("正在解析...")
        
        # 异步执行解析
        def parse_thread():
            try:
                channel_info = self.parser.get_channel(apk_path)
                self.root.after(0, lambda: self._on_parse_success(channel_info))
            except Exception as e:
                self.root.after(0, lambda: self._on_parse_error(str(e)))
        
        threading.Thread(target=parse_thread, daemon=True).start()
    
    def _on_parse_success(self, channel_info):
        """解析成功回调"""
        logger.debug(f"GUI收到的channel_info: {channel_info}")
        self._update_status("解析完成")
        self.select_button.configure(text="选择 APK 文件", state='normal')
        
        # 格式化文本
        result_text = f"""渠道名称: {channel_info.get('channel', '未知')}
详细信息: {channel_info.get('详细信息', '未知')}
渠道长度: {channel_info.get('长度', '未知')}

文件名: {channel_info.get('file', '未知')}
文件大小: {channel_info.get('size', '未知')}"""
        
        # 复制到剪贴板
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(result_text)
            clipboard_msg = "\n\n✅ 已复制到剪贴板"
        except:
            clipboard_msg = ""
        
        # 使用系统消息框显示
        messagebox.showinfo("解析成功", result_text + clipboard_msg)
    
    def _on_parse_error(self, error_msg):
        """解析失败回调"""
        self._update_status(f"解析失败: {error_msg}")
        self.select_button.configure(text="选择 APK 文件", state='normal')
        messagebox.showerror("解析失败", f"无法解析APK渠道信息:\n\n{error_msg}")
    
    def _clear_parse(self):
        """清空解析界面"""
        self._update_status("就绪")
    
    def _open_directory(self, dir_path):
        """打开目录"""
        import sys
        import subprocess
        
        try:
            if sys.platform == 'darwin':  # macOS
                subprocess.run(['open', dir_path])
            elif sys.platform == 'win32':  # Windows
                os.startfile(dir_path)
            else:  # Linux
                subprocess.run(['xdg-open', dir_path])
        except Exception as e:
            logger.error(f"打开目录失败: {str(e)}")
    
    def _update_status(self, message):
        """更新状态栏"""
        self.status_bar.configure(text=message)
        logger.info(message)
    
    def _load_config(self):
        """加载配置文件"""
        return FileHelper.read_json(self.config_file)
    
    def _save_config(self):
        """保存配置文件"""
        try:
            FileHelper.write_json(self.config_file, self.config)
        except Exception as e:
            logger.error(f"保存配置失败: {str(e)}")
    
    def _on_closing(self):
        """窗口关闭事件"""
        self._save_config()
        self.root.destroy()

