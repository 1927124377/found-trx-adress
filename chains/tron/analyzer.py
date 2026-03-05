"""
TRON Blockchain Analyzer
Implements BaseAnalyzer for TRX transaction analysis
"""

from core.base_analyzer import BaseAnalyzer
from typing import Dict, Any, List
import pandas as pd
from datetime import datetime

class TronAnalyzer(BaseAnalyzer):
    """TRON 区块链分析器实现"""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化 TRON 分析器
        
        Args:
            config: 配置字典
        """
        if config is None:
            config = {}
        super().__init__(config)
    
    def analyze_basic_stats(self, df: pd.DataFrame, target_address: str) -> Dict:
        """
        基础统计分析
        
        Args:
            df: 交易数据 DataFrame
            target_address: 目标地址
            
        Returns:
            统计信息字典
        """
        if df.empty:
            return {'error': 'No transaction data'}
        
        # 计算基础统计
        stats = {
            'address': target_address,
            'total_transactions': len(df),
            'total_amount': df['amount'].sum() if 'amount' in df.columns else 0,
            'avg_amount': df['amount'].mean() if 'amount' in df.columns else 0,
            'max_amount': df['amount'].max() if 'amount' in df.columns else 0,
            'min_amount': df['amount'].min() if 'amount' in df.columns else 0,
            'total_fees': df['fee'].sum() if 'fee' in df.columns else 0,
        }
        
        # 时间范围
        if 'timestamp' in df.columns:
            stats['first_transaction'] = datetime.fromtimestamp(df['timestamp'].min() / 1000).isoformat()
            stats['last_transaction'] = datetime.fromtimestamp(df['timestamp'].max() / 1000).isoformat()
        
        return stats
    
    def get_top_counterparties(self, df: pd.DataFrame, limit: int = 5) -> pd.Series:
        """
        获取主要交易对手
        
        Args:
            df: 交易数据 DataFrame
            limit: 返回数量限制
            
        Returns:
            交易对手 Series
        """
        if df.empty or 'to_address' not in df.columns:
            return pd.Series()
        
        # 统计交易对手频率
        counterparties = df['to_address'].value_counts().head(limit)
        return counterparties
    
    def generate_analysis_report(self, df: pd.DataFrame, target_address: str) -> Dict:
        """
        生成完整分析报告
        
        Args:
            df: 交易数据 DataFrame
            target_address: 目标地址
            
        Returns:
            完整分析报告
        """
        # 基础统计
        basic_stats = self.analyze_basic_stats(df, target_address)
        
        # 交易对手分析
        top_counterparties = self.get_top_counterparties(df)
        
        # 交易类型分布
        if 'contract_type' in df.columns:
            contract_types = df['contract_type'].value_counts().to_dict()
        else:
            contract_types = {}
        
        # 生成报告
        report = {
            'address': target_address,
            'generated_at': datetime.now().isoformat(),
            'basic_stats': basic_stats,
            'top_counterparties': top_counterparties.to_dict(),
            'contract_types': contract_types,
            'transaction_count': len(df),
        }
        
        return report
    
    def detect_whale_activity(self, df: pd.DataFrame, threshold: float = 1000000) -> List[Dict]:
        """
        检测大额交易（鲸鱼活动）
        
        Args:
            df: 交易数据 DataFrame
            threshold: 大额阈值（TRX，默认 100 万）
            
        Returns:
            大额交易列表
        """
        if df.empty or 'amount' not in df.columns:
            return []
        
        whale_txs = df[df['amount'] >= threshold]
        return whale_txs.to_dict('records')
    
    def calculate_activity_score(self, df: pd.DataFrame) -> float:
        """
        计算账户活跃度评分
        
        Args:
            df: 交易数据 DataFrame
            
        Returns:
            活跃度评分 (0-100)
        """
        if df.empty:
            return 0.0
        
        # 基于交易频率、金额多样性等计算
        tx_count = len(df)
        unique_counterparties = df['to_address'].nunique() if 'to_address' in df.columns else 0
        
        # 简单评分公式
        score = min(100, (tx_count * 0.5 + unique_counterparties * 2))
        return score
