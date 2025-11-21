import requests
from typing import List, Dict, Optional
import time

class ManifoldClient:
    """Client for interacting with Manifold Markets API"""
    
    BASE_URL = "https://api.manifold.markets/v0"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.headers = {}
        if api_key:
            self.headers["Authorization"] = f"Key {api_key}"
    
    def get_markets(self, limit: int = 1000, creator_username: Optional[str] = None) -> List[Dict]:
        """Fetch markets, optionally filtered by creator"""
        try:
            params = {"limit": limit}
            response = requests.get(f"{self.BASE_URL}/markets", params=params, timeout=10)
            response.raise_for_status()
            markets = response.json()
            
            if creator_username:
                markets = [m for m in markets if m.get("creatorUsername") == creator_username]
            
            return markets
        except Exception as e:
            print(f"Error fetching markets: {e}")
            return []
    
    def get_market(self, market_id: str) -> Optional[Dict]:
        """Fetch a specific market by ID"""
        try:
            response = requests.get(f"{self.BASE_URL}/market/{market_id}", timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching market {market_id}: {e}")
            return None
    
    def get_user(self, username: str) -> Optional[Dict]:
        """Fetch user information"""
        try:
            response = requests.get(f"{self.BASE_URL}/user/{username}", timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching user {username}: {e}")
            return None
    
    def get_bets(self, market_id: Optional[str] = None, username: Optional[str] = None) -> List[Dict]:
        """Fetch bets, optionally filtered by market or username"""
        try:
            params = {}
            if market_id:
                params["contractId"] = market_id
            if username:
                params["username"] = username
            
            response = requests.get(f"{self.BASE_URL}/bets", params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching bets: {e}")
            return []
    
    def place_bet(self, market_id: str, amount: float, outcome: str) -> Optional[Dict]:
        """Place a bet on a market"""
        if not self.api_key:
            raise ValueError("API key required to place bets")
        
        try:
            data = {
                "contractId": market_id,
                "amount": amount,
                "outcome": outcome
            }
            response = requests.post(
                f"{self.BASE_URL}/bet",
                headers=self.headers,
                json=data,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error placing bet: {e}")
            return None
    
    def get_mikhailtal_markets(self) -> List[Dict]:
        """Fetch all markets created by MikhailTal"""
        return self.get_markets(creator_username="MikhailTal")
    
    def get_open_markets(self, creator_username: Optional[str] = None) -> List[Dict]:
        """Fetch only open/active markets"""
        markets = self.get_markets(creator_username=creator_username)
        return [m for m in markets if not m.get("isResolved", False) and m.get("closeTime", 0) > time.time() * 1000]
