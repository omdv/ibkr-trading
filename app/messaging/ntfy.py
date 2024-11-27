"""
Send messages via ntfy.sh
"""

import requests
from typing import List
from ib_async.contract import Contract

from models import OptionSpread
from settings import Settings


class MessageHandler:
  def __init__(self, settings: Settings):
    self.ntfy_topic = settings.ntfy_topic
    self.ntfy_enabled = settings.ntfy_enabled
    self.ntfy_url = f"https://ntfy.sh/{self.ntfy_topic}"

  def send_positions(self, positions: List[OptionSpread]) -> None:
    """Send option spreads update via ntfy.sh"""
    message_body = self._format_option_spreads(positions)
    self._send_message(message_body)

  def send_target_spread(self, contract: Contract) -> None:
    """Send target spread update via ntfy.sh"""
    message_body = self._format_option_spread(contract)
    self._send_message(message_body)

  def _send_message(self, message: str, priority: str = "default") -> None:
    """Helper method to send message via ntfy.sh"""
    if not self.ntfy_enabled:
      return

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

  def _format_option_spreads(self, positions: List[OptionSpread]) -> str:
    """Format multiple option spreads into readable message"""
    message = "Current positions:\n"
    for position in positions:
      message += self._format_option_spread(position)
    return message

  def _format_option_spread(self, spread: OptionSpread) -> str:
    """Format one option spread into readable message"""
    message = f"{str(spread)}\n"
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
