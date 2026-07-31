from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters
)

from config import (
    BOT_TOKEN,
    WEBHOOK_URL,
    WEBHOOK_PATH,
    PORT
)

from handlers import start, chat, clear


def main():

    app = Application.builder()\
        .token(BOT_TOKEN)\
        .build()


    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("clear", clear)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            chat
        )
    )


    print("Bot started with webhook")


    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=WEBHOOK_PATH,
        webhook_url=f"{WEBHOOK_URL}/{WEBHOOK_PATH}"
    )


if __name__ == "__main__":
    main()