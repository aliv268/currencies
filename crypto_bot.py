import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# ---------- تنظیمات ----------
BOT_TOKEN = os.getenv("BOT_TOKEN")  # توکن از متغیر محیطی
BASE_URL = os.getenv("BASE_URL")    # آدرس API از متغیر محیطی

# ---------- فانکشن برای گرفتن تعداد رمزارزها ----------
def get_crypto_count():
    try:
        response = requests.get(BASE_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        # اگر خروجی به صورت لیست باشه
        if isinstance(data, list):
            return len(data)

        # اگر خروجی داخل data باشه
        if "data" in data and isinstance(data["data"], list):
            return len(data["data"])

        return "ساختار داده پشتیبانی نمی‌شود!"
    except requests.RequestException as e:
        return f"خطا در دریافت داده: {str(e)}"

# ---------- هندلر دستور /count ----------
async def count_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    count = get_crypto_count()
    await update.message.reply_text(f"تعداد رمزارزهای موجود: {count}")

# ---------- راه‌اندازی ربات ----------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("count", count_command))
    print("ربات با موفقیت راه‌اندازی شد ✅")
    app.run_polling()

if __name__ == "__main__":
    main()
