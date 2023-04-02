import os
import openai
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# Get API key and bot token from environment variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Set up OpenAI API credentials
openai.api_key = OPENAI_API_KEY

# Define conversation states
START, TYPING_REPLY = range(2)

# Define conversation flow
def start(update, context):
    context.user_data["conversation_state"] = START
    update.message.reply_text("Hi! I'm ChatGPT. What's your name?")
    return TYPING_REPLY

def reply(update, context):
    # Send user's message to OpenAI API
    prompt = f"Conversation with {update.message.from_user.first_name}:\n{update.message.text}"
    response = "I'm sorry, I don't understand. Can you please rephrase your question?"

    # Generate response using OpenAI API
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        ).choices[0].text.strip()
    except:
        pass

    # Send response to user
    update.message.reply_text(response)

    # Wait for next message
    return TYPING_REPLY

def cancel(update, context):
    update.message.reply_text("Bye! Have a good day.")
    return ConversationHandler.END

def main():
    # Set up Telegram bot
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Define conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            TYPING_REPLY: [MessageHandler(Filters.text & ~Filters.command, reply)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add conversation handler to dispatcher
    dispatcher.add_handler(conv_handler)

    # Start bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
