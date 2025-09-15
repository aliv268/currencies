import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ---------- تنظیمات ----------
BOT_TOKEN = os.getenv("BOT_TOKEN")  # توکن ربات از Railway
BASE_URL = os.getenv("BASE_URL")    # آدرس API از Railway
API_KEY = os.getenv("API_KEY")      # کلید Ompfinex از Railway

# ---------- فانکشن برای گرفتن تعداد رمزارزها ----------
def get_crypto_count():
    try:
        # اضافه کردن API Key به هدر
        headers = {
            "Authorization": f"Bearer {API_KEY}"
        }

        # ارسال درخواست به API
        response = requests.get(BASE_URL, headers=headers, timeout=10)
        response.raise_for_status()  # مدیریت خطای HTTP

        # پردازش JSON
        data = response.json()

        # حالت: اگر کل خروجی لیست باشه
        if isinstance(data, list):
            return len(data)

        # حالت: اگر خروجی داخل data باشه
        if "data" in data and isinstance(data["data"], list):
            return len(data["data"])

        return "ساختار داده پشتیبانی نمی‌شود!"
    except requests.HTTPError as http_err:
        return f"HTTP Error: {http_err}"
    except requests.RequestException as req_err:
        return f"خطا در دریافت داده: {str(req_err)}"

# ---------- هندلر دستور /count ----------
async def count_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    count = get_crypto_count()
    await update.message.reply_text(f"تعداد رمزارزهای موجود: {count}")

# ---------- راه‌اندازی ربات ----------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # دستور /count
    app.add_handler(CommandHandler("count", count_command))

    print("ربات با موفقیت راه‌اندازی شد ✅")
    app.run_polling()

if __name__ == "__main__":
    main()
