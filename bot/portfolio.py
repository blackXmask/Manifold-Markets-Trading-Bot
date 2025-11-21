import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd

class PortfolioTracker:
    """Track trading performance and portfolio metrics"""
    
    def __init__(self, storage_file: str = "data/portfolio.json"):
        self.storage_file = storage_file
        self.trades = []
        self.load_trades()
    
    def load_trades(self):
        """Load trade history from file"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    self.trades = json.load(f)
            except Exception as e:
                print(f"Error loading trades: {e}")
                self.trades = []
        else:
            os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
            self.trades = []
    
    def save_trades(self):
        """Save trade history to file"""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.trades, f, indent=2)
        except Exception as e:
            print(f"Error saving trades: {e}")
    
    def add_trade(
        self,
        market_id: str,
        market_question: str,
        direction: str,
        amount: float,
        probability: float,
        ai_probability: float,
        edge: float,
        timestamp: Optional[str] = None
    ):
        """Record a new trade"""
        trade = {
            "id": len(self.trades) + 1,
            "timestamp": timestamp or datetime.now().isoformat(),
            "market_id": market_id,
            "market_question": market_question,
            "direction": direction,
            "amount": amount,
            "probability": probability,
            "ai_probability": ai_probability,
            "edge": edge,
            "status": "open",
            "pnl": 0
        }
        self.trades.append(trade)
        self.save_trades()
    
    def update_trade_outcome(self, market_id: str, outcome: str, pnl: float):
        """Update trade with outcome and P&L"""
        for trade in self.trades:
            if trade["market_id"] == market_id and trade["status"] == "open":
                trade["status"] = "closed"
                trade["outcome"] = outcome
                trade["pnl"] = pnl
        self.save_trades()
    
    def get_statistics(self) -> Dict:
        """Calculate portfolio statistics"""
        if not self.trades:
            return {
                "total_trades": 0,
                "open_trades": 0,
                "closed_trades": 0,
                "total_pnl": 0,
                "win_rate": 0,
                "avg_edge": 0,
                "total_invested": 0,
                "roi": 0
            }
        
        df = pd.DataFrame(self.trades)
        
        open_trades = df[df["status"] == "open"]
        closed_trades = df[df["status"] == "closed"]
        
        total_pnl = df["pnl"].sum()
        total_invested = df["amount"].sum()
        
        wins = len(closed_trades[closed_trades["pnl"] > 0]) if len(closed_trades) > 0 else 0
        win_rate = wins / len(closed_trades) if len(closed_trades) > 0 else 0
        
        roi = (total_pnl / total_invested * 100) if total_invested > 0 else 0
        
        return {
            "total_trades": len(self.trades),
            "open_trades": len(open_trades),
            "closed_trades": len(closed_trades),
            "total_pnl": round(total_pnl, 2),
            "win_rate": round(win_rate * 100, 2),
            "avg_edge": round(df["edge"].mean() * 100, 2),
            "total_invested": round(total_invested, 2),
            "roi": round(roi, 2)
        }
    
    def get_recent_trades(self, limit: int = 10) -> List[Dict]:
        """Get most recent trades"""
        return sorted(self.trades, key=lambda x: x["timestamp"], reverse=True)[:limit]
    
    def get_trades_dataframe(self) -> pd.DataFrame:
        """Get trades as pandas DataFrame"""
        if not self.trades:
            return pd.DataFrame()
        return pd.DataFrame(self.trades)
