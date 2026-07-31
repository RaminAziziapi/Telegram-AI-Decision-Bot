from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_ID
from claude_api import ask_claude
import memory


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(
            "دسترسی ندارید."
        )
        return

    await update.message.reply_text(
        "سلام رامین 👋\nمن آماده‌ام. هر چیزی می‌خواهی بپرس."
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id != ADMIN_ID:
        return

    text = update.message.text

    memory.add_message(
        user_id,
        "user",
        text
    )

    try:

        answer = ask_claude(
            memory.get_history(user_id)
        )

        memory.add_message(
            user_id,
            "assistant",
            answer
        )

        await update.message.reply_text(answer)

    except Exception as e:

        await update.message.reply_text(
            f"خطا:\n{e}"
        )


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):

    memory.clear_history(
        update.effective_user.id
    )

    await update.message.reply_text(
        "حافظه چت پاک شد."
    )