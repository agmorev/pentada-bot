from aiogram import types
from loader import dp
from keyboards.inline import info_markup, edr_markup
import datetime
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.storage import FSMContext
import feedparser
import requests
import json
import pandas as pd
import re
from states.edrpou import Edrpou
from states.zed import Zed
from states.broker import Broker
import sqlite3


@dp.message_handler(text="ℹ️ Інфо")
async def bot_info(message: types.Message):
    await message.answer('<b>ІНФОРМАЦІЙНІ РЕСУРСИ</b>')
    await message.answer('Новини в митній сфері, зміни в митному законодавстві, законодавство з питань фінансових гарантій, митні класифікатори та сторонні ресурси',
                         reply_markup=info_markup)

@dp.callback_query_handler(text_contains="news")
async def info_news(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer('📰 <b>МИТНІ НОВИНИ</b>')
    await call.message.answer('Останні новини в митній сфері, зміни в митному законодавстві, контрабанда та порушення митних правил')
    url = 'http://www.qdpro.com.ua/rss'
    posts = feedparser.parse(url)
    posts.entries = sorted(list(posts.entries)[:10], key=lambda k: k['published'])
    for entry in posts.entries:
        link_markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="📖 Читати далі...", url=entry['link']),
                ],
            ],
        )
        fdate = datetime.datetime.strptime(entry.get('published'), '%a, %d %b %Y %H:%M:%S %z').strftime('%d.%m.%Y %H:%M')
        await call.message.answer(entry['title']+'|'+fdate, reply_markup=link_markup)

@dp.callback_query_handler(text_contains="laws")
async def info_laws(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer('⚖️ <b>ЗАКОНОДАВСТВО</b>')
    await call.message.answer('Нормативно-правові акти з питань фінансових гарантій')
    link_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📖 Читати далі...", url='https://zakon.rada.gov.ua/laws/show/4495-17#n2535'),
            ],
        ],
    )
    await call.message.answer('1️⃣ Митний кодекс України | № 4495-VI, 13.03.2012, Кодекс, Верховна Рада України', reply_markup=link_markup)
    link_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📖 Читати далі...", url='https://zakon.rada.gov.ua/laws/show/461-2012-%D0%BF#Text'),
            ],
        ],
    )
    await call.message.answer('2️⃣ Про затвердження переліку товарів, ввезення яких на митну територію України та/або переміщення територією України прохідним та внутрішнім транзитом здійснюється за умови обов’язкового надання митним органам забезпечення сплати митних платежів | №461, 21.05.2012, Постанова, Кабінет Міністрів України', reply_markup=link_markup)
    link_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📖 Читати далі...", url='https://zakon.rada.gov.ua/laws/show/z0860-20#Text'),
            ],
        ],
    )
    await call.message.answer('3️⃣ Про затвердження форм бланків фінансових гарантій та порядку їх заповнення | №404, 07.07.2020, Наказ, Міністерство фінансів України', reply_markup=link_markup)
    link_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📖 Читати далі...", url='https://zakon.rada.gov.ua/laws/show/390-2013-%D0%BF#Text'),
            ],
        ],
    )
    await call.message.answer('4️⃣ Про визначення пунктів пропуску через державний кордон України, через які здійснюється переміщення підакцизних товарів, та визнання такими, що втратили чинність, деяких актів Кабінету Міністрів України | №390, 29.05.2013, Постанова, Кабінет Міністрів України', reply_markup=link_markup)
    link_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📖 Читати далі...", url='https://zakon.rada.gov.ua/laws/show/85-2018-%D0%BF#Text'),
            ],
        ],
    )
    await call.message.answer('5️⃣ Про затвердження Порядку надання розстрочення сплати податку на додану вартість та застосування забезпечення виконання зобов’язань під час ввезення на митну територію України обладнання для власного виробництва на території України | №85, 07.02.2018, Постанова, Кабінет Міністрів України', reply_markup=link_markup)

