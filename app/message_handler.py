import os
import requests
from typing import List
from ib_async.contract import Contract

from models import OptionSpreads


class MessageHandler:
  def __init__(self):
    # Replace Twilio initialization with ntfy topic
    self.ntfy_topic = os.getenv("NOTIFYSH_TOPIC")
    self.ntfy_url = f"https://ntfy.sh/{self.ntfy_topic}"

  def send_option_spreads(self, positions: List[OptionSpreads]) -> None:
    """
    Send option spreads update via ntfy.sh
    """
    message_body = self._format_option_spreads(positions)
    self._send_message(message_body)

  def _send_message(self, message: str, priority: str = "default") -> None:
    """Helper method to send message via ntfy.sh"""
    try:
      requests.post(
        self.ntfy_url,
        data=message.encode("utf-8"),
        headers={
          "Title": "Trading Bot Update",
          "Priority": priority,
          "Tags": "trading-bot",
        },
      )
    except Exception as e:
      print(f"Failed to send notification: {str(e)}")

  def _format_option_spreads(self, positions: List[OptionSpreads]) -> str:
    """Format position information into readable message"""
    message = "Current Option Spreads:\n"
    for position in positions:
      message += f"{position.expiry}: {position.symbol} - {position.size} x {position.strike} {position.right}\n"
    return message

  def _format_contract_message(self, contract: Contract) -> str:
    """Format contract information into readable message"""
    message = f"Target Spread: {contract.symbol}\n"
    message += f"Expiry: {contract.lastTradeDateOrContractMonth}\n"
    message += f"Strike: {contract.strike}\n"
    message += f"Right: {contract.right}\n"
    return message

  def send_alert(self, alert_message: str) -> None:
    """Send immediate alert message"""
    self._send_message(f"🚨 ALERT: {alert_message}", priority="urgent")

  def send_notification(self, notification_message: str) -> None:
    """Send notification message"""
    self._send_message(f"📢 {notification_message}", priority="default")


if __name__ == "__main__":
  message_handler = MessageHandler()

  # Send an alert
  message_handler.send_alert("High volatility detected!")
