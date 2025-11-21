# 🤖 Manifold Markets Trading Bot 

A professional AI-powered trading bot for Manifold Markets, specifically targeting markets created by **MikhailTal**. Features a beautiful dark blue themed GUI built with Streamlit, advanced AI strategies, portfolio optimization, arbitrage detection, ensemble learning, backtesting, and real-time performance analytics.

## ✨ Features

### 🎯 Core Trading Features
- **Targeted Trading**: Automatically filters and trades only on markets created by MikhailTal
- **AI-Powered Analysis**: Uses GPT-5 for probability estimation and sentiment analysis
- **Kelly Criterion**: Optimal bet sizing with market impact adjustment
- **Risk Management**: Configurable confidence thresholds, edges, and position limits

### 🎲 Portfolio Optimization
- **Correlation Analysis**: Calculate correlation matrix between market positions
- **Mean-Variance Optimization**: Optimize portfolio weights for best risk-adjusted returns
- **Diversification Metrics**: Track portfolio diversification ratio
- **Position Sizing**: Get optimal position size recommendations across multiple markets
- **Risk Analysis**: Identify correlated market pairs and concentration risk

### ⚡ Arbitrage Detection
- **Binary Market Arbitrage**: Detect when YES + NO probabilities don't sum to 1
- **Cross-Market Arbitrage**: Find discrepancies between related markets
- **Automated Scanning**: Scan all available markets for arbitrage opportunities
- **Capital Allocation**: Calculate optimal bet sizes for arbitrage trades
- **Profit Estimation**: Estimate expected profit for each arbitrage opportunity

### 🤖 Ensemble AI Strategy
- **Multi-Model Prediction**: Combine LLM, base rates, momentum, and contrarian signals
- **Weighted Voting**: Ensemble probabilities with configurable model weights
- **Confidence Scoring**: Measure prediction confidence and model agreement
- **Variance Analysis**: Quantify uncertainty across different models
- **Model Calibration**: Adjust weights based on historical performance

### 📉 Backtesting Framework
- **Historical Simulation**: Test strategies on past market data
- **Performance Metrics**: Calculate ROI, Sharpe ratio, max drawdown, win rate
- **Strategy Comparison**: Compare multiple strategy configurations side-by-side
- **Trade-by-Trade Analysis**: Detailed breakdown of each simulated trade
- **Risk Assessment**: Evaluate strategy risk before deploying live

### 🔔 Alert System
- **Webhook Notifications**: Send alerts to any webhook endpoint
- **Email Alerts**: Receive notifications via email
- **Trading Opportunities**: Get alerted to high-edge trading chances
- **P&L Milestones**: Notifications for profit/loss thresholds
- **Arbitrage Alerts**: Instant notifications of arbitrage opportunities
- **Alert History**: Track all past alerts and notifications

### 📊 Advanced Analytics
- **Real-time Dashboard**: Live P&L tracking, ROI, win rate, and portfolio metrics
- **Performance Charts**: Cumulative P&L, win/loss distribution, edge analysis
- **Trade History**: Detailed logs of all trades with export functionality
- **Market Analysis**: AI-driven insights on market sentiment and key factors
- **Correlation Heatmaps**: Visualize market correlations
- **Backtesting Charts**: Performance visualization for backtested strategies

### 🎨 Professional GUI
- **Dark Blue Theme**: Modern, professional interface optimized for trading
- **9 Interactive Tabs**: Dashboard, Live Trading, Analytics, Trade History, Portfolio Optimizer, Arbitrage, Ensemble AI, Backtesting, Alerts
- **Live Market Monitoring**: Real-time market data with refresh capability
- **Interactive Trading**: One-click bet placement with AI recommendations
- **Configuration Panel**: Easy-to-use settings for API keys and trading parameters

## 🚀 Quick Start

### 1. Get Your API Keys

