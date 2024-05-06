from ai_system import run_qa_system
from pdf_to_text import pdf2txt
from dotenv import load_dotenv
import telebot
import asyncio
import os

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

global flag
global text


@bot.message_handler(commands=['start'])
def send_start(message):
    global flag
    bot.send_message(
        message.chat.id, 'Бот готов к работе 🤖\n📎 Отправьте файл для начала 📎')
    flag = False
    global text


@bot.message_handler(commands=['stop'])
def send_end(message):
    global flag
    bot.send_message(
        message.chat.id, 'Диалог завершён️\n📎 Отправьте файл для продолжения 📎')
    flag = False


@bot.message_handler(func=lambda _: True)
def msg_control(message):
    global flag
    global text

    if ('text' not in globals()) or (not flag):    # если файл не принят
        bot.delete_message(message.chat.id, message.message_id)

    else:
        response = asyncio.run(run_qa_system(text, message.text))
        bot.send_message(message.chat.id, response)


@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        chat_id = message.chat.id
        global flag
        global text

        print('Text in work...')

        if message.document.mime_type == 'application/pdf':
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            bot.send_message(
                message.chat.id, 'Обрабатываю файл...')

            with open('input.pdf', 'wb') as file:
                file.write(downloaded_file)
            text = pdf2txt('input.pdf')

            with open('result.txt', 'w') as f:
                f.write(text)

            doc = open('result.txt', 'rb')
            bot.send_document(chat_id, doc)
            bot.send_message(
                chat_id, 'Файл успешно обработан ✅\nБот готов к диалогу 💬')
            flag = True

        elif message.document.mime_type == 'text/plain':
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            bot.send_message(
                message.chat.id, 'Обрабатываю файл...')
            text = downloaded_file.decode('utf-8')
            bot.send_message(
                chat_id, 'Файл успешно обработан ✅\nБот готов к диалогу 💬')
            flag = True

        else:
            bot.send_message(
                message.chat.id, '✖️Пожалуйста, отправьте .pdf или .txt ✖️')
            flag = False
            return

    except Exception as e:
        print(f"Caught exception: {type(e)}")
        print(f"Error message: {str(e)}")
        bot.reply_to(message, f"️⛔ ERROR ⛔️")


bot.polling()
