# python main.py
import time
import telebot
import random
import requests
import atexit
from notifiers import get_notifier
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from telebot import types, apihelper
import sqlite3
import config

bot = telebot.TeleBot(config.TOKEN)
driver = webdriver.Edge()
telegram = get_notifier('telegram')


def bot_online():
    try:
        connect = sqlite3.connect('bot.db')
        cursor = connect.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS chats (
            id INTEGER
        )""")
        connect.commit()
        all_results = []
        cursor.execute("SELECT id FROM chats")
        for i in cursor.execute("SELECT id FROM chats"):
            all_results += i
        connect.commit()
        for i in range(0, len(all_results)):
            telegram.notify(token=config.TOKEN, chat_id=all_results[i], message="Доброе утро😇")
    except Exception as e:
        print(repr(e))
        telegram.notify(token=config.TOKEN, chat_id=config.admin_id, message=repr(e))


bot_online()


def first():  # первая страница выбора функций
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Моя длина 🍆')
    item2 = types.KeyboardButton('Как дела?😊')
    item3 = types.KeyboardButton('Информация о...😏')
    item4 = types.KeyboardButton('Добавить инфу 📂')
    item5 = types.KeyboardButton('Посоветуй фильм 🎥')
    item6 = types.KeyboardButton('Дальше ➡')
    markup.add(item1, item2, item3, item4, item5, item6)
    return markup


def db_chats(message):
    try:
        connect = sqlite3.connect('bot.db')
        cursor = connect.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS chats (
            id INTEGER
        )""")
        connect.commit()
        chat_id = message.chat.id
        cursor.execute(f"SELECT id FROM chats WHERE id = '{chat_id}'")
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO chats VALUES(?)", [chat_id])
        connect.commit()
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS '{chat_id}' (
            id INTEGER,
            username TEXT
        )""")
        user_id = message.from_user.id
        user_username = '@' + message.from_user.username
        cursor.execute(f"SELECT id FROM '{chat_id}' WHERE id = '{user_id}'")
        if cursor.fetchone() is None:
            cursor.execute(f"INSERT INTO '{chat_id}' VALUES(?, ?)", (user_id, user_username))
        else:
            cursor.execute(f"UPDATE '{chat_id}' SET username = '{user_username}' WHERE id = '{user_id}'")
        connect.commit()
    except Exception as e:
        print(repr(e))
        telegram.notify(token=config.TOKEN, chat_id=config.admin_id, message=repr(e))


def db_profile(message):
    try:
        connect = sqlite3.connect('bot.db')
        cursor = connect.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER,
            username TEXT,
            About TEXT,
            Steam TEXT,
            Discord TEXT,
            VK TEXT,
            YouTube TEXT,
            Twitch TEXT,
            Twitter TEXT,
            Pinterest TEXT,
            Tg_channel TEXT,
            Epic_Games TEXT,
            Site TEXT,
            Tic_Tok TEXT
        )""")
        connect.commit()
        user_id = message.from_user.id
        user_username = '@' + message.from_user.username
        cursor.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
        if cursor.fetchone() is None:
            cursor.execute(f"INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (user_id, user_username, 'не указано', 'не указано', 'не указано', 'не указано', 'не указано\
', 'не указано', 'не указано', 'не указано', 'не указано', 'не указано', 'не указано', 'не указано'))
        else:
            cursor.execute(f"UPDATE users SET username = '{user_username}' WHERE id = '{user_id}'")
        connect.commit()
    except Exception as e:
        print(repr(e))
        telegram.notify(token=config.TOKEN, chat_id=config.admin_id, message=repr(e))


def info_profile(message):
    try:
        db_chats(message)
        db_profile(message)
    except Exception as e:
        print(repr(e))
        telegram.notify(token=config.TOKEN, chat_id=config.admin_id, message=repr(e))
    try:
        connect = sqlite3.connect('bot.db')
        cursor = connect.cursor()
        last_name = lambda x: x if str(x) != 'None' else ''
        if '@' in message.text:
            user_username = message.text
            cursor.execute(f"SELECT * FROM users WHERE username = '{user_username}'")
            connect.commit()
            if cursor.fetchone() is None:
                bot.send_message(message.chat.id, 'Такого пользователя нет в базе ФСБ')
                connect.commit()
            else:
                all_results = []
                for i in cursor.execute(f"SELECT * FROM users WHERE username = '{user_username}'"):
                    all_results += i
                connect.commit()
                bot.send_message(message.chat.id, f"Профиль пользователя {all_results[1]} 👮\
\n \
\n<b>О себе:</b> {all_results[2]}\
\n \
\n<b>Steam:</b> {all_results[3]}\
\n \
\n<b>Discord:</b> {all_results[4]}\
\n \
\n<b>VK:</b> {all_results[5]}\
\n \
\n<b>Ютуб:</b> {all_results[6]}\
\n \
\n<b>Twitch:</b> {all_results[7]}\
\n \
\n<b>ТикТок:</b> {all_results[13]}\
\n \
\n<b>Twitter:</b> {all_results[8]}", disable_web_page_preview=1, parse_mode='html')

        elif message.text.lower() == 'я':
            user_username = '@' + message.from_user.username
            cursor.execute(f"SELECT * FROM users WHERE username = '{user_username}'")
            connect.commit()
            if cursor.fetchone() is None:
                bot.send_message(message.chat.id, 'Тебя даже в базе нет. Но это поправимо...')
                db_profile(message)
            else:
                all_results = []
                for i in cursor.execute(f"SELECT * FROM users WHERE username = '{user_username}'"):
                    all_results += i
                connect.commit()
                bot.send_message(message.chat.id, f"Твой профиль, <b>{message.from_user.first_name} \
{last_name(message.from_user.last_name)}</b> 👮\
\n \
\n<b>О себе:</b> {all_results[2]}\
\n \
\n<b>Steam:</b> {all_results[3]}\
\n \
\n<b>Discord:</b> {all_results[4]}\
\n \
\n<b>VK:</b> {all_results[5]}\
\n \
\n<b>Ютуб:</b> {all_results[6]}\
\n \
\n<b>Twitch:</b> {all_results[7]}\
\n \
\n<b>ТикТок:</b> {all_results[13]}\
\n \
\n<b>Twitter:</b> {all_results[8]}", disable_web_page_preview=1, parse_mode='html')

        else:
            bot.send_message(message.chat.id, 'Нормально введи что сказано, додик')
    except Exception as e:
        print(repr(e))
        telegram.notify(token=config.TOKEN, chat_id=config.admin_id, message=repr(e))


def about_profile(message):
    try:
        connect = sqlite3.connect('bot.db')
        cursor = connect.cursor()
        user_id = message.from_user.id
        cursor.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
        if cursor.fetchone() is None:
            bot.send_message(message.chat.id, f"{message.from_user.first_name},вы не зареганы. Ща я вас внесу в базу \
и попробуйте еще раз", reply_markup=first())
            db_profile(message)
        else:
            about = message.text
            cursor.execute(f"UPDATE users SET About = '{about}' WHERE id = '{user_id}'")
            connect.commit()
            bot.send_message(message.chat.id, 'Готово! Теперь вы можете посмотреть информацию о \
себе или другом юзере в соответвующем пункте меню', reply_markup=first())
    except Exception as e:
        print(repr(e))
        telegram.notify(token=config.TOKEN, chat_id=config.admin_id, message=repr(e))


def steam_profile(message):
    try:
        if 'steamcommunity' in message.text:
            connect = sqlite3.connect('bot.db')
            cursor = connect.cursor()
            user_id = message.from_user.id
            cursor.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
            if cursor.fetchone() is None:
                bot.send_message(message.chat.id, f"{message.from_user.first_name},вы не зареганы. Ща я вас внесу в \
базу и попробуйте еще раз", reply_markup=first())
                db_profile(message)
            else:
                steam = message.text
                cursor.execute(f"UPDATE users SET Steam = '{steam}' WHERE id = '{user_id}'")
                connect.commit()
                bot.send_message(message.chat.id, 'Готово! Теперь вы можете посмотреть информацию о \
себе или другом юзере в соответвующем пункте меню', reply_markup=first())
        else:
            bot.send_message(message.chat.id, 'Ты даун, даже ссылку вставить не можешь', reply_markup=first())
    except Exception as e:
        print(repr(e))
        telegram.notify(token=config.TOKEN, chat_id=config.admin_id, message=repr(e))


def vk_profile(message):
    try:
        if 'vk' in message.text:
            connect = sqlite3.connect('bot.db')
            cursor = connect.cursor()
            user_id = message.from_user.id
            cursor.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
            if cursor.fetchone() is None:
                bot.send_message(message.chat.id, f"{message.from_user.first_name},вы не зареганы. Ща я вас внесу в \
базу и попробуйте еще раз", reply_markup=first())
                db_profile(message)
            else:
                vk = message.text
                cursor.execute(f"UPDATE users SET VK = '{vk}' WHERE id = '{user_id}'")
                connect.commit()
                bot.send_message(message.chat.id, 'Готово! Теперь вы можете посмотреть информацию о \
себе или другом юзере в соответвующем пункте меню', reply_markup=first())
        else:
            bot.send_message(message.chat.id, 'Ты даун, даже ссылку вставить не можешь', reply_markup=first())
    except Exception as e:
        print(repr(e))
        telegram.notify(token=config.TOKEN, chat_id=config.admin_id, message=repr(e))


def discord_profile(message):
    try:
        if '#' in message.text:
            connect = sqlite3.connect('bot.db')
            cursor = connect.cursor()
            user_id = message.from_user.id
            cursor.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
            if cursor.fetchone() is None:
                bot.send_message(message.chat.id, f"{message.from_user.first_name},вы не зареганы. Ща я вас внесу в \
базу и попробуйте еще раз", reply_markup=first())
                db_profile(message)
            else:
                discord = message.text
                cursor.execute(f"UPDATE users SET Discord = '{discord}' WHERE id = '{user_id}'")
                connect.commit()
                bot.send_message(message.chat.id, 'Готово! Теперь вы можете посмотреть информацию о \
себе или другом юзере в соответвующем пункте меню', reply_markup=first())
        else:
            bot.send_message(message.chat.id, 'Вы забыли указать тег', reply_markup=first())
    except Exception as e:
        print(repr(e))
        telegram.notify(token=config.TOKEN, chat_id=config.admin_id, message=repr(e))


def youtube_profile(message):
    try:
        if 'youtube.com/' in message.text:
            connect = sqlite3.connect('bot.db')
            cursor = connect.cursor()
            user_id = message.from_user.id
            cursor.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
            if cursor.fetchone() is None:
                bot.send_message(message.chat.id, f"{message.from_user.first_name},вы не зареганы. Ща я вас внесу в \
базу и попробуйте еще раз", reply_markup=first())
                db_profile(message)
            else:
                cursor.execute(f"UPDATE users SET YouTube = '{message.text}' WHERE id = '{user_id}'")
                connect.commit()
                bot.send_message(message.chat.id, 'Готово! Теперь вы можете посмотреть информацию о \
себе или другом юзере в соответвующем пункте меню', reply_markup=first())
        else:
            bot.send_message(message.chat.id, 'Ты даун, даже ссылку вставить не можешь', reply_markup=first())
    except Exception as e:
        print(repr(e))
        telegram.notify(token=config.TOKEN, chat_id=config.admin_id, message=repr(e))


def twitch_profile(message):
    try:
        if 'twitch.tv' in message.text:
            connect = sqlite3.connect('bot.db')
            cursor = connect.cursor()
            user_id = message.from_user.id
            cursor.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
            if cursor.fetchone() is None:
                bot.send_message(message.chat.id, f"{message.from_user.first_name},вы не зареганы. Ща я вас внесу в \
базу и попробуйте еще раз", reply_markup=first())
                db_profile(message)
            else:
                cursor.execute(f"UPDATE users SET Twitch = '{message.text}' WHERE id = '{user_id}'")
                connect.commit()
                bot.send_message(message.chat.id, 'Готово! Теперь вы можете посмотреть информацию о \
себе или другом юзере в соответвующем пункте меню', reply_markup=first())
        else:
            bot.send_message(message.chat.id, 'Ты даун, даже ссылку вставить не можешь', reply_markup=first())
    except Exception as e:
        print(repr(e))
        telegram.notify(token=config.TOKEN, chat_id=config.admin_id, message=repr(e))


def twitter_profile(message):
    try:
        if 'twitter.com' in message.text:
            connect = sqlite3.connect('bot.db')
            cursor = connect.cursor()
            user_id = message.from_user.id
            cursor.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
            if cursor.fetchone() is None:
                bot.send_message(message.chat.id, f"{message.from_user.first_name},вы не зареганы. Ща я вас внесу в \
базу и попробуйте еще раз", reply_markup=first())
                db_profile(message)
            else:
                cursor.execute(f"UPDATE users SET Twitter = '{message.text}' WHERE id = '{user_id}'")
                connect.commit()
                bot.send_message(message.chat.id, 'Готово! Теперь вы можете посмотреть информацию о \
себе или другом юзере в соответвующем пункте меню', reply_markup=first())
        else:
            bot.send_message(message.chat.id, 'Ты даун, даже ссылку вставить не можешь', reply_markup=first())
    except Exception as e:
        print(repr(e))
        telegram.notify(token=config.TOKEN, chat_id=config.admin_id, message=repr(e))


def tic_tok_profile(message):
    try:
        connect = sqlite3.connect('bot.db')
        cursor = connect.cursor()
        user_id = message.from_user.id
        cursor.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
        if cursor.fetchone() is None:
            bot.send_message(message.chat.id, f"{message.from_user.first_name},вы не зареганы. Ща я вас внесу в базу \
и попробуйте еще раз", reply_markup=first())
            db_profile(message)
        else:
            cursor.execute(f"UPDATE users SET Tic_Tok = '{message.text}' WHERE id = '{user_id}'")
            connect.commit()
            bot.send_message(message.chat.id, 'Готово! Больше сюда не пиши', reply_markup=first())
    except Exception as e:
        print(repr(e))
        telegram.notify(token=config.TOKEN, chat_id=config.admin_id, message=repr(e))


def dollar_alerts(message):
    try:
        chat_id = message.chat.id
        if any(map(str.isdigit, message.text)):
            connect = sqlite3.connect('bot.db')
            cursor = connect.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS chats (
                id INTEGER 
            )""")
            connect.commit()
            cursor.execute(f"SELECT id FROM chats WHERE id = '{chat_id}'")
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO chats VALUES(?)", [chat_id])
                connect.commit()
            cursor.execute(f"SELECT id FROM chats WHERE id = '{chat_id}'")

            alert_time = int(''.join(filter(str.isdigit, message.text)))
            while True:
                resp_dollar = requests.get('https://coinmarketcap.com/ru/currencies/tether/').text
                soup = BeautifulSoup(resp_dollar, 'lxml')
                title_dollar = soup.find('div', {'class': 'priceValue'}).find('span')
                resp_euro = requests.get('https://coinmarketcap.com/ru/currencies/tether-eurt/').text
                soup = BeautifulSoup(resp_euro, 'lxml')
                title_euro = soup.find('div', {'class': 'priceValue'}).find('span')
                telegram.notify(token=config.TOKEN, chat_id=chat_id, message=f'💵 = {title_dollar.get_text()} \
\n💶 = {title_euro.get_text()}')
                sleep(60*alert_time)
        else:
            telegram.notify(token=config.TOKEN, chat_id=chat_id, message='Чел, цифрами число пиши')
    except Exception as e:
        print(repr(e))
        telegram.notify(token=config.TOKEN, chat_id=config.admin_id, message=repr(e))


def btc_alerts(message):
    try:
        chat_id = message.chat.id
        if any(map(str.isdigit, message.text)):
            connect = sqlite3.connect('bot.db')
            cursor = connect.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS chats (
                id INTEGER
                dollar_alerts INTEGER
                btc_alerts INTEGER 
            )""")
            connect.commit()
            cursor.execute(f"SELECT id FROM chats WHERE id = '{chat_id}'")
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO chats VALUES(?, ?, ?)", [chat_id])
                connect.commit()

            cursor.execute(f"SELECT id FROM chats WHERE id = '{chat_id}'")

            alert_time = int(''.join(filter(str.isdigit, message.text)))
            while True:
                resp_btc = requests.get('https://coinmarketcap.com/currencies/bitcoin/').text
                soup_btc = BeautifulSoup(resp_btc, 'lxml')
                title_btc = soup_btc.find('div', {'class': 'priceValue'}).find('span')
                resp_eth = requests.get('https://coinmarketcap.com/currencies/ethereum/').text
                soup_eth = BeautifulSoup(resp_eth, 'lxml')
                title_eth = soup_eth.find('div', {'class': 'priceValue'}).find('span')
                telegram.notify(token=config.TOKEN, chat_id=chat_id, message=f'BTC = {title_btc.get_text()} \
\nETH = {title_eth.get_text()}')
                sleep(60*alert_time)
        else:
            telegram.notify(token=config.TOKEN, chat_id=chat_id, message='Чел, цифрами число пиши')
    except Exception as e:
        print(repr(e))
        telegram.notify(token=config.TOKEN, chat_id=config.admin_id, message=repr(e))


