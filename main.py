import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from elevenlabs.client import ElevenLabs

# ================== CONFIG ==================
BOT_TOKEN = os.getenv("8755030358:AAG1wpWu-2ccAVN9dL_PHf59kMAjw8ou7vo")
ELEVEN_API_KEY = os.getenv("dd60bd6e80117889c301aa7f5aa9094ec0ee9b56fa0e625b38a3bc87f1cfcb93")

FEMALE_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"
MALE_VOICE_ID = "pNInz6obpgDQGcFmaJgB"
# ============================================

logging.basicConfig(level=logging.INFO)

client = ElevenLabs(api_key=ELEVEN_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to my Text to Speech Bot\n\nSend Your Text (Hindi or English)"
    )

async def tts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    try:
        # Female Voice
        audio_female = client.text_to_speech.convert(
            voice_id=FEMALE_VOICE_ID,
            model_id="eleven_multilingual_v2",
            text=text
        )

        with open("female.mp3", "wb") as f:
            for chunk in audio_female:
                f.write(chunk)

        await update.message.reply_voice(voice=open("female.mp3", "rb"))

        # Male Voice
        audio_male = client.text_to_speech.convert(
            voice_id=MALE_VOICE_ID,
            model_id="eleven_multilingual_v2",
            text=text
        )

        with open("male.mp3", "wb") as f:
            for chunk in audio_male:
                f.write(chunk)

        await update.message.reply_voice(voice=open("male.mp3", "rb"))

        os.remove("female.mp3")
        os.remove("male.mp3")

    except Exception as e:
        print(e)
        await update.message.reply_text("❌ Error generating voice")

def main():
    if not BOT_TOKEN:
        print("BOT_TOKEN missing!")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tts))

    print("Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
