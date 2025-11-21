import os
import re
from typing import Optional, Dict
from openai import OpenAI

class TradingStrategies:
    """AI-powered trading strategies for Manifold Markets"""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        self.openai_api_key = openai_api_key
        if openai_api_key:
            # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
            # do not change this unless explicitly requested by the user
            self.client = OpenAI(api_key=openai_api_key)
    
    def estimate_probability_llm(self, question: str, description: str = "") -> Optional[float]:
        """
        Use LLM to estimate probability of a YES outcome
        
        Args:
            question: Market question
            description: Additional market description/context
        
        Returns:
            Estimated probability (0-1) or None if estimation fails
        """
        if not self.openai_api_key:
            return None
        
        try:
            prompt = f"""You are a probability estimation expert. Analyze the following prediction market question and estimate the probability of a YES outcome.

Question: {question}

{f"Additional context: {description}" if description else ""}

Provide a probability estimate between 0 and 1, considering:
- Historical precedents
- Current trends and evidence
- Base rates and statistical reasoning
- Potential biases

Respond with ONLY a number between 0 and 1 (e.g., 0.65 for 65% probability)."""

            # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-5",
                messages=[{"role": "user", "content": prompt}],
                max_completion_tokens=100
            )
            
            result = response.choices[0].message.content.strip()
            
            prob_match = re.search(r'0?\.\d+|\d+\.\d+|0|1', result)
            if prob_match:
                probability = float(prob_match.group())
                return max(0.01, min(0.99, probability))
            
            return None
            
        except Exception as e:
            print(f"Error estimating probability with LLM: {e}")
            return None
    
    def analyze_market_sentiment(self, question: str, description: str = "") -> Dict:
        """
        Analyze market sentiment and key factors
        
        Returns:
            Dict with sentiment analysis, key_factors, confidence
        """
        if not self.openai_api_key:
            return {
                "sentiment": "neutral",
                "key_factors": [],
                "confidence": 0.5,
                "reasoning": "No OpenAI API key provided"
            }
        
        try:
            prompt = f"""Analyze this prediction market question and provide:
1. Sentiment (bullish/bearish/neutral)
2. Key factors that will influence the outcome
3. Confidence level (0-1)
4. Brief reasoning

Question: {question}
{f"Context: {description}" if description else ""}

Respond in this exact format:
Sentiment: [bullish/bearish/neutral]
Key Factors: [factor1, factor2, factor3]
Confidence: [0-1]
Reasoning: [brief explanation]"""

            # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-5",
                messages=[{"role": "user", "content": prompt}],
                max_completion_tokens=300
            )
            
            result = response.choices[0].message.content.strip()
            
            sentiment_match = re.search(r'Sentiment:\s*(\w+)', result, re.IGNORECASE)
            factors_match = re.search(r'Key Factors:\s*\[(.*?)\]', result, re.IGNORECASE)
            confidence_match = re.search(r'Confidence:\s*(0?\.\d+|\d+\.\d+|0|1)', result, re.IGNORECASE)
            reasoning_match = re.search(r'Reasoning:\s*(.+)', result, re.IGNORECASE | re.DOTALL)
            
            sentiment = sentiment_match.group(1).lower() if sentiment_match else "neutral"
            factors = [f.strip() for f in factors_match.group(1).split(',')] if factors_match else []
            confidence = float(confidence_match.group(1)) if confidence_match else 0.5
            reasoning = reasoning_match.group(1).strip() if reasoning_match else "No reasoning provided"
            
            return {
                "sentiment": sentiment,
                "key_factors": factors,
                "confidence": confidence,
                "reasoning": reasoning
            }
            
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return {
                "sentiment": "neutral",
                "key_factors": [],
                "confidence": 0.5,
                "reasoning": f"Error: {str(e)}"
            }
    
    def detect_mispricing(
        self,
        ai_probability: float,
        market_probability: float,
        min_confidence: float = 0.6,
        min_edge: float = 0.05
    ) -> Optional[Dict]:
        """
        Detect if market is mispriced based on AI analysis
        
        Returns:
            Dict with recommendation, edge, confidence or None
        """
        edge = abs(ai_probability - market_probability)
        
        if edge < min_edge:
            return None
        
        confidence = min(1.0, edge / 0.3)
        
        if confidence < min_confidence:
            return None
        
        direction = "YES" if ai_probability > market_probability else "NO"
        
        return {
            "direction": direction,
            "edge": edge,
            "confidence": confidence,
            "ai_probability": ai_probability,
            "market_probability": market_probability,
            "recommendation": f"Bet {direction} - Market underpricing by {edge*100:.1f}%"
        }
