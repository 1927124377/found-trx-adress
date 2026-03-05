#!/usr/bin/env python3
"""
Binance Address Insight Crawler
Extends found-trx-adress to support Binance Smart Chain and other chains
via Binance AI Agent Skill API.
"""

import requests
import pandas as pd
import argparse
import sys
import os
from datetime import datetime
import json

class BinanceAddressInsight:
    def __init__(self, api_key=None, api_secret=None):
        """
        Initialize Binance Address Insight client
        
        Args:
            api_key (str): Binance API key (optional for public data)
            api_secret (str): Binance API secret (optional for public data)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.binance.com"
        
    def query_address_info(self, wallet_address, chain="BSC"):
        """
        Query address information using Binance AI Agent Skill
        
        Args:
            wallet_address (str): Wallet address to analyze
            chain (str): Blockchain network (BSC, ETH, etc.)
            
        Returns:
            dict: Address insight data including:
                - holdings: Token holdings and valuations
                - 24h_changes: 24-hour changes
                - concentration: Address concentration metrics
                - whale_smart_money: Whale/smart money indicators
        """
        try:
            # Binance AI Agent Skill endpoint for address insight
            url = f"{self.base_url}/api/v3/ai-agent/address-insight"
            
            headers = {}
            if self.api_key:
                headers['X-MBX-APIKEY'] = self.api_key
                
            params = {
                'address': wallet_address,
                'chain': chain
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error querying Binance API: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Exception in query_address_info: {e}")
            return None
    
    def get_token_info(self, token_address, chain="BSC"):
        """
        Get detailed token information
        
        Args:
            token_address (str): Token contract address
            chain (str): Blockchain network
            
        Returns:
            dict: Token details including symbol, price, liquidity, holders, etc.
        """
        try:
            url = f"{self.base_url}/api/v3/ai-agent/token-info"
            
            headers = {}
            if self.api_key:
                headers['X-MBX-APIKEY'] = self.api_key
                
            params = {
                'token': token_address,
                'chain': chain
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error querying token info: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Exception in get_token_info: {e}")
            return None
    
    def query_token_audit(self, token_address, chain="BSC"):
        """
        Perform token contract audit
        
        Args:
            token_address (str): Token contract address
            chain (str): Blockchain network
            
        Returns:
            dict: Audit results with risk assessment (关注/谨慎/回避)
        """
        try:
            url = f"{self.base_url}/api/v3/ai-agent/token-audit"
            
            headers = {}
            if self.api_key:
                headers['X-MBX-APIKEY'] = self.api_key
                
            params = {
                'token': token_address,
                'chain': chain
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error querying token audit: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Exception in query_token_audit: {e}")
            return None

def crawl_binance_address(address, output_file='binance_transactions.xlsx', chain='BSC'):
    """
    Crawl Binance address insight data
    
    Args:
        address (str): Wallet address to analyze
        output_file (str): Output Excel file name
        chain (str): Blockchain network (BSC, ETH, etc.)
    """
    print(f"Starting Binance address insight crawl for: {address} (Chain: {chain})")
    
    # Initialize Binance client
    client = BinanceAddressInsight()
    
    # Get address insight
    address_data = client.query_address_info(address, chain)
    if not address_data:
        print("Failed to retrieve address insight data")
        return
    
    # Get detailed token information for each holding
    holdings = address_data.get('holdings', [])
    enriched_holdings = []
    
    for holding in holdings:
        token_address = holding.get('token_address')
        if token_address:
            # Get token details
            token_info = client.get_token_info(token_address, chain)
            if token_info:
                # Get token audit
                token_audit = client.query_token_audit(token_address, chain)
                
                # Enrich holding data
                enriched_holding = {
                    **holding,
                    'token_symbol': token_info.get('symbol'),
                    'token_price': token_info.get('price'),
                    'liquidity': token_info.get('liquidity'),
                    'holders_count': token_info.get('holders'),
                    'trading_activity': token_info.get('activity'),
                    'audit_risk': token_audit.get('risk_label') if token_audit else 'Unknown',
                    'audit_details': token_audit.get('risk_fields') if token_audit else {}
                }
                enriched_holdings.append(enriched_holding)
        else:
            enriched_holdings.append(holding)
    
    # Create DataFrame
    df = pd.DataFrame(enriched_holdings)
    
    # Save to Excel
    df.to_excel(output_file, index=False)
    print(f"Saved Binance address insight to {output_file}")
    
    if not df.empty:
        print(df.head())

if __name__ == "__main__":
    # ===== Configuration =====
    DEFAULT_ADDRESS = ""
    # ========================
    
    parser = argparse.ArgumentParser(description="Crawl Binance address insight data")
    parser.add_argument('--address', default=DEFAULT_ADDRESS, help="Wallet address to analyze")
    parser.add_argument('--output', default='binance_transactions.xlsx', help="Output Excel file")
    parser.add_argument('--chain', default='BSC', choices=['BSC', 'ETH'], help="Blockchain network")
    
    args = parser.parse_args()
    
    if not args.address:
        print("Error: Must provide wallet address")
        sys.exit(1)
    
    crawl_binance_address(args.address, args.output, args.chain)