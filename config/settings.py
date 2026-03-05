"""
Configuration Management for found-trx-adress
Loads configuration from environment variables and config files
"""

import os
import json
from typing import Dict, Any
from pathlib import Path

class Config:
    """配置管理类"""
    
    def __init__(self, config_file: str = None):
        """
        初始化配置
        
        Args:
            config_file: 配置文件路径（可选）
        """
        self.config = {}
        
        # 从配置文件加载
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                self.config = json.load(f)
        
        # 从环境变量加载（优先级更高）
        self._load_from_env()
    
    def _load_from_env(self):
        """从环境变量加载配置"""
        # TRON 配置
        if os.getenv('TRON_API_KEY'):
            self.config['tron'] = self.config.get('tron', {})
            self.config['tron']['api_key'] = os.getenv('TRON_API_KEY')
        
        # Binance 配置
        if os.getenv('BINANCE_API_KEY'):
            self.config['binance'] = self.config.get('binance', {})
            self.config['binance']['api_key'] = os.getenv('BINANCE_API_KEY')
        
        if os.getenv('BINANCE_API_SECRET'):
            self.config['binance'] = self.config.get('binance', {})
            self.config['binance']['api_secret'] = os.getenv('BINANCE_API_SECRET')
        
        # 通用配置
        if os.getenv('OUTPUT_FORMAT'):
            self.config['output_format'] = os.getenv('OUTPUT_FORMAT')
        
        if os.getenv('OUTPUT_DIR'):
            self.config['output_dir'] = os.getenv('OUTPUT_DIR')
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键（支持点号分隔，如 'tron.api_key'）
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_tron_config(self) -> Dict[str, Any]:
        """获取 TRON 配置"""
        return self.config.get('tron', {})
    
    def get_binance_config(self) -> Dict[str, Any]:
        """获取 Binance 配置"""
        return self.config.get('binance', {})
    
    def save(self, config_file: str):
        """
        保存配置到文件
        
        Args:
            config_file: 配置文件路径
        """
        # 确保目录存在
        Path(config_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def __repr__(self):
        return f"Config({self.config})"


# 快捷函数
def load_config(config_file: str = None) -> Config:
    """
    加载配置
    
    Args:
        config_file: 配置文件路径
        
    Returns:
        Config 对象
    """
    # 默认配置文件路径
    if config_file is None:
        config_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'config',
            'settings.json'
        )
    
    return Config(config_file)


def get_tron_api_key() -> str:
    """获取 TRON API key"""
    return os.getenv('TRON_API_KEY', '')


def get_binance_credentials() -> tuple:
    """获取 Binance 凭证"""
    return (
        os.getenv('BINANCE_API_KEY', ''),
        os.getenv('BINANCE_API_SECRET', '')
    )
