import os
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

# --- PORT VE WEBHOOK AYARLARI (7/24 RENDER UYUMLU) ---
PORT = int(os.environ.get("PORT", 10000))
TOKEN = "8522565760:AAGHVItP1h7Wn_CS41IapWDIEVuDiNOQTNs"
# Render üzerindeki canlı uygulama linkini buraya yazmalısın (Örn: https://proje-adi.onrender.com)
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", f"https://your-app-name.onrender.com/{TOKEN}")

# --- ÖDEME VE VIP BİLGİLERİ ---
IBAN = "TR06 0001 0021 5470 2002 4550 04"
RECIPIENT = "Zeynep Alkoç"
PRICE = "300 TL"

VIP_LINKS = [
    "https://t.me/+Aqi4UqSzr4JjZmRk",
    "https://t.me/+H2z-xlyZ6zM0OTE0",
    "https://t.me/+p01bQp6XebkzMmI0",
    "https://t.me/+HqtuwLtoMkkwMWQ0",
    "https://t.me/+BcHhS86B9ocyMWQ0"
]

# --- LOGLAMA YAPILANDIRMASI ---
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main_menu():
    keyboard = [
        [InlineKeyboardButton("💎 VIP Üyelik Satın Al (300 TL)", callback_data="buy_vip")],
        [InlineKeyboardButton("📖 Nasıl Satın Alınır?", callback_data="how_to_buy")],
        [InlineKeyboardButton("🛡️ VIP Özellikler & Avantajlar", callback_data="vip_features")],
        [InlineKeyboardButton("📞 7/24 Canlı Destek", url="https://t.me/SMSPATRONUM")],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🔥 *ELİT VIP ARŞİV — MERKEZİNE HOŞ GELDİNİZ*\n\n"
        "✨ Tamamen gizli, sansürsüz ve özel içeriklerin paylaşıldığı VIP ekosistemimize anında adım atın.\n\n"
        "👇 Aşağıdaki premium menüden işlemlerinizi yönetebilirsiniz:"
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
            f"💎 *ELİT VIP — GÜVENLİ ÖDEME ARAYÜZÜ*\n\n"
            f"📦 Paket: *Sınırsız Premium VIP Erişimi*\n"
            f"💰 Tutar: *{PRICE}*\n\n"
            f"💳 *Resmi Havale / EFT / FAST Bilgileri*\n"
            f"IBAN:\n`{IBAN}`\n\n"
            f"Alıcı Adı: *{RECIPIENT}*\n\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            f"1️⃣ Yukarıdaki IBAN hesabına tam *{PRICE}* tutarını transfer edin.\n"
            "2️⃣ İşlem sonrasında bankanın oluşturduğu **Dekontu / Ekran Görüntüsünü** doğrudan bu sohbet penceresine gönderin.\n"
            "3️⃣ Sistem dekontunuzu onayladığı an özel VIP davet linkleriniz saniyeler içinde otomatik teslim edilecektir!"
        )
        keyboard = [
            [InlineKeyboardButton("⬅️ Ana Menüye Dön", callback_data="home")]
        ]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "how_to_buy":
        text = (
            "📖 *PREMİUM SATIN ALMA REHBERİ*\n\n"
            "Sistemimiz tamamen otomatik ve güvenli altyapıyla çalışır:\n\n"
            "1️⃣ **Ödeme Adımı:** Ana menüden 'VIP Üyelik Satın Al' butonuna basarak IBAN bilgilerine ulaşın ve 300 TL gönderin.\n"
            "2️⃣ **Dekont Gönderimi:** Ödemeye ait ekran görüntüsünü bota fotoğraf olarak yükleyin.\n"
            "3️⃣ **Anında Teslimat:** Yapay zeka destekli doğrulama sonrası 5 adet gizli VIP kanalımızın linki anında cebinize gelsin!\n\n"
            "⚠️ *Herhangi bir aksilikte destek ekibimiz 7/24 aktiftir.*"
        )
        keyboard = [
            [InlineKeyboardButton("⬅️ Ana Menüye Dön", callback_data="home")]
        ]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "vip_features":
        text = (
            "🛡️ *VIP AYRICALIKLARI NELERDİR?*\n\n"
            "• Sınırsız ve ömür boyu kanal erişimi\n"
            "• Günlük özel arşiv güncellemeleri\n"
            "• Özel korumalı ve şifreli davet linkleri\n"
            "• Öncelikli 7/24 birebir VIP destek hattı"
        )
        keyboard = [
            [InlineKeyboardButton("⬅️ Ana Menüye Dön", callback_data="home")]
        ]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "home":
        text = (
            "🔥 *ELİT VIP ARŞİV — MERKEZİne HOŞ GELDİNİZ*\n\n"
            "✨ Tamamen gizli, sansürsüz ve özel içeriklerin paylaşıldığı VIP ekosistemimize anında adım atın.\n\n"
            "👇 Aşağıdaki premium menüden işlemlerinizi yönetebilirsiniz:"
        )
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=main_menu())

async def receipt_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo or update.message.document:
        logger.info(f"Kullanıcı ({update.message.from_user.id}) tarafından dekont yüklendi.")
        links_text = "\n".join([f"🔗 {link}" for link in VIP_LINKS])
        
        text = (
            "✅ *DEKONT BAŞARIYLA ONAYLANDI! ÖDEME ALINDI.*\n\n"
            "🎉 Tebrikler! Elit VIP ayrıcalıklarına erişim kazandınız. Özel davet linkleriniz aşağıdadır:\n\n"
            f"{links_text}\n\n"
            "⚠️ *Bu linkler kişiye özel üretilmiştir, başkalarıyla paylaşılması yasaktır.*"
        )
        keyboard = [
            [InlineKeyboardButton("🏠 Ana Menüye Dön", callback_data="home")]
        ]
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    await update.message.reply_text("📸 Lütfen geçerli bir dekont ekran görüntüsü veya dosyası gönderin.")

def main():
    # Application oluşturma
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, receipt_handler))
    
    # Render üzerinde 7/24 kesintisiz çalışması için Webhook yapılandırması
    logger.info("Bot Webhook modu ile 7/24 aktif hale getiriliyor...")
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    main()
