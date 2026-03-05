from abc import ABC, abstractmethod
from typing import Dict, List, Any
import requests

class BaseCrawler(ABC):
    """抽象爬虫基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.session = requests.Session()
        
    @abstractmethod
    def crawl_transactions(self, address: str, **kwargs) -> List[Dict]:
        """爬取交易数据的抽象方法"""
        pass
        
    @abstractmethod
    def flatten_transaction(self, tx_data: Dict) -> Dict:
        """扁平化交易数据的抽象方法"""
        pass
        
    def _make_request(self, url: str, params: Dict = None) -> Dict:
        """通用请求方法"""
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()