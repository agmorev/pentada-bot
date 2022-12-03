from aiogram import types
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from states.getfile import Getfile, GetEdrFile
from states.notes import Telesend, Usersend
from states.signin import Signin
from keyboards.inline.cabinet_markup import (
    login_markup,
    client_cabinet_markup, order_markup, client_report_markup,
    admin_cabinet_markup, admin_report_markup, admin_notifications_markup
)
import datetime
from aiogram.types import ContentType
import sqlite3
import firebirdsql
from sshtunnel import SSHTunnelForwarder
import pandas as pd
from io import BytesIO
import requests
import math
import re
import time
import json


user_email=''
user_password=''
user_company=''
user_fullname=''

admins = [
        1061732281, #Алексей Морев
        # 541114745, #Владимир Петров
        # 119717130, #Игорь Пиковский
        # 1902720524, #Юрий Куц
        # 910530618, #Андрей Кузнецов
        # -1001206691663, #24/7 група
    ]
clients = [
        514845824, #МойДомашний-Эковис
    ]


###################################################### КАБІНЕТ ##################################################

@dp.message_handler(text="💼 Кабінет")
async def bot_info(message: types.Message):
    await message.answer('⚠️ Особистий кабінет користувача передбачає додаткові можливості для наших клієнтів. Доступ до кабінету відкривається гарантом після укладення договору.', reply_markup=login_markup)


###################################################### LOGIN ##################################################

@dp.callback_query_handler(text_contains="login")
async def cabinet_login(call: types.CallbackQuery):
    await call.answer(cache_time=60)

    userid = call.message.chat.id
    print(userid)

    #SHOW ADMIN INTERFACE
    if userid in admins:
        await call.message.answer('<b>КАБІНЕТ КЕРІВНИКА</b>')
        await call.message.answer("Оберіть необхідну функцію", reply_markup=admin_cabinet_markup)
    elif userid in clients:
        await call.message.answer('<b>ОСОБИСТИЙ КАБІНЕТ</b>')
        await call.message.answer("Оберіть необхідну функцію", reply_markup=client_cabinet_markup)
    else:
        await call.message.answer('⛔️У доступі до особистого кабінету *відмовлено*.\nНаправте заявку для підключення або зверніться для реєстрації\n📧 office@pentada-trans.com', parse_mode="Markdown")


###################################################### SIGNIN ##################################################

