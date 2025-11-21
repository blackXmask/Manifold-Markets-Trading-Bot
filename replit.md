# Manifold Markets Trading Bot v2.0

## Overview

A professional AI-powered trading bot for Manifold Markets with a beautiful dark blue themed GUI. The bot specifically targets markets created by **MikhailTal** and uses advanced strategies including:

- GPT-5 powered probability estimation with ensemble learning
- Kelly criterion for optimal bet sizing with market impact adjustment
- Portfolio optimization with correlation analysis
- Arbitrage detection for risk-free profits
- Backtesting framework for strategy validation
- Real-time alerts via webhook and email
- Comprehensive performance analytics and risk management

## Recent Changes

**November 21, 2025** - v2.0 Release - Advanced Features
- Added portfolio optimization with correlation analysis and mean-variance optimization
- Implemented arbitrage detection for binary and cross-market opportunities
- Created ensemble AI strategy combining LLM, base rates, momentum, and contrarian signals
- Built backtesting framework with comprehensive performance metrics
- Added alert system with webhook and email notifications
- Expanded GUI from 4 tabs to 9 tabs with advanced features
- Enhanced documentation with manifoldbot contribution proposals

**November 21, 2025** - v1.0 Initial Release
- Created full-featured trading bot with Streamlit GUI
- Implemented AI strategies with GPT-5 integration
- Added Kelly criterion position sizing with market impact adjustment
- Built comprehensive performance tracking system
- Created dark blue themed professional interface
- Added real-time market monitoring and trading execution

## Project Architecture

```
bot/
├── api_client.py           # Manifold Markets API integration
├── strategies.py           # AI-powered trading strategies (GPT-5)
├── kelly.py                # Kelly criterion calculator
├── portfolio.py            # Performance tracking and analytics
├── config.py               # Configuration management
├── portfolio_optimizer.py  # Portfolio optimization and correlation analysis
├── arbitrage.py            # Arbitrage detection
├── ensemble_strategy.py    # Ensemble AI prediction
├── backtesting.py          # Backtesting framework
└── alerts.py               # Alert and notification system

app.py                # Main Streamlit application (9 tabs)
data/                 # Trade history storage
examples/             # Example scripts
docs/                 # Documentation and contribution guides
```

## User Preferences

- **Language**: Python 3.11
- **Framework**: Streamlit for web interface
- **AI Model**: GPT-5 (latest OpenAI model)
- **Theme**: Dark blue professional trading interface
- **Trading Style**: Conservative (quarter-Kelly) with risk management

## Key Features

### Trading
- Automated market discovery (MikhailTal markets only)
- AI probability estimation using GPT-5
- Ensemble AI combining multiple prediction models
- Optimal bet sizing with Kelly criterion
- Market impact adjustment to prevent moving markets
- Configurable confidence and edge thresholds

### Portfolio Optimization
- Correlation analysis between markets
- Mean-variance portfolio optimization
- Diversification ratio calculation
- Optimal position size recommendations
- Correlated market pair identification

### Arbitrage Detection
- Binary market arbitrage (YES + NO ≠ 1)
- Cross-market arbitrage opportunities
- Automated scanning across all markets
- Optimal capital allocation calculation
- Profit estimation for each opportunity

### Backtesting
- Historical market simulation
- Strategy performance metrics (ROI, Sharpe, drawdown)
- Multiple strategy comparison
- Trade-by-trade analysis
- Risk assessment before live trading

### Alerts & Notifications
- Webhook notifications
- Email alerts
- Trading opportunity alerts
- P&L milestone notifications
- Arbitrage opportunity alerts

### Analytics
- Real-time P&L tracking
- ROI and win rate calculations
- Cumulative performance charts
- Win/loss distribution analysis
- Correlation heatmaps
- Trade history with CSV export

### Risk Management
- Fractional Kelly (default 25%)
- Position limits (min/max bet sizes)
- Edge requirements (minimum 5% edge)
- Confidence thresholds (minimum 60%)
- Market liquidity checks
- Portfolio diversification monitoring

## Configuration

### Required Environment Variables
- `MANIFOLD_API_KEY`: Your Manifold Markets API key
- `OPENAI_API_KEY`: Your OpenAI API key (optional)

### Trading Parameters
- **Bankroll**: $1,000 (default)
- **Kelly Fraction**: 0.25 (quarter-Kelly)
- **Min Confidence**: 0.6 (60%)
- **Min Edge**: 0.05 (5%)
- **Min Bet**: $10
- **Max Bet**: $100

## Improvements Over manifoldbot

1. **Professional Web Interface**: 9-tab Streamlit GUI vs CLI
2. **Enhanced AI**: GPT-5 with ensemble learning and sentiment analysis
3. **Portfolio Optimization**: Correlation analysis and optimal allocation
4. **Arbitrage Detection**: Automated risk-free profit scanning
5. **Backtesting Framework**: Historical strategy validation
6. **Alert System**: Real-time webhook and email notifications
7. **Better Risk Management**: Fractional Kelly + market impact + diversification
8. **Advanced Analytics**: Live charts, heatmaps, and performance tracking
9. **User Experience**: One-click trading with comprehensive AI insights
10. **Targeted Markets**: Filters for specific creators
11. **Dark Blue Theme**: Professional trading interface

## Future Enhancements

### Planned Features
- Portfolio optimization across multiple markets
- Arbitrage detection between related markets
- Ensemble ML models for probability estimation
- Backtesting framework for strategy validation
- Real-time alerts and notifications
- Advanced correlation analysis

### Potential manifoldbot Contributions
- Streamlit UI integration
- Enhanced Kelly criterion implementation
- GPT-5 support
- Sentiment analysis module
- Advanced analytics and tracking
- Market filtering capabilities
- Comprehensive risk controls

## Technical Details

### Kelly Criterion Implementation
Uses fractional Kelly with market impact adjustment:
```python
kelly_bet = (p * b - q) / b * kelly_fraction
adjusted_bet = min(kelly_bet, liquidity * 0.1)
```

### AI Strategy
GPT-5 analyzes markets considering:
- Historical precedents and base rates
- Current trends and evidence
- Statistical reasoning
- Potential cognitive biases

### Performance Tracking
All trades persisted in `data/portfolio.json` with:
- Timestamp and market details
- Direction and amount
- Probabilities (AI vs market)
- Edge and outcome
- P&L calculation

## Usage

1. Configure API keys in sidebar
2. Set trading parameters
3. Click "Refresh Markets" to load opportunities
4. Analyze markets with AI
5. Review recommendations and place bets
6. Monitor performance in dashboard and analytics

## Support

The bot includes:
- Comprehensive README.md documentation
- Example scripts in `examples/`
- Contribution guidelines in CONTRIBUTING.md
- Code comments and docstrings throughout

## Notes

- Manifold Markets uses play money (no real financial risk)
- All trading is automated but requires manual initiation
- Performance depends on market efficiency and AI accuracy
- Conservative settings recommended for beginners
- Monitor results and adjust parameters based on performance
