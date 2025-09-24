import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.environ['BOT_TOKEN']

VIDEO_SETS = [
    [  # Set 1
        {"name": "📹 AMALIA LATEST", "url": "https://dupload.net/m7nqxwg1dfyo"},
        {"name": "📹 ALTER DANE LATEST", "url": "https://dupload.net/34i96yr07gqk"},
        {"name": "📹 BLAIR SEVI ROUND 2", "url": "https://dupload.net/tuovhzmn5ev8"},
        {"name": "📹 LOUISE CANETE LATEST 2025", "url": "https://dupload.net/xhq8fy6y5zjm"},
        {"name": "📹 ENIGMATIC LATEST SERIES", "url": "https://dupload.net/n6y4haxo482j"}
    ],
    [  # Set 2
        {"name": "🎬 ALTER DANE BEST SET", "url": "https://dl.surf/f/56c4ca63"},
        {"name": "🎬 LOUISE CANETE FULSET", "url": "https://dl.surf/f/84c7d5e0"},
        {"name": "🎬 AMALIA 2025 LATEST UNRELEASED", "url": "https://dl.surf/f/2e1a03cd"},
        {"name": "🎬 SHEENY BERRY ROUND 6", "url": "https://dl.surf/f/fb23a00d"},
        {"name": "🎬 BEST PINAY SET VIDEOS", "url": "https://dl.surf/f/8a18d410"}
    ]
]

async def show_set(update: Update, context: ContextTypes.DEFAULT_TYPE, set_index: int):
    videos = VIDEO_SETS[set_index]
    
    keyboard = []
    for i in range(0, len(videos), 2):
        row = []
        if i < len(videos):
            row.append(InlineKeyboardButton(videos[i]["name"], url=videos[i]["url"]))
        if i + 1 < len(videos):
            row.append(InlineKeyboardButton(videos[i+1]["name"], url=videos[i+1]["url"]))
        keyboard.append(row)
    
    nav_buttons = []
    if set_index > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"page_{set_index-1}"))
    
    if set_index < len(VIDEO_SETS) - 1:
        nav_buttons.append(InlineKeyboardButton("More Videos ➡️", callback_data=f"page_{set_index+1}"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = f"🎬 **Videos Available**\n\nSet {set_index + 1} of {len(VIDEO_SETS)}"
    
    if hasattr(update, 'callback_query'):
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_set(update, context, 0)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("page_"):
        set_index = int(query.data.split("_")[1])
        await show_set(update, context, set_index)

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))
    print("🚀 Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()