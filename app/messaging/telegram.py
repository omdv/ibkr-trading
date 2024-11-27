import os
import logging

from telegram import Update
from telegram.ext import (
  Application,
  CommandHandler,
  MessageHandler,
  filters,
  ContextTypes,
)

# Configure logging
logging.basicConfig(
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class TelegramHandler:
  def __init__(self):
    self.token = os.getenv("TELEGRAM_BOT_TOKEN")
    allowed_users = os.getenv("TELEGRAM_ALLOWED_USER_IDS", "")
    self.allowed_user_ids = [int(uid.strip()) for uid in allowed_users.split(",")]
    self.application = Application.builder().token(self.token).build()
    self._setup_handlers()

  def _setup_handlers(self):
    """
    Set up command and message handlers
    """
    # Command handlers
    self.application.add_handler(CommandHandler("start", self.start_command))
    self.application.add_handler(CommandHandler("help", self.help_command))
    self.application.add_handler(CommandHandler("pos", self.positions_command))

    # Message handler
    self.application.add_handler(
      MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
    )

  async def _check_user_permission(self, update: Update) -> bool:
    """
    Check if user is allowed to use the bot
    """
    user_id = update.effective_user.id
    is_allowed = user_id in self.allowed_user_ids

    if not is_allowed:
      logger.warning(f"Unauthorized access attempt from user ID: {user_id}")
      await update.message.reply_text("Sorry, you are not authorized to use this bot.")
    else:
      logger.info(f"User ID {user_id} is authorized to use the bot")
    return is_allowed

  async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /start command
    """
    if not await self._check_user_permission(update):
      return
    await update.message.reply_text("Use /help to see available commands.")

  async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /help command
    """
    if not await self._check_user_permission(update):
      return
    await update.message.reply_text("/start, /help")

  async def positions_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /pos command
    """
    if not await self._check_user_permission(update):
      return
    await update.message.reply_text("Positions command")

  async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle incoming messages
    """
    if not await self._check_user_permission(update):
      return

    message_text = update.message.text
    logger.info(f"Received message: {message_text}")
    await update.message.reply_text(f"Received message: {message_text}")

  def run(self):
    """
    Start the bot
    """
    logger.info("Starting bot...")
    # Changed from start() to run_polling()
    self.application.run_polling(allowed_updates=Update.ALL_TYPES)

  def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle errors
    """
    logger.error(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
  telegram_handler = TelegramHandler()
  telegram_handler.run()
