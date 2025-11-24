"""渠道解析模块"""
import os
from typing import Dict, Optional
from core.java_runner import JavaRunner
from utils.logger import logger
from utils.file_helper import FileHelper


class ChannelParser:
    """APK渠道信息解析器"""
    
    def __init__(self):
        """初始化解析器"""
        self.runner = JavaRunner()
    
    def get_channel(self, apk_path: str) -> Dict[str, str]:
        """
        解析APK渠道信息
        
        Args:
            apk_path: APK文件路径
            
        Returns:
            渠道信息字典
            
        Raises:
            Exception: 解析失败时抛出异常
        """
        # 验证APK文件
        if not FileHelper.is_apk_file(apk_path):
            raise Exception(f"无效的APK文件: {apk_path}")
        
        logger.info(f"开始解析APK渠道: {apk_path}")
        
        # 执行VasDolly get命令
        args = ['get', '-c', apk_path]
        stdout, stderr, code = self.runner.run_command(args)
        
        if code != 0:
            error_msg = stderr if stderr else "解析失败"
            logger.error(f"解析失败: {error_msg}")
            raise Exception(f"解析失败: {error_msg}")
        
        # 解析输出
        channel_info = self._parse_output(stdout)
        
        if not channel_info or 'channel' not in channel_info:
            # 可能没有渠道信息
            logger.warning("APK中未找到渠道信息")
            return {
                'channel': '无渠道信息',
                'status': '该APK未包含渠道标识',
                'file': os.path.basename(apk_path),
                'size': FileHelper.get_file_size(apk_path)
            }
        
        # 过滤掉调试信息，只保留有用的字段
        filtered_info = {}
        useful_keys = ['channel', '详细信息', '长度', 'file', 'size']
        for key in useful_keys:
            if key in channel_info:
                filtered_info[key] = channel_info[key]
        
        # 添加文件信息
        filtered_info['file'] = os.path.basename(apk_path)
        filtered_info['size'] = FileHelper.get_file_size(apk_path)
        
        logger.info(f"解析成功，渠道: {filtered_info.get('channel', '未知')}")
        logger.debug(f"返回的channel_info字典内容: {filtered_info}")
        return filtered_info
    
    def _parse_output(self, output: str) -> Dict[str, str]:
        """
        解析VasDolly命令输出
        
        VasDolly输出格式示例：
        Channel: xiaomi,len=7
        或者多行键值对
        
        Args:
            output: 命令输出字符串
            
        Returns:
            解析后的字典
        """
        channel_info = {}
        
        if not output or not output.strip():
            return channel_info
        
        lines = output.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # VasDolly特殊格式: Channel: xxx,len=N
            if line.startswith('Channel:') or line.startswith('channel:'):
                # 提取完整的渠道信息（包括len）
                channel_str = line.split(':', 1)[1].strip()
                
                # 提取渠道名（用于channel字段）
                if ',' in channel_str:
                    channel_name = channel_str.split(',')[0].strip()
                    # 提取长度信息
                    len_part = channel_str.split(',', 1)[1].strip()
                    channel_info['channel'] = channel_name
                    channel_info['详细信息'] = channel_str  # 保存完整信息
                    if len_part.startswith('len='):
                        channel_info['长度'] = len_part.split('=')[1]
                else:
                    channel_info['channel'] = channel_str.strip()
                continue
            
            # 解析键值对 (key: value 或 key=value)
            if ':' in line and not line.startswith('try to') and not line.startswith('get'):
                parts = line.split(':', 1)
                key = parts[0].strip()
                value = parts[1].strip() if len(parts) > 1 else ''
                if key and value:
                    channel_info[key.lower()] = value
            elif '=' in line:
                parts = line.split('=', 1)
                key = parts[0].strip()
                value = parts[1].strip() if len(parts) > 1 else ''
                if key and value:
                    channel_info[key.lower()] = value
        
        return channel_info
    
    def check_apk_signature(self, apk_path: str) -> bool:
        """
        检查APK签名方案（VasDolly需要v2签名）
        
        Args:
            apk_path: APK文件路径
            
        Returns:
            是否支持v2签名
        """
        # 这个功能需要使用apksigner工具，这里简化处理
        # 实际项目中可以集成apksigner检查
        logger.info(f"检查APK签名: {apk_path}")
        return True
    
    def batch_parse(self, apk_paths: list) -> Dict[str, Dict]:
        """
        批量解析多个APK
        
        Args:
            apk_paths: APK文件路径列表
            
        Returns:
            {apk_path: channel_info} 字典
        """
        results = {}
        
        for apk_path in apk_paths:
            try:
                channel_info = self.get_channel(apk_path)
                results[apk_path] = {
                    'success': True,
                    'data': channel_info
                }
            except Exception as e:
                logger.error(f"解析 {apk_path} 失败: {str(e)}")
                results[apk_path] = {
                    'success': False,
                    'error': str(e)
                }
        
        return results

