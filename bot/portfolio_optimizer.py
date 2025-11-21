import numpy as np
import pandas as pd
from typing import List, Dict, Optional
from scipy.optimize import minimize
from scipy.stats import pearsonr

class PortfolioOptimizer:
    """Portfolio optimization with correlation analysis for multiple markets"""
    
    def __init__(self, risk_free_rate: float = 0.0):
        self.risk_free_rate = risk_free_rate
    
    def calculate_correlation_matrix(self, positions: List[Dict]) -> Optional[pd.DataFrame]:
        """
        Calculate correlation matrix between market positions
        
        Args:
            positions: List of position dicts with market data and outcomes
        
        Returns:
            Correlation matrix DataFrame or None if insufficient data
        """
        if len(positions) < 2:
            return None
        
        market_returns = {}
        for pos in positions:
            market_id = pos.get('market_id')
            if market_id not in market_returns:
                market_returns[market_id] = []
            
            if pos.get('status') == 'closed':
                roi = pos.get('pnl', 0) / pos.get('amount', 1) if pos.get('amount', 0) > 0 else 0
                market_returns[market_id].append(roi)
        
        market_returns = {k: v for k, v in market_returns.items() if len(v) > 1}
        
        if len(market_returns) < 2:
            return None
        
        df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in market_returns.items()]))
        correlation_matrix = df.corr()
        
        return correlation_matrix
    
    def calculate_portfolio_variance(
        self,
        weights: np.ndarray,
        returns: np.ndarray,
        correlation_matrix: np.ndarray
    ) -> float:
        """
        Calculate portfolio variance given weights and correlation matrix
        
        Args:
            weights: Array of position weights
            returns: Array of expected returns (2D: observations x assets)
            correlation_matrix: Correlation matrix between positions
        
        Returns:
            Portfolio variance
        """
        if returns.ndim == 1:
            returns = returns.reshape(-1, 1)
        
        if returns.shape[1] != len(weights):
            std_devs = np.ones(len(weights)) * 0.1
        else:
            std_devs = np.std(returns, axis=0)
            std_devs = np.where(std_devs == 0, 0.1, std_devs)
        
        cov_matrix = np.outer(std_devs, std_devs) * correlation_matrix
        portfolio_variance = np.dot(weights, np.dot(cov_matrix, weights))
        return max(0.0, portfolio_variance)
    
    def optimize_portfolio_weights(
        self,
        expected_returns: List[float],
        correlation_matrix: np.ndarray,
        risk_tolerance: float = 0.5
    ) -> Dict:
        """
        Optimize portfolio weights using mean-variance optimization
        
        Args:
            expected_returns: Expected return for each position
            correlation_matrix: Correlation matrix between positions
            risk_tolerance: Risk tolerance parameter (0=min variance, 1=max return)
        
        Returns:
            Dict with optimal weights and portfolio metrics
        """
        n_assets = len(expected_returns)
        
        if n_assets == 0:
            return {"weights": [], "expected_return": 0, "variance": 0, "std_dev": 0, "sharpe_ratio": 0}
        
        returns_array = np.array(expected_returns)
        
        def objective(weights):
            portfolio_return = np.dot(weights, returns_array)
            portfolio_var = self.calculate_portfolio_variance(
                weights, returns_array.reshape(-1, 1), correlation_matrix
            )
            return -(risk_tolerance * portfolio_return - (1 - risk_tolerance) * portfolio_var)
        
        constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0}
        bounds = tuple((0.0, 1.0) for _ in range(n_assets))
        initial_weights = np.array([1.0 / n_assets] * n_assets)
        
        try:
            result = minimize(
                objective,
                initial_weights,
                method='SLSQP',
                bounds=bounds,
                constraints=constraints,
                options={'maxiter': 1000, 'ftol': 1e-9}
            )
            
            if not result.success or np.any(np.isnan(result.x)):
                optimal_weights = initial_weights
            else:
                optimal_weights = result.x
                optimal_weights = np.clip(optimal_weights, 0, 1)
                optimal_weights = optimal_weights / optimal_weights.sum()
        
        except Exception as e:
            print(f"Optimization failed: {e}")
            optimal_weights = initial_weights
        
        portfolio_return = np.dot(optimal_weights, returns_array)
        portfolio_var = self.calculate_portfolio_variance(
            optimal_weights, returns_array.reshape(-1, 1), correlation_matrix
        )
        portfolio_std = np.sqrt(max(0, portfolio_var))
        
        sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_std if portfolio_std > 0 else 0
        
        return {
            "weights": optimal_weights.tolist(),
            "expected_return": float(portfolio_return),
            "variance": float(portfolio_var),
            "std_dev": float(portfolio_std),
            "sharpe_ratio": float(sharpe_ratio)
        }
    
    def suggest_position_sizes(
        self,
        markets: List[Dict],
        total_capital: float,
        expected_returns: List[float]
    ) -> List[Dict]:
        """
        Suggest optimal position sizes for multiple markets
        
        Args:
            markets: List of market opportunities
            total_capital: Total available capital
            expected_returns: Expected return for each market
        
        Returns:
            List of position size recommendations
        """
        if not markets or not expected_returns:
            return []
        
        n_markets = len(markets)
        
        correlation_matrix = np.eye(n_markets) * 0.5 + np.ones((n_markets, n_markets)) * 0.1
        np.fill_diagonal(correlation_matrix, 1.0)
        
        optimization_result = self.optimize_portfolio_weights(
            expected_returns,
            correlation_matrix,
            risk_tolerance=0.6
        )
        
        suggestions = []
        for i, market in enumerate(markets):
            weight = optimization_result["weights"][i]
            position_size = total_capital * weight
            
            suggestions.append({
                "market_id": market.get("id"),
                "market_question": market.get("question"),
                "weight": round(weight, 4),
                "suggested_size": round(position_size, 2),
                "expected_return": expected_returns[i]
            })
        
        return suggestions
    
    def calculate_diversification_ratio(self, correlation_matrix: pd.DataFrame) -> float:
        """
        Calculate portfolio diversification ratio
        
        Args:
            correlation_matrix: Correlation matrix between positions
        
        Returns:
            Diversification ratio (1 = fully diversified, 0 = concentrated)
        """
        if correlation_matrix is None or correlation_matrix.empty:
            return 0.0
        
        n_assets = len(correlation_matrix)
        if n_assets <= 1:
            return 0.0
        
        avg_correlation = (correlation_matrix.sum().sum() - n_assets) / (n_assets * (n_assets - 1))
        
        diversification_ratio = 1 - avg_correlation
        
        return max(0.0, min(1.0, diversification_ratio))
    
    def identify_correlated_markets(
        self,
        correlation_matrix: pd.DataFrame,
        threshold: float = 0.7
    ) -> List[Dict]:
        """
        Identify highly correlated market pairs
        
        Args:
            correlation_matrix: Correlation matrix between markets
            threshold: Correlation threshold for flagging
        
        Returns:
            List of correlated market pairs
        """
        if correlation_matrix is None or correlation_matrix.empty:
            return []
        
        correlated_pairs = []
        markets = correlation_matrix.columns.tolist()
        
        for i in range(len(markets)):
            for j in range(i + 1, len(markets)):
                correlation = correlation_matrix.iloc[i, j]
                
                if abs(correlation) >= threshold:
                    correlated_pairs.append({
                        "market1": markets[i],
                        "market2": markets[j],
                        "correlation": round(correlation, 3),
                        "type": "positive" if correlation > 0 else "negative"
                    })
        
        return sorted(correlated_pairs, key=lambda x: abs(x["correlation"]), reverse=True)
