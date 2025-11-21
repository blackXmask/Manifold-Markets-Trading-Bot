import numpy as np
from typing import Optional, Dict

class KellyCriterion:
    """Kelly criterion calculator for optimal bet sizing"""
    
    @staticmethod
    def calculate_kelly_fraction(
        probability: float,
        market_probability: float,
        kelly_fraction: float = 0.25,
        min_edge: float = 0.05
    ) -> Optional[float]:
        """
        Calculate optimal bet size using fractional Kelly criterion
        
        Args:
            probability: Our estimated probability of YES (0-1)
            market_probability: Current market probability (0-1)
            kelly_fraction: Fraction of Kelly to use (default 0.25 for quarter-Kelly)
            min_edge: Minimum edge required to bet (default 5%)
        
        Returns:
            Fraction of bankroll to bet (0-1), or None if no bet
        """
        if probability <= 0 or probability >= 1:
            return None
        
        if market_probability <= 0 or market_probability >= 1:
            return None
        
        edge_yes = probability - market_probability
        edge_no = (1 - probability) - (1 - market_probability)
        
        bet_direction = None
        edge = 0
        
        if edge_yes >= min_edge:
            bet_direction = "YES"
            edge = edge_yes
            p = probability
            q = 1 - probability
            b = (1 - market_probability) / market_probability
            kelly = (p * b - q) / b
        elif edge_no >= min_edge:
            bet_direction = "NO"
            edge = edge_no
            p = 1 - probability
            q = probability
            b = market_probability / (1 - market_probability)
            kelly = (p * b - q) / b
        else:
            return None
        
        if kelly <= 0:
            return None
        
        kelly_bet = kelly * kelly_fraction
        
        kelly_bet = max(0, min(kelly_bet, 0.5))
        
        return kelly_bet
    
    @staticmethod
    def adjust_for_market_impact(
        bet_size: float,
        market_liquidity: float,
        impact_threshold: float = 0.1
    ) -> float:
        """
        Adjust bet size based on market liquidity to minimize price impact
        
        Args:
            bet_size: Proposed bet size in currency units
            market_liquidity: Total liquidity in the market
            impact_threshold: Maximum fraction of liquidity to bet
        
        Returns:
            Adjusted bet size
        """
        if market_liquidity <= 0:
            return bet_size
        
        max_bet = market_liquidity * impact_threshold
        return min(bet_size, max_bet)
    
    @staticmethod
    def calculate_optimal_bet(
        bankroll: float,
        probability: float,
        market_probability: float,
        market_liquidity: float,
        kelly_fraction: float = 0.25,
        min_edge: float = 0.05,
        min_bet: float = 10,
        max_bet: float = 1000
    ) -> Optional[Dict]:
        """
        Calculate optimal bet with all adjustments
        
        Returns:
            Dict with bet_amount, direction, kelly_fraction, edge, or None
        """
        kelly_bet_fraction = KellyCriterion.calculate_kelly_fraction(
            probability, market_probability, kelly_fraction, min_edge
        )
        
        if kelly_bet_fraction is None:
            return None
        
        bet_amount = bankroll * kelly_bet_fraction
        
        bet_amount = KellyCriterion.adjust_for_market_impact(
            bet_amount, market_liquidity, impact_threshold=0.1
        )
        
        bet_amount = max(min_bet, min(bet_amount, max_bet))
        
        edge_yes = probability - market_probability
        direction = "YES" if edge_yes > 0 else "NO"
        edge = abs(edge_yes)
        
        return {
            "bet_amount": round(bet_amount, 2),
            "direction": direction,
            "kelly_fraction": round(kelly_bet_fraction, 4),
            "edge": round(edge, 4),
            "probability": probability,
            "market_probability": market_probability
        }
