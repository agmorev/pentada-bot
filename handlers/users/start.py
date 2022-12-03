from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, bot
from keyboards.default import main_menu

import sqlite3
import datetime


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):

    #Save information about new user to the database
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    full_name = message.from_user.full_name
    date = datetime.datetime.now()
    print('--------------------------START-------------------------------')
    print(user_id, first_name, last_name, username, full_name, date)
    try:
        conn = sqlite3.connect('/home/agmorev/pentadabot_v2/data/pentada.db')
        cursor = conn.cursor()
        print("Successfully Connected to SQLite")
        result = [user_id[0] for user_id in cursor.execute("SELECT user_id FROM teleusers;")]
        conn.commit()
        print(result)
        if str(user_id) in result:
            print("User already exists!!!")
        else:
            query2 = "INSERT INTO teleusers ('user_id', 'first_name', 'last_name', 'username', 'full_name', 'date') VALUES (?, ?, ?, ?, ?, ?);"
            variables = (user_id, first_name, last_name, username, full_name, date)
            cursor.execute(query2, variables)
            conn.commit()
            print("Record inserted successfully into teleusers table ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if (conn):
            conn.close()
            print("The SQLite connection is closed")

    #Hello message to user
    try:
        await bot.send_message("1061732281", f"‼️ Зареєстровано нового користувача у боті {first_name} {last_name} {username} ({user_id})")
    except:
        pass
    await message.answer(f'Вітаємо Вас, {message.from_user.full_name}!', reply_markup=main_menu)
