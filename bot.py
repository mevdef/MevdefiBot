from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # Get from @BotFather
TWITTER_URL = "https://x.com/salejames299"
CHANNEL_URL = "https://t.me/StayXRewards"
GROUP_URL = "https://t.me/Bilcoinofficialuk"

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("Join Channel", url=CHANNEL_URL)],
        [InlineKeyboardButton("Join Group", url=GROUP_URL)],
        [InlineKeyboardButton("Follow Twitter", url=TWITTER_URL)],
        [InlineKeyboardButton("I've Completed All Tasks", callback_data='verify')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        f"Hi {user.first_name}! To qualify for Mr Kay's Airdrop:\n\n"
        "1. Join our Telegram channel\n"
        "2. Join our Telegram group\n"
        "3. Follow our Twitter\n"
        "4. Click the button below after completing all tasks\n\n"
        "You'll then be asked to submit your SOL wallet address to receive your 100 SOL reward!",
        reply_markup=reply_markup
    )

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if query.data == 'verify':
        query.edit_message_text(
            "Well done! Hope you didn't cheat the system 😉\n\n"
            "Please send me your SOL wallet address now to receive your 100 SOL reward."
        )
        context.user_data['awaiting_wallet'] = True

def handle_message(update: Update, context: CallbackContext) -> None:
    if 'awaiting_wallet' in context.user_data and context.user_data['awaiting_wallet']:
        wallet_address = update.message.text.strip()
        # Basic SOL wallet validation (simple length check)
        if len(wallet_address) == 44 and wallet_address.isalnum():
            update.message.reply_text(
                "🎉 Congratulations! You've passed Mr Kay's Airdrop call!\n\n"
                "100 SOL is on its way to your address!\n\n"
                "Note: This is a testing bot, no actual SOL will be sent."
            )
            context.user_data['awaiting_wallet'] = False
        else:
            update.message.reply_text("This doesn't look like a valid SOL wallet address. It should be 44 characters long with letters and numbers only. Please try again.")

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
