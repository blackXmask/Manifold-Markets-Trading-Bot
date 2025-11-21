from typing import List, Dict, Optional
import re

class ArbitrageDetector:
    """Detect arbitrage opportunities between related markets"""
    
    def __init__(self, min_profit_threshold: float = 0.02):
        self.min_profit_threshold = min_profit_threshold
    
    def find_related_markets(self, markets: List[Dict]) -> List[List[Dict]]:
        """
        Find groups of related markets that might have arbitrage opportunities
        
        Args:
            markets: List of all available markets
        
        Returns:
            List of related market groups
        """
        related_groups = []
        
        for i, market1 in enumerate(markets):
            q1 = market1.get('question', '').lower()
            
            for j, market2 in enumerate(markets[i+1:], start=i+1):
                q2 = market2.get('question', '').lower()
                
                if self._are_markets_related(q1, q2):
                    found = False
                    for group in related_groups:
                        if market1 in group or market2 in group:
                            if market1 not in group:
                                group.append(market1)
                            if market2 not in group:
                                group.append(market2)
                            found = True
                            break
                    
                    if not found:
                        related_groups.append([market1, market2])
        
        return related_groups
    
    def _are_markets_related(self, question1: str, question2: str) -> bool:
        """Check if two market questions are related"""
        keywords1 = set(re.findall(r'\w+', question1.lower()))
        keywords2 = set(re.findall(r'\w+', question2.lower()))
        
        common_words = keywords1 & keywords2
        stop_words = {'will', 'be', 'the', 'a', 'an', 'in', 'on', 'at', 'by', 'for', 'to', 'of', 'is', 'are'}
        significant_common = common_words - stop_words
        
        if len(significant_common) >= 3:
            return True
        
        return False
    
    def detect_binary_arbitrage(self, market: Dict) -> Optional[Dict]:
        """
        Detect arbitrage in a single binary market
        
        For binary markets, YES + NO probabilities should equal 1.
        If market inefficiency exists, there might be arbitrage.
        
        Args:
            market: Market data
        
        Returns:
            Arbitrage opportunity details or None
        """
        prob_yes = market.get('probability', 0.5)
        prob_no = 1 - prob_yes
        
        implied_total = prob_yes + prob_no
        
        if abs(implied_total - 1.0) < 0.01:
            return None
        
        if implied_total < 0.99:
            return {
                "type": "binary_arbitrage",
                "market_id": market.get('id'),
                "market_question": market.get('question'),
                "prob_yes": prob_yes,
                "prob_no": prob_no,
                "implied_total": implied_total,
                "potential_profit": 1.0 - implied_total,
                "strategy": "Buy both YES and NO"
            }
        
        return None
    
    def detect_cross_market_arbitrage(
        self,
        market1: Dict,
        market2: Dict
    ) -> Optional[Dict]:
        """
        Detect arbitrage between two related markets
        
        Args:
            market1: First market
            market2: Second market (should be inversely related)
        
        Returns:
            Arbitrage opportunity or None
        """
        q1 = market1.get('question', '').lower()
        q2 = market2.get('question', '').lower()
        
        is_inverse = ('not' in q2 and 'not' not in q1) or ('not' in q1 and 'not' not in q2)
        
        if not is_inverse:
            return None
        
        prob1 = market1.get('probability', 0.5)
        prob2 = market2.get('probability', 0.5)
        
        if is_inverse:
            expected_prob2 = 1 - prob1
            discrepancy = abs(prob2 - expected_prob2)
            
            if discrepancy > self.min_profit_threshold:
                return {
                    "type": "inverse_market_arbitrage",
                    "market1_id": market1.get('id'),
                    "market1_question": market1.get('question'),
                    "market1_prob": prob1,
                    "market2_id": market2.get('id'),
                    "market2_question": market2.get('question'),
                    "market2_prob": prob2,
                    "discrepancy": discrepancy,
                    "potential_profit": discrepancy,
                    "strategy": f"Bet YES on market with prob {min(prob1, 1-prob2):.2f}"
                }
        
        return None
    
    def scan_for_arbitrage(self, markets: List[Dict]) -> List[Dict]:
        """
        Scan all markets for arbitrage opportunities
        
        Args:
            markets: List of markets to scan
        
        Returns:
            List of arbitrage opportunities
        """
        opportunities = []
        
        for market in markets:
            arb = self.detect_binary_arbitrage(market)
            if arb:
                opportunities.append(arb)
        
        related_groups = self.find_related_markets(markets)
        
        for group in related_groups:
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    arb = self.detect_cross_market_arbitrage(group[i], group[j])
                    if arb:
                        opportunities.append(arb)
        
        return sorted(opportunities, key=lambda x: x.get('potential_profit', 0), reverse=True)
    
    def calculate_arbitrage_allocation(
        self,
        opportunity: Dict,
        total_capital: float
    ) -> Dict:
        """
        Calculate optimal capital allocation for an arbitrage opportunity
        
        Args:
            opportunity: Arbitrage opportunity details
            total_capital: Total capital available
        
        Returns:
            Allocation recommendation
        """
        if opportunity['type'] == 'binary_arbitrage':
            prob_yes = opportunity['prob_yes']
            prob_no = opportunity['prob_no']
            
            total_implied = prob_yes + prob_no
            
            allocation_yes = total_capital * (prob_no / total_implied)
            allocation_no = total_capital * (prob_yes / total_implied)
            
            expected_profit = total_capital * (1 - total_implied)
            
            return {
                "bet_yes": round(allocation_yes, 2),
                "bet_no": round(allocation_no, 2),
                "total_invested": round(allocation_yes + allocation_no, 2),
                "expected_profit": round(expected_profit, 2),
                "roi": round(expected_profit / total_capital * 100, 2)
            }
        
        elif opportunity['type'] == 'inverse_market_arbitrage':
            allocation = total_capital * 0.5
            expected_profit = total_capital * opportunity['potential_profit']
            
            return {
                "total_invested": round(allocation, 2),
                "expected_profit": round(expected_profit, 2),
                "roi": round(expected_profit / allocation * 100, 2)
            }
        
        return {}