@bot.message_handler(commands=['all'])
def tag_all(message):
    try:
        db_chats(message)
        db_profile(message)
    except Exception as e:
        print(repr(e))
        telegram.notify(token=config.TOKEN, chat_id=config.admin_id, message=repr(e))
    try:
        connect = sqlite3.connect('bot.db')
        cursor = connect.cursor()
        chat_id = message.chat.id
        all_results = []
        for i in cursor.execute(f"SELECT username FROM '{chat_id}'"):
            all_results += i
        connect.commit()
        msg = ' '.join(all_results)
        bot.send_message(message.chat.id, msg)
    except Exception as e:
        print(repr(e))
        telegram.notify(token=config.TOKEN, chat_id=config.admin_id, message=repr(e))


@bot.message_handler(commands=['profile'])
def profile(message):
    try:
        db_chats(message)
    except Exception as e:
        print(repr(e))
        telegram.notify(token=config.TOKEN, chat_id=config.admin_id, message=repr(e))
    markup = types.InlineKeyboardMarkup(row_width=4)
    item0 = types.InlineKeyboardButton('О себе', callback_data='About')
    item1 = types.InlineKeyboardButton('Steam', callback_data='Steam')
    item2 = types.InlineKeyboardButton('Discord', callback_data='Discord')
    item3 = types.InlineKeyboardButton('VK', callback_data='VK')
    item4 = types.InlineKeyboardButton('YouTube', callback_data='YouTube')
    item5 = types.InlineKeyboardButton('Twitch', callback_data='Twitch')
    item6 = types.InlineKeyboardButton('Twitter', callback_data='Twitter')
    item7 = types.InlineKeyboardButton('Pinterest', callback_data='Pinterest')
    item8 = types.InlineKeyboardButton('Tg канал', callback_data='Tg_channel')
    item9 = types.InlineKeyboardButton('Epic Games', callback_data='Epic_Games')
    item10 = types.InlineKeyboardButton('Сайт', callback_data='Site')
    item11 = types.InlineKeyboardButton('Tic Tok', callback_data='Tic_Tok')
    markup.add(item0, item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11)

    bot.send_message(message.chat.id, 'Какую информацию о себе вы хотите добавить в профиль сервера?\
\n(Пока не все работает, сам тыкай и проверяй)', reply_markup=markup)
    db_profile(message)


