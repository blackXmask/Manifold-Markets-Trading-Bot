from typing import Dict, List, Optional
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json

class AlertSystem:
    """Real-time alerts and notifications for trading opportunities"""
    
    def __init__(
        self,
        webhook_url: Optional[str] = None,
        email_config: Optional[Dict] = None
    ):
        self.webhook_url = webhook_url
        self.email_config = email_config or {}
        self.alert_history = []
    
    def send_webhook_alert(self, alert_data: Dict) -> bool:
        """
        Send alert via webhook
        
        Args:
            alert_data: Alert information to send
        
        Returns:
            True if successful, False otherwise
        """
        if not self.webhook_url:
            return False
        
        try:
            payload = {
                "timestamp": datetime.now().isoformat(),
                "alert_type": alert_data.get('type', 'general'),
                "message": alert_data.get('message', ''),
                "data": alert_data.get('data', {})
            }
            
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            response.raise_for_status()
            return True
            
        except Exception as e:
            print(f"Webhook alert failed: {e}")
            return False
    
    def send_email_alert(self, alert_data: Dict) -> bool:
        """
        Send alert via email
        
        Args:
            alert_data: Alert information to send
        
        Returns:
            True if successful, False otherwise
        """
        if not self.email_config.get('smtp_server'):
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config.get('from_address', 'bot@manifold.com')
            msg['To'] = self.email_config.get('to_address', '')
            msg['Subject'] = f"Trading Alert: {alert_data.get('type', 'General')}"
            
            body = f"""
Trading Bot Alert

Type: {alert_data.get('type', 'General')}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Message: {alert_data.get('message', '')}

Details:
{json.dumps(alert_data.get('data', {}), indent=2)}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(
                self.email_config.get('smtp_server', ''),
                self.email_config.get('smtp_port', 587)
            ) as server:
                server.starttls()
                server.login(
                    self.email_config.get('username', ''),
                    self.email_config.get('password', '')
                )
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Email alert failed: {e}")
            return False
    
    def alert_trading_opportunity(
        self,
        market_question: str,
        ai_probability: float,
        market_probability: float,
        edge: float,
        recommended_bet: float,
        direction: str
    ):
        """Alert about a trading opportunity"""
        alert_data = {
            "type": "trading_opportunity",
            "message": f"High-edge opportunity detected: {market_question[:100]}...",
            "data": {
                "market_question": market_question,
                "ai_probability": ai_probability,
                "market_probability": market_probability,
                "edge": edge,
                "recommended_bet": recommended_bet,
                "direction": direction
            }
        }
        
        self.alert_history.append(alert_data)
        
        self.send_webhook_alert(alert_data)
        self.send_email_alert(alert_data)
    
    def alert_pnl_milestone(
        self,
        total_pnl: float,
        roi: float,
        milestone_type: str
    ):
        """Alert about P&L milestone"""
        alert_data = {
            "type": "pnl_milestone",
            "message": f"P&L Milestone: {milestone_type}",
            "data": {
                "total_pnl": total_pnl,
                "roi": roi,
                "milestone_type": milestone_type
            }
        }
        
        self.alert_history.append(alert_data)
        
        self.send_webhook_alert(alert_data)
        self.send_email_alert(alert_data)
    
    def alert_arbitrage_opportunity(
        self,
        opportunity: Dict
    ):
        """Alert about arbitrage opportunity"""
        alert_data = {
            "type": "arbitrage_opportunity",
            "message": f"Arbitrage detected: {opportunity.get('type', 'Unknown')}",
            "data": opportunity
        }
        
        self.alert_history.append(alert_data)
        
        self.send_webhook_alert(alert_data)
        self.send_email_alert(alert_data)
    
    def alert_portfolio_warning(
        self,
        warning_type: str,
        details: Dict
    ):
        """Alert about portfolio warnings"""
        alert_data = {
            "type": "portfolio_warning",
            "message": f"Portfolio Warning: {warning_type}",
            "data": details
        }
        
        self.alert_history.append(alert_data)
        
        self.send_webhook_alert(alert_data)
        self.send_email_alert(alert_data)
    
    def get_alert_history(self, limit: int = 50) -> List[Dict]:
        """Get recent alert history"""
        return self.alert_history[-limit:]
    
    def clear_alert_history(self):
        """Clear alert history"""
        self.alert_history = []