@dp.callback_query_handler(text_contains="termins")
async def info_termins(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer('🔠 <b>ТЕРМІНОЛОГІЯ</b>')
    await call.message.answer('Термінологічний словник з питань фінансових гарантій')
    await call.message.answer('''1️⃣ <u>Гарант (незалежний фінансовий посередник)</u> – юридична особа, створена відповідно до законодавства України та внесена до Реєстру гарантів, діє на підставі Митного кодексу України та Угоди про надання фінансових гарантій з Держмитслужбою та має право на видачу фінансових гарантій митним органам.''')
    await call.message.answer('''2️⃣ <u>Фінансова гарантія</u> є безвідкличним зобов’язанням гаранта, внесеного до реєстру гарантів, виплатити на вимогу митного органу кошти в межах певної суми у разі невиконання забезпечених цією гарантією зобов’язань із сплати митних платежів.''')
    await call.message.answer('''3️⃣ <u>Індивідуальна фінансова гарантія</u> надається у паперовому або електронному вигляді на суму митних платежів за:
1) однією митною декларацією в межах однієї зовнішньоторговельної операції;
2) однією митною декларацією в межах однієї транзитної операції;
3) одним документом контролю за переміщенням товарів;
4) однією операцією з переміщення через митний кордон України товарів громадянами у випадках, визначених розділом XII Митного кодексу України.''')
    await call.message.answer('''4️⃣ <u>Багаторазова фінансова гарантія</u> надається для забезпечення сплати митних платежів за кількома митними деклараціями або документами контролю за переміщенням товарів при ввезенні товарів на митну територію України з метою транзиту або для вільного обігу на цій території для одного власника в рамках одного зовнішньоекономічного договору.''')
    await call.message.answer('''5️⃣ <u>Загальна фінансова гарантія</u> використовується для забезпечення сплати митних платежів за кількома зобов’язаннями АЕО, що випливають з митних процедур відповідно до Митного кодексу України у будь-якій митниці на всій митній території України незалежно від митного режиму.''')
    await call.message.answer('''6️⃣ <u>Гарантійний випадок</u> – факт невиконання особою, відповідальною за сплату митних платежів, зобов’язань, забезпечених фінансовою гарантією, що випливають з митних процедур, у зв’язку з настанням якого гарант зобов’язується сплатити митному органу кошти в сумі митних платежів за відповідною фінансовою гарантією.''')

@dp.callback_query_handler(text_contains="edrpou")
async def edr_request(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer('💶 <b>ІНФОРМАЦІЯ ПРО КОНТРАГЕНТА</b>')
    await call.message.answer('⚠️Пошук інформації про юридичну особу або фізичну особу-підприємця за кодом ЄДРПОУ (8 знаків) або назвою')
    await call.message.answer('👨‍💻 Введіть код або назву особи:')
    await Edrpou.edrpou_state.set()

@dp.message_handler(state=Edrpou.edrpou_state)
async def select_status(message: types.Message, state: FSMContext):
    await state.update_data(q=message.text)

    # Save record about user to database
    userid = message.from_user.id
    fullname = message.from_user.full_name
    q = message.text
    date = datetime.datetime.now()
    try:
        conn = sqlite3.connect('/home/agmorev/pentadabot_v2/data/pentada.db')
        cursor = conn.cursor()
        print("EDR service successfully connected to SQLite | ", fullname, ' | ', date)
        query3 = "INSERT INTO edrpou ('userid', 'fullname', 'q', 'date') VALUES (?, ?, ?, ?);"
        variables = (userid, fullname, q, date)
        cursor.execute(query3, variables)
        conn.commit()
        print("Record inserted successfully into calcs table ", cursor.rowcount)
        print(userid, fullname, q, date)
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if (conn):
            conn.close()
            print("The SQLite connection is closed")

    await message.answer("Оберіть статус підприємства", reply_markup=edr_markup)
    await Edrpou.next()

@dp.callback_query_handler(text=['stopped', 'registered', 'stopping', 'bankruptcy', 'invalid', 'sanitation', 'canceled', 'all'], state=Edrpou.company_status)
async def answer_status(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    query = await state.get_data()
    q = query.get("q")
    response = requests.get('https://e-data.com.ua/api/v1/search/data/?search={}'.format(q))
    data = json.loads(response.text)
    print(list(data.values()).count('припинено'))
    if call.data == 'stopped':
        response = requests.get('https://e-data.com.ua/api/v1/search/data/?search={}&state[]=1'.format(q))
    elif call.data == 'registered':
        response = requests.get('https://e-data.com.ua/api/v1/search/data/?search={}&state[]=2'.format(q))
    elif call.data == 'stopping':
        response = requests.get('https://e-data.com.ua/api/v1/search/data/?search={}&state[]=3'.format(q))
    elif call.data == 'bankruptcy':
        response = requests.get('https://e-data.com.ua/api/v1/search/data/?search={}&state[]=4'.format(q))
    elif call.data == 'invalid':
        response = requests.get('https://e-data.com.ua/api/v1/search/data/?search={}&state[]=5'.format(q))
    elif call.data == 'sanitation':
        response = requests.get('https://e-data.com.ua/api/v1/search/data/?search={}&state[]=6'.format(q))
    elif call.data == 'canceled':
        response = requests.get('https://e-data.com.ua/api/v1/search/data/?search={}&state[]=7'.format(q))
    elif call.data == 'all':
        response = requests.get('https://e-data.com.ua/api/v1/search/data/?search={}'.format(q))

    data = json.loads(response.text)


    try:
        for fop in range(len(data['data']['fops'])):
            try:
                fop_id = data['data']['fops'][fop]['id']
                fop_name = data['data']['fops'][fop]['name']
                fop_address = data['data']['fops'][fop]['address']
                fop_state_name = data['data']['fops'][fop]['state_name']
                fop_reg_date = data['data']['fops'][fop]['reg_date']
                fop_link_markup = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text="📑 Деталі...", callback_data="fop_details_"+fop_id),
                        ],
                    ],
                )
                await call.message.answer('*Назва:* {}\n*Статус:* {}\n*Адреса:* {}\n*Дата реєстрації:* {}\n'.format(fop_name, fop_state_name, fop_address, fop_reg_date), reply_markup=fop_link_markup, parse_mode="Markdown")
            except:
                continue

        for uo in range(len(data['data']['uos'])):
            try:
                try:
                    uo_id = data['data']['uos'][uo]['id']
                except:
                    uo_id = data['data']['uos'][uo]['uo_id']
                try:
                    uo_name = data['data']['uos'][uo]['name']
                except:
                    uo_name = data['data']['uos'][uo]['uo_name']
                try:
                    uo_edrpou = data['data']['uos'][uo]['edrpou']
                except:
                    uo_edrpou = data['data']['uos'][uo]['uo_edrpou']
                try:
                    uo_address = data['data']['uos'][uo]['address']
                except:
                    uo_address = data['data']['uos'][uo]['uo_address']
                uo_state_name = data['data']['uos'][uo]['state_name']
                try:
                    uo_reg_date = data['data']['uos'][uo]['reg_date']
                except:
                    uo_reg_date = data['data']['uos'][uo]['uo_reg_date']
                uo_link_markup = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text="📑 Деталі...", callback_data="uo_details_"+uo_id),
                        ],
                    ],
                )
                await call.message.answer('*Назва:* {}\n*Статус:* {}\n*ЄДРПОУ:* {}\n*Адреса:* {}\n*Дата реєстрації:* {}'.format(uo_name, uo_state_name, uo_edrpou, uo_address, uo_reg_date), reply_markup=uo_link_markup, parse_mode="Markdown")
            except:
                continue
    except:
        await call.message.answer('🚫 В Єдиному державному реєстрі *відсутні записи* за вказаним запитом!!!', parse_mode="Markdown")
    await state.finish()