@bot.message_handler(commands=['start'])
def welcome(message):
    db_chats(message)
    sticker = open('jolyne.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    bot.send_message(message.chat.id, "Привет, {0.first_name}!\nЯ - <b>{1.first_name}</b>, искусственный интеллект \
высокого уровня со множеством функций, большая часть из котороых не работает!".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=first())
    try:
        db_chats(message)
        db_profile(message)
    except Exception as e:
        print(repr(e))
        telegram.notify(token=config.TOKEN, chat_id=config.admin_id, message=repr(e))


@bot.message_handler(commands=['next'])  # вторая страница
def second(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Везер Репорто 🌦️')
    item2 = types.KeyboardButton('YouTube для бедных 🎞️')
    item3 = types.KeyboardButton('Уведомления 🌐')
    item4 = types.KeyboardButton('Время 🕢')
    item5 = types.KeyboardButton('Секретная хуйня ⚙')
    item6 = types.KeyboardButton('Назад ↩')

    markup.add(item1, item2, item3, item4, item5, item6)

    bot.send_message(message.chat.id, 'Это вторая страница разнообразной (бес)полезной лабуды', reply_markup=markup)

    try:
        db_chats(message)
    except Exception as e:
        print(repr(e))
        telegram.notify(token=config.TOKEN, chat_id=config.admin_id, message=repr(e))


@bot.message_handler(commands=['weather'])  # парсинг погоды
def weather(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Украина 🇺🇦", callback_data='odessa')
    item2 = types.InlineKeyboardButton('Россия 🇷🇺', callback_data='piter')
    item3 = types.InlineKeyboardButton('Казахстан 🇰🇿', callback_data='astana')
    item4 = types.InlineKeyboardButton('Армения 🇦🇲', callback_data='erevan')

    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id, 'В столице какой из величайших стран шиноби вы хотите узнать погоду?',
                     reply_markup=markup)


@bot.message_handler(commands=['alerts'])
def alerts(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('Курс 💲 и €', callback_data='dollar_alerts')
    item2 = types.InlineKeyboardButton('Новости', callback_data='news_alerts')
    item3 = types.InlineKeyboardButton('Курс BTC и ETH', callback_data='btc_alerts')
    item4 = types.InlineKeyboardButton('Пока хз', callback_data='else')
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, 'Эта функция будет переодически отправлять уведомления в выбранной категории',
                     reply_markup=markup)


@bot.message_handler(commands=['youtube_search_start'])
def youtube_search_start(message):
    msg = bot.send_message(message.chat.id, 'Напишите в ответ на это сообщение, о чем вы хотите найти видосики?')
    bot.register_next_step_handler(msg, youtube_search)


@bot.message_handler(commands=['news'])
def last_news_search(message):  # последняя новость с сайта SVTV
    try:
        news_href = 'https://svtv.org/news/'
        driver.get(news_href)
        sleep(2)
        news = driver.find_element_by_class_name('card-news')
        bot.send_message(message.chat.id, news.get_attribute('href'))
    except Exception as e:
        bot.send_message(message.chat.id, 'Временно не работает по причине того, что пидорасы из РосКомПозора \
заблокировали этот сайт')
        print(repr(e))
        telegram.notify(token=config.TOKEN, chat_id=config.admin_id, message=repr(e))


@bot.message_handler(commands=['time'])
def msk_time(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton('Нажмите, чтобы запустить часы', callback_data='time')
    markup.add(item1)
    bot.send_message(message.chat.id, 'Эта функция показывает точное московское время (вплоть до секунд)',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def buttons(message):
    if message.text == 'Моя длина 🍆':
        if message.from_user.first_name == 'Evil Morty':
            bot.send_message(message.chat.id, str(random.randint(20, 30)) + ' см')
        elif message.from_user.username == 'SlayKas':
            bot.send_message(message.chat.id, str(random.randint(100000, 3000000)) + ' см')
        elif message.from_user.first_name == 'му{66]90]8²⅛>':
            bot.send_message(message.chat.id, '1 см')
        else:
            bot.send_message(message.chat.id, str(random.randint(0, 20)) + ' см')
    elif message.text == 'Как дела?😊':
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("Хорошо👍", callback_data='good')
        item2 = types.InlineKeyboardButton("Хуева👎", callback_data='bad')
        markup.add(item1, item2)
        bot.send_message(message.chat.id, 'Ну такое себе. А ты как?', reply_markup=markup)
    elif message.text == 'Посоветуй фильм 🎥':
        bot.send_message(message.chat.id, 'Вам наверняка понравится ' + config.kino[(random.randint(0, 49))])
    elif message.text == 'Добавить инфу 📂':
        profile(message)
    elif message.text == 'Информация о...😏':
        msg = bot.send_message(message.chat.id, 'Скиньте юзернем (в формате @[username] ) пользователя, чтобы я вывела\
его данные. \nИли введите "Я", если хотите вывести свой профиль')
        bot.register_next_step_handler(msg, info_profile)
    elif message.text == 'Секретная хуйня ⚙':
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("Исходный код🤢", callback_data='code')
        item2 = types.InlineKeyboardButton('Лучший канал в ТГ📱', callback_data='channel')
        item3 = types.InlineKeyboardButton('Узнать все о себе🧑‍💼', callback_data='info')
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, 'Секретные хуйни будут пополняться, проверяйте переодически',
                         reply_markup=markup)
    elif message.text == 'Лучшее аниме':
        bot.send_message(message.chat.id, 'Глупо спорить о том, какое а{Н}име лучше, а к{А}кое хуже. Существует огром\
ное количество жан{Р}ов и в каждом из них тысячи тайтлов... Даже я, бот, не  способен пересмотреть их все. И даже если\
 бы пересмотрел, то создать одн{У}, объективную и верную оценку просто напросто невозможно. Ни один топ, тем более если\
 мы говорим об аниме, не может отрази{Т}ь чувства и эмоции каждого из нас. Я считаю, что вопрос просто напросто не име\
ет смысла. Каждый, будь он человек или бот имеет право на собственные интересы, любимые и нелюбимые вещи. Любите, то \
что вам нравится и не устраивайте глупых срачей! У каждог{О} свои вкусы!❤')
    elif message.text == 'Дальше ➡':
        second(message)
    elif message.text == 'Везер Репорто 🌦️':
        weather(message)
    elif message.text == 'YouTube для бедных 🎞️':
        youtube_search_start(message)
    elif message.text == '👩‍💻Мой ID':
        bot.send_message(message.chat.id, f'Ваш ID: {message.from_user.id}')
    elif message.text == '🦧Мой юзернейм':
        bot.send_message(message.chat.id, f'Ваш username: @{message.from_user.username}')
    elif message.text == '🈴Мое имя (не аниме)':
        if message.from_user.last_name == 'None':
            bot.send_message(message.chat.id, f'Ваш ник: {message.from_user.first_name}')
        else:
            bot.send_message(message.chat.id, f'Ваш ник: {message.from_user.first_name} {message.from_user.last_name}')
    elif message.text == 'Последние новости 🌐':
        last_news_search(message)
    elif message.text == 'Уведомления 🌐':
        alerts(message)
    elif message.text == 'Время 🕢' or message.text.lower() == 'время':
        msk_time(message)
    elif message.text == 'Назад ↩':
        bot.send_message(message.chat.id, 'Первая страница выбора функций', reply_markup=first())
    elif ('@all' in message.text) or ('@everyone' in message.text):
        tag_all(message)
    else:
        pass


def youtube_search(message):  # поиск видео на ютубе
    try:
        bot.send_message(message.chat.id, 'Начинаю поиск по вашему запросу (чел, мог бы просто на ютуб зайти)')
        video_href = 'https://www.youtube.com/results?search_query=' + message.text
        driver.get(video_href)
        sleep(2)
        videos = driver.find_elements_by_id('video-title')
        for i in range(len(videos)):
            bot.send_message(message.chat.id, videos[i].get_attribute('href'))
            if i == 4:
                break
    except Exception as e:
        print(repr(e))
        telegram.notify(token=config.TOKEN, chat_id=config.admin_id, message=repr(e))


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            try:
                db_chats(call.message)
                db_profile(call.message)
            except Exception as e:
                print(repr(e))
                telegram.notify(token=config.TOKEN, chat_id=config.admin_id, message=repr(e))
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отлично')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Соболезную')
            elif call.data == 'code':
                bot.send_message(call.message.chat.id, 'PasteBin(может не работать, там какие-то фильтры ругаются \
на ОПАСНЫЙ КОНТЕНТ (ну такой колхозный код и правда опасен): https://pastebin.com/nG04h1KZ \nGitHub(тут должно работать\
): https://github.com/thommmasss/jolyne.bot/blob/main/main.py')
            elif call.data == 'channel':
                bot.send_message(call.message.chat.id,
                                 'На мой субъективный двоичный взгляд, лучший канал это:\n @dramaturgT')
            elif call.data == 'info':
                markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item_id = types.KeyboardButton('👩‍💻Мой ID')
                item_name = types.KeyboardButton('🈴Мое имя (не аниме)')
                item_username = types.KeyboardButton('🦧Мой юзернейм')
                item_start = types.KeyboardButton('/start')

                markup_reply.add(item_id, item_username, item_name, item_start)
                bot.send_message(call.message.chat.id, 'Что вы хотите, чтобы я рассказал о Вас (и передал данные \
в фсб)?', reply_markup=markup_reply)
            elif call.data == 'odessa':
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
                resp = requests.get('https://www.gismeteo.ru/weather-odessa-4982/', headers=headers).text
                soup = BeautifulSoup(resp, 'html.parser')
                title = soup.find('span', class_='unit_temperature_c')
                bot.send_message(call.message.chat.id, f'Погода в Одессе:\n {title.get_text()} C')

            elif call.data == 'piter':
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
                resp = requests.get('https://www.gismeteo.by/weather-sankt-peterburg-4079/', headers=headers).text
                soup = BeautifulSoup(resp, 'html.parser')
                title = soup.find('span', class_='unit_temperature_c')
                bot.send_message(call.message.chat.id, f'Погода в Разчленинграде:\n {title.get_text()} C')

            elif call.data == 'astana':
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
                resp = requests.get('https://www.gismeteo.by/weather-nur-sultan-5164/', headers=headers).text
                soup = BeautifulSoup(resp, 'html.parser')
                title = soup.find('span', class_='unit_temperature_c')
                bot.send_message(call.message.chat.id, f'Погода в Астане:\n {title.get_text()} C')

            elif call.data == 'erevan':
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
                resp = requests.get('https://www.gismeteo.by/weather-yerevan-5298/', headers=headers).text
                soup = BeautifulSoup(resp, 'html.parser')
                title = soup.find('span', class_='unit_temperature_c')
                bot.send_message(call.message.chat.id, f'Погода в Ереване:\n {title.get_text()} C')
            elif call.data == 'time':
                while True:
                    sleep(1)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"\
Точное московское время: \n {time.strftime('%m/%d/%Y, %H:%M:%S')}")
            elif call.data == 'bad' or call.data == 'good':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="На \
самом деле мне глубочайше все равно, просто я запрограммирован спрашивать, как у тебя дела😘", reply_markup=None)
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            # база данных
            elif call.data == 'About':
                msg = bot.send_message(call.message.chat.id, 'Пиши тут чо хочешь (главное не забудь указать номер \
карты, пин-код, имя держателя карты (фамилия и имя на английском), срок действия и CVC-код (с обратной стороны карты)')
                bot.register_next_step_handler(msg, about_profile)
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            elif call.data == 'Steam':
                msg = bot.send_message(call.message.chat.id, 'Скиньте ссылку на свой акк в Стиме \
(в формате https://steamcommunity.com/id/[id профиля])', disable_web_page_preview=1)
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
                bot.register_next_step_handler(msg, steam_profile)
            elif call.data == 'Discord':
                msg = bot.send_message(call.message.chat.id, 'Напишите свой ник \
в Дискорде (в формате [ник]#[тег])')
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
                bot.register_next_step_handler(msg, discord_profile)
            elif call.data == 'VK':
                msg = bot.send_message(call.message.chat.id, 'Скиньте ссылку на свой акк ВКонтакте \
(в формате vk.com/[id профиля])', disable_web_page_preview=1)
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
                bot.register_next_step_handler(msg, vk_profile)
            elif call.data == 'YouTube':
                msg = bot.send_message(call.message.chat.id, 'Скиньте ссылку на свой канал на Ютубе \
(в формате youtube.com/channel/[id])', disable_web_page_preview=1)
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
                bot.register_next_step_handler(msg, youtube_profile)
            elif call.data == 'Twitch':
                msg = bot.send_message(call.message.chat.id, 'Скиньте ссылку на свой канал на толерантной помойке, \
ой, Твиче (в формате twitch.tv/[id канала])', disable_web_page_preview=1)
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
                bot.register_next_step_handler(msg, twitch_profile)
            elif call.data == 'Twitter':
                msg = bot.send_message(call.message.chat.id, 'Капец, кто ты вообще такой, что сидишь в Твиторе? \
Ну скидывай ссылочку на акк (в формате twitter.com/[id акка])', disable_web_page_preview=1)
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
                bot.register_next_step_handler(msg, twitter_profile)
            elif call.data == 'Tic_Tok':
                msg = bot.send_message(call.message.chat.id, 'Извини, но я в душе не ебу, как в этом тиктаке \
записываются акки. Пиши чо хочешь, но лучше не пиши)')
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
                bot.register_next_step_handler(msg, tic_tok_profile)
            elif call.data == 'btc_alerts':
                msg = bot.send_message(call.message.chat.id, 'Раз в сколько минут ваз уведомлять об изменении цены?')
                bot.register_next_step_handler(msg, btc_alerts)
            elif call.data == 'dollar_alerts':
                msg = bot.send_message(call.message.chat.id, 'Раз в сколько минут ваз уведомлять об изменении цены?')
                bot.register_next_step_handler(msg, dollar_alerts)
            else:
                bot.send_message(call.message.chat.id, 'Такой функции пока что нет, но скоро будет')
    except Exception as e:
        print(repr(e))
        telegram.notify(token=config.TOKEN, chat_id=config.admin_id, message=repr(e))


@atexit.register
def bot_offline():
    try:
        connect = sqlite3.connect('bot.db')
        cursor = connect.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS chats (
            id INTEGER
        )""")
        connect.commit()
        all_results = []
        cursor.execute("SELECT id FROM chats")
        for i in cursor.execute("SELECT id FROM chats"):
            all_results += i
        connect.commit()
        for i in range(0, len(all_results)):
            telegram.notify(token=config.TOKEN, chat_id=all_results[i], message="Я пошла спать😴")
        cursor.close()
        connect.close()
    except Exception as e:
        print(repr(e))
        telegram.notify(token=config.TOKEN, chat_id=config.admin_id, message=repr(e))


# RUN
bot.polling(none_stop=True)
bot.user(can_join_groups=True)
bot.user(can_read_all_group_messages=True)
