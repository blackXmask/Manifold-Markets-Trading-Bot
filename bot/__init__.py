"""
Manifold Markets Trading Bot
A professional AI-powered trading bot for Manifold Markets
"""

from .api_client import ManifoldClient
from .strategies import TradingStrategies
from .kelly import KellyCriterion
from .portfolio import PortfolioTracker
from .config import Config
from .portfolio_optimizer import PortfolioOptimizer
from .arbitrage import ArbitrageDetector
from .ensemble_strategy import EnsembleStrategy
from .backtesting import Backtester
from .alerts import AlertSystem

__version__ = "2.0.0"
__all__ = [
    "ManifoldClient",
    "TradingStrategies",
    "KellyCriterion",
    "PortfolioTracker",
    "Config",
    "PortfolioOptimizer",
    "ArbitrageDetector",
    "EnsembleStrategy",
    "Backtester",
    "AlertSystem"
]
