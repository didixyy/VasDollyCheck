"""GUI组件模块"""
import tkinter as tk
from typing import Callable


class FileSelectFrame(tk.Frame):
    """文件选择框架组件"""
    
    def __init__(
        self,
        parent,
        label_text: str,
        button_text: str = "浏览",
        on_select: Callable = None,
        file_types: list = None,
        title: str = "选择文件",
        **kwargs
    ):
        super().__init__(parent, **kwargs)
        
        self.on_select = on_select
        self.selected_file = None
        self.file_types = file_types or [("所有文件", "*.*")]
        self.title = title
        
        # 标签
        self.label = tk.Label(self, text=label_text, width=10, anchor='w')
        self.label.pack(side='left', padx=5)
        
        # 文件路径输入框
        self.entry = tk.Entry(self, state='readonly')
        self.entry.pack(side='left', fill='x', expand=True, padx=5)
        
        # 浏览按钮
        self.button = tk.Button(
            self,
            text=button_text,
            command=self._on_button_click,
            width=8
        )
        self.button.pack(side='right', padx=5)
    
    def _on_button_click(self):
        """按钮点击事件"""
        from tkinter import filedialog
        import os
        
        # 打开文件选择对话框
        initial_dir = os.path.dirname(self.selected_file) if self.selected_file else os.path.expanduser("~")
        file_path = filedialog.askopenfilename(
            title=self.title,
            initialdir=initial_dir,
            filetypes=self.file_types
        )
        
        if file_path:
            self.set_file(file_path)
            # 调用回调函数，传递文件路径
            if self.on_select:
                self.on_select(file_path)
    
    def set_file(self, file_path: str):
        """设置选中的文件"""
        self.selected_file = file_path
        self.entry.configure(state='normal')
        self.entry.delete(0, 'end')
        self.entry.insert(0, file_path)
        self.entry.configure(state='readonly')
    
    def get_file(self) -> str:
        """获取选中的文件"""
        return self.selected_file
    
    def clear(self):
        """清空选择"""
        self.selected_file = None
        self.entry.configure(state='normal')
        self.entry.delete(0, 'end')
        self.entry.configure(state='readonly')

