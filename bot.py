import os
import sys
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# Configuration
BOT_TOKEN = os.environ.get('BOT_TOKEN', '7837000233:AAEJSMzMxsK46FlqfdXmW9F1WD_ANDuocbo')
TWITTER_URL = "https://x.com/salejames299"
CHANNEL_URL = "https://t.me/tactical_osint"
GROUP_URL = "https://t.me/iFROGYOUofiicial"
WEBHOOK_URL = "https://MevdefiBot-3.onrender.com"  # Your specific Render URL

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("✅ I Completed All Tasks", callback_data="tasks_done")
    ]]
    
    await update.message.reply_text(
        "🎉 *Welcome to Mr Kay Birdrop Test Bot!*\n\n"
        "📋 *Complete these tasks to earn 100 SOL:*\n"
        f"1. Follow [Twitter]({TWITTER_URL})\n"
        f"2. Join [Telegram Channel]({CHANNEL_URL})\n"
        f"3. Join [Telegram Group]({GROUP_URL})\n\n"
        "_Note: This is a test bot. No real SOL will be sent_",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "tasks_done":
        await query.edit_message_text(
            "🪙 *Send your Solana wallet address now!*\n\n"
            "Example: `DJ8v4jP4JZf7Q2WkUqCx3bTm9g4a1BvCxW`\n\n"
            "_We won't store your address_",
            parse_mode="Markdown"
        )
        context.user_data["awaiting_address"] = True

async def handle_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_address"):
        sol_address = update.message.text.strip()
        
        if 32 <= len(sol_address) <= 44:
            await update.message.reply_text(
                f"🎉 *Congratulations!* 🎉\n\n"
                "You passed Mr Kay Birdrop's test!\n"
                f"💸 100 SOL is on its way to:\n`{sol_address}`\n\n"
                "⚠️ Hope you didn't cheat the system!\n"
                "🚨 _Note: This is a testing bot. No real SOL will be sent_",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(
                "⚠️ *Invalid Solana address!*\n\n"
                "Please send a valid SOL address (32-44 characters)\n"
                "Example: `DJ8v4jP4JZf7Q2WkUqCx3bTm9g4a1BvCxW`",
                parse_mode="Markdown"
            )
        context.user_data["awaiting_address"] = False

def main():
    try:
        if not BOT_TOKEN or len(BOT_TOKEN) < 30:
            print("❌ Invalid Telegram bot token")
            sys.exit(1)
            
        print("🤖 Starting MevdefiBot-3...")
        app = Application.builder().token(BOT_TOKEN).build()
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(handle_button))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_address))
        
        port = int(os.environ.get('PORT', 8443))
        
        print(f"🌐 Webhook URL: {WEBHOOK_URL}")
        app.run_webhook(
            listen="0.0.0.0",
            port=port,
            webhook_url=WEBHOOK_URL,
            secret_token=os.environ.get("SECRET_TOKEN", "DEFAULT_SECRET")
        )
    except Exception as e:
        print(f"🔥 Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
