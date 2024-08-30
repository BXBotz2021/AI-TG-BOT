import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import openai
from config import Config

# Initialize OpenAI API
openai.api_key = Config.OPENAI_API_KEY

# Initialize Pyrogram Client
bot = Client(
    "AI_Telegram_Bot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)

# Function to get a response from OpenAI's GPT model
async def get_ai_response(prompt: str) -> str:
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# /start command handler
@bot.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    start_text = """👋 Hello {},

I am your AI assistant. Just send me a message, and I will reply using AI!

Click the buttons below for more information or help.
""".format(message.from_user.first_name)

    # Inline keyboard with buttons
    start_buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📚 Help", callback_data="help"),
             InlineKeyboardButton("🌐 About", callback_data="about")],
            [InlineKeyboardButton("👨‍💻 My Developer", url="https://t.me/MUFAZTG_NEW")]  # Replace YourUsername with your actual Telegram username
        ]
    )

    await message.reply_text(
        text=start_text,
        reply_markup=start_buttons
    )

# Callback query handler for inline buttons
@bot.on_callback_query()
async def handle_callback_query(client, callback_query):
    if callback_query.data == "help":
        help_text = "You can use this bot to interact with AI. Just type your question or message, and I will respond."
        await callback_query.message.edit_text(help_text)
    
    elif callback_query.data == "about":
        about_text = "This bot is powered by OpenAI's GPT-3 and built using Pyrogram."
        await callback_query.message.edit_text(about_text)

# Handle incoming text messages
@bot.on_message(filters.private & filters.text)
async def handle_message(client, message: Message):
    user_input = message.text
    response_text = await get_ai_response(user_input)
    
    await message.reply_text(response_text)

# Run the bot
bot.run()
