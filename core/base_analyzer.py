from abc import ABC, abstractmethod
from typing import Dict, Any, List
import pandas as pd

class BaseAnalyzer(ABC):
    """抽象分析基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    @abstractmethod
    def analyze_basic_stats(self, df: pd.DataFrame, target_address: str) -> Dict:
        """基础统计分析的抽象方法"""
        pass
        
    @abstractmethod
    def get_top_counterparties(self, df: pd.DataFrame, limit: int = 5) -> pd.Series:
        """获取主要交易对手的抽象方法"""
        pass
        
    @abstractmethod
    def generate_analysis_report(self, df: pd.DataFrame, target_address: str) -> Dict:
        """生成完整分析报告的抽象方法"""
        pass