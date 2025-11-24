"""文件操作辅助模块"""
import os
import json
from pathlib import Path
from typing import Dict, Any


class FileHelper:
    """文件操作辅助类"""
    
    @staticmethod
    def read_json(file_path: str) -> Dict[str, Any]:
        """读取JSON文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}
    
    @staticmethod
    def write_json(file_path: str, data: Dict[str, Any]):
        """写入JSON文件"""
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def ensure_dir(dir_path: str):
        """确保目录存在"""
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def get_file_size(file_path: str) -> str:
        """获取文件大小（人类可读格式）"""
        size = os.path.getsize(file_path)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"
    
    @staticmethod
    def is_apk_file(file_path: str) -> bool:
        """检查是否是APK文件"""
        return file_path.lower().endswith('.apk') and os.path.isfile(file_path)
    
    @staticmethod
    def get_resource_path(relative_path: str) -> str:
        """获取资源文件路径（支持打包后的路径）"""
        try:
            # PyInstaller创建的临时文件夹路径
            import sys
            if hasattr(sys, '_MEIPASS'):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)
        except Exception:
            return relative_path

