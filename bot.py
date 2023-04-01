import telegram
import os
import telegram.ext
import openai
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_text(prompt):
    response = openai.Completion.create(
      engine="davinci",
      prompt=prompt,
      max_tokens=1024,
      n=1,
      stop=None,
      temperature=0.7,
    )
    return response.choices[0].text.strip()

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hi, I'm a ChatGPT bot! What can I help you with?")

def reply_to_message(update, context):
    user_message = update.message.text
    prompt = f"User: {user_message}\nBot:"
    bot_response = generate_text(prompt)
    context.bot.send_message(chat_id=update.message.chat_id, text=bot_response)

def main():
    updater = telegram.ext.Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = telegram.ext.CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    reply_handler = telegram.ext.MessageHandler(telegram.ext.Filters.text, reply_to_message)
    dispatcher.add_handler(reply_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
