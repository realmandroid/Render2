import os
import telegram
import openai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Set up the Telegram bot and OpenAI API
bot = telegram.Bot(token=os.environ['TELEGRAM_BOT_TOKEN'])
openai.api_key = os.environ['OPENAI_API_KEY']

# Define a function to handle incoming messages
def handle_message(update, context):
    # Get the user input from the Telegram message
    user_input = update.message.text
    
    # Send the user input to ChatGPT and get a response
    response = openai.Completion.create(
        engine='davinci',
        prompt=user_input,
        max_tokens=60,
        temperature=0.5,
    )
    bot_response = response.choices[0].text.strip()
    
    # Send the response back to the user in Telegram
    bot.send_message(chat_id=update.message.chat_id, text=bot_response)

# Set up the Telegram bot's message handler
updater = Updater(use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_message))

# Start the Telegram bot
updater.start_polling()
