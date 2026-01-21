import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("8034370178:AAG8v-USbfjdlWwmKmlPxWPWdRAaRle3Y1w")
SCRIPT_URL = os.getenv("https://script.google.com/macros/s/AKfycbwYV8iRFOiEGtvN2otPvfDn7LrQHp3jeeF5u2twODyFVkV1Yfi-NuuM7JePR_Qy2II6/exec")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "FORMAT INPUT:\n"
        "/input tanggal/item/jml/harga/nama toko/alamat/uraian/kegiatan/pembayaran/akun/admin"
    )

async def input_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.replace("/input", "").strip()
        parts = [p.strip() for p in text.split("/")]

        if len(parts) != 11:
            await update.message.reply_text("FORMAT SALAH")
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
            "admin": parts[10]
        }

        r = requests.post(SCRIPT_URL, json=payload)

        if r.status_code == 200:
            await update.message.reply_text("DATA MASUK EXCEL")
        else:
            await update.message.reply_text("GAGAL SIMPAN")

    except Exception as e:
        await update.message.reply_text(str(e))

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^/input"), input_data))
    print("BOT AKTIF 24 JAM")
    app.run_polling()

if __name__ == "__main__":
    main()
