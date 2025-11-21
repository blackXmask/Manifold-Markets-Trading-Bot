"""
Simple example of using the trading bot without GUI
Run this script to see how the bot works programmatically
"""

import os
from bot import ManifoldClient, TradingStrategies, KellyCriterion, PortfolioTracker, Config

def main():
    print("🤖 Manifold Trading Bot - Simple Example\n")
    
    # Initialize components
    client = ManifoldClient(os.getenv("MANIFOLD_API_KEY"))
    strategies = TradingStrategies(os.getenv("OPENAI_API_KEY"))
    portfolio = PortfolioTracker()
    
    # Fetch MikhailTal markets
    print("📊 Fetching MikhailTal markets...")
    markets = client.get_open_markets(creator_username="MikhailTal")
    print(f"Found {len(markets)} open markets\n")
    
    # Analyze first market
    if markets:
        market = markets[0]
        print(f"🎯 Analyzing: {market['question']}")
        print(f"   Market Probability: {market.get('probability', 0)*100:.1f}%")
        print(f"   Volume: ${market.get('volume', 0):.2f}")
        print(f"   Liquidity: ${market.get('totalLiquidity', 0):.2f}\n")
        
        # Get AI probability estimate
        if strategies.openai_api_key:
            print("🤖 Getting AI probability estimate...")
            ai_prob = strategies.estimate_probability_llm(
                market['question'],
                market.get('description', '')
            )
            
            if ai_prob:
                print(f"   AI Probability: {ai_prob*100:.1f}%")
                
                # Calculate optimal bet
                market_prob = market.get('probability', 0.5)
                edge = abs(ai_prob - market_prob)
                print(f"   Edge: {edge*100:.1f}%\n")
                
                if edge >= Config.MIN_EDGE:
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
                        print("💰 Recommendation:")
                        print(f"   Bet ${bet_info['bet_amount']} {bet_info['direction']}")
                        print(f"   Kelly Fraction: {bet_info['kelly_fraction']}")
                        print(f"   Confidence: High\n")
                        
                        # Uncomment to actually place bet
                        # result = client.place_bet(
                        #     market['id'],
                        #     bet_info['bet_amount'],
                        #     bet_info['direction']
                        # )
                        # if result:
                        #     portfolio.add_trade(
                        #         market['id'],
                        #         market['question'],
                        #         bet_info['direction'],
                        #         bet_info['bet_amount'],
                        #         market_prob,
                        #         ai_prob,
                        #         bet_info['edge']
                        #     )
                        #     print("✅ Bet placed successfully!")
                    else:
                        print("ℹ️  No bet recommended (insufficient edge)\n")
                else:
                    print("ℹ️  Edge too small to trade\n")
            else:
                print("❌ Failed to get AI probability\n")
        else:
            print("⚠️  OpenAI API key not configured\n")
    
    # Show portfolio stats
    print("📈 Portfolio Statistics:")
    stats = portfolio.get_statistics()
    print(f"   Total Trades: {stats['total_trades']}")
    print(f"   Total P&L: ${stats['total_pnl']}")
    print(f"   ROI: {stats['roi']}%")
    print(f"   Win Rate: {stats['win_rate']}%")

if __name__ == "__main__":
    main()
