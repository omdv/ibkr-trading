from twilio.rest import Client
import os
from typing import Dict


class TradingBotMessageHandler:
  def __init__(self):
    # Initialize Twilio client with your credentials
    self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    self.from_number = f"whatsapp:{os.getenv('TWILIO_WHATSAPP_NUMBER')}"
    self.to_number = f"whatsapp:{os.getenv('ADMIN_WHATSAPP_NUMBER')}"
    self.client = Client(self.account_sid, self.auth_token)

  def send_status_update(self, status: Dict) -> None:
    """
    Send trading bot status update via WhatsApp
    status: Dictionary containing status information
    """
    message_body = self._format_status_message(status)
    self._send_message(message_body)

  def send_alert(self, alert_message: str) -> None:
    """Send immediate alert message"""
    self._send_message(f"ALERT: {alert_message}")

  def send_trade_notification(self, trade_info: Dict) -> None:
    """Send notification about executed trade"""
    message = self._format_trade_message(trade_info)
    self._send_message(message)

  def _send_message(self, message: str) -> None:
    """Helper method to send WhatsApp message via Twilio"""
    try:
      self.client.messages.create(
        body=message, from_=self.from_number, to=self.to_number
      )
    except Exception as e:
      print(f"Failed to send WhatsApp message: {str(e)}")

  def _format_status_message(self, status: Dict) -> str:
    """Format status dictionary into readable message"""
    message = "Trading Bot Status:\n"
    message += f"Active: {status.get('active', False)}\n"
    message += f"Position: {status.get('position', 'None')}\n"
    message += f"Last Trade: {status.get('last_trade', 'None')}\n"
    message += f"Balance: ${status.get('balance', 0):,.2f}\n"
    message += f"24h PnL: {status.get('daily_pnl', '0.00')}%"
    return message

  def _format_trade_message(self, trade: Dict) -> str:
    """Format trade information into readable message"""
    message = "Trade Executed:\n"
    message += f"Action: {trade.get('action', 'Unknown')}\n"
    message += f"Symbol: {trade.get('symbol', 'Unknown')}\n"
    message += f"Price: ${trade.get('price', 0):,.2f}\n"
    message += f"Size: {trade.get('size', 0)}\n"
    message += f"Time: {trade.get('timestamp', 'Unknown')}"
    return message


if __name__ == "__main__":
  message_handler = TradingBotMessageHandler()

  # Send a status update
  status = {
    "active": True,
    "position": "LONG",
    "last_trade": "BTC/USD",
    "balance": 10000,
    "daily_pnl": "+2.5",
  }
  message_handler.send_status_update(status)

  # Send an alert
  message_handler.send_alert("High volatility detected!")

  # Send a trade notification
  trade = {
    "action": "BUY",
    "symbol": "BTC/USD",
    "price": 50000,
    "size": 0.1,
    "timestamp": "2024-03-20 14:30:00",
  }
  message_handler.send_trade_notification(trade)
