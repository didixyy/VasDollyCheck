"""Java运行时管理模块"""
import os
import subprocess
import platform
from pathlib import Path
from typing import Tuple, Optional
from utils.logger import logger
from utils.file_helper import FileHelper


class JavaRunner:
    """Java运行时管理器"""
    
    def __init__(self):
        """初始化Java运行时"""
        self.java_path = None
        self.vasdolly_jar = None
        self.system = platform.system()
        
        try:
            self.java_path = self._find_java()
            self.vasdolly_jar = self._find_vasdolly_jar()
            logger.info(f"Java路径: {self.java_path}")
            logger.info(f"VasDolly路径: {self.vasdolly_jar}")
        except Exception as e:
            logger.error(f"初始化失败: {str(e)}")
            raise
    
    def _find_java(self) -> str:
        """
        查找Java可执行文件
        优先级: 1. 系统Java  2. 内置JRE
        """
        # 1. 尝试系统Java
        try:
            java_cmd = 'java.exe' if self.system == 'Windows' else 'java'
            result = subprocess.run(
                [java_cmd, '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                logger.info("检测到系统Java环境")
                return java_cmd
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
            logger.warning(f"未找到系统Java: {str(e)}")
        
        # 2. 使用内置JRE
        logger.info("尝试使用内置JRE...")
        if self.system == 'Windows':
            java_exe = FileHelper.get_resource_path('resources/jre/windows/bin/java.exe')
        elif self.system == 'Darwin':  # macOS
            java_exe = FileHelper.get_resource_path('resources/jre/macos/bin/java')
        else:  # Linux
            java_exe = FileHelper.get_resource_path('resources/jre/linux/bin/java')
        
        if os.path.exists(java_exe):
            logger.info(f"使用内置JRE: {java_exe}")
            # 确保可执行权限（Unix系统）
            if self.system != 'Windows':
                try:
                    os.chmod(java_exe, 0o755)
                except Exception:
                    pass
            return java_exe
        
        raise Exception(
            "未找到Java环境！\n\n"
            "请选择以下方式之一：\n"
            "1. 安装Java运行环境 (JRE 8+)\n"
            "2. 下载包含JRE的完整版本\n\n"
            "Java下载地址: https://adoptium.net/"
        )
    
    def _find_vasdolly_jar(self) -> str:
        """查找VasDolly jar文件"""
        # 尝试多个可能的位置
        possible_paths = [
            FileHelper.get_resource_path('resources/VasDolly.jar'),
            FileHelper.get_resource_path('VasDolly.jar'),
            'resources/VasDolly.jar',
            'VasDolly.jar',
        ]
        
        for jar_path in possible_paths:
            if os.path.exists(jar_path):
                logger.info(f"找到VasDolly.jar: {jar_path}")
                return jar_path
        
        raise Exception(
            "未找到VasDolly.jar！\n\n"
            "请从以下地址下载VasDolly.jar并放到resources目录：\n"
            "https://github.com/Tencent/VasDolly/releases\n\n"
            "或将jar文件放在程序同目录下"
        )
    
    def check_environment(self) -> Tuple[bool, str]:
        """
        检查运行环境
        Returns: (是否正常, 消息)
        """
        try:
            if not self.java_path:
                return False, "Java环境未初始化"
            
            if not self.vasdolly_jar:
                return False, "VasDolly.jar未找到"
            
            # 测试Java命令
            result = subprocess.run(
                [self.java_path, '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                return False, "Java命令执行失败"
            
            return True, "环境检查通过"
            
        except Exception as e:
            return False, f"环境检查失败: {str(e)}"
    
    def run_command(self, args: list, timeout: int = 60) -> Tuple[str, str, int]:
        """
        执行VasDolly命令
        
        Args:
            args: 命令参数列表
            timeout: 超时时间（秒）
            
        Returns:
            (stdout, stderr, returncode)
        """
        if not self.java_path or not self.vasdolly_jar:
            raise Exception("Java环境未正确初始化")
        
        cmd = [self.java_path, '-jar', self.vasdolly_jar] + args
        logger.info(f"执行命令: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding='utf-8',
                errors='ignore'
            )
            
            logger.debug(f"命令返回码: {result.returncode}")
            if result.stdout:
                logger.debug(f"标准输出: {result.stdout}")
            if result.stderr:
                logger.debug(f"标准错误: {result.stderr}")
            
            return result.stdout, result.stderr, result.returncode
            
        except subprocess.TimeoutExpired:
            error_msg = f"命令执行超时（{timeout}秒）"
            logger.error(error_msg)
            return "", error_msg, -1
        except Exception as e:
            error_msg = f"命令执行失败: {str(e)}"
            logger.error(error_msg)
            return "", error_msg, -1
    
    def get_java_version(self) -> Optional[str]:
        """获取Java版本信息"""
        try:
            result = subprocess.run(
                [self.java_path, '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            # Java版本信息通常在stderr中
            version_output = result.stderr if result.stderr else result.stdout
            # 提取第一行
            first_line = version_output.split('\n')[0] if version_output else ""
            return first_line.strip()
        except Exception as e:
            logger.error(f"获取Java版本失败: {str(e)}")
            return None

