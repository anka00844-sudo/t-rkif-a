```python
import os
import threading
import http.server
import socketserver
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================================================
# RENDER WEB SERVER
# =========================================================

PORT = int(os.environ.get("PORT", 10000))


class HealthCheckHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"ANKA VIP Bot is live and running!")

    def log_message(self, format, *args):
        pass


def run_web_server():
    try:
        with socketserver.TCPServer(("", PORT), HealthCheckHandler) as httpd:
            print(f"Web server running on port {PORT}")
            httpd.serve_forever()
    except Exception as e:
        print(f"Web server error: {e}")


threading.Thread(
    target=run_web_server,
    daemon=True
).start()


# =========================================================
# AYARLAR
# =========================================================

# Render'da Environment Variable olarak BOT_TOKEN ekle.
BOT_TOKEN = os.environ.get("8522565760:AAGsZTXZXpD8p1qSwvsObgrLmr95qlKOfoU", "")

PRICE = 300

IBAN = "TR06 0001 0021 5470 2002 4550 04"
RECIPIENT = "Zeynep Alkoç"

# Telegram linklerini BURAYA doğrudan https:// şeklinde koy.
LINKS = [
    "https://t.me/+Aqi4UqSzr4JjZmRk",
    "https://t.me/+H2z-xlyZ6zM0OTE0",
    "https://t.me/+p01bQp6XebkzMmI0",
    "https://t.me/+HqtuwLtoMkkwMWQ0",
    "https://t.me/+BcHhS86B9ocyMWQ0",
]

SUPPORT_USERNAME = "ANKA"


# =========================================================
# LOG
# =========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# =========================================================
# ANA MENÜ
# =========================================================

def main_menu():
    keyboard = [
        [
            InlineKeyboardButton(
                "🛒 VIP Paket Satın Al — 300 TL",
                callback_data="buy"
            )
        ],
        [
            InlineKeyboardButton(
                "📖 Nasıl Satın Alacağım?",
                callback_data="how"
            )
        ],
        [
            InlineKeyboardButton(
                "📦 Ürün Bilgileri",
                callback_data="info"
            )
        ],
        [
            InlineKeyboardButton(
                "📞 Destek",
                callback_data="support"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# START
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "💎 *ANKA VIP*\n\n"
        "🔐 Özel VIP erişim paketi\n"
        "⚡ Hızlı dijital teslimat\n"
        "💰 Paket fiyatı: *300 TL*\n\n"
        "Aşağıdaki menüden işlem yapmak istediğiniz seçeneği seçebilirsiniz."
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=main_menu()
    )


# =========================================================
# BUTONLAR
# =========================================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    # -----------------------------------------------------
    # SATIN AL
    # -----------------------------------------------------

    if query.data == "buy":

        text = (
            "🛒 *VIP PAKET SATIN AL*\n\n"
            f"💰 Fiyat: *{PRICE} TL*\n\n"
            "💳 *ÖDEME BİLGİLERİ*\n\n"
            f"IBAN:\n`{IBAN}`\n\n"
            f"Alıcı: *{RECIPIENT}*\n\n"
            "━━━━━━━━━━━━━━━━\n\n"
            f"1️⃣ Yukarıdaki hesaba *{PRICE} TL* gönderin.\n"
            "2️⃣ Ödeme yaptıktan sonra banka dekontunuzu bu bota gönderin.\n"
            "3️⃣ Dekont kontrol edildikten sonra VIP erişiminiz gönderilecektir."
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "📸 DEKONT GÖNDERECEĞİM",
                    callback_data="receipt"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Ana Menü",
                    callback_data="home"
                )
            ],
        ]

        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # -----------------------------------------------------
    # NASIL SATIN ALACAĞIM
    # -----------------------------------------------------

    elif query.data == "how":

        text = (
            "📖 *NASIL SATIN ALACAKSINIZ?*\n\n"
            "1️⃣ *VIP Paket Satın Al* butonuna basın.\n"
            f"2️⃣ Size gösterilen IBAN'a *{PRICE} TL* gönderin.\n"
            "3️⃣ Ödeme yaptıktan sonra dekontunuzu bota gönderin.\n"
            "4️⃣ Ödeme kontrolünden sonra VIP erişim bilgileriniz gönderilir. 🔐"
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "🛒 HEMEN SATIN AL",
                    callback_data="buy"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Ana Menü",
                    callback_data="home"
                )
            ],
        ]

        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # -----------------------------------------------------
    # ÜRÜN BİLGİLERİ
    # -----------------------------------------------------

    elif query.data == "info":

        text = (
            "📦 *VIP ÜRÜN BİLGİLERİ*\n\n"
            "💎 VIP Paket\n"
            "🔗 5 adet VIP erişim\n"
            f"💰 Fiyat: *{PRICE} TL*\n"
            "⚡ Dijital teslimat\n"
            "🔐 Ödeme kontrolü sonrası erişim"
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "🛒 SATIN AL",
                    callback_data="buy"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Ana Menü",
                    callback_data="home"
                )
            ],
        ]

        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
```