@dp.callback_query_handler(text_contains="signin")
async def cabinet_signin(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await Signin.company_state.set()
    await call.message.answer('📤 <b>НАПРАВЛЕННЯ ЗАЯВКИ</b>')
    await call.message.answer('Відправлення заявки від клієнта на підключення до особистого кабінету. Підключення можливе лише після підписання договору з клієнтом.')
    await call.message.answer("1️⃣Введіть назву або код ЄДР компанії:")

@dp.message_handler(state=Signin.company_state)
async def company_input(message: types.Message, state: FSMContext):
    company = message.text
    await state.update_data(answer1=company)
    await message.answer("2️⃣Введіть прізвище, ім'я та по батькові користувача:")
    await Signin.next()

@dp.message_handler(state=Signin.name_state)
async def name_input(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(answer2=name)
    await message.answer("3️⃣Введіть email користувача:")
    await Signin.next()

@dp.message_handler(state=Signin.email_state)
async def email_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    company = data.get("answer1")
    name = data.get("answer2")
    email = message.text
    userid = message.from_user.id
    fullname = message.from_user.full_name
    await state.finish()
    await message.answer("‼️ Заявку направлено на обробку. Після підключення Вас буде поінформовано додатково.")
    await bot.send_message("1061732281", f"‼️ Нова заявка на підключення до особистого кабінету клієнта:\nкомпанія: {company}\nкористувач: {name}\nemail: {email}\nid: {userid}\nназва: {fullname}")


##########################################################################ЗАЯВКИ#################################################################

@dp.callback_query_handler(text_contains="orders")
async def cabinet_orders(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer('📑 <b>ЗАЯВКИ</b>')
    await call.message.answer('Оформлення та направлення заявки на видачу фінансової гарантії.', reply_markup=order_markup)

@dp.callback_query_handler(text_contains="order_download")
async def cabinet_order_download(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer('📤 <b>ЗАВАНТАЖЕННЯ ЗАЯВКИ</b>')
    await call.message.answer('Заявку буде завантажено в файлі order.xlsx. Ви можете скористатися цим бланком для заповнення і відправити готову заявку через відповідний сервіс Кабінету.')
    await bot.send_document(chat_id=call.message.chat.id, document="BQACAgIAAxkBAAIhxF_5xaVZIcmAKdtbNI1mQebl0coIAAIgCwACb5fQS5KVIbblRc5PHgQ")

@dp.callback_query_handler(text_contains="order_send")
async def cabinet_order_send(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await Getfile.load_state.set()
    await call.message.answer('📤 <b>НАПРАВЛЕННЯ ЗАЯВКИ</b>')
    await call.message.answer('Відправлення підготовленої заявки в форматі doc, docx, xls, xlsx або митної декларації в форматі imfx. Завантажте необхідний файл, використовуючи меню Telegram.')

@dp.message_handler(state=Getfile.load_state, content_types=ContentType.DOCUMENT)
async def load_file(message: types.Message, state: FSMContext):
    await message.document.download()
    order_fileid = message.document.file_id
    order_filename = message.document.file_name
    ext = ('doc', 'docx', 'xls', 'xlsx', 'imfx')
    if order_filename.endswith(ext):
        await state.update_data(answer=order_fileid)
        # await bot.send_message("-400711737", f"‼️ Нова ЗАЯВКА від користувача {user_fullname} ({user_email}) компанії {user_company}")
        # await message.forward("-400711737")
        await bot.send_message("-1001206691663", f"‼️ Нова ЗАЯВКА від користувача {user_fullname} ({user_email}) компанії {user_company}")
        await message.forward("-1001206691663")
        await message.reply(f"Заявку завантажено у файлі {order_filename} та направлено оператору для обробки.")
        await state.finish()
    else:
        await message.reply('❗️Завантажений Вами файл не відповідає формату doc, docx, xls, xlsx, imfx!!! Очікую на завантаження коректного файлу...')

@dp.message_handler(state=Getfile.load_state, content_types=ContentType.ANY)
async def load_file_reply(message: types.Message, state: FSMContext):
    await message.reply('❗️Введене Вами не є файлом та/або файл не відповідає формату doc, docx, imfx!!! Очікую на завантаження файлу...')


###########################################################################ЗВІТИ###################################################################

@dp.callback_query_handler(text_contains="reports")
async def cabinet_reports(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer('📊 <b>ЗВІТИ</b>')

    # GET USER INFO
    userid = call.message.chat.id

    if userid in admins:
        await call.message.answer('Отримання звітів про видані клієнту гарантії впродовж обраного періоду часу', reply_markup=admin_report_markup)
    else:
        await call.message.answer('Отримання звітів про видані клієнту гарантії впродовж обраного періоду часу', reply_markup=client_report_markup)

@dp.callback_query_handler(text=["admin_report_2021", "admin_report_2022"])
async def year_reports(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    if call.data == "admin_report_2021":
        await call.message.answer('📊 <b>РІЧНИЙ ЗВІТ 2021</b>')
        year = "2021"
    elif call.data == "admin_report_2022":
        await call.message.answer('📊 <b>РІЧНИЙ ЗВІТ 2022</b>')
        year = "2022"

    # GET USER INFO
    userid = call.message.chat.id
    fullname = call.message.chat.full_name
    date = datetime.datetime.now()

    try:
        conn = sqlite3.connect('/home/agmorev/pentadabot_v2/data/pentada.db')
        #conn = sqlite3.connect('D:\PYTHON\PROJECTS\Bots\pentadabot_v2\data\pentada.db')
        cursor = conn.cursor()
        print('-----------------CABINET-------------------')
        print("Cabinet successfully connected to SQLite by | ", fullname,' | ', date)
        cursor.execute('SELECT * FROM users WHERE user_id={};'.format(str(userid)))
        found = cursor.fetchone()
        if found:
            global user_email, user_fullname, user_com, user_com_code
            user_email = found[1]
            user_fullname = found[3]+' '+found[4]
            user_com = found[5]
            user_com_code = found[6]
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to work with sqlite table users", error)
    finally:
        if (conn):
            conn.close()
            print("The SQLite connection is closed")

    # GET DATA FROM DATABASE
    server = SSHTunnelForwarder(
                ('mail.pentada-brok.com', 57300),
                ssh_username="agmorev",
                ssh_password="Jur48dl§hfi!83",
                remote_bind_address=('192.168.70.99', 3051),
                local_bind_address=('127.0.0.1', 53051)
            )
    server.start()
    print(server)
    conn = firebirdsql.connect(
            host='127.0.0.1',
            database='C:\MasterD\MDGarant\PentadaDB\Db\MDGARANT.FDB',
            port=53051,
            user='SYSDBA',
            password='masterkey',
            charset='UTF8'
    )

    if userid in admins:
        df = pd.read_sql('''
                        SELECT
                            GL_NUM,
                            GL_DATE_CR,
                            GL_CL_NAME,
                            GL_CL_OKPO,
                            GL_CAR_NAME,
                            GL_CAR_ADR,
                            GL_CCD_07_01,
                            GL_CCD_07_02,
                            GL_CCD_07_03,
                            GL_CCD_DATE,
                            GG_33_01,
                            GG_31_01,
                            GG_35_01,
                            GL_SUMMA,
                            GL_PR,
                            GL_DATE_EXP
                        FROM GARANT_LIST
                        INNER JOIN GARANT_LIST_GOODS
                        ON GARANT_LIST.IDENT=GARANT_LIST_GOODS.IDENT
                        WHERE GL_DATE_CR>'01.01.{} 00:00' AND GL_DATE_CR<'31.12.{} 23:59' AND GL_PR!=2;
                        '''.format(year, year), conn)
    else:
        df = pd.read_sql('''
                        SELECT
                            GL_NUM,
                            GL_DATE_CR,
                            GL_CL_NAME,
                            GL_CL_OKPO,
                            GL_CAR_NAME,
                            GL_CAR_ADR,
                            GL_CCD_07_01,
                            GL_CCD_07_02,
                            GL_CCD_07_03,
                            GL_CCD_DATE,
                            GG_33_01,
                            GG_31_01,
                            GG_35_01,
                            GL_SUMMA,
                            GL_PR,
                            GL_DATE_EXP
                        FROM GARANT_LIST
                        INNER JOIN GARANT_LIST_GOODS
                        ON GARANT_LIST.IDENT=GARANT_LIST_GOODS.IDENT
                        WHERE GL_DATE_CR>'01.01.{} 00:00' AND GL_DATE_CR<'31.12.{} 23:59' AND GL_CL_OKPO LIKE '%{}' AND GL_PR!=2;
                        '''.format(year, year, user_com_code), conn)

    pd.set_option('display.float_format', lambda x: '%.2f' % x)
    df.fillna("-", inplace=True)
    df['GL_DATE_CR'].replace({'30.12.1899 00:00': ''}, inplace=True)
    df['GL_CCD_DATE'].replace({'30.12.1899 00:00': ''}, inplace=True)
    df['GL_DATE_EXP'].replace({'30.12.1899 00:00': ''}, inplace=True)

    df = df.groupby('GL_NUM').agg({
        'GL_DATE_CR': 'first',
        'GL_CL_NAME': 'first',
        'GL_CL_OKPO': 'first',
        'GL_CAR_NAME': 'first',
        'GL_CAR_ADR': 'first',
        'GL_CCD_07_01': 'first',
        'GL_CCD_07_02': 'first',
        'GL_CCD_07_03': 'first',
        'GL_CCD_DATE': 'first',
        'GG_33_01': ', '.join,
        'GG_31_01': '; '.join,
        'GG_35_01': sum,
        'GL_SUMMA': 'first',
        'GL_PR': 'first',
        'GL_DATE_EXP': 'first'
    })

    total_number = df.shape[0]
    total_sum = "{:,.2f}".format(df['GL_SUMMA'].sum())
    df['COUNT'] = 1
    final_table = df.groupby('GL_CL_NAME').agg({'COUNT': 'count', 'GL_SUMMA': 'sum'}).reset_index(drop=False)
    print(final_table)
    year_table = final_table.rename(columns={'GL_CL_NAME': 'Клієнт', 'COUNT': 'Кількість', 'GL_SUMMA': 'Сума'})
    table1 = year_table.sort_values(by=['Кількість'], ascending=False).to_string(header=False, columns=['Клієнт', 'Кількість'], sparsify=False, index=False, max_colwidth=15, col_space=10, formatters={"Сума": "{:,.2f}".format})
    table2 = year_table.sort_values(by=['Сума'], ascending=False).to_string(header=False, columns=['Клієнт', 'Сума'], sparsify=False, index=False, max_colwidth=15, col_space=10, justify='left', formatters={"Сума": "{:,.2f}".format})

    await call.message.answer('📊В {} році оформлено фінансових гарантій:\n-кількість - *{}* ГД\n-сума - *{}* грн.'.format(year, total_number, total_sum), parse_mode='Markdown')
    if userid in admins:
        await call.message.answer('🔝*За кількістю:*\n{}'.format(table1), parse_mode='Markdown')
        await call.message.answer('🔝*За сумою:*\n{}'.format(table2), parse_mode='Markdown')

    #FORM XLSX TABLE AND SEND TO USER
    in_memory = BytesIO()
    in_memory.name = '{}.xlsx'.format(call.data)
    df.to_excel(in_memory)
    in_memory.seek(0,0)
    await call.message.answer_document(in_memory)

    conn.close()
    server.stop()

@dp.callback_query_handler(text_contains=["admin_report_month"])
async def month_reports(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer('📊 <b>ПОТОЧНИЙ МІСЯЦЬ</b>')

    # GET USER INFO
    userid = call.message.chat.id
    fullname = call.message.chat.full_name
    date = datetime.datetime.now()

    try:
        conn = sqlite3.connect('/home/agmorev/pentadabot_v2/data/pentada.db')
        #conn = sqlite3.connect('D:\PYTHON\PROJECTS\Bots\pentadabot_v2\data\pentada.db')
        cursor = conn.cursor()
        print('-----------------CABINET-------------------')
        print("Cabinet successfully connected to SQLite by | ", fullname,' | ', date)
        cursor.execute('SELECT * FROM users WHERE user_id={};'.format(str(userid)))
        found = cursor.fetchone()
        if found:
            global user_email, user_fullname, user_com, user_com_code
            user_email = found[1]
            user_fullname = found[3]+' '+found[4]
            user_com = found[5]
            user_com_code = found[6]
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to work with sqlite table users", error)
    finally:
        if (conn):
            conn.close()
            print("The SQLite connection is closed")

    # GET DATA FROM DATABASE
    server = SSHTunnelForwarder(
                ('mail.pentada-brok.com', 57300),
                ssh_username="agmorev",
                ssh_password="Jur48dl§hfi!83",
                remote_bind_address=('192.168.70.99', 3051),
                local_bind_address=('127.0.0.1', 53051)
            )
    server.start()
    print(server)
    conn = firebirdsql.connect(
            host='127.0.0.1',
            database='C:\MasterD\MDGarant\PentadaDB\Db\MDGARANT.FDB',
            port=53051,
            user='SYSDBA',
            password='masterkey',
            charset='UTF8'
    )

    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    today = datetime.date.today()
    if today.day == 1:
        month = today.month
        year = today.year
    else:
        month = yesterday.month
        year = yesterday.year

    if userid in admins:
        df = pd.read_sql('''
                        SELECT
                            GL_NUM,
                            GL_DATE_CR,
                            GL_CL_NAME,
                            GL_CL_OKPO,
                            GL_CAR_NAME,
                            GL_CAR_ADR,
                            GL_CCD_07_01,
                            GL_CCD_07_02,
                            GL_CCD_07_03,
                            GL_CCD_DATE,
                            GG_33_01,
                            GG_31_01,
                            GG_35_01,
                            GL_SUMMA,
                            GL_PR,
                            GL_DATE_EXP
                        FROM GARANT_LIST
                        INNER JOIN GARANT_LIST_GOODS
                        ON GARANT_LIST.IDENT=GARANT_LIST_GOODS.IDENT
                        WHERE GL_DATE_CR>'01.{}.{} 00:00' AND GL_DATE_CR<'{} 23:59' AND GL_PR!=2;
                        '''.format(month, year, today), conn)
    else:
        df = pd.read_sql('''
                        SELECT
                            GL_NUM,
                            GL_DATE_CR,
                            GL_CL_NAME,
                            GL_CL_OKPO,
                            GL_CAR_NAME,
                            GL_CAR_ADR,
                            GL_CCD_07_01,
                            GL_CCD_07_02,
                            GL_CCD_07_03,
                            GL_CCD_DATE,
                            GG_33_01,
                            GG_31_01,
                            GG_35_01,
                            GL_SUMMA,
                            GL_PR,
                            GL_DATE_EXP
                        FROM GARANT_LIST
                        INNER JOIN GARANT_LIST_GOODS
                        ON GARANT_LIST.IDENT=GARANT_LIST_GOODS.IDENT
                        WHERE GL_DATE_CR>'01.{}.{} 00:00' AND GL_DATE_CR<'{} 23:59' AND GL_CL_OKPO LIKE '%{}' AND GL_PR!=2;
                        '''.format(month, year, today, user_com_code), conn)

    pd.set_option('display.float_format', lambda x: '%.2f' % x)
    df.fillna("-", inplace=True)
    df['GL_DATE_CR'].replace({'30.12.1899 00:00': ''}, inplace=True)
    df['GL_CCD_DATE'].replace({'30.12.1899 00:00': ''}, inplace=True)
    df['GL_DATE_EXP'].replace({'30.12.1899 00:00': ''}, inplace=True)

    df = df.groupby('GL_NUM').agg({
        'GL_DATE_CR': 'first',
        'GL_CL_NAME': 'first',
        'GL_CL_OKPO': 'first',
        'GL_CAR_NAME': 'first',
        'GL_CAR_ADR': 'first',
        'GL_CCD_07_01': 'first',
        'GL_CCD_07_02': 'first',
        'GL_CCD_07_03': 'first',
        'GL_CCD_DATE': 'first',
        'GG_33_01': ', '.join,
        'GG_31_01': '; '.join,
        'GG_35_01': sum,
        'GL_SUMMA': 'first',
        'GL_PR': 'first',
        'GL_DATE_EXP': 'first'
    })

    total_number = df.shape[0]
    total_sum = "{:,.2f}".format(df['GL_SUMMA'].sum())
    df['COUNT'] = 1
    final_table = df.groupby('GL_CL_NAME').agg({'COUNT': 'count', 'GL_SUMMA': 'sum'}).reset_index(drop=False)
    month_table = final_table.rename(columns={'GL_CL_NAME': 'Клієнт', 'COUNT': 'Кількість', 'GL_SUMMA': 'Сума'})
    table1 = month_table.sort_values(by=['Кількість'], ascending=False).to_string(header=False, columns=['Клієнт', 'Кількість'], sparsify=False, index=False, max_colwidth=15, col_space=10, formatters={"Сума": "{:,.2f}".format})
    table2 = month_table.sort_values(by=['Сума'], ascending=False).to_string(header=False, columns=['Клієнт', 'Сума'], sparsify=False, index=False, max_colwidth=15, col_space=10, justify='left', formatters={"Сума": "{:,.2f}".format})

    await call.message.answer('📊З початку місяця оформлено фінансових гарантій:\n-кількість - *{}* ГД\n-сума - *{}* грн.'.format(total_number, total_sum), parse_mode='Markdown')
    if userid in admins:
        await call.message.answer('🔝*За кількістю:*\n{}'.format(table1), parse_mode='Markdown')
        await call.message.answer('🔝*За сумою:*\n{}'.format(table2), parse_mode='Markdown')

    #FORM XLSX TABLE AND SEND TO USER
    in_memory = BytesIO()
    in_memory.name = '{}.xlsx'.format(call.data)
    df.to_excel(in_memory)
    in_memory.seek(0,0)
    await call.message.answer_document(in_memory)

    conn.close()
    server.stop()

@dp.callback_query_handler(text_contains=["admin_report_yesterday"])
async def yesterday_reports(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer('📊 <b>МИНУЛА ДОБА</b>')

    # GET USER INFO
    userid = call.message.chat.id
    fullname = call.message.chat.full_name
    date = datetime.datetime.now()

    try:
        conn = sqlite3.connect('/home/agmorev/pentadabot_v2/data/pentada.db')
        #conn = sqlite3.connect('D:\PYTHON\PROJECTS\Bots\pentadabot_v2\data\pentada.db')
        cursor = conn.cursor()
        print('-----------------CABINET-------------------')
        print("Cabinet successfully connected to SQLite by | ", fullname,' | ', date)
        cursor.execute('SELECT * FROM users WHERE user_id={};'.format(str(userid)))
        found = cursor.fetchone()
        if found:
            global user_email, user_fullname, user_com, user_com_code
            user_email = found[1]
            user_fullname = found[3]+' '+found[4]
            user_com = found[5]
            user_com_code = found[6]
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to work with sqlite table users", error)
    finally:
        if (conn):
            conn.close()
            print("The SQLite connection is closed")

    # GET DATA FROM DATABASE
    server = SSHTunnelForwarder(
                ('mail.pentada-brok.com', 57300),
                ssh_username="agmorev",
                ssh_password="Jur48dl§hfi!83",
                remote_bind_address=('192.168.70.99', 3051),
                local_bind_address=('127.0.0.1', 53051)
            )
    server.start()
    print(server)
    conn = firebirdsql.connect(
            host='127.0.0.1',
            database='C:\MasterD\MDGarant\PentadaDB\Db\MDGARANT.FDB',
            port=53051,
            user='SYSDBA',
            password='masterkey',
            charset='UTF8'
    )

    yesterday = datetime.date.today() - datetime.timedelta(days=1)

    if userid in admins:
        df = pd.read_sql('''
                        SELECT
                            GL_NUM,
                            GL_DATE_CR,
                            GL_CL_NAME,
                            GL_CL_OKPO,
                            GL_CAR_NAME,
                            GL_CAR_ADR,
                            GL_CCD_07_01,
                            GL_CCD_07_02,
                            GL_CCD_07_03,
                            GL_CCD_DATE,
                            GG_33_01,
                            GG_31_01,
                            GG_35_01,
                            GL_SUMMA,
                            GL_PR,
                            GL_DATE_EXP
                        FROM GARANT_LIST
                        INNER JOIN GARANT_LIST_GOODS
                        ON GARANT_LIST.IDENT=GARANT_LIST_GOODS.IDENT
                        WHERE GL_DATE_CR>'{} 00:00' AND GL_DATE_CR<'{} 23:59' AND GL_PR!=2;
                        '''.format(yesterday, yesterday), conn)
    else:
        df = pd.read_sql('''
                        SELECT
                            GL_NUM,
                            GL_DATE_CR,
                            GL_CL_NAME,
                            GL_CL_OKPO,
                            GL_CAR_NAME,
                            GL_CAR_ADR,
                            GL_CCD_07_01,
                            GL_CCD_07_02,
                            GL_CCD_07_03,
                            GL_CCD_DATE,
                            GG_33_01,
                            GG_31_01,
                            GG_35_01,
                            GL_SUMMA,
                            GL_PR,
                            GL_DATE_EXP
                        FROM GARANT_LIST
                        INNER JOIN GARANT_LIST_GOODS
                        ON GARANT_LIST.IDENT=GARANT_LIST_GOODS.IDENT
                        WHERE GL_DATE_CR>'{} 00:00' AND GL_DATE_CR<'{} 23:59' AND GL_CL_OKPO LIKE '%{}' AND GL_PR!=2;
                        '''.format(yesterday, yesterday, user_com_code), conn)

    pd.set_option('display.float_format', lambda x: '%.2f' % x)
    df.fillna("-", inplace=True)
    df['GL_DATE_CR'].replace({'30.12.1899 00:00': ''}, inplace=True)
    df['GL_CCD_DATE'].replace({'30.12.1899 00:00': ''}, inplace=True)
    df['GL_DATE_EXP'].replace({'30.12.1899 00:00': ''}, inplace=True)

    df = df.groupby('GL_NUM').agg({
        'GL_DATE_CR': 'first',
        'GL_CL_NAME': 'first',
        'GL_CL_OKPO': 'first',
        'GL_CAR_NAME': 'first',
        'GL_CAR_ADR': 'first',
        'GL_CCD_07_01': 'first',
        'GL_CCD_07_02': 'first',
        'GL_CCD_07_03': 'first',
        'GL_CCD_DATE': 'first',
        'GG_33_01': ', '.join,
        'GG_31_01': '; '.join,
        'GG_35_01': sum,
        'GL_SUMMA': 'first',
        'GL_PR': 'first',
        'GL_DATE_EXP': 'first'
    })

    total_number = df.shape[0]
    total_sum = "{:,.2f}".format(df['GL_SUMMA'].sum())
    df['COUNT'] = 1
    final_table = df.groupby('GL_CL_NAME').agg({'COUNT': 'count', 'GL_SUMMA': 'sum'}).reset_index(drop=False)
    yesterday_table = final_table.rename(columns={'GL_CL_NAME': 'Клієнт', 'COUNT': 'Кількість', 'GL_SUMMA': 'Сума'})
    table1 = yesterday_table.sort_values(by=['Кількість'], ascending=False).to_string(header=False, columns=['Клієнт', 'Кількість'], sparsify=False, index=False, max_colwidth=15, col_space=10, justify='left', formatters={"Сума": "{:,.2f}".format})
    table2 = yesterday_table.sort_values(by=['Сума'], ascending=False).to_string(header=False, columns=['Клієнт', 'Сума'], sparsify=False, index=False, max_colwidth=15, col_space=10, justify='left', formatters={"Сума": "{:,.2f}".format})

    await call.message.answer('📊За минулу добу *{}* оформлено фінансових гарантій:\n-кількість - *{}* ГД\n-сума - *{}* грн.'.format(yesterday.strftime("%d.%m.%Y"), total_number, total_sum), parse_mode='Markdown')
    if userid in admins:
        await call.message.answer('🔝*За кількістю:*\n{}'.format(table1), parse_mode='Markdown')
        await call.message.answer('🔝*За сумою:*\n{}'.format(table2), parse_mode='Markdown')

    conn.close()
    server.stop()

    #FORM XLSX TABLE AND SEND TO USER
    in_memory = BytesIO()
    in_memory.name = '{}.xlsx'.format(call.data)
    df.to_excel(in_memory)
    in_memory.seek(0,0)
    await call.message.answer_document(in_memory)

@dp.callback_query_handler(text_contains=["admin_report_today"])
async def today_reports(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer('📊 <b>ПОТОЧНА ДОБА</b>')

    # GET USER INFO
    userid = call.message.chat.id
    fullname = call.message.chat.full_name
    date = datetime.datetime.now()

    try:
        conn = sqlite3.connect('/home/agmorev/pentadabot_v2/data/pentada.db')
        #conn = sqlite3.connect('D:\PYTHON\PROJECTS\Bots\pentadabot_v2\data\pentada.db')
        cursor = conn.cursor()
        print('-----------------CABINET-------------------')
        print("Cabinet successfully connected to SQLite by | ", fullname,' | ', date)
        cursor.execute('SELECT * FROM users WHERE user_id={};'.format(str(userid)))
        found = cursor.fetchone()
        if found:
            global user_email, user_fullname, user_com, user_com_code
            user_email = found[1]
            user_fullname = found[3]+' '+found[4]
            user_com = found[5]
            user_com_code = found[6]
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to work with sqlite table users", error)
    finally:
        if (conn):
            conn.close()
            print("The SQLite connection is closed")

    # GET DATA FROM DATABASE
    server = SSHTunnelForwarder(
                ('mail.pentada-brok.com', 57300),
                ssh_username="agmorev",
                ssh_password="Jur48dl§hfi!83",
                remote_bind_address=('192.168.70.99', 3051),
                local_bind_address=('127.0.0.1', 53051)
            )
    server.start()
    print(server)
    conn = firebirdsql.connect(
            host='127.0.0.1',
            database='C:\MasterD\MDGarant\PentadaDB\Db\MDGARANT.FDB',
            port=53051,
            user='SYSDBA',
            password='masterkey',
            charset='UTF8'
    )

    today = datetime.date.today()

    if userid in admins:
        df = pd.read_sql('''
                        SELECT
                            GL_NUM,
                            GL_DATE_CR,
                            GL_CL_NAME,
                            GL_CL_OKPO,
                            GL_CAR_NAME,
                            GL_CAR_ADR,
                            GL_CCD_07_01,
                            GL_CCD_07_02,
                            GL_CCD_07_03,
                            GL_CCD_DATE,
                            GG_33_01,
                            GG_31_01,
                            GG_35_01,
                            GL_SUMMA,
                            GL_PR,
                            GL_DATE_EXP
                        FROM GARANT_LIST
                        INNER JOIN GARANT_LIST_GOODS
                        ON GARANT_LIST.IDENT=GARANT_LIST_GOODS.IDENT
                        WHERE GL_DATE_CR>'{} 00:00' AND GL_DATE_CR<'{} 23:59' AND GL_PR!=2;
                        '''.format(today, today), conn)
    else:
        df = pd.read_sql('''
                        SELECT
                            GL_NUM,
                            GL_DATE_CR,
                            GL_CL_NAME,
                            GL_CL_OKPO,
                            GL_CAR_NAME,
                            GL_CAR_ADR,
                            GL_CCD_07_01,
                            GL_CCD_07_02,
                            GL_CCD_07_03,
                            GL_CCD_DATE,
                            GG_33_01,
                            GG_31_01,
                            GG_35_01,
                            GL_SUMMA,
                            GL_PR,
                            GL_DATE_EXP
                        FROM GARANT_LIST
                        INNER JOIN GARANT_LIST_GOODS
                        ON GARANT_LIST.IDENT=GARANT_LIST_GOODS.IDENT
                        WHERE GL_DATE_CR>'{} 00:00' AND GL_DATE_CR<'{} 23:59' AND GL_CL_OKPO LIKE '%{}' AND GL_PR!=2;
                        '''.format(today, today, user_com_code), conn)

    pd.set_option('display.float_format', lambda x: '%.2f' % x)
    df.fillna("-", inplace=True)
    df['GL_DATE_CR'].replace({'30.12.1899 00:00': ''}, inplace=True)
    df['GL_CCD_DATE'].replace({'30.12.1899 00:00': ''}, inplace=True)
    df['GL_DATE_EXP'].replace({'30.12.1899 00:00': ''}, inplace=True)

    df = df.groupby('GL_NUM').agg({
        'GL_DATE_CR': 'first',
        'GL_CL_NAME': 'first',
        'GL_CL_OKPO': 'first',
        'GL_CAR_NAME': 'first',
        'GL_CAR_ADR': 'first',
        'GL_CCD_07_01': 'first',
        'GL_CCD_07_02': 'first',
        'GL_CCD_07_03': 'first',
        'GL_CCD_DATE': 'first',
        'GG_33_01': ', '.join,
        'GG_31_01': '; '.join,
        'GG_35_01': sum,
        'GL_SUMMA': 'first',
        'GL_PR': 'first',
        'GL_DATE_EXP': 'first'
    })

    total_number = df.shape[0]
    total_sum = "{:,.2f}".format(df['GL_SUMMA'].sum())
    df['COUNT'] = 1
    final_table = df.groupby('GL_CL_NAME').agg({'COUNT': 'count', 'GL_SUMMA': 'sum'}).reset_index(drop=False)
    today_table = final_table.rename(columns={'GL_CL_NAME': 'Клієнт', 'COUNT': 'Кількість', 'GL_SUMMA': 'Сума'})
    table1 = today_table.sort_values(by=['Кількість'], ascending=False).to_string(header=False, columns=['Клієнт', 'Кількість'], sparsify=False, index=False, max_colwidth=15, col_space=10, justify='left', formatters={"Сума": "{:,.2f}".format})
    table2 = today_table.sort_values(by=['Сума'], ascending=False).to_string(header=False, columns=['Клієнт', 'Сума'], sparsify=False, index=False, max_colwidth=15, col_space=10, justify='left', formatters={"Сума": "{:,.2f}".format})

    await call.message.answer('📊За поточну добу *{}* оформлено фінансових гарантій:\n-кількість - *{}* ГД\n-сума - *{}* грн.'.format(today.strftime("%d.%m.%Y"), total_number, total_sum), parse_mode='Markdown')
    if userid in admins:
        await call.message.answer('🔝*За кількістю:*\n{}'.format(table1), parse_mode='Markdown')
        await call.message.answer('🔝*За сумою:*\n{}'.format(table2), parse_mode='Markdown')

    conn.close()
    server.stop()

    #FORM XLSX TABLE AND SEND TO USER
    in_memory = BytesIO()
    in_memory.name = '{}.xlsx'.format(call.data)
    df.to_excel(in_memory)
    in_memory.seek(0,0)
    await call.message.answer_document(in_memory)

@dp.callback_query_handler(text_contains=["report_simissued"])
async def simissued_reports(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer('⛔️ <b>ОДНОЧАСНО ВИДАНІ ГАРАНТІЇ</b>')

    # GET USER INFO
    userid = call.message.chat.id

    # GET DATA FROM DATABASE
    server = SSHTunnelForwarder(
                ('mail.pentada-brok.com', 57300),
                ssh_username="agmorev",
                ssh_password="Jur48dl§hfi!83",
                remote_bind_address=('192.168.70.99', 3051),
                local_bind_address=('127.0.0.1', 53051)
            )
    server.start()
    print(server)
    conn = firebirdsql.connect(
            host='127.0.0.1',
            database='C:\MasterD\MDGarant\PentadaDB\Db\MDGARANT.FDB',
            port=53051,
            user='SYSDBA',
            password='masterkey',
            charset='UTF8'
    )

    if userid in admins:
        df = pd.read_sql('''
                        SELECT
                            GL_NUM,
                            GL_DATE_CR,
                            GL_CL_NAME,
                            GL_CL_OKPO,
                            GL_CAR_NAME,
                            GL_CAR_ADR,
                            GL_CCD_07_01,
                            GL_CCD_07_02,
                            GL_CCD_07_03,
                            GL_CCD_DATE,
                            GG_33_01,
                            GG_31_01,
                            GG_35_01,
                            GL_SUMMA,
                            GL_PR,
                            GL_DATE_EXP
                        FROM GARANT_LIST
                        INNER JOIN GARANT_LIST_GOODS
                        ON GARANT_LIST.IDENT=GARANT_LIST_GOODS.IDENT
                        WHERE GL_PR=1 OR GL_PR=3;
                        ''', conn)
    else:
        df = pd.read_sql('''
                        SELECT
                            GL_NUM,
                            GL_DATE_CR,
                            GL_CL_NAME,
                            GL_CL_OKPO,
                            GL_CAR_NAME,
                            GL_CAR_ADR,
                            GL_CCD_07_01,
                            GL_CCD_07_02,
                            GL_CCD_07_03,
                            GL_CCD_DATE,
                            GG_33_01,
                            GG_31_01,
                            GG_35_01,
                            GL_SUMMA,
                            GL_PR,
                            GL_DATE_EXP
                        FROM GARANT_LIST
                        INNER JOIN GARANT_LIST_GOODS
                        ON GARANT_LIST.IDENT=GARANT_LIST_GOODS.IDENT
                        WHERE GL_PR=1 OR GL_PR=3;
                        ''', conn)

    pd.set_option('display.float_format', lambda x: '%.2f' % x)
    df.fillna("-", inplace=True)
    df['GL_DATE_CR'].replace({'30.12.1899 00:00': ''}, inplace=True)
    df['GL_CCD_DATE'].replace({'30.12.1899 00:00': ''}, inplace=True)
    df['GL_DATE_EXP'].replace({'30.12.1899 00:00': ''}, inplace=True)

    df = df.groupby('GL_NUM').agg({
        'GL_DATE_CR': 'first',
        'GL_CL_NAME': 'first',
        'GL_CL_OKPO': 'first',
        'GL_CAR_NAME': 'first',
        'GL_CAR_ADR': 'first',
        'GL_CCD_07_01': 'first',
        'GL_CCD_07_02': 'first',
        'GL_CCD_07_03': 'first',
        'GL_CCD_DATE': 'first',
        'GG_33_01': ', '.join,
        'GG_31_01': '; '.join,
        'GG_35_01': sum,
        'GL_SUMMA': 'first',
        'GL_PR': 'first',
        'GL_DATE_EXP': 'first'
    })

    total_number = df.shape[0]
    total_sum = "{:,.2f}".format(df['GL_SUMMA'].sum())

    await call.message.answer('⚠️На даний час одночасно виданих фінансових гарантій:\n-кількість - *{}* ГД\n-сума - *{}* грн.'.format(total_number, total_sum), parse_mode='Markdown')

    #FORM XLSX TABLE AND SEND TO USER
    in_memory = BytesIO()
    in_memory.name = '{}.xlsx'.format(call.data)
    df.to_excel(in_memory)
    in_memory.seek(0,0)
    await call.message.answer_document(in_memory)

    conn.close()
    server.stop()

@dp.callback_query_handler(text_contains=["report_expiration"])
async def expiration_reports(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer('⌛️ <b>ЗАВЕРШЕННЯ ТЕРМІНУ ДІЇ</b>')

    # GET USER INFO
    userid = call.message.chat.id

    # GET DATA FROM DATABASE
    server = SSHTunnelForwarder(
                ('mail.pentada-brok.com', 57300),
                ssh_username="agmorev",
                ssh_password="Jur48dl§hfi!83",
                remote_bind_address=('192.168.70.99', 3051),
                local_bind_address=('127.0.0.1', 53051)
            )
    server.start()
    print(server)
    conn = firebirdsql.connect(
            host='127.0.0.1',
            database='C:\MasterD\MDGarant\PentadaDB\Db\MDGARANT.FDB',
            port=53051,
            user='SYSDBA',
            password='masterkey',
            charset='UTF8'
    )

    exp_date = (datetime.datetime.today() + datetime.timedelta(days=3)).strftime("%Y-%m-%d")
    if userid in admins:
        df = pd.read_sql('''
                        SELECT
                            GL_NUM,
                            GL_DATE_CR,
                            GL_CL_NAME,
                            GL_CL_OKPO,
                            GL_CAR_NAME,
                            GL_CAR_ADR,
                            GL_CCD_07_01,
                            GL_CCD_07_02,
                            GL_CCD_07_03,
                            GL_CCD_DATE,
                            GG_33_01,
                            GG_31_01,
                            GG_35_01,
                            GL_SUMMA,
                            GL_PR,
                            GL_DATE_EXP
                        FROM GARANT_LIST
                        INNER JOIN GARANT_LIST_GOODS
                        ON GARANT_LIST.IDENT=GARANT_LIST_GOODS.IDENT
                        WHERE (GL_PR=1 OR GL_PR=3) AND (GL_DATE_EXP<='{}');
                        '''.format(exp_date), conn)

    pd.set_option('display.float_format', lambda x: '%.2f' % x)
    df.fillna("-", inplace=True)
    df['GL_DATE_CR'].replace({'30.12.1899 00:00': ''}, inplace=True)
    df['GL_CCD_DATE'].replace({'30.12.1899 00:00': ''}, inplace=True)
    df['GL_DATE_EXP'].replace({'30.12.1899 00:00': ''}, inplace=True)

    df = df.groupby('GL_NUM').agg({
        'GL_DATE_CR': 'first',
        'GL_CL_NAME': 'first',
        'GL_CL_OKPO': 'first',
        'GL_CAR_NAME': 'first',
        'GL_CAR_ADR': 'first',
        'GL_CCD_07_01': 'first',
        'GL_CCD_07_02': 'first',
        'GL_CCD_07_03': 'first',
        'GL_CCD_DATE': 'first',
        'GG_33_01': ', '.join,
        'GG_31_01': '; '.join,
        'GG_35_01': sum,
        'GL_SUMMA': 'first',
        'GL_PR': 'first',
        'GL_DATE_EXP': 'first'
    })

    total_number = df.shape[0]
    total_sum = "{:,.2f}".format(df['GL_SUMMA'].sum())

    await call.message.answer('‼️ На даний час термін дії закінчується за 3 дні для фінансових гарантій:\n-кількість - *{}* ГД\n-сума - *{}* грн.'.format(total_number, total_sum), parse_mode='Markdown')

    #FORM XLSX TABLE AND SEND TO USER
    in_memory = BytesIO()
    in_memory.name = '{}.xlsx'.format(call.data)
    df.to_excel(in_memory)
    in_memory.seek(0,0)
    await call.message.answer_document(in_memory)

    conn.close()
    server.stop()


############################################################### ІНФОРМАЦІЯ З ЄДР##################################################################3

@dp.callback_query_handler(text_contains="edr_info")
async def cabinet_edr_info(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await GetEdrFile.load_state.set()
    await call.message.answer('🗂 <b>ІНФОРМАЦІЯ З ЄДР</b>')
    await call.message.answer('Завантаження з Єдиного державного реєстру інформації про компанії на підставі кодів з файлу у форматі xlsx. Завантажте необхідний файл, використовуючи меню Telegram.')

@dp.message_handler(state=GetEdrFile.load_state, content_types=ContentType.DOCUMENT)
async def load_edr_file(message: types.Message, state: FSMContext):

    #INFO ABOUT USER
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username

    await message.document.download()
    edr_fileid = message.document.file_id
    edr_filename = message.document.file_name
    edr_filepath = await bot.get_file(edr_fileid)
    ext = ('xlsx')
    if edr_filename.endswith(ext):
        await state.update_data(answer=edr_fileid)
        await message.reply(f"Перелік кодів ЄДР завантажено у файлі {edr_filename}. Обробляється...")
        await bot.send_message("1061732281", f"‼️ Новий запит на інформацію з ЄДР від користувача {first_name} {last_name} {username} ({user_id})")
        await state.finish()
        doc = open('/home/agmorev/pentadabot_v2/data/waiting.mp4', 'rb')
        msg = await message.answer_animation(doc, caption='Зачекайте...')

        # ЄДР ПАРСЕР БЛОК
        df = pd.read_excel(edr_filepath.file_path, sheet_name=0)
        df.insert(1, 'Назва', '', True)
        df.insert(2, 'Адреса реєстрації', '', True)
        df.insert(3, 'Дата реєстрації', '', True)
        df.insert(4, 'Статутний фонд', '', True)
        df.insert(5, 'Діяльність', '', True)
        df.insert(6, 'Керівник', '', True)
        df.insert(7, 'Пошта', '', True)
        df.insert(8, 'Телефон', '', True)
        df.insert(9, 'Статус', '', True)
        print(df)

        # OUTPUT TABLE CREATING
        email_pattern = r'\S+@\S+\.\S+'
        phone_pattern = r'\+\d{12}'
        for index, row in df.iterrows():
            # Exclude foreign companies
            if math.isnan(row["Код"]):
                time.sleep(1)
                continue
            if len(str(int(row["Код"]))) < 8:
                c_code = str(int(row["Код"])).zfill(8)
            else:
                c_code = str(int(row["Код"]))
            response = requests.get('https://e-data.com.ua/api/v1/search/data/?search={}'.format(c_code))
            data = json.loads(response.text)
            try:
                try:
                    c_id = data['data']['uos'][0]['uo_id']
                except:
                    time.sleep(1)
                    continue
                response2 = requests.get('https://e-data.com.ua/api/v1/uo/data/{}'.format(c_id))
                data2 = json.loads(response2.text)
                try:
                    c_name = data2['data']['name']
                except:
                    c_name = ""
                try:
                    c_regdate = data2['data']['reg_date']
                except:
                    c_regdate = ""
                try:
                    c_capital = data2['data']['authorized_capital']
                except:
                    c_capital = ""
                try:
                    c_signer = data2['data']['singers'][0]
                except:
                    c_signer = ""
                try:
                    c_activity = data2['data']['activity_kinds'][0]['name']
                except:
                    c_activity = ""
                if data2['data']['contacts']:
                    c_contacts = data2['data']['contacts']
                    try:
                        c_phones = "; ".join(re.findall(phone_pattern, c_contacts))
                    except:
                        c_phones = ""
                    try:
                        c_email = "; ".join(re.findall(email_pattern, c_contacts, re.IGNORECASE))
                    except:
                        c_email = ""
                else:
                    c_email = ""
                    c_phones = ""
                try:
                    c_status = data2['data']['state_name']
                except:
                    c_status = ""
                try:
                    c_address = data2['data']['address']
                except:
                    c_address = ""
                time.sleep(1)
            except:
                try:
                    c_name = data['data']['uos'][0]['uo_name']
                except:
                    c_name = ""
                try:
                    c_regdate = data['data']['uos'][0]['uo_reg_date']
                except:
                    c_regdate = ""
                try:
                    c_capital = data['data']['uos'][0]['uo_authorized_capital']
                except:
                    c_capital = ""
                if data['data']['uos'][0]['uo_contacts']:
                    c_contacts = data['data']['uos'][0]['uo_contacts']
                    try:
                        c_phones = "; ".join(re.findall(phone_pattern, c_contacts))
                    except:
                        c_phones = ""
                    try:
                        c_email = "; ".join(re.findall(email_pattern, c_contacts, re.IGNORECASE))
                    except:
                        c_email = ""
                else:
                    c_email = ""
                    c_phones = ""
                try:
                    c_status = data['data']['uos'][0]['state_name']
                except:
                    c_status = ""
                try:
                    c_address = data['data']['uos'][0]['uo_address']
                except:
                    c_address = ""
                c_activity = ""
                c_signer = ""
                time.sleep(1)

            df.at[index,'Назва'] = c_name
            df.at[index,'Адреса реєстрації'] = c_address
            df.at[index,'Дата реєстрації'] = c_regdate
            df.at[index,'Статутний фонд'] = c_capital
            df.at[index,'Діяльність'] = c_activity
            df.at[index,'Керівник'] = c_signer
            df.at[index,'Пошта'] = c_email
            df.at[index,'Телефон'] = c_phones
            df.at[index,'Статус'] = c_status

            time.sleep(1)

        await msg.delete()

        #FORM XLSX TABLE AND SEND TO USER
        today = datetime.datetime.today().strftime("%d-%m-%Y")
        in_memory = BytesIO()
        in_memory.name = 'edrpou{}.xlsx'.format(today)
        df.to_excel(in_memory)
        in_memory.seek(0,0)
        await message.answer_document(in_memory)

        #DUPLICATE MESSAGE AND FILE TO ADMIN
        in_memory = BytesIO()
        in_memory.name = 'edrpou{}.xlsx'.format(today)
        df.to_excel(in_memory)
        in_memory.seek(0,0)
        await bot.send_document("1061732281", document=in_memory)
    else:
        await message.reply('❗️Завантажений Вами файл не відповідає формату xlsx!!! Очікую на завантаження коректного файлу...')

@dp.message_handler(state=GetEdrFile.load_state, content_types=ContentType.ANY)
async def load_edr_file_reply(message: types.Message, state: FSMContext):
    await message.reply('❗️Введене Вами не є файлом та/або файл не відповідає формату xlsx!!! Очікую на завантаження файлу...')



####################################################################### РОЗСИЛКИ ############################################################################

@dp.callback_query_handler(text_contains="notifications")
async def cabinet_notifications(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer('📨 <b>РОЗСИЛКИ</b>')
    await call.message.answer('Одинична та масова розсилка повідомлень та реклами користувачам та клієнтам.', reply_markup=admin_notifications_markup)


###################################### НАПРАВЛЕННЯ ПОВІДОМЛЕННЯ КОНКРЕТНОМУ КОРИСТУВАЧУ БОТА ################################################################

@dp.callback_query_handler(text_contains="usersend")
async def cabinet_notification_usersend(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await Usersend.userid_state.set()
    await call.message.answer('✉️ <b>НАПРАВЛЕННЯ ПОВІДОМЛЕННЯ</b>')
    await call.message.answer('Направлення одиничного повідомлення конкретному користувачу бота.')
    await call.message.answer('1️⃣Введіть ID користувача бота - адресата:')

@dp.message_handler(state=Usersend.userid_state, content_types=ContentType.TEXT)
async def userid_input(message: types.Message, state: FSMContext):
    await state.update_data(answer1=message.text)
    await message.answer("2️⃣Завантажте повідомлення та/або медіа-контент для розсилки, використовуючи меню месенджера:")
    await Usersend.next()

@dp.message_handler(state=Usersend.message_state, content_types=ContentType.ANY)
async def user_message_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    recepient_id = data.get("answer1")

    #INFO ABOUT USER
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username

    await state.finish()

    # SEND MESSAGE TO BOT USER
    try:
        if message.content_type == "text":
            await bot.send_message(recepient_id, message.text)
        elif message.content_type == "document":
            await message.document.download()
            await bot.send_document(recepient_id, message.document.file_id)
        elif message.content_type == "photo":
            await message.photo[-1].download()
            await bot.send_photo(recepient_id, message.photo[-1].file_id, message.caption)
        else:
            await message.answer("‼️ Прийнятними є лише наступний тип повідомлення: текст, документ, зображення. Завантажте відповідний контент.")
    except:
        await message.answer("🚫 Проблема. Повідомлення не відправлено.")
    await message.answer("✅ Розсилку успішно завершено.")
    await bot.send_message("1061732281", f"‼️ Нова розсилка від користувача {first_name} {last_name} {username} ({user_id})")


################################################ МАСОВА РОЗСИЛКА КОРИСТУВАЧАМ БОТА ############################################################################

@dp.callback_query_handler(text_contains="telesend")
async def cabinet_notifications_telesend(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await Telesend.message_state.set()
    await call.message.answer('✉️ <b>РОЗСИЛКА КОРИСТУВАЧАМ</b>')
    await call.message.answer('Масова розсилка повідомлень та реклами користувачам бота.')
    await call.message.answer('Завантажте повідомлення та/або медіа-контент для розсилки, використовуючи меню месенджера.')

@dp.message_handler(state=Telesend.message_state, content_types=ContentType.ANY)
async def load_message(message: types.Message, state: FSMContext):

    #INFO ABOUT USER
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username

    await state.finish()

    try:
        connection = sqlite3.connect('data/pentada.db')
        cursor = connection.cursor()
        print("Successfully Connected to SQLite")
        cursor.execute("""SELECT user_id from teleusers""")
        get_id = cursor.fetchall()
        connection.commit()
        connection.close()

        # SEND MESSAGE TO BOT USERS
        for id in get_id:
            try:
                if message.content_type == "text":
                    await bot.send_message(id, message.text)
                elif message.content_type == "document":
                    await message.document.download()
                    await bot.send_document(id, message.document.file_id)
                elif message.content_type == "photo":
                    await message.photo[-1].download()
                    await bot.send_photo(id, message.photo[-1].file_id, message.caption)
                else:
                    await message.answer("‼️ Прийнятними є лише наступний тип повідомлення: текст, документ, зображення. Завантажте відповідний контент.")
            except:
                continue
        await message.answer("✅ Розсилку успішно завершено.")
        await bot.send_message("1061732281", f"‼️ Нова розсилка від користувача {first_name} {last_name} {username} ({user_id})")
    except:
        print("Проблема із зчитуванням з бази даних")


############################################################## РЕКВІЗИТИ ГАРАНТА ############################################################################
@dp.callback_query_handler(text_contains="requisits")
async def cabinet_requisits(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer('🏦 <b>РЕКВІЗИТИ ГАРАНТА</b>')
    await call.message.answer('Основні реквізити ПТ "ПЕНТАДА ТРАНС".')
    requisits_info = "\n".join(
        [
            '<b>ПТ «ПЕНТАДА ТРАНС»</b>',
            '',
            '04080, Україна, м. Київ',
            'вул. Хвойки Вікентія, буд. 21, офіс 360',
            'код ЄДРПОУ 36701373',
            'ІПН 367013726544',
            '',
            'П/Р: UA693808050000000026006586065',
            'БАНК: АТ «Райффайзен Банк Аваль»',
            'МФО: 380805',
            'П/Р: UA043005060000026006001053834',
            'БАНК: АТ «ПЕРШИЙ ІНВЕСТИЦІЙНИЙ БАНК»',
            'МФО: 300506',
            '',
            'тел.: +38 (067) 447 60 66',
            'email: office@pentada-trans.com'
        ]
    )
    await call.message.answer(requisits_info)

@dp.callback_query_handler(text_contains="officials")
async def cabinet_officials(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer('👨‍💻 <b>КОНТАКТНІ ОСОБИ</b>')
    await call.message.answer('Контактні особи ПТ "ПЕНТАДА ТРАНС", уповноважені на обмін інформацією та документами з клієнтом.')
    officials_contacts = "\n".join(
        [
            'Морев Олексій Геннадійович, заступник директора',
            '☎️ +380674769791',
            '📧 agmorev@pentada-trans.com;',
            '',
            'Бабайцева Вероніка Ігорівна, заступник директора',
            '☎️ +380674475467',
            '📧 bvi@pentada-trans.com;',
            '',
            'Тараненко Світлана Олександрівна, головний бухгалтер',
            '☎️ +380671657517',
            '📧 fin@pentada-trans.com;',
            '',
            'Кузнецов Андрій Петрович, начальник відділу логістики та гарантування',
            '☎️ +380674769780',
            '📧 akuznetsov@pentada-trans.com;',
            '',
            'Менеджери з логістики та гарантування (оператори) - 24/7',
            '☎️ +380674476066',
            '📧 zayavka_gd@pentada-trans.com.'
        ]
    )
    await call.message.answer(officials_contacts)