from typing import List, Dict, Optional
from datetime import datetime, timedelta
import pandas as pd
from .strategies import TradingStrategies
from .kelly import KellyCriterion

class Backtester:
    """Backtesting framework for trading strategies"""
    
    def __init__(
        self,
        initial_capital: float = 1000,
        strategy: Optional[TradingStrategies] = None
    ):
        self.initial_capital = initial_capital
        self.strategy = strategy
        self.results = []
    
    def simulate_trade(
        self,
        market: Dict,
        ai_probability: float,
        kelly_fraction: float = 0.25,
        min_edge: float = 0.05,
        min_bet: float = 10,
        max_bet: float = 100
    ) -> Optional[Dict]:
        """
        Simulate a single trade
        
        Args:
            market: Market data
            ai_probability: AI estimated probability
            kelly_fraction: Kelly fraction to use
            min_edge: Minimum edge required
            min_bet: Minimum bet size
            max_bet: Maximum bet size
        
        Returns:
            Trade simulation result
        """
        market_prob = market.get('probability', 0.5)
        
        bet_info = KellyCriterion.calculate_optimal_bet(
            self.initial_capital,
            ai_probability,
            market_prob,
            market.get('totalLiquidity', 1000),
            kelly_fraction,
            min_edge,
            min_bet,
            max_bet
        )
        
        if not bet_info:
            return None
        
        outcome = market.get('resolution')
        if not outcome:
            return None
        
        bet_amount = bet_info['bet_amount']
        direction = bet_info['direction']
        
        if outcome == direction:
            if direction == "YES":
                payout = bet_amount / market_prob
            else:
                payout = bet_amount / (1 - market_prob)
            pnl = payout - bet_amount
        else:
            pnl = -bet_amount
        
        return {
            "market_id": market.get('id'),
            "market_question": market.get('question'),
            "direction": direction,
            "amount": bet_amount,
            "ai_probability": ai_probability,
            "market_probability": market_prob,
            "edge": bet_info['edge'],
            "outcome": outcome,
            "pnl": pnl,
            "roi": (pnl / bet_amount * 100) if bet_amount > 0 else 0
        }
    
    def backtest_strategy(
        self,
        historical_markets: List[Dict],
        kelly_fraction: float = 0.25,
        min_edge: float = 0.05
    ) -> Dict:
        """
        Run backtest on historical markets
        
        Args:
            historical_markets: List of resolved markets with outcomes
            kelly_fraction: Kelly fraction parameter
            min_edge: Minimum edge threshold
        
        Returns:
            Backtest results with performance metrics
        """
        self.results = []
        current_capital = self.initial_capital
        
        for market in historical_markets:
            if not market.get('isResolved'):
                continue
            
            question = market.get('question', '')
            description = market.get('description', '')
            
            if self.strategy and self.strategy.openai_api_key:
                ai_prob = self.strategy.estimate_probability_llm(question, description)
            else:
                ai_prob = 0.5
            
            if not ai_prob:
                continue
            
            trade_result = self.simulate_trade(
                market,
                ai_prob,
                kelly_fraction,
                min_edge,
                min_bet=current_capital * 0.01,
                max_bet=current_capital * 0.1
            )
            
            if trade_result:
                self.results.append(trade_result)
                current_capital += trade_result['pnl']
                
                if current_capital <= 0:
                    break
        
        return self.calculate_metrics()
    
    def calculate_metrics(self) -> Dict:
        """Calculate performance metrics from backtest results"""
        if not self.results:
            return {
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "win_rate": 0,
                "total_pnl": 0,
                "avg_pnl": 0,
                "max_drawdown": 0,
                "sharpe_ratio": 0,
                "roi": 0,
                "final_capital": self.initial_capital
            }
        
        df = pd.DataFrame(self.results)
        
        total_trades = len(df)
        winning_trades = len(df[df['pnl'] > 0])
        losing_trades = len(df[df['pnl'] < 0])
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        total_pnl = df['pnl'].sum()
        avg_pnl = df['pnl'].mean()
        
        cumulative_pnl = df['pnl'].cumsum()
        running_max = cumulative_pnl.cummax()
        drawdown = running_max - cumulative_pnl
        max_drawdown = drawdown.max()
        
        returns = df['pnl'] / self.initial_capital
        sharpe_ratio = (returns.mean() / returns.std()) * (252 ** 0.5) if returns.std() > 0 else 0
        
        final_capital = self.initial_capital + total_pnl
        roi = (total_pnl / self.initial_capital * 100)
        
        return {
            "total_trades": total_trades,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate": round(win_rate, 2),
            "total_pnl": round(total_pnl, 2),
            "avg_pnl": round(avg_pnl, 2),
            "max_drawdown": round(max_drawdown, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "roi": round(roi, 2),
            "final_capital": round(final_capital, 2)
        }
    
    def get_trade_history(self) -> pd.DataFrame:
        """Get backtest trade history as DataFrame"""
        if not self.results:
            return pd.DataFrame()
        return pd.DataFrame(self.results)
    
    def compare_strategies(
        self,
        historical_markets: List[Dict],
        strategy_configs: List[Dict]
    ) -> pd.DataFrame:
        """
        Compare multiple strategy configurations
        
        Args:
            historical_markets: Historical market data
            strategy_configs: List of strategy config dicts
        
        Returns:
            DataFrame comparing strategy performance
        """
        comparison = []
        
        for config in strategy_configs:
            name = config.get('name', 'Unnamed')
            kelly_fraction = config.get('kelly_fraction', 0.25)
            min_edge = config.get('min_edge', 0.05)
            
            self.results = []
            metrics = self.backtest_strategy(
                historical_markets,
                kelly_fraction,
                min_edge
            )
            
            metrics['strategy_name'] = name
            metrics['kelly_fraction'] = kelly_fraction
            metrics['min_edge'] = min_edge
            comparison.append(metrics)
        
        return pd.DataFrame(comparison)