@dp.callback_query_handler(text_contains="details_")
async def edr_details(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    if call.data.startswith("fop_details_"):
        c_id = call.data[12:]
        res = requests.get('https://e-data.com.ua/api/v1/fop/data/{}'.format(c_id))
        data = json.loads(res.text)
        c_name = data['data']['name']
        c_address = data['data']['address']
        c_state_name = data['data']['state_name']
        c_reg_date = data['data']['reg_date']
        c_reg_num = data['data']['reg_num']
        c_contacts = data['data']['contacts']
        c_activity = data['data']['activity_kinds']
        await call.message.answer('*ЗАГАЛЬНА ІНФОРМАЦІЯ:*', parse_mode="Markdown")
        await call.message.answer('*Назва:* {}\n*Статус:* {}\n*Адреса:* {}\n*Дата реєстрації:* {}\n*Номер реєстрації:* {}\n*Контакти:* {}'.format(c_name, c_state_name, c_address, c_reg_date, c_reg_num, c_contacts), parse_mode="Markdown")
        await call.message.answer('*ВИДИ ДІЯЛЬНОСТІ:*', parse_mode="Markdown")
        for i in range(len(c_activity)):
            activity_code = data['data']['activity_kinds'][i]['code']
            activity_name = data['data']['activity_kinds'][i]['name']
            await call.message.answer('*{}* - {}'.format(activity_code, activity_name), parse_mode="Markdown")
    if call.data.startswith("uo_details_"):
        c_id = call.data[11:]
        res = requests.get('https://e-data.com.ua/api/v1/uo/data/{}'.format(c_id))
        data = json.loads(res.text)
        c_name = data['data']['name']
        c_state_name = data['data']['state_name']
        c_edrpou = data['data']['edrpou']
        c_address = data['data']['address']
        c_management = data['data']['superior_management']
        c_authorized_capital = data['data']['authorized_capital']
        c_reg_date = data['data']['reg_date']
        c_reg_num = data['data']['reg_num']
        c_authority_name = data['data']['authority_name']
        c_contacts = data['data']['contacts']
        await call.message.answer('*ЗАГАЛЬНА ІНФОРМАЦІЯ:*', parse_mode="Markdown")
        await call.message.answer('*Назва:* {}\n*Статус:* {}\n*ЄДРПОУ:* {}\n*Адреса:* {}\n*Органи управління:* {}\n*Статутний капітал:* {}\n*Дата реєстрації:* {}\n*Номер реєстрації:* {}\n*Орган реєстрації:* {}\n*Контакти:* {}'.format(c_name, c_state_name, c_edrpou, c_address, c_management, c_authorized_capital, c_reg_date, c_reg_num, c_authority_name, c_contacts), parse_mode="Markdown")

        await call.message.answer('*ЗАСНОВНИКИ:*', parse_mode="Markdown")
        for f in range(len(data['data']['founders'])):
            founders = data['data']['founders'][f]
            await call.message.answer('{}'.format(founders), parse_mode="Markdown")

        await call.message.answer('*БЕНЕФІЦІАРИ:*', parse_mode="Markdown")
        for b in range(len(data['data']['beneficiaries'])):
            beneficiaries = data['data']['beneficiaries'][b]
            await call.message.answer('{}'.format(beneficiaries), parse_mode="Markdown")

        await call.message.answer('*КЕРІВНИКИ:*', parse_mode="Markdown")
        for s in range(len(data['data']['singers'])):
            signers = data['data']['singers'][s]
            await call.message.answer('{}'.format(signers), parse_mode="Markdown")

        await call.message.answer('*ВИДИ ДІЯЛЬНОСТІ:*', parse_mode="Markdown")
        for i in range(len(data['data']['activity_kinds'])):
            activity_code = data['data']['activity_kinds'][i]['code']
            activity_name = data['data']['activity_kinds'][i]['name']
            await call.message.answer('*{}* - {}'.format(activity_code, activity_name), parse_mode="Markdown")


@dp.callback_query_handler(text_contains="zed")
async def zed_request(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer("🗄 <b>ІНФОРМАЦІЯ ПРО СУБ'ЄКТА ЗЕД</b>")
    await call.message.answer('⚠️Перевірка за ідентифікаційним кодом або назвою')
    await call.message.answer('👨‍💻 Введіть код або назву особи:')
    await Zed.zed_state.set()

@dp.message_handler(state=Zed.zed_state)
async def zed_status(message: types.Message, state: FSMContext):
    q = message.text
    await state.update_data(q=message.text)
    doc = open('/home/agmorev/pentadabot_v2/data/waiting.mp4', 'rb')
    msg = await message.answer_animation(doc, caption='Зачекайте...')

    # Save record about user to database
    userid = message.from_user.id
    fullname = message.from_user.full_name
    date = datetime.datetime.now()
    try:
        conn = sqlite3.connect('/home/agmorev/pentadabot_v2/data/pentada.db')
        cursor = conn.cursor()
        print("ZED service successfully connected to SQLite | ", fullname, ' | ', date)
        query3 = "INSERT INTO zedcoms ('userid', 'fullname', 'q', 'date') VALUES (?, ?, ?, ?);"
        variables = (userid, fullname, q, date)
        cursor.execute(query3, variables)
        conn.commit()
        print("Record inserted successfully into zedcoms table ", cursor.rowcount)
        print(userid, fullname, q, date)
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if (conn):
            conn.close()
            print("The SQLite connection is closed")

    conn = sqlite3.connect('/home/agmorev/pentadabot_v2/data/companies.db')
    df = pd.read_sql('SELECT * FROM companies WHERE CODE="{}" OR NAME LIKE "%{}%"'.format(q, q.upper()), conn)
    if len(df) == 0:
        await message.answer("🚫 В реєстрі суб'єктів ЗЕД *відсутні записи* за вказаним запитом!!!", parse_mode="Markdown")
    else:
        for index, row in df.iterrows():
            try:
                zed_name = row['NAME']
            except:
                zed_name = ''
            try:
                zed_edrpou = int(row['CODE'])
            except:
                zed_edrpou = ''
            try:
                zed_address = row['ADDRESS']
            except:
                zed_address = ''
            try:
                zed_code = row['ZED_CODE']
            except:
                zed_code = ''
            try:
                zed_reg_date = datetime.datetime.strptime(row['REG_DATE'], '%Y-%m-%d %H:%M:%S').strftime("%d.%m.%Y")
            except:
                zed_reg_date = ''
            try:
                zed_stop = datetime.datetime.strptime(row['DEL_DATE'], '%Y-%m-%d %H:%M:%S').strftime("%d.%m.%Y")
            except:
                zed_stop = ''
            await message.answer('*Назва:* {}\n*ЄДРПОУ:* {}\n*Адреса:* {}\n*Обліковий номер:* {}\n*Дата обліку:* {}\n*Анульовано:* {}\n'.format(zed_name, str(zed_edrpou), zed_address, zed_code, zed_reg_date, zed_stop), parse_mode="Markdown")

    await msg.delete()
    await state.finish()


@dp.callback_query_handler(text_contains="broker")
async def broker_request(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer("🗃 <b>ІНФОРМАЦІЯ ПРО МИТНОГО БРОКЕРА</b>")
    await call.message.answer('⚠️Перевірка за ідентифікаційним кодом або назвою')
    await call.message.answer('👨‍💻 Введіть код або назву особи:')
    await Broker.broker_state.set()

@dp.message_handler(state=Broker.broker_state)
async def broker_status(message: types.Message, state: FSMContext):
    q = message.text
    await state.update_data(q=message.text)
    doc = open('/home/agmorev/pentadabot_v2/data/waiting.mp4', 'rb')
    msg = await message.answer_animation(doc, caption='Зачекайте...')

    # Save record about user to database
    userid = message.from_user.id
    fullname = message.from_user.full_name
    date = datetime.datetime.now()
    try:
        conn = sqlite3.connect('/home/agmorev/pentadabot_v2/data/pentada.db')
        cursor = conn.cursor()
        print("BROKER service successfully connected to SQLite | ", fullname, ' | ', date)
        query3 = "INSERT INTO brokers ('userid', 'fullname', 'q', 'date') VALUES (?, ?, ?, ?);"
        variables = (userid, fullname, q, date)
        cursor.execute(query3, variables)
        conn.commit()
        print("Record inserted successfully into brokers table ", cursor.rowcount)
        print(userid, fullname, q, date)
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if (conn):
            conn.close()
            print("The SQLite connection is closed")

    conn = sqlite3.connect('/home/agmorev/pentadabot_v2/data/brokers.db')
    df = pd.read_sql('SELECT * FROM brokers WHERE CODE="{}" OR NAME LIKE "%{}%"'.format(q, q.upper()), conn)

    if len(df) == 0:
        await message.answer("🚫 В реєстрі митних брокерів *відсутні записи* за вказаним запитом!!!", parse_mode="Markdown")
    else:
        for index, row in df.iterrows():
            try:
                broker_name = row['NAME']
            except:
                broker_name = ''
            try:
                broker_edrpou = row['CODE']
            except:
                broker_edrpou = ''
            try:
                broker_address = row['ADDRESS']
            except:
                broker_address = ''
            try:
                broker_code = row['NUMBER']
            except:
                broker_code = ''
            try:
                broker_reg_date = datetime.datetime.strptime(row['DATE'], '%Y-%m-%d %H:%M:%S').strftime("%d.%m.%Y")
            except:
                broker_reg_date = ''
            try:
                broker_stop = row['NOTE']
            except:
                broker_stop = ''
            await message.answer('*Назва:* {}\n*ЄДРПОУ:* {}\n*Адреса:* {}\n*Серія, номер дозволу:* {}\n*Дата надання дозволу:* {}\n*Примітки:* {}\n'.format(broker_name, broker_edrpou, broker_address, broker_code, broker_reg_date, broker_stop), parse_mode="Markdown")
    await msg.delete()
    await state.finish()