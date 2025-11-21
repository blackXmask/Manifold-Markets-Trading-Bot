#  Manifold Markets Trading Bot

A professional AI-powered trading bot for **Manifold Markets**, targeting markets created by **MikhailTal**. Features a sleek **Streamlit GUI**, advanced AI strategies, portfolio optimization, arbitrage detection, ensemble learning, backtesting, and real-time analytics.

<p align="center">
  <img src="https://github.com/user-attachments/assets/f13edb5e-181f-44fb-9dc7-1e5200904c8f" alt="q1" width="720" />
  <br>
  <img src="https://github.com/user-attachments/assets/651b68df-a982-43f4-a8ad-c8a358f654c6" alt="q2" width="720" />
  <br>
  <img src="https://github.com/user-attachments/assets/339d446f-7849-4929-9a39-91b829e4085d" alt="q3" width="720" />
</p>

---

## ✨ Key Features

### Core Trading

* **Targeted Markets**: Trades only on MikhailTal's markets
* **AI-Powered Analysis**: GPT-5 probability estimation & sentiment analysis
* **Kelly Criterion**: Optimized bet sizing
* **Risk Management**: Confidence thresholds, edge detection, position limits
<img width="1332" height="71" alt="q4" src="https://github.com/user-attachments/assets/8adbb1ca-344d-401d-a894-c1c79fedc389" />


### Portfolio & Arbitrage

* **Portfolio Optimization**: Correlation, diversification & position sizing
* **Arbitrage Detection**: Binary & cross-market opportunities
* **Real-Time Alerts**: Webhook, email, and trading opportunity notifications

### Analytics & GUI

* **Backtesting Framework**: Historical simulations & strategy comparisons
* **Interactive Dashboard**: P&L, ROI, win rate, correlation heatmaps
* **Professional GUI**: Dark blue theme, 9 interactive tabs, live market monitoring

---

## 🚀 Quick Start

### 1. Get API Keys

* **Manifold Markets**: [Generate API key](https://manifold.markets/profile/edit)
* **OpenAI** (optional): [API key](https://platform.openai.com/account/api-keys)

### 2. Setup Virtual Environment

```bash
# Create & activate venv
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate      # Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Keys

Insert API keys in `.env` or input fields:

```bash
MANIFOLD_API_KEY=your_manifold_api_key
OPENAI_API_KEY=your_openai_api_key
```

### 4. Run Bot

```bash
streamlit run app.py --server.port 5000
```

---

## ⚙️ How It Works

1. Fetch markets from MikhailTal
2. AI analyzes probability & sentiment
3. Detect edge & calculate bet using Kelly criterion
4. Adjust for market liquidity and execute trade
5. Track performance in real-time dashboard

---

## 🏗️ Architecture

```
app.py                 # Streamlit frontend
bot/                    # Core trading logic
├── api_client.py       # API integration
├── strategies.py       # AI trading strategies
├── kelly.py            # Bet sizing
├── portfolio.py        # Portfolio & P&L tracking
└── config.py           # Config management
data/portfolio.json     # Trade history
```

---

## ⚡ Why Use This Bot

* Professional web GUI with interactive tabs
* GPT-5 powered AI predictions with ensemble strategies
* Portfolio optimization & arbitrage detection
* Real-time alerts & advanced analytics
* Risk-managed fractional Kelly betting

---

## 📝 License

MIT License – Free to use and modify.

---

## ⚠️ Disclaimer

For **educational & research purposes** only.

* Manifold Markets uses play money
* AI predictions are not financial advice
* Review trades before execution

---

## 📧 Support

* Check configuration & API keys
* Monitor trade history & performance
* Adjust settings as needed

---

**Happy Trading! 📈**

---