**Manifold Markets API Key (Required):**
1. Go to [manifold.markets](https://manifold.markets)
2. Create an account and log in
3. Navigate to your profile → Edit
4. Scroll down to find the API key section
5. Click "Refresh" to generate a key

**OpenAI API Key (Optional but Recommended):**
1. Go to [platform.openai.com](https://platform.openai.com)
2. Create an account and log in
3. Navigate to API keys section
4. Create a new API key

### 2. Configure Environment

Create a `.env` file in the project root:

```bash
MANIFOLD_API_KEY=your_manifold_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Bot

The bot will start automatically on Replit, or run manually:

```bash
streamlit run app.py --server.port 5000
```

## 📖 How It Works

### Trading Strategy

1. **Market Discovery**: Fetches all open markets created by MikhailTal
2. **AI Analysis**: Uses GPT-5 to estimate probability and analyze sentiment
3. **Edge Detection**: Compares AI probability vs market probability
4. **Position Sizing**: Calculates optimal bet using fractional Kelly criterion
5. **Market Impact**: Adjusts bet size based on market liquidity
6. **Execution**: Places bet if edge exceeds threshold and confidence is high

### Kelly Criterion Implementation

The bot uses a sophisticated Kelly criterion implementation:

```
Kelly % = (p * b - q) / b

Where:
- p = probability of winning
- q = probability of losing (1 - p)
- b = odds received on the bet
```

Features:
- **Fractional Kelly**: Uses 25% of full Kelly by default (conservative)
- **Market Impact Adjustment**: Limits bets to 10% of market liquidity
- **Dynamic Sizing**: Scales with bankroll and edge size

### AI Strategy

**Probability Estimation:**
- Analyzes market question and context
- Considers historical precedents and base rates
- Evaluates current trends and evidence
- Outputs calibrated probability estimate

**Sentiment Analysis:**
- Identifies bullish/bearish/neutral sentiment
- Extracts key factors influencing outcome
- Provides confidence level and reasoning

## 🎮 Usage Guide

### Dashboard Tab
- View overall performance metrics (P&L, ROI, win rate)
- Monitor portfolio breakdown and trading activity
- Analyze cumulative P&L chart

### Live Trading Tab
1. Click "Refresh Markets" to load MikhailTal's markets
2. Expand a market to see details
3. Click "Analyze with AI" to get probability estimate
4. Review AI recommendation and edge
5. Click "Place Bet" to execute (if edge is sufficient)

### Analytics Tab
- View win/loss distribution pie chart
- Analyze edge distribution histogram
- Track trading activity over time

### Trade History Tab
- Review all past trades with details
- Filter and sort trade history
- Export trades to CSV for analysis

## ⚙️ Configuration

### Trading Parameters (Sidebar)

- **Bankroll**: Your total trading capital ($100-$100,000)
- **Min Confidence**: Minimum AI confidence to trade (0-1)
- **Min Edge**: Minimum edge required to bet (0-0.5)
- **Kelly Fraction**: Fraction of Kelly to use (0.1-1.0)
- **Min/Max Bet**: Bet size limits

### Recommended Settings

**Conservative:**
- Kelly Fraction: 0.25
- Min Confidence: 0.7
- Min Edge: 0.1

**Moderate:**
- Kelly Fraction: 0.5
- Min Confidence: 0.6
- Min Edge: 0.05

**Aggressive:**
- Kelly Fraction: 1.0
- Min Confidence: 0.5
- Min Edge: 0.03

## 🏗️ Architecture

```
manifold-trading-bot/
├── app.py                 # Main Streamlit application
├── bot/
│   ├── __init__.py       # Package initialization
│   ├── api_client.py     # Manifold Markets API client
│   ├── strategies.py     # AI trading strategies
│   ├── kelly.py          # Kelly criterion calculator
│   ├── portfolio.py      # Performance tracking
│   └── config.py         # Configuration management
├── data/
│   └── portfolio.json    # Trade history storage
└── README.md
```

## 🔬 Improvements Over manifoldbot

1. **Professional Web GUI**: Full-featured Streamlit interface vs command-line (9 interactive tabs)
2. **Enhanced AI**: GPT-5 integration with sentiment analysis and ensemble learning
3. **Portfolio Optimization**: Correlation analysis and mean-variance optimization
4. **Arbitrage Detection**: Automated scanning for risk-free profit opportunities
5. **Ensemble Strategy**: Combine multiple models for improved prediction accuracy
6. **Backtesting Framework**: Test strategies on historical data before going live
7. **Alert System**: Real-time notifications via webhook and email
8. **Better Risk Management**: Fractional Kelly with market impact adjustment
9. **Advanced Analytics**: Real-time charts, correlation heatmaps, performance tracking
10. **User Experience**: Interactive trading with one-click execution
11. **Targeted Trading**: Filters specifically for MikhailTal markets

## 📊 Performance Tracking

The bot tracks:
- Total P&L and ROI
- Win rate and average edge
- Individual trade outcomes
- Cumulative performance over time
- Position sizing and risk metrics

All data is persisted in `data/portfolio.json`.

## 🛡️ Risk Management

- **Position Limits**: Configurable min/max bet sizes
- **Edge Requirements**: Only trades with sufficient edge
- **Confidence Thresholds**: Filters low-confidence predictions
- **Market Impact**: Adjusts for liquidity to avoid moving markets
- **Fractional Kelly**: Conservative sizing to reduce variance

## 🤝 Contributing to manifoldbot

We've prepared comprehensive contribution proposals for manifoldbot. See [MANIFOLDBOT_CONTRIBUTIONS.md](docs/MANIFOLDBOT_CONTRIBUTIONS.md) for details.

**High-Priority Contributions:**
1. **Streamlit Web Interface**: Professional GUI with 9 interactive tabs
2. **Enhanced Kelly Criterion**: Fractional Kelly with market impact adjustment
3. **GPT-5 Integration**: Update to latest OpenAI model
4. **Ensemble AI Strategy**: Multi-model prediction system
5. **Backtesting Framework**: Historical strategy testing
6. **Portfolio Optimization**: Correlation analysis and optimal allocation
7. **Arbitrage Detection**: Automated arbitrage scanning
8. **Alert System**: Webhook and email notifications

Each contribution includes:
- Implementation code
- Example usage
- Benefits analysis
- Integration guide
- Pull request template

## 📝 License

MIT License - Feel free to use and modify

## ⚠️ Disclaimer

This bot is for educational and research purposes. Manifold Markets uses play money, but:

- Past performance does not guarantee future results
- AI predictions are not perfect and can be wrong
- Always review trades before execution
- Start with small positions to test strategies
- Monitor performance and adjust parameters

## 🙏 Acknowledgments

- Built on top of [manifoldbot](https://github.com/microprediction/manifoldbot)
- Powered by OpenAI GPT-5
- Uses Manifold Markets API
- Implements Kelly criterion from gambling theory

## 📧 Support

For issues or questions:
1. Check the configuration settings
2. Verify API keys are correct
3. Review the trade history for patterns
4. Adjust parameters based on performance

---

**Happy Trading! 📈**
