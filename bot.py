import os
from pyrogram import Client, filters
from pyrogram.types import Message
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

@bot.on_message(filters.private & filters.text)
async def handle_message(client, message: Message):
    user_input = message.text
    response_text = await get_ai_response(user_input)
    
    await message.reply_text(response_text)

# Run the bot
bot.run()
