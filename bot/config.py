import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration management for the trading bot"""
    
    MANIFOLD_API_KEY = os.getenv("MANIFOLD_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    TARGET_CREATOR = "MikhailTal"
    
    MIN_CONFIDENCE = 0.6
    MIN_EDGE = 0.05
    
    DEFAULT_BANKROLL = 1000
    MIN_BET = 10
    MAX_BET = 100
    
    KELLY_FRACTION = 0.25
    
    MARKET_IMPACT_THRESHOLD = 0.1
    
    AUTO_TRADE_ENABLED = False
    
    REFRESH_INTERVAL = 60
    
    @staticmethod
    def get_config_dict():
        """Get all configuration as dictionary"""
        return {
            "manifold_api_key": Config.MANIFOLD_API_KEY,
            "openai_api_key": Config.OPENAI_API_KEY,
            "target_creator": Config.TARGET_CREATOR,
            "min_confidence": Config.MIN_CONFIDENCE,
            "min_edge": Config.MIN_EDGE,
            "default_bankroll": Config.DEFAULT_BANKROLL,
            "min_bet": Config.MIN_BET,
            "max_bet": Config.MAX_BET,
            "kelly_fraction": Config.KELLY_FRACTION,
            "auto_trade_enabled": Config.AUTO_TRADE_ENABLED
        }
    
    @staticmethod
    def update_config(config_dict: dict):
        """Update configuration from dictionary"""
        if "min_confidence" in config_dict:
            Config.MIN_CONFIDENCE = config_dict["min_confidence"]
        if "min_edge" in config_dict:
            Config.MIN_EDGE = config_dict["min_edge"]
        if "default_bankroll" in config_dict:
            Config.DEFAULT_BANKROLL = config_dict["default_bankroll"]
        if "min_bet" in config_dict:
            Config.MIN_BET = config_dict["min_bet"]
        if "max_bet" in config_dict:
            Config.MAX_BET = config_dict["max_bet"]
        if "kelly_fraction" in config_dict:
            Config.KELLY_FRACTION = config_dict["kelly_fraction"]
        if "auto_trade_enabled" in config_dict:
            Config.AUTO_TRADE_ENABLED = config_dict["auto_trade_enabled"]
