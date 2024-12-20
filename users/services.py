import os

import requests
import telebot


TOKEN = os.getenv('TG_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN, threaded=False)
SERVER_URL = os.getenv('SERVER_URL')


@bot.message_handler(commands=['start'])
def start_command(message):
    try:
        chat_id = message.chat.id
        command_args = message.text.split()[1:]

        if len(command_args) > 0:
            token = command_args[0]
            print(token)
            data = {
                'telegram_id': message.from_user.id,
                'username': message.from_user.username,
                'first_name': message.from_user.first_name,
                'last_name': message.from_user.last_name,
                'token': token
            }
            response = requests.post(f'{SERVER_URL}/authenticate/', json=data)
            print(response)
            if response.status_code == 200:
                bot.send_message(chat_id, "Вы успешно вошли!")
            else:
                bot.send_message(chat_id, "Произошла ошибка при входе.")
        else:
            bot.send_message(chat_id, "Неверный формат команды. Попробуйте еще раз.")

    except IndexError:
        bot.send_message(message.chat.id, "Ошибка: Токен не предоставлен.")


@bot.message_handler(func=lambda message: True)
def other_handle_message(message):
    """Обработка остальных сообщений введенных в ручную"""

    bot.send_message(message.chat.id, f'{message.from_user.first_name}! Для начала авторизуйтесь.')