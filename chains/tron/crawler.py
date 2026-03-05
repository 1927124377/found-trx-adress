"""
TRON Blockchain Crawler
Implements BaseCrawler for TRX transaction data
"""

from core.base_crawler import BaseCrawler
from typing import Dict, List, Any
import requests
import os
from datetime import datetime

class TronCrawler(BaseCrawler):
    """TRON 区块链爬虫实现"""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化 TRON 爬虫
        
        Args:
            config: 配置字典，包含 API key 等
        """
        if config is None:
            config = {}
        
        # 从环境变量获取 API key（优先）
        api_key = os.getenv('TRON_API_KEY', config.get('api_key', ''))
        
        super().__init__(config)
        self.api_key = api_key
        self.base_url = "https://apilist.tronscanapi.com/api"
        
        # 设置请求头
        if self.api_key:
            self.session.headers.update({'TRON-PRO-API-KEY': self.api_key})
    
    def crawl_transactions(self, address: str, limit: int = 50, **kwargs) -> List[Dict]:
        """
        爬取 TRX 交易数据
        
        Args:
            address: TRON 钱包地址
            limit: 返回交易数量限制（默认 50）
            
        Returns:
            交易列表
        """
        url = f"{self.base_url}/accountv2/get_transactions"
        params = {
            'address': address,
            'limit': limit,
            'start': 0
        }
        
        try:
            response = self._make_request(url, params)
            transactions = response.get('data', [])
            return transactions
        except Exception as e:
            print(f"Error crawling TRON transactions: {e}")
            return []
    
    def flatten_transaction(self, tx_data: Dict) -> Dict:
        """
        扁平化 TRX 交易数据
        
        Args:
            tx_data: 原始交易数据
            
        Returns:
            扁平化的交易字典
        """
        return {
            'tx_hash': tx_data.get('hash', ''),
            'block': tx_data.get('block', 0),
            'timestamp': tx_data.get('timestamp', 0),
            'datetime': datetime.fromtimestamp(tx_data.get('timestamp', 0) / 1000).isoformat(),
            'from_address': tx_data.get('from_address', ''),
            'to_address': tx_data.get('to_address', ''),
            'amount': tx_data.get('amount', 0),
            'token_name': tx_data.get('token_name', 'TRX'),
            'contract_type': tx_data.get('contract_type', 0),
            'result': tx_data.get('result', ''),
            'fee': tx_data.get('fee', 0)
        }
    
    def get_account_info(self, address: str) -> Dict:
        """
        获取账户信息
        
        Args:
            address: TRON 钱包地址
            
        Returns:
            账户信息字典
        """
        url = f"{self.base_url}/accountv2/get_account"
        params = {'address': address}
        
        try:
            response = self._make_request(url, params)
            return response
        except Exception as e:
            print(f"Error getting account info: {e}")
            return {}
    
    def get_trc20_transfers(self, address: str, limit: int = 50) -> List[Dict]:
        """
        获取 TRC20 转账记录
        
        Args:
            address: TRON 钱包地址
            limit: 返回记录数量限制
            
        Returns:
            TRC20 转账列表
        """
        url = f"{self.base_url}/transfer"
        params = {
            'relatedAddress': address,
            'limit': limit,
            'start': 0
        }
        
        try:
            response = self._make_request(url, params)
            transfers = response.get('token_transfers', [])
            return transfers
        except Exception as e:
            print(f"Error getting TRC20 transfers: {e}")
            return []
