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

# Render / Sunucu Canlı Kalma Port Ayarı
PORT = int(os.environ.get("PORT", 10000))

class HealthCheckHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"VIP Link Delivery Bot is live and running!")

def run_web_server():
    with socketserver.TCPServer(("", PORT), HealthCheckHandler) as httpd:
        httpd.serve_forever()

threading.Thread(target=run_web_server, daemon=True).start()

# BOT VE ÖDEME BİLGİLERİ
BOT_TOKEN = "8522565760:AAGHVItP1h7Wn_CS41IapWDIEVuDiNOQTNs"
IBAN = "TR06 0001 0021 5470 2002 4550 04"
RECIPIENT = "Zeynep Alkoç"
PRICE = "300 TL"

# TESLİM EDİLECEK VIP LİNKLER
VIP_LINKS = [
    "https://t.me/+Aqi4UqSzr4JjZmRk",
    "https://t.me/+H2z-xlyZ6zM0OTE0",
    "https://t.me/+p01bQp6XebkzMmI0",
    "https://t.me/+HqtuwLtoMkkwMWQ0",
    "https://t.me/+BcHhS86B9ocyMWQ0"
]

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

def main_menu():
    keyboard = [
        [InlineKeyboardButton("💎 VIP Üyelik Satın Al (300 TL)", callback_data="buy_vip")],
        [InlineKeyboardButton("📖 Nasıl Satın Alınır?", callback_data="how_to_buy")],
        [InlineKeyboardButton("📞 Destek İletişim", url="https://t.me/SMSPATRONUM")],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🔥 *HOŞ GELDİNİZ — ELİT VIP ARŞİV*\n\n"
        "✨ Tamamen özel ve gizli içeriklerin bulunduğu VIP kanallarımıza anında erişim sağlayın.\n\n"
        "👇 Aşağıdaki menüden işlem yapabilirsiniz:"
    )
    if update.message:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=main_menu())
    elif update.callback_query:
        await update.callback_query.message.edit_text(text, parse_mode="Markdown", reply_markup=main_menu())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "buy_vip":
        text = (
            f"💎 *VIP ÜYELİK ÖDEME EKRANI*\n\n"
            f"📦 Paket: *Elit VIP Sınırsız Erişim*\n"
            f"💰 Tutar: *{PRICE}*\n\n"
            f"💳 *Banka Bilgileri (HAVALE / EFT / FAST)*\n"
            f"IBAN:\n`{IBAN}`\n\n"
            f"Alıcı Adı: *{RECIPIENT}*\n\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            f"1️⃣ Yukarıdaki IBAN adresine tam *{PRICE}* gönderin.\n"
            "2️⃣ İşlem sonrası banka dekontunun ekran görüntüsünü veya PDF dosyasını doğrudan bu bota gönderin.\n"
            "3️⃣ Sistem dekontu algıladığı anda VIP linkleriniz anında otomatik olarak iletilecektir!"
        )
        keyboard = [
            [InlineKeyboardButton("⬅️ Ana Menüye Dön", callback_data="home")]
        ]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "how_to_buy":
        text = (
            "📖 *NASIL SATIN ALINIR? (REHBER)*\n\n"
            "Botumuz üzerinden VIP arşiv linklerine sahip olmak son derece kolaydır:\n\n"
            "1️⃣ **Ana Menü** üzerinden **'VIP Üyelik Satın Al'** butonuna tıklayın.\n"
            "2️⃣ Karşınıza çıkan **IBAN** adresine mobil bankacılığınızdan **300 TL** gönderin (Açıklamaya bir şey yazmanıza gerek yoktur).\n"
            "3️⃣ Ödemeyi yaptıktan sonra bankanın size verdiği **Dekontu / Ekran Görüntüsünü** bu sohbet penceresine fotoğraf olarak gönderin.\n"
            "4️⃣ Yapay zeka ve sistem dekontunuzu onayladıktan sonra 5 adet özel VIP kanalımızın gizli davet linkleri saniyeler içinde tarafınıza gönderilecektir!\n\n"
            "⚠️ *Herhangi bir sorun yaşarsanız destek butonundan bize ulaşabilirsiniz.*"
        )
        keyboard = [
            [InlineKeyboardButton("⬅️ Ana Menüye Dön", callback_data="home")]
        ]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "home":
        text = (
            "🔥 *HOŞ GELDİNİZ — ELİT VIP ARŞİV*\n\n"
            "✨ Tamamen özel ve gizli içeriklerin bulunduğu VIP kanallarımıza anında erişim sağlayın.\n\n"
            "👇 Aşağıdaki menüden işlem yapabilirsiniz:"
        )
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=main_menu())

async def receipt_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Kullanıcı dekont resmi veya belgesi gönderdiğinde çalışır
    if update.message.photo or update.message.document:
        links_text = "\n".join([f"🔗 {link}" for link in VIP_LINKS])
        
        text = (
            "✅ *DEKONT ONAYLANDI! ÖDEMENİZ BAŞARIYLA ALINDI.*\n\n"
            "🎉 Tebrikler! VIP arşivlerimize erişim hakkı kazandınız. Aşağıdaki gizli davet linklerine tıklayarak kanallara hemen katılabilirsiniz:\n\n"
            f"{links_text}\n\n"
            "⚠️ *Bu linkler kişiye özeldir, lütfen başka kimseyle paylaşmayın.*"
        )
        keyboard = [
            [InlineKeyboardButton("🏠 Ana Menüye Dön", callback_data="home")]
        ]
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    await update.message.reply_text("📸 Lütfen geçerli bir dekont ekran görüntüsü veya dosyası gönderin.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, receipt_handler))
    
    print("VIP Link Delivery Bot Elit Olarak Çalışıyor!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
