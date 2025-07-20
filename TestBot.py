import telebot
from telebot import types
import sqlite3


bot = telebot.TeleBot('7993533872:AAHxp_G65JsUsLSyJ05M0eiad5D0iYTH6zo')  
name = None

@bot.message_handler(commands = ['start'])

def start(message):
    connect = sqlite3.connect('sqlitebase.db')
    cur = connect.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, pass TEXT NOT NULL)')

    connect.commit()
    cur.close() 
    connect.close()

    bot.send_message(message.chat.id, 'Привет, это первичная регистрация! Введи свое имя')
    bot.register_next_step_handler(message, user_name)

def proc_name(username):
    connect = sqlite3.connect('sqlitebase.db')
    cur = connect.cursor()
    cur.execute('SELECT name FROM users')
    result = cur.fetchall()

    cur.close() 
    connect.close()

    MatchName = 0

    for name1 in result:
        if username == name1[0]:
            MatchName = 1
            break

    return MatchName

def user_name(message):
    global name

    name = message.text.strip()
    i = proc_name(name)

    if i == 1:
        bot.send_message(message.chat.id, 'Имя занято. Попробуйте еще раз')
        bot.register_next_step_handler(message, user_name)
            
    else:
        bot.send_message(message.chat.id, 'Введите пароль')
        bot.register_next_step_handler(message, user_pass)
    

def user_pass(message):
    password = message.text.strip()

    connect = sqlite3.connect('sqlitebase.db')
    cur = connect.cursor()
    cur.execute('INSERT INTO users (name, pass) VALUES (?, ?)', (name, password))

    connect.commit()
    cur.close() 
    connect.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Список пользователей', callback_data = 'users'))
    bot.send_message(message.chat.id, 'Вы зарегестрированы', reply_markup = markup)

@bot.callback_query_handler(func = lambda call: True)

def callback(call):
    connect = sqlite3.connect('sqlitebase.db')
    cur = connect.cursor()
    cur.execute('SELECT * FROM users')

    users = cur.fetchall()
    info = ''

    for element in users:
        info += f'Имя: {element[1]}, пароль: {element[2]}\n'

    cur.close() 
    connect.close()

    print(info)
    bot.send_message(call.message.chat.id, info)


bot.polling(none_stop=True)