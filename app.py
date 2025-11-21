import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time
import os
import numpy as np

from bot import (
    ManifoldClient, TradingStrategies, KellyCriterion, PortfolioTracker, Config,
    PortfolioOptimizer, ArbitrageDetector, EnsembleStrategy, Backtester, AlertSystem
)

st.set_page_config(
    page_title="Manifold Trading Bot",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

DARK_BLUE_THEME = """
<style>
    :root {
        --primary-blue: #1e3a8a;
        --secondary-blue: #1e40af;
        --accent-blue: #3b82f6;
        --dark-bg: #0f172a;
        --card-bg: #1e293b;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #3b82f6;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .stat-value {
        font-size: 32px;
        font-weight: bold;
        color: #60a5fa;
        margin: 0;
    }
    
    .stat-label {
        font-size: 14px;
        color: #94a3b8;
        margin: 0;
    }
    
    .market-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        transition: all 0.3s;
    }
    
    .market-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    .trade-button {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        font-weight: bold;
        cursor: pointer;
    }
    
    .success-badge {
        background: #065f46;
        color: #10b981;
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 12px;
    }
    
    .warning-badge {
        background: #78350f;
        color: #f59e0b;
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 12px;
    }
    
    .error-badge {
        background: #7f1d1d;
        color: #ef4444;
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 12px;
    }
    
    h1, h2, h3 {
        color: #e2e8f0 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #1e293b;
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #334155;
        color: #94a3b8;
        border-radius: 5px;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
    }
</style>
"""

st.markdown(DARK_BLUE_THEME, unsafe_allow_html=True)

if 'client' not in st.session_state:
    st.session_state.client = None
if 'strategies' not in st.session_state:
    st.session_state.strategies = None
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = PortfolioTracker()
if 'markets' not in st.session_state:
    st.session_state.markets = []
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = None
if 'optimizer' not in st.session_state:
    st.session_state.optimizer = PortfolioOptimizer()
if 'arbitrage_detector' not in st.session_state:
    st.session_state.arbitrage_detector = ArbitrageDetector()
if 'ensemble' not in st.session_state:
    st.session_state.ensemble = None
if 'backtester' not in st.session_state:
    st.session_state.backtester = None
if 'alert_system' not in st.session_state:
    st.session_state.alert_system = AlertSystem()

st.markdown("""
<div class="main-header">
    <h1 style='margin:0; color:white;'>📈 Manifold Markets Trading Bot</h1>
    <p style='margin:5px 0 0 0; color:#e2e8f0;'>AI-Powered Trading on MikhailTal Markets</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    with st.expander("🔑 API Keys", expanded=True):
        manifold_key = st.text_input(
            "Manifold API Key",
            value=Config.MANIFOLD_API_KEY,
            type="password",
            help="Get your API key from manifold.markets"
        )
        
        openai_key = st.text_input(
            "OpenAI API Key",
            value=Config.OPENAI_API_KEY,
            type="password",
            help="Optional: For AI-powered predictions"
        )
        
        if st.button("💾 Save API Keys"):
            Config.MANIFOLD_API_KEY = manifold_key
            Config.OPENAI_API_KEY = openai_key
            st.session_state.client = ManifoldClient(manifold_key) if manifold_key else ManifoldClient()
            st.session_state.strategies = TradingStrategies(openai_key) if openai_key else TradingStrategies()
            st.success("✅ API keys saved!")
    
    with st.expander("🎯 Trading Parameters"):
        Config.DEFAULT_BANKROLL = st.number_input(
            "Bankroll ($)",
            min_value=100,
            max_value=100000,
            value=Config.DEFAULT_BANKROLL,
            step=100
        )
        
        Config.MIN_CONFIDENCE = st.slider(
            "Min Confidence",
            min_value=0.0,
            max_value=1.0,
            value=Config.MIN_CONFIDENCE,
            step=0.05
        )
        
        Config.MIN_EDGE = st.slider(
            "Min Edge (%)",
            min_value=0.0,
            max_value=0.5,
            value=Config.MIN_EDGE,
            step=0.01,
            format="%.2f"
        )
        
        Config.KELLY_FRACTION = st.slider(
            "Kelly Fraction",
            min_value=0.1,
            max_value=1.0,
            value=Config.KELLY_FRACTION,
            step=0.05
        )
        
        Config.MIN_BET = st.number_input(
            "Min Bet ($)",
            min_value=1,
            max_value=100,
            value=Config.MIN_BET
        )
        
        Config.MAX_BET = st.number_input(
            "Max Bet ($)",
            min_value=10,
            max_value=10000,
            value=Config.MAX_BET
        )
    
    st.markdown("---")
    st.markdown("### 📊 Bot Status")
    
    if st.session_state.client:
        st.markdown('<span class="success-badge">🟢 Connected</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="error-badge">🔴 Disconnected</span>', unsafe_allow_html=True)
    
    if st.session_state.strategies and st.session_state.strategies.openai_api_key:
        st.markdown('<span class="success-badge">🤖 AI Enabled</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="warning-badge">⚠️ AI Disabled</span>', unsafe_allow_html=True)

if not st.session_state.client:
    st.session_state.client = ManifoldClient(Config.MANIFOLD_API_KEY) if Config.MANIFOLD_API_KEY else ManifoldClient()
if not st.session_state.strategies:
    st.session_state.strategies = TradingStrategies(Config.OPENAI_API_KEY) if Config.OPENAI_API_KEY else TradingStrategies()
if not st.session_state.ensemble:
    st.session_state.ensemble = EnsembleStrategy(st.session_state.strategies)
if not st.session_state.backtester:
    st.session_state.backtester = Backtester(Config.DEFAULT_BANKROLL, st.session_state.strategies)

tabs = st.tabs([
    "📊 Dashboard",
    "🎯 Live Trading", 
    "📈 Analytics",
    "📜 Trade History",
    "🎲 Portfolio Optimizer",
    "⚡ Arbitrage",
    "🤖 Ensemble AI",
    "📉 Backtesting",
    "🔔 Alerts"
])

with tabs[0]:
    st.markdown("### 📊 Performance Overview")
    
    stats = st.session_state.portfolio.get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <p class="stat-label">Total P&L</p>
            <p class="stat-value" style="color: {'#10b981' if stats['total_pnl'] >= 0 else '#ef4444'}">${stats['total_pnl']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <p class="stat-label">ROI</p>
            <p class="stat-value" style="color: {'#10b981' if stats['roi'] >= 0 else '#ef4444'}">{stats['roi']}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <p class="stat-label">Win Rate</p>
            <p class="stat-value">{stats['win_rate']}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <p class="stat-label">Total Trades</p>
            <p class="stat-value">{stats['total_trades']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown("#### 📊 Portfolio Breakdown")
        st.metric("Open Positions", stats['open_trades'])
        st.metric("Closed Positions", stats['closed_trades'])
        st.metric("Total Invested", f"${stats['total_invested']}")
        st.metric("Avg Edge", f"{stats['avg_edge']}%")
    
    with col6:
        st.markdown("#### 📈 P&L Chart")
        
        df = st.session_state.portfolio.get_trades_dataframe()
        if not df.empty:
            df_sorted = df.sort_values('timestamp')
            df_sorted['cumulative_pnl'] = df_sorted['pnl'].cumsum()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_sorted['timestamp'],
                y=df_sorted['cumulative_pnl'],
                mode='lines+markers',
                name='Cumulative P&L',
                line=dict(color='#3b82f6', width=3),
                fill='tozeroy',
                fillcolor='rgba(59, 130, 246, 0.2)'
            ))
            
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=300,
                margin=dict(l=0, r=0, t=30, b=0),
                xaxis_title="Time",
                yaxis_title="Cumulative P&L ($)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No trade data available yet. Start trading to see your P&L chart!")

with tabs[1]:
    st.markdown("### 🎯 Live Market Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🔄 Refresh Markets", use_container_width=True):
            with st.spinner("Fetching MikhailTal markets..."):
                st.session_state.markets = st.session_state.client.get_open_markets(creator_username=Config.TARGET_CREATOR)
                st.session_state.last_refresh = datetime.now()
            st.success(f"✅ Loaded {len(st.session_state.markets)} markets")
    
    with col2:
        if st.session_state.last_refresh:
            st.info(f"Last refresh: {st.session_state.last_refresh.strftime('%H:%M:%S')}")
    
    if st.session_state.markets:
        st.markdown(f"**Found {len(st.session_state.markets)} open markets by MikhailTal**")
        
        for idx, market in enumerate(st.session_state.markets[:10]):
            with st.expander(f"📊 {market.get('question', 'Unknown Market')}", expanded=(idx == 0)):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Market Probability:** {market.get('probability', 0)*100:.1f}%")
                    st.markdown(f"**Volume:** ${market.get('volume', 0):.2f}")
                    st.markdown(f"**Liquidity:** ${market.get('totalLiquidity', 0):.2f}")
                    
                    if st.session_state.strategies and st.session_state.strategies.openai_api_key:
                        if st.button(f"🤖 Analyze with AI", key=f"analyze_{market['id']}"):
                            with st.spinner("Analyzing with AI..."):
                                ai_prob = st.session_state.strategies.estimate_probability_llm(
                                    market.get('question', ''),
                                    market.get('description', '')
                                )
                                
                                if ai_prob:
                                    st.session_state[f"ai_prob_{market['id']}"] = ai_prob
                                    
                                    sentiment = st.session_state.strategies.analyze_market_sentiment(
                                        market.get('question', ''),
                                        market.get('description', '')
                                    )
                                    st.session_state[f"sentiment_{market['id']}"] = sentiment
                
                with col2:
                    if f"ai_prob_{market['id']}" in st.session_state:
                        ai_prob = st.session_state[f"ai_prob_{market['id']}"]
                        market_prob = market.get('probability', 0.5)
                        
                        st.markdown(f"**AI Probability:** {ai_prob*100:.1f}%")
                        edge = abs(ai_prob - market_prob)
                        st.markdown(f"**Edge:** {edge*100:.1f}%")
                        
                        bet_info = KellyCriterion.calculate_optimal_bet(
                            Config.DEFAULT_BANKROLL,
                            ai_prob,
                            market_prob,
                            market.get('totalLiquidity', 1000),
                            Config.KELLY_FRACTION,
                            Config.MIN_EDGE,
                            Config.MIN_BET,
                            Config.MAX_BET
                        )
                        
                        if bet_info:
                            st.success(f"**Recommended Bet:** ${bet_info['bet_amount']} {bet_info['direction']}")
                            
                            if st.button(f"💰 Place Bet", key=f"bet_{market['id']}"):
                                if Config.MANIFOLD_API_KEY:
                                    result = st.session_state.client.place_bet(
                                        market['id'],
                                        bet_info['bet_amount'],
                                        bet_info['direction']
                                    )
                                    
                                    if result:
                                        st.session_state.portfolio.add_trade(
                                            market['id'],
                                            market['question'],
                                            bet_info['direction'],
                                            bet_info['bet_amount'],
                                            market_prob,
                                            ai_prob,
                                            bet_info['edge']
                                        )
                                        st.success("✅ Bet placed successfully!")
                                        st.rerun()
                                    else:
                                        st.error("❌ Failed to place bet")
                                else:
                                    st.error("❌ Manifold API key required")
                        else:
                            st.info("No bet recommended (insufficient edge)")
                    
                if f"sentiment_{market['id']}" in st.session_state:
                    sentiment = st.session_state[f"sentiment_{market['id']}"]
                    st.markdown("**AI Analysis:**")
                    st.markdown(f"- Sentiment: {sentiment['sentiment'].upper()}")
                    st.markdown(f"- Confidence: {sentiment['confidence']*100:.0f}%")
                    st.markdown(f"- Reasoning: {sentiment['reasoning']}")
    else:
        st.info("Click 'Refresh Markets' to load available markets")

with tabs[2]:
    st.markdown("### 📈 Advanced Analytics")
    
    df = st.session_state.portfolio.get_trades_dataframe()
    
    if not df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Win/Loss Distribution")
            wins = len(df[(df['status'] == 'closed') & (df['pnl'] > 0)])
            losses = len(df[(df['status'] == 'closed') & (df['pnl'] < 0)])
            
            fig = go.Figure(data=[go.Pie(
                labels=['Wins', 'Losses'],
                values=[wins, losses],
                marker=dict(colors=['#10b981', '#ef4444'])
            )])
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Edge Distribution")
            fig = px.histogram(
                df,
                x='edge',
                nbins=20,
                title='Edge Distribution',
                color_discrete_sequence=['#3b82f6']
            )
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### Trading Activity Over Time")
        df_sorted = df.sort_values('timestamp')
        df_sorted['date'] = pd.to_datetime(df_sorted['timestamp']).dt.date
        daily_trades = df_sorted.groupby('date').size().reset_index(name='count')
        
        fig = go.Figure(data=[go.Bar(
            x=daily_trades['date'],
            y=daily_trades['count'],
            marker_color='#3b82f6'
        )])
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            height=300,
            xaxis_title="Date",
            yaxis_title="Number of Trades"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No analytics data available yet. Start trading to see analytics!")

with tabs[3]:
    st.markdown("### 📜 Trade History")
    
    recent_trades = st.session_state.portfolio.get_recent_trades(50)
    
    if recent_trades:
        df_display = pd.DataFrame(recent_trades)
        
        df_display['timestamp'] = pd.to_datetime(df_display['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
        
        display_columns = ['timestamp', 'market_question', 'direction', 'amount', 'probability', 'ai_probability', 'edge', 'status', 'pnl']
        df_display = df_display[display_columns]
        
        df_display.columns = ['Time', 'Market', 'Direction', 'Amount', 'Market Prob', 'AI Prob', 'Edge', 'Status', 'P&L']
        
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Amount": st.column_config.NumberColumn("Amount", format="$%.2f"),
                "Market Prob": st.column_config.NumberColumn("Market Prob", format="%.2f"),
                "AI Prob": st.column_config.NumberColumn("AI Prob", format="%.2f"),
                "Edge": st.column_config.NumberColumn("Edge", format="%.2f"),
                "P&L": st.column_config.NumberColumn("P&L", format="$%.2f"),
            }
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Export to CSV"):
                csv = df_display.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"trades_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
    else:
        st.info("No trades recorded yet. Start trading to build your history!")

with tabs[4]:
    st.markdown("### 🎲 Portfolio Optimization")
    
    st.markdown("""
    Optimize position sizing across multiple markets using correlation analysis and mean-variance optimization.
    """)
    
    try:
        df = st.session_state.portfolio.get_trades_dataframe()
    except Exception as e:
        df = pd.DataFrame()
        st.error(f"Error loading portfolio data: {e}")
    
    if not df.empty and len(df) > 1:
        corr_matrix = st.session_state.optimizer.calculate_correlation_matrix(df.to_dict('records'))
        
        if corr_matrix is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Correlation Matrix")
                fig = go.Figure(data=go.Heatmap(
                    z=corr_matrix.values,
                    x=corr_matrix.columns,
                    y=corr_matrix.index,
                    colorscale='RdBu',
                    zmid=0
                ))
                fig.update_layout(
                    template='plotly_dark',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### Diversification Metrics")
                div_ratio = st.session_state.optimizer.calculate_diversification_ratio(corr_matrix)
                st.metric("Diversification Ratio", f"{div_ratio:.2%}")
                
                correlated_pairs = st.session_state.optimizer.identify_correlated_markets(corr_matrix, threshold=0.7)
                
                if correlated_pairs:
                    st.markdown("**Highly Correlated Pairs:**")
                    for pair in correlated_pairs[:5]:
                        st.markdown(f"- {pair['type'].upper()}: {pair['correlation']:.2f}")
        
        if st.session_state.markets:
            st.markdown("#### Position Size Recommendations")
            
            expected_returns = []
            markets_for_opt = st.session_state.markets[:5]
            
            for market in markets_for_opt:
                market_prob = market.get('probability', 0.5)
                expected_return = (1 / market_prob - 1) * market_prob if market_prob > 0 else 0
                expected_returns.append(min(expected_return, 0.5))
            
            suggestions = st.session_state.optimizer.suggest_position_sizes(
                markets_for_opt,
                Config.DEFAULT_BANKROLL,
                expected_returns
            )
            
            if suggestions:
                df_suggestions = pd.DataFrame(suggestions)
                st.dataframe(df_suggestions, use_container_width=True, hide_index=True)
    else:
        st.info("Need at least 2 trades to calculate correlations. Start trading to enable portfolio optimization!")

with tabs[5]:
    st.markdown("### ⚡ Arbitrage Detection")
    
    st.markdown("""
    Scan markets for arbitrage opportunities including binary market inefficiencies and cross-market discrepancies.
    """)
    
    if not st.session_state.markets:
        st.info("Please refresh markets first in the Live Trading tab.")
    else:
        if st.button("🔍 Scan for Arbitrage"):
            with st.spinner("Scanning markets for arbitrage opportunities..."):
                try:
                    opportunities = st.session_state.arbitrage_detector.scan_for_arbitrage(st.session_state.markets)
                    st.session_state.arbitrage_opportunities = opportunities
                except Exception as e:
                    st.error(f"Arbitrage scan failed: {e}")
                    st.session_state.arbitrage_opportunities = []
    
    if 'arbitrage_opportunities' in st.session_state and st.session_state.arbitrage_opportunities:
        st.success(f"Found {len(st.session_state.arbitrage_opportunities)} arbitrage opportunities!")
        
        for idx, opp in enumerate(st.session_state.arbitrage_opportunities[:10]):
            with st.expander(f"⚡ {opp['type'].replace('_', ' ').title()} - Profit: {opp.get('potential_profit', 0)*100:.2f}%"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    if opp['type'] == 'binary_arbitrage':
                        st.markdown(f"**Market:** {opp['market_question'][:100]}")
                        st.markdown(f"**YES Probability:** {opp['prob_yes']:.2%}")
                        st.markdown(f"**NO Probability:** {opp['prob_no']:.2%}")
                        st.markdown(f"**Implied Total:** {opp['implied_total']:.2%}")
                    elif opp['type'] == 'inverse_market_arbitrage':
                        st.markdown(f"**Market 1:** {opp['market1_question'][:80]}")
                        st.markdown(f"**Market 1 Probability:** {opp['market1_prob']:.2%}")
                        st.markdown(f"**Market 2:** {opp['market2_question'][:80]}")
                        st.markdown(f"**Market 2 Probability:** {opp['market2_prob']:.2%}")
                        st.markdown(f"**Discrepancy:** {opp['discrepancy']:.2%}")
                    
                    st.markdown(f"**Strategy:** {opp['strategy']}")
                
                with col2:
                    allocation = st.session_state.arbitrage_detector.calculate_arbitrage_allocation(
                        opp,
                        Config.DEFAULT_BANKROLL
                    )
                    
                    if allocation:
                        st.markdown("**Capital Allocation:**")
                        for key, value in allocation.items():
                            st.metric(key.replace('_', ' ').title(), f"${value:.2f}" if 'roi' not in key else f"{value:.1f}%")
        else:
            if 'arbitrage_opportunities' in st.session_state:
                st.info("No arbitrage opportunities found in current markets.")
            else:
                st.info("Click 'Scan for Arbitrage' to find opportunities")

with tabs[6]:
    st.markdown("### 🤖 Ensemble AI Strategy")
    
    st.markdown("""
    Combine multiple prediction models (LLM, base rates, momentum, contrarian) for improved accuracy.
    """)
    
    if not st.session_state.ensemble:
        st.warning("⚠️ Ensemble strategy not initialized. Please save API keys first.")
    else:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.session_state.markets:
                market_idx = st.selectbox(
                    "Select Market for Ensemble Analysis",
                    range(min(len(st.session_state.markets), 10)),
                    format_func=lambda x: st.session_state.markets[x]['question'][:80]
                )
                
                if st.button("🤖 Run Ensemble Analysis"):
                    market = st.session_state.markets[market_idx]
                    
                    with st.spinner("Running ensemble prediction..."):
                        try:
                            ensemble_result = st.session_state.ensemble.ensemble_predict(
                                market['question'],
                                market.get('description', ''),
                                market
                            )
                            st.session_state.ensemble_result = ensemble_result
                        except Exception as e:
                            st.error(f"Ensemble analysis failed: {e}")
            else:
                st.info("Refresh markets first to enable ensemble analysis")
        
        with col2:
            if 'ensemble_result' in st.session_state:
                result = st.session_state.ensemble_result
                
                st.markdown("#### Ensemble Prediction")
                st.metric("Ensemble Probability", f"{result['ensemble_probability']:.2%}")
                st.metric("Confidence", f"{result['confidence']:.2%}")
                st.metric("Model Agreement", f"{result['model_agreement']:.2%}")
                st.metric("Variance", f"{result['variance']:.4f}")
        
        if 'ensemble_result' in st.session_state:
            st.markdown("#### Individual Model Predictions")
            
            predictions = st.session_state.ensemble_result['predictions']
            df_predictions = pd.DataFrame([
                {"Model": k.replace('_', ' ').title(), "Probability": f"{v:.2%}"}
                for k, v in predictions.items()
            ])
            st.dataframe(df_predictions, use_container_width=True, hide_index=True)
            
            fig = go.Figure(data=[go.Bar(
                x=list(predictions.keys()),
                y=list(predictions.values()),
                marker_color='#3b82f6'
            )])
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                height=300,
                yaxis_title="Probability"
            )
            st.plotly_chart(fig, use_container_width=True)

with tabs[7]:
    st.markdown("### 📉 Backtesting Framework")
    
    st.markdown("""
    Test trading strategies on historical market data to evaluate performance before going live.
    """)
    
    st.warning("⚠️ Note: Backtesting requires resolved historical markets from Manifold API.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        kelly_fraction_backtest = st.slider("Kelly Fraction for Backtest", 0.1, 1.0, 0.25, 0.05)
        min_edge_backtest = st.slider("Min Edge for Backtest", 0.0, 0.2, 0.05, 0.01)
    
    with col2:
        st.markdown("#### Strategy Configuration")
        st.markdown(f"- **Kelly Fraction:** {kelly_fraction_backtest}")
        st.markdown(f"- **Min Edge:** {min_edge_backtest*100:.0f}%")
        st.markdown(f"- **Initial Capital:** ${Config.DEFAULT_BANKROLL}")
    
    if st.button("▶️ Run Backtest (Simulated)"):
        with st.spinner("Running backtest simulation..."):
            simulated_markets = []
            for i in range(20):
                simulated_markets.append({
                    'id': f'sim_{i}',
                    'question': f'Simulated Market {i+1}',
                    'probability': np.random.uniform(0.3, 0.7),
                    'totalLiquidity': np.random.uniform(500, 2000),
                    'isResolved': True,
                    'resolution': 'YES' if np.random.random() > 0.5 else 'NO'
                })
            
            metrics = st.session_state.backtester.backtest_strategy(
                simulated_markets,
                kelly_fraction_backtest,
                min_edge_backtest
            )
            
            st.session_state.backtest_results = metrics
    
    if 'backtest_results' in st.session_state:
        st.markdown("### 📊 Backtest Results")
        
        metrics = st.session_state.backtest_results
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Trades", metrics['total_trades'])
            st.metric("Win Rate", f"{metrics['win_rate']}%")
        
        with col2:
            st.metric("Total P&L", f"${metrics['total_pnl']}")
            st.metric("Avg P&L", f"${metrics['avg_pnl']}")
        
        with col3:
            st.metric("ROI", f"{metrics['roi']}%")
            st.metric("Sharpe Ratio", f"{metrics['sharpe_ratio']:.2f}")
        
        with col4:
            st.metric("Final Capital", f"${metrics['final_capital']}")
            st.metric("Max Drawdown", f"${metrics['max_drawdown']}")
        
        trade_history = st.session_state.backtester.get_trade_history()
        if not trade_history.empty:
            st.markdown("#### Trade History")
            st.dataframe(trade_history.head(20), use_container_width=True)

with tabs[8]:
    st.markdown("### 🔔 Alert Configuration")
    
    st.markdown("""
    Configure real-time alerts for trading opportunities, P&L milestones, and portfolio warnings.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Webhook Configuration")
        webhook_url = st.text_input("Webhook URL", placeholder="https://your-webhook.com/endpoint")
        
        if st.button("💾 Save Webhook"):
            st.session_state.alert_system.webhook_url = webhook_url
            st.success("Webhook URL saved!")
        
        if st.button("🧪 Test Webhook"):
            if webhook_url:
                with st.spinner("Testing webhook..."):
                    try:
                        success = st.session_state.alert_system.send_webhook_alert({
                            "type": "test",
                            "message": "Test alert from Manifold Trading Bot",
                            "data": {"timestamp": datetime.now().isoformat()}
                        })
                        if success:
                            st.success("✅ Webhook test successful!")
                        else:
                            st.error("❌ Webhook test failed - check URL and network")
                    except Exception as e:
                        st.error(f"❌ Webhook test error: {e}")
            else:
                st.warning("Please enter a webhook URL first")
    
    with col2:
        st.markdown("#### Alert Thresholds")
        
        edge_threshold = st.slider("Edge Threshold for Alerts", 0.05, 0.3, 0.1, 0.01)
        pnl_threshold = st.slider("P&L Milestone ($)", 50, 500, 100, 50)
        
        st.markdown(f"**Active Thresholds:**")
        st.markdown(f"- Alert on edges > {edge_threshold*100:.0f}%")
        st.markdown(f"- Alert on P&L milestones of ${pnl_threshold}")
    
    st.markdown("#### Recent Alerts")
    
    alert_history = st.session_state.alert_system.get_alert_history(10)
    
    if alert_history:
        for alert in alert_history:
            st.markdown(f"""
            <div class="metric-card">
                <p><strong>{alert['type'].replace('_', ' ').title()}</strong></p>
                <p>{alert['message']}</p>
                <p style="font-size: 12px; color: #94a3b8;">Data: {str(alert.get('data', {}))[:100]}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No alerts yet. Alerts will appear here when triggered.")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #94a3b8; padding: 20px;'>
    <p>🤖 Manifold Markets Trading Bot v2.0 | Built for MikhailTal Markets</p>
    <p style='font-size: 12px;'>Powered by GPT-5 • Kelly Criterion • Portfolio Optimization • Arbitrage Detection • Ensemble AI • Backtesting</p>
</div>
""", unsafe_allow_html=True)
