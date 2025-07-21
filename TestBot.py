import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('7993533872:AAHxp_G65JsUsLSyJ05M0eiad5D0iYTH6zo')  
name = None
key = 0

@bot.message_handler(commands = ['start'])

def start(message):
    connect = sqlite3.connect('sqbase.db')
    cur = connect.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, key INTEGER)')

    connect.commit()
    cur.close() 
    connect.close()

    bot.send_message(message.chat.id, 'Привет, это Бот помошник с учебой. Он будет пересылать ваши работы, а я буду их делать')
    bot.register_next_step_handler(message, register_new_member)

def register_new_member(message):
    global name

    name = message.from_user.username

    connect = sqlite3.connect('sqbase.db')
    cur = connect.cursor()
    cur.execute('INSERT INTO users (name) VALUES (?)', (name,))

    connect.commit()
    cur.close() 
    connect.close()

    markup = types.ReplyKeyboardMarkup()
    but1 = types.KeyboardButton('Купить помощь')
    markup.row(but1)
    but2 = types.KeyboardButton('Посмотреть наличие помощи')
    but3 = types.KeyboardButton('Сама помощь')
    markup.row(but3, but2)

    bot.send_message(message.chat.id, f'Вот {message.from_user.username} магазин и остальные функции.', reply_markup = markup)

def on_click(message):
    markup = types.InlineKeyboardMarkup()
    web_app_info = types.WebAppInfo(url="https://your-webapp-url.com")


bot.polling(none_stop=True)