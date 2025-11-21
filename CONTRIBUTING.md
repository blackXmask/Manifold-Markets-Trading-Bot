# Contributing to manifoldbot

This project builds upon and improves the [manifoldbot](https://github.com/microprediction/manifoldbot) package. Here are potential contributions we could make back to the main manifoldbot repository:

## 🎯 Proposed Pull Requests

### 1. Web Interface Integration
**Priority: High**

Add Streamlit-based web interface to manifoldbot for easier bot management and monitoring.

**Benefits:**
- Lower barrier to entry for non-technical users
- Real-time visualization of bot performance
- Interactive market analysis and trading
- Better debugging and monitoring capabilities

**Files to contribute:**
- `manifoldbot/ui/` - Streamlit interface components
- `manifoldbot/ui/dashboard.py` - Performance dashboard
- `manifoldbot/ui/trading.py` - Live trading interface

### 2. Enhanced Kelly Criterion
**Priority: High**

Improve position sizing with fractional Kelly and market impact adjustment.

**Current manifoldbot implementation:**
```python
# Basic Kelly without market impact consideration
kelly = (p * b - q) / b
```

**Our improvement:**
```python
# Fractional Kelly with market impact adjustment
kelly = (p * b - q) / b
kelly_bet = kelly * kelly_fraction  # Conservative sizing
adjusted_bet = min(kelly_bet, liquidity * 0.1)  # Prevent market impact
```

**Benefits:**
- Reduces variance and drawdowns
- Prevents moving markets with large bets
- More robust for different market conditions

**Files to contribute:**
- `manifoldbot/betting/kelly_improved.py`

### 3. GPT-5 Integration
**Priority: Medium**

Update LLM integration to support GPT-5 (released August 2025).

**Changes:**
- Update model parameter from "gpt-4" to "gpt-5"
- Remove temperature parameter (not supported in GPT-5)
- Use max_completion_tokens instead of max_tokens
- Add structured output support

**Files to contribute:**
- `manifoldbot/strategies/llm_strategy.py`

### 4. Sentiment Analysis Module
**Priority: Medium**

Add comprehensive market sentiment analysis.

**Features:**
- Bullish/bearish/neutral classification
- Key factor extraction
- Confidence scoring
- Reasoning explanation

**Files to contribute:**
- `manifoldbot/analysis/sentiment.py`

### 5. Performance Analytics
**Priority: Medium**

Enhanced performance tracking and analytics.

**Features:**
- Cumulative P&L tracking
- Win rate and ROI calculations
- Trade history persistence
- Export to CSV functionality
- Interactive charts

**Files to contribute:**
- `manifoldbot/analytics/tracker.py`
- `manifoldbot/analytics/visualizations.py`

### 6. Market Filtering
**Priority: Low**

Add ability to filter markets by creator, tags, or custom criteria.

**Use cases:**
- Trade only specific creators' markets
- Focus on certain market categories
- Custom market selection logic

**Files to contribute:**
- `manifoldbot/filters/market_filters.py`

### 7. Risk Management Controls
**Priority: High**

Comprehensive risk management system.

**Features:**
- Position limits (min/max bet sizes)
- Edge requirements (minimum edge to trade)
- Confidence thresholds
- Exposure limits per market
- Daily/weekly loss limits

**Files to contribute:**
- `manifoldbot/risk/controls.py`

### 8. API Rate Limiting
**Priority: Low**

Add proper rate limiting and retry logic for API calls.

**Features:**
- Exponential backoff on failures
- Respect API rate limits
- Queue system for multiple bets
- Error handling and logging

**Files to contribute:**
- `manifoldbot/api/rate_limiter.py`

## 📝 How to Contribute

### Step 1: Identify Contribution
Choose one of the proposed improvements above or suggest your own.

### Step 2: Fork manifoldbot
```bash
git clone https://github.com/microprediction/manifoldbot
cd manifoldbot
git checkout -b feature/your-feature-name
```

### Step 3: Implement Changes
- Write clean, documented code
- Follow existing code style
- Add tests for new functionality
- Update documentation

### Step 4: Test Thoroughly
```bash
pytest tests/
```

### Step 5: Submit Pull Request
- Clear description of changes
- Benefits and use cases
- Example usage
- Test results

## 🎨 Code Style Guidelines

### Python Style
- Follow PEP 8
- Use type hints
- Docstrings for all public methods
- Clear variable names

### Example:
```python
def calculate_kelly_fraction(
    probability: float,
    market_probability: float,
    kelly_fraction: float = 0.25
) -> Optional[float]:
    """
    Calculate optimal bet size using fractional Kelly criterion.
    
    Args:
        probability: Our estimated probability (0-1)
        market_probability: Current market probability (0-1)
        kelly_fraction: Fraction of Kelly to use (default 0.25)
    
    Returns:
        Fraction of bankroll to bet, or None if no bet
    """
    # Implementation
    pass
```

## 🧪 Testing Requirements

All contributions should include:
- Unit tests for core functionality
- Integration tests for API interactions
- Example usage scripts
- Documentation updates

## 📚 Documentation

Update these files as needed:
- `README.md` - Main documentation
- `CHANGELOG.md` - Version history
- `docs/` - Detailed guides
- Inline code comments

## 🤝 Community

Join the discussion:
- Create issues for bugs or feature requests
- Discuss major changes before implementing
- Help review other pull requests
- Share your bot's performance

## ⚖️ License

All contributions will be under the MIT license to match manifoldbot.

---

**Thank you for contributing to manifoldbot!** 🎉
