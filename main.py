from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters
)

from config import BOT_TOKEN
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


    print("Bot started")

    app.run_polling()



if __name__ == "__main__":
    main()