from telegram.ext import Application, CommandHandler
from app.core import config
from app.bot import handlers

def main():
    print("Starting Telegram Bot Worker...")
    if not config.TELEGRAM_TOKEN or not config.ADMIN_ID:
        print("Error: TELEGRAM_TOKEN and ADMIN_ID environment variables must be set.")
        return

    application = Application.builder().token(config.TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", handlers.start_command))
    application.add_handler(CommandHandler("key", handlers.key_info_command))
    application.add_handler(CommandHandler("add", handlers.add_key_command))
    application.add_handler(CommandHandler("setexpire", handlers.set_expire_command))
    application.add_handler(CommandHandler("remove", handlers.remove_key_command))
    application.add_handler(CommandHandler("reset", handlers.reset_key_command))
    application.add_handler(CommandHandler("list", handlers.list_keys_command))

    application.run_polling()

if __name__ == '__main__':
    main()