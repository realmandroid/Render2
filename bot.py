import telegram
from telegram.ext import Updater, MessageHandler, Filters
from fpdf import FPDF

# Replace YOUR_TOKEN with your actual bot token
bot = telegram.Bot(token='YOUR_TOKEN')

def generate_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=text, ln=1)
    pdf.output("output.pdf")

def handle_message(update, context):
    message_text = update.message.text
    generate_pdf(message_text)
    context.bot.send_document(chat_id=update.effective_chat.id, document=open('output.pdf', 'rb'))

if __name__ == '__main__':
    updater = Updater(token='YOUR_TOKEN', use_context=True)
    dispatcher = updater.dispatcher
    handler = MessageHandler(Filters.text, handle_message)
    dispatcher.add_handler(handler)
    updater.start_polling()
