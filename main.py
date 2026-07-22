import os
import logging
import google.generativeai as genai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

PERSONALITY_PROMPT = """
تو یک شخصیت به اسم "Let Me Decide" هستی. کاربر یک سؤال یا دودلی برات می‌فرسته و تو باید به جاش تصمیم بگیری.

قوانین شخصیت تو:
- همیشه قاطع باش، هیچوقت نگو "بستگی داره" یا "خودت تصمیم بگیر".
- جواب‌هات کوتاه باشن، حداکثر ۲ تا ۳ جمله.
- کمی شوخ و طعنه‌دار باش، مثل یک دوست باحال و با اعتمادبه‌نفس.
- جواب باید همیشه با کلمه "تصمیم:" شروع بشه.
- از ایموجی مناسب در پایان جواب استفاده کن.
- به زبان فارسی محاوره‌ای و طبیعی جواب بده.

الان کاربر این سؤال رو پرسیده، تصمیم قاطع بگیر:
"""

def build_keyboard():
    keyboard = [
        [InlineKeyboardButton("🎲 تصمیم دوباره", callback_data="decide_again")],
        [InlineKeyboardButton("📤 اشتراک‌گذاری", switch_inline_query="")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! 😎 من Let Me Decide هستم.\n"
        "به جای تو تصمیم می‌گیرم، قاطع و بدون چون‌وچرا.\n"
        "فقط دودلیت رو بنویس، بقیه‌ش با من."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_question = update.message.text
    context.user_data["last_question"] = user_question
    await send_decision(update.message.reply_text, user_question)

async def send_decision(reply_func, question):
    try:
        full_prompt = PERSONALITY_PROMPT + question
        response = model.generate_content(full_prompt)
        answer = response.text.strip()
    except Exception as e:
        logger.error(f"Gemini error: {e}")
        answer = "تصمیم: الان مغزم قاطی کرد، یه‌بار دیگه بپرس. 🤖"

    await reply_func(answer, reply_markup=build_keyboard())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "decide_again":
        last_question = context.user_data.get("last_question")
        if last_question:
            await send_decision(query.message.reply_text, last_question)
        else:
            await query.message.reply_text("اول یه سؤال بپرس، بعد بگو تصمیم دوباره بگیرم. 😏")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))

    logger.info("Bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
