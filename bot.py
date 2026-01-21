import os
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ENV dari Railway
BOT_TOKEN = os.getenv("BOT_TOKEN")
SCRIPT_URL = os.getenv("SCRIPT_URL")


# ===== COMMAND /start =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Bot Belanja Aktif\n\n"
        "Format input:\n"
        "/input tanggal/item/jml/harga_satuan/nama_toko/alamat_toko/"
        "uraian_belanja/kegiatan/cara_pembayaran/akun/admin\n\n"
        "Contoh:\n"
        "/input 2026-01-21/Pulpen/2/5000/Toko A/Bogor/"
        "ATK Rapat/Rapat Bulanan/Tunai/Operasional/Buldan"
    )


# ===== COMMAND /input =====
async def input_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.replace("/input", "").strip()
        parts = [p.strip() for p in text.split("/")]

        if len(parts) != 11:
            await update.message.reply_text(
                "❌ FORMAT SALAH\n"
                "Jumlah data harus 11 dipisahkan dengan /\n\n"
                "Contoh:\n"
                "/input 2026-01-21/Pulpen/2/5000/Toko A/Bogor/"
                "ATK Rapat/Rapat Bulanan/Tunai/Operasional/Buldan"
            )
            return

        payload = {
            "tanggal": parts[0],
            "item": parts[1],
            "jml": parts[2],
            "harga_satuan": parts[3],
            "nama_toko": parts[4],
            "alamat_toko": parts[5],
            "uraian_belanja": parts[6],
            "kegiatan": parts[7],
            "cara_pembayaran": parts[8],
            "akun": parts[9],
            "admin": parts[10],
        }

        response = requests.post(SCRIPT_URL, json=payload, timeout=10)

        if response.status_code == 200:
            await update.message.reply_text("✅ Data berhasil masuk ke Excel")
        else:
            await update.message.reply_text("❌ Gagal menyimpan ke Excel")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


# ===== MAIN =====
def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN belum diset")

    if not SCRIPT_URL:
        raise RuntimeError("SCRIPT_URL belum diset")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^/input"), input_data))

    print("🤖 Bot berjalan (polling)")
    app.run_polling()


if __name__ == "__main__":
    main()

