from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_IDS
from ai_api import ask_ai
import memory


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in ADMIN_IDS:
        await update.message.reply_text(
            "دسترسی ندارید."
        )
        return

    await update.message.reply_text(
        "سلام رامین 👋\n"
        "من آماده‌ام. هر چیزی می‌خواهی بپرس."
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in ADMIN_IDS:
        return

    text = update.message.text

    memory.add_message(
        user_id,
        "user",
        text
    )

    try:

        answer = ask_ai(
            memory.get_history(user_id)
        )

        memory.add_message(
            user_id,
            "assistant",
            answer
        )

        await update.message.reply_text(
            answer
        )

    except Exception as e:

        await update.message.reply_text(
            f"خطا:\n{e}"
        )


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in ADMIN_IDS:
        return

    memory.clear_history(
        user_id
    )

    await update.message.reply_text(
        "حافظه چت پاک شد."
    )