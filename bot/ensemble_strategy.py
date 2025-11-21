from typing import List, Dict, Optional
import numpy as np
from .strategies import TradingStrategies

class EnsembleStrategy:
    """Ensemble strategy combining multiple prediction models"""
    
    def __init__(
        self,
        llm_strategy: Optional[TradingStrategies] = None,
        weights: Optional[Dict[str, float]] = None
    ):
        self.llm_strategy = llm_strategy
        self.weights = weights or {
            "llm": 0.5,
            "base_rate": 0.2,
            "market_momentum": 0.15,
            "contrarian": 0.15
        }
    
    def base_rate_estimate(self, question: str) -> float:
        """
        Estimate probability based on base rates and common outcomes
        
        Args:
            question: Market question
        
        Returns:
            Base rate probability estimate
        """
        q_lower = question.lower()
        
        optimistic_keywords = ['will', 'success', 'achieve', 'reach', 'exceed', 'grow']
        pessimistic_keywords = ['fail', 'decline', 'decrease', 'not', "won't", 'unable']
        
        optimistic_count = sum(1 for keyword in optimistic_keywords if keyword in q_lower)
        pessimistic_count = sum(1 for keyword in pessimistic_keywords if keyword in q_lower)
        
        if 'by 20' in q_lower or 'in 20' in q_lower:
            year_match = None
            for word in q_lower.split():
                if word.isdigit() and len(word) == 4 and word.startswith('20'):
                    year_match = int(word)
                    break
            
            if year_match:
                if year_match <= 2026:
                    return 0.6
                elif year_match <= 2030:
                    return 0.4
                else:
                    return 0.25
        
        if pessimistic_count > optimistic_count:
            return 0.35
        elif optimistic_count > pessimistic_count:
            return 0.65
        else:
            return 0.5
    
    def market_momentum_estimate(self, market: Dict) -> float:
        """
        Estimate probability based on market momentum and volume
        
        Args:
            market: Market data with probability and volume
        
        Returns:
            Momentum-adjusted probability
        """
        current_prob = market.get('probability', 0.5)
        volume = market.get('volume', 0)
        
        if volume > 1000:
            momentum_factor = 1.0
        elif volume > 500:
            momentum_factor = 0.8
        elif volume > 100:
            momentum_factor = 0.6
        else:
            momentum_factor = 0.4
        
        if current_prob > 0.7:
            adjusted = current_prob + (1 - current_prob) * momentum_factor * 0.1
        elif current_prob < 0.3:
            adjusted = current_prob - current_prob * momentum_factor * 0.1
        else:
            adjusted = current_prob
        
        return max(0.01, min(0.99, adjusted))
    
    def contrarian_estimate(self, market: Dict) -> float:
        """
        Contrarian estimate that bets against extreme probabilities
        
        Args:
            market: Market data
        
        Returns:
            Contrarian probability estimate
        """
        current_prob = market.get('probability', 0.5)
        
        if current_prob > 0.8:
            return 0.8 - (current_prob - 0.8) * 0.5
        elif current_prob < 0.2:
            return 0.2 + (0.2 - current_prob) * 0.5
        else:
            return current_prob
    
    def ensemble_predict(
        self,
        question: str,
        description: str,
        market_data: Dict
    ) -> Dict:
        """
        Combine multiple prediction models into ensemble estimate
        
        Args:
            question: Market question
            description: Market description
            market_data: Market data including current probability
        
        Returns:
            Dict with ensemble prediction and component predictions
        """
        predictions = {}
        
        if self.llm_strategy and self.llm_strategy.openai_api_key:
            llm_prob = self.llm_strategy.estimate_probability_llm(question, description)
            if llm_prob:
                predictions['llm'] = llm_prob
        
        predictions['base_rate'] = self.base_rate_estimate(question)
        predictions['market_momentum'] = self.market_momentum_estimate(market_data)
        predictions['contrarian'] = self.contrarian_estimate(market_data)
        
        ensemble_prob = 0.0
        total_weight = 0.0
        
        for model_name, prob in predictions.items():
            weight = self.weights.get(model_name, 0.0)
            ensemble_prob += prob * weight
            total_weight += weight
        
        if total_weight > 0:
            ensemble_prob = ensemble_prob / total_weight
        else:
            ensemble_prob = market_data.get('probability', 0.5)
        
        variance = np.var(list(predictions.values())) if len(predictions) > 1 else 0.0
        
        confidence = 1.0 / (1.0 + variance * 10)
        
        return {
            "ensemble_probability": round(ensemble_prob, 4),
            "confidence": round(confidence, 4),
            "variance": round(variance, 4),
            "predictions": {k: round(v, 4) for k, v in predictions.items()},
            "model_agreement": round(1.0 - variance, 4)
        }
    
    def calibrate_weights(self, historical_performance: Dict[str, float]):
        """
        Calibrate ensemble weights based on historical model performance
        
        Args:
            historical_performance: Dict mapping model names to accuracy scores
        """
        total_performance = sum(historical_performance.values())
        
        if total_performance > 0:
            self.weights = {
                model: perf / total_performance
                for model, perf in historical_performance.items()
            }
    
    def evaluate_prediction_quality(
        self,
        predictions: Dict[str, float],
        actual_outcome: float
    ) -> Dict:
        """
        Evaluate the quality of ensemble predictions
        
        Args:
            predictions: Dict of model predictions
            actual_outcome: Actual outcome (0 or 1)
        
        Returns:
            Performance metrics for each model
        """
        performance = {}
        
        for model_name, prediction in predictions.items():
            error = abs(prediction - actual_outcome)
            brier_score = (prediction - actual_outcome) ** 2
            
            performance[model_name] = {
                "error": round(error, 4),
                "brier_score": round(brier_score, 4),
                "accuracy": round(1.0 - error, 4)
            }
        
        return performance
