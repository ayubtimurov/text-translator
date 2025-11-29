from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler, ConversationHandler
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


# COMMANDS

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_text = "Starting Text Translator Bot in Telegram"
    await update.message.reply_text(start_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    *Help Command:*
/start - Start the bot
/about - About the bot
/set_input_language - Select input language
/set_output_language - Select output language
/ui_language - Select interface language
"""
    await update.message.reply_text(help_text)


# /ui_language

async def set_ui_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
    [
        InlineKeyboardButton("🇺🇸 English", callback_data="lang_eng"),
        InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_rus")
    ],
    [
        InlineKeyboardButton("🇹🇯 Тоҷикӣ", callback_data="lang_taj"),
        InlineKeyboardButton("🇹🇷 Türkçe ", callback_data="lang_turk")
    ],
    [
        InlineKeyboardButton("❌ Cancel", callback_data="lang_cancel")
    ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Please choose the interface language:",
        reply_markup=reply_markup
    )

async def ui_language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "lang_eng":
        await query.edit_message_text("You selected: English 🇺🇸")
    elif query.data == "lang_rus":
        await query.edit_message_text("Вы выбрали русский язык")
    elif query.data == "lang_taj":
        await query.edit_message_text("Шумо тоҷикиро интихоб кардед")
    elif query.data == "lang_turk":
        await query.edit_message_text("Türkçe'yi seçtiniz")
    elif query.data == "lang_cancel":
        await query.edit_message_text("You canceled interface language selection ❌")


# /input_language

SELECTING_LANGUAGE = 1

LANGUAGES = {
    "tj": "🇹🇯 Тоҷикӣ (Tajik)",
    "uz": "🇺🇿 Uzbekcha (Uzbek)",
    "en": "🇺🇸 English",
    "zh": "🇨🇳 中文 (Chinese)",
    "ar": "🇸🇦 العربية (Arabic)",
    "az": "🇦🇿 Azərbaycanca (Azerbaijani)",
    "by": "🇧🇾 Беларуская (Belarusian)",
    "bn": "🇮🇳 বাংলা (Bengali)",
    "bg": "🇧🇬 Български (Bulgarian)",
    "es": "🇪🇸 Español (Spanish)",
    "fr": "🇫🇷 Français (French)",
    "de": "🇩🇪 Deutsch (German)",
    "hi": "🇮🇳 हिन्दी (Hindi)",
    "it": "🇮🇹 Italiano (Italian)",
    "ja": "🇯🇵 日本語 (Japanese)",
    "ko": "🇰🇷 한국어 (Korean)",
    "pt": "🇵🇹 Português (Portuguese)",
    "ru": "🇷🇺 Русский (Russian)",
    "tr": "🇹🇷 Türkçe (Turkish)",
    "uk": "🇺🇦 Українська (Ukrainian)",
    "ur": "🇵🇰 اردو (Urdu)"
}

async def set_input_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔍 Type language name to search:\n"
        "Examples: english, spanish, русский\n\n"
        "Or send /cancel to cancel"
    )
    return SELECTING_LANGUAGE

async def search_input_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query_text = update.message.text.lower()

    matches = []
    for code, name in LANGUAGES.items():
        if query_text in name.lower():
            matches.append((code, name))

    if not matches:
        await update.message.reply_text(
            f"❌ No languages found for '{query_text}'\n"
            "Try again or send /cancel"
        )
        return SELECTING_LANGUAGE
    
    keyboard = []
    for code, name in matches[:10]:
        keyboard.append([
            InlineKeyboardButton(name, callback_data=f"lang_{code}")
        ])

    keyboard.append([
        InlineKeyboardButton("❌ Cancel", callback_data="lang_cancel")
    ])

    await update.message.reply_text(
        f"Found {len(matches)} language(s):",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return SELECTING_LANGUAGE

async def input_language_selected(update: Update, context: ContextTypes):
    query = update.callback_query
    await query.answer()

    if query.data == "lang_cancel":
        await query.edit_message_text("❌ Input language selection cancelled")
        return ConversationHandler.END
    
    lang_code = query.data.replace("lang_", "")
    lang_name = LANGUAGES.get(lang_code, lang_code)

    await query.edit_message_text(
        f"✅ Input language selected: {lang_name}"
    )

    return ConversationHandler.END

async def input_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Cancelled")
    return ConversationHandler.END

# output_languege

async def set_output_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("set output language command recieved")
    await update.message.reply_text(
        "🔍 Type language name to search:\n"
        "Examples: english, spanish, русский\n\n"
        "Or send /cancel to cancel"
    )
    return SELECTING_LANGUAGE

async def search_output_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("searching languages")
    query_text = update.message.text.lower()

    matches = []
    for code, name in LANGUAGES.items():
        if query_text in name.lower():
            matches.append((code, name))

    if not matches:
        await update.message.reply_text(
            f"❌ No languages found for '{query_text}'\n"
            "Try again or send /cancel"
        )
        return SELECTING_LANGUAGE
    
    keyboard = []
    for code, name in matches[:10]:
        keyboard.append([
            InlineKeyboardButton(name, callback_data=f"lang_{code}")
        ])

    keyboard.append([
        InlineKeyboardButton("❌ Cancel", callback_data="lang_cancel")
    ])

    await update.message.reply_text(
        f"Found {len(matches)} language(s):",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return SELECTING_LANGUAGE

async def output_language_selected(update: Update, context: ContextTypes):
    print("output language selected")
    query = update.callback_query
    await query.answer()

    if query.data == "lang_cancel":
        await query.edit_message_text("❌ Output language selection cancelled")
        return ConversationHandler.END
    
    lang_code = query.data.replace("lang_", "")
    lang_name = LANGUAGES.get(lang_code, lang_code)

    await query.edit_message_text(
        f"✅ Output language selected: {lang_name}"
    )

    return ConversationHandler.END

async def output_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("output language canceled")
    await update.message.reply_text("❌ Cancelled")
    return ConversationHandler.END


def main():
    print("Starting...")
    app = Application.builder().token(TOKEN).build()

    #   /set_input_language
    input_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("set_input_language", set_input_language)],
        states={
            SELECTING_LANGUAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, search_input_language),
                CallbackQueryHandler(input_language_selected, pattern=r"^lang_")
            ]
        },
        fallbacks=[CommandHandler("cancel", input_cancel)]
    )
    app.add_handler(input_conv_handler)

    #      /set_output_language
    output_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("set_output_language", set_output_language)],
        states={
            SELECTING_LANGUAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, search_output_language),
                CallbackQueryHandler(output_language_selected, pattern=r"^lang_")
            ]
        },
        fallbacks=[CommandHandler("cancel", output_cancel)]
    )
    app.add_handler(output_conv_handler)

    app.add_handler(CommandHandler("ui_language", set_ui_language))
    app.add_handler(CallbackQueryHandler(ui_language_callback, pattern=r"^lang_(eng|rus|taj|turk)$"))
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))

    print("Polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
