from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from states.wcalc import Warranty_calculation, Cvalue_calculation
from keyboards.inline import calcs_markup, vehicle_markup
import re
import datetime
import sqlite3
import pandas as pd


def wcalc_algorithm(vehicle, code, weight, value):
    wtotal = 0
    if vehicle == 'Автомобільний':
        if code == '2203' or code == '2204' or code == '2205' or code == '2206':
            if value <= 400000:
                wtotal = 500
            else:
                wtotal = value*0.05/100
            if wtotal < 500:
                wtotal = 500
        elif code == '2207' or code == '2208':
            wtotal = value*0.05/100
            if wtotal < 500:
                wtotal = 500
        elif value <= 50000:
            wtotal = 250
        elif (value > 50000) and (value <= 100000):
            wtotal = 250
        elif (value > 100000) and (value <= 200000):
            wtotal = 500
        elif (value > 200000) and (value <= 300000):
            wtotal = 500
        elif (value > 300000) and (value <= 500000):
            wtotal = 500
        elif (value > 500000) and (value <= 800000):
            wtotal = 500
        elif (value > 800000) and (value <= 1000000):
            wtotal = 500
        elif (value > 1000000) and (value <= 1500000):
            wtotal = value*0.05/100
        elif (value > 1500000) and (value <= 2000000):
            wtotal = value*0.05/100
        elif value > 2000000:
            wtotal = value*0.05/100
    if vehicle == 'Залізничний':
        usd = 26
        if code == '2710' or code == '2707':
            wtotal = weight/1000*0.3*usd
        elif code == '2711':
            wtotal = weight/1000*0.35*usd
        elif code == '2709' or code == '2905':
            wtotal = weight/1000*0.25*usd
        elif code == '2207' or '2208':
            wtotal = value*0.2/100
        elif code == '2204':
            wtotal = weight/1000*0.32*usd
        elif code == '3105':
            wtotal = weight/1000*0.25*usd
        elif code == '2909':
            wtotal = weight/1000*0.4*usd
        elif value <= 50000:
            wtotal = 450
        elif (value > 50000) and (value <= 100000):
            wtotal = 620
        elif (value > 100000) and (value <= 200000):
            wtotal = 1000
        elif (value > 200000) and (value <= 300000):
            wtotal = 1200
        elif (value > 300000) and (value <= 500000):
            wtotal = 1500
        elif (value > 500000) and (value <= 800000):
            wtotal = 1700
        elif (value > 800000) and (value <= 1000000):
            wtotal = 2100
        elif (value > 1000000) and (value <= 1500000):
            wtotal = 2800
        elif (value > 1500000) and (value <= 2000000):
            wtotal = 3300
        elif value > 2000000:
            wtotal = value*0.2/100
    if vehicle == 'Морський':
        wtotal = weight/1000*0.25*usd
    if vehicle == 'Трубопровідний':
        wtotal = weight/1000*0.35*usd
    return wtotal

@dp.message_handler(text="🧮 Калькулятори")
async def bot_represents(message: types.Message):
    await message.answer('<b>КАЛЬКУЛЯТОРИ</b>')
    await message.answer('Оберіть калькулятор для попереднього розрахунку''',
                         reply_markup=calcs_markup)


#Warranty calculation process
@dp.callback_query_handler(text_contains="warranty_calc")
async def warranty_calculator(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer('💶 <b>ВАРТІСТЬ ГАРАНТІЇ</b>')
    await call.message.answer('⚠️Для попереднього розрахунку вартості фінансової гарантії надайте послідовно відповіді на наступні 4 питання')
    await call.message.answer('1️⃣Оберіть вид транспортного засобу:', reply_markup=vehicle_markup)
    await Warranty_calculation.vehicle_state.set()

@dp.callback_query_handler(text=['auto', 'railway', 'sea', 'pipeline'], state=Warranty_calculation.vehicle_state)
async def answer_vehicle(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    if call.data == 'auto':
        vehicle = 'Автомобільний'
    elif call.data == 'railway':
        vehicle = 'Залізничний'
    elif call.data == 'sea':
        vehicle = 'Морський'
    elif call.data == 'pipeline':
        vehicle = 'Трубопровідний'
    await state.update_data(answer1=vehicle)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(vehicle)
    await call.message.answer("2️⃣Введіть код товару на рівні 4-х знаків:")
    await Warranty_calculation.next()

@dp.message_handler(state=Warranty_calculation.cncode_state)
async def answer_cncode(message: types.Message, state: FSMContext):
    if re.match(r'\d{4}', message.text) and len(message.text) == 4:
        cncode = message.text
        await state.update_data(answer2=cncode)
        await message.answer("3️⃣Введіть вагу товарів в кілограмах:")
        await Warranty_calculation.next()
    else:
        await message.answer('❗️Код товару має містити тільки перших 4 знаки (товарна позиція)!!! Очікую на коректний код товару...')

@dp.message_handler(state=Warranty_calculation.weight_state)
async def answer_weight(message: types.Message, state: FSMContext):
    if re.match(r'^[0-9]+$', message.text):
        weight = message.text
        await state.update_data(answer3=weight)
        await message.answer("4️⃣Введіть суму митних платежів:")
        await Warranty_calculation.next()
    else:
        await message.answer('❗️Вага товару має містити тільки цифри!!! Очікую на коректну вагу товару...')

@dp.message_handler(state=Warranty_calculation.value_state)
async def answer_value(message: types.Message, state: FSMContext):
    if re.match(r'^[0-9]+$', message.text):
        data = await state.get_data()
        vehicle = data.get("answer1")
        cncode = data.get("answer2")
        weight = data.get("answer3")
        value = message.text
        await state.update_data(answer4=value)
        price = str(float("{0:.2f}".format(wcalc_algorithm(vehicle,cncode,int(weight),int(value)))))
        result = 'Вид транспорту: '+str(vehicle)+'\nКод товару: '+str(cncode)+'\nВага товару: '+str(weight)+' кг\nСума платежів: '+str(value)+' грн\n-----------------------------------------------------\n<b>Вартість гарантії: '+price+' грн</b>'

        userid = message.from_user.id
        fullname = message.from_user.full_name
        date = datetime.datetime.now()
        try:
            conn = sqlite3.connect('/home/agmorev/pentadabot_v2/data/pentada.db')
            cursor = conn.cursor()
            print('---------------------CALCULATOR--------------------------')
            print("Calculator successfully connected to SQLite | ", fullname, ' | ', date)
            query2 = "INSERT INTO calcs ('userid', 'fullname', 'vehicle', 'code', 'weight', 'value', 'price', 'date') VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
            variables = (userid, fullname, vehicle, cncode, weight, value, price, date)
            cursor.execute(query2, variables)
            conn.commit()
            print("Record inserted successfully into calcs table ", cursor.rowcount)
            print(userid, fullname, vehicle, cncode, weight, value, price, date)
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if (conn):
                conn.close()
                print("The SQLite connection is closed")

        await message.answer('‼️ <b>Розрахунок є попереднім</b> ‼️\nОстаточну вартість буде узгоджено при укладанні договору з гарантом.')
        await message.answer(result)
        await state.finish()
    else:
        await message.answer('❗Сума митних платежів має бути цілим числом!!!!!! Очікую на коректну суму...')


#Customs value calculation process
@dp.callback_query_handler(text_contains="customs_value")
async def cvalue_calculator(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer('💲 <b>ПОКАЗНИКИ МИТНОЇ ВАРТОСТІ</b>')
    await call.message.answer('⚠️Розрахунок показників митної вартості за кодом товару та країною походження')
    await call.message.answer('👨‍💻 Введіть код товару (10 знаків):')
    await Cvalue_calculation.cncode_state.set()

@dp.message_handler(state=Cvalue_calculation.cncode_state)
async def cvalue_cncode(message: types.Message, state: FSMContext):
    if re.match(r'\d{10}', message.text) and len(message.text) == 10:
        cncode = message.text
        await state.update_data(answer1=cncode)
        await message.answer("👨‍💻Введіть країну походження у форматі скороченої назви (PL) або повної (Польща):")
        await Cvalue_calculation.next()
    else:
        await message.answer('❗️Код товару має містити 10 знаків!!! Очікую на коректний код товару...')

@dp.message_handler(state=Cvalue_calculation.country_state)
async def cvalue_country(message: types.Message, state: FSMContext):
    if re.match(r'^[A-ZА-я -]+$', message.text):
        doc = open('/home/agmorev/pentadabot_v2/data/waiting.mp4', 'rb')
        msg = await message.answer_animation(doc, caption='Зачекайте...')
        df = pd.read_excel('/home/agmorev/pentadabot_v2/data/cvalue.xlsx', sheet_name=0)
        country = message.text
        data = await state.get_data()
        cncode = data.get("answer1")
        df['Країна походження товару'] = df['Країна походження товару'].str.upper()
        try:
            cond = df[(df['Код УКТЗЕД Підкатегорія - 10 знаків'] == int(cncode)) & (df['Країна походження товару'].str.contains(country.upper()))]
            min_value = cond['Мінімальна митна вартість'].values[0]
            avr_value = cond['Середня митна вартість'].values[0]
            max_value = cond['Максимальна митна вартість'].values[0]
            result = '*Код товару:* '+str(cncode)+'\n*Країна походження:* '+str(country)+'\n*Мін. митна вартість:* '+str("{:.2f}".format(min_value))+'$\n*Сер. митна вартість:* '+str("{:.2f}".format(avr_value))+'$\n*Макс. митна вартість:* '+str("{:.2f}".format(max_value))+'$'
            await msg.delete()
            await message.answer('‼️ Розрахунок здійснено на підставі відкритих даних Держмитслужби')
            await message.answer(result, parse_mode='Markdown')
            await state.finish()
        except:
            await msg.delete()
            await message.answer('‼️ Запис за вказаним запитом не знайдено')
            await state.finish()

        userid = message.from_user.id
        fullname = message.from_user.full_name
        date = datetime.datetime.now()
        try:
            conn = sqlite3.connect('/home/agmorev/pentadabot_v2/data/pentada.db')
            # conn = sqlite3.connect('D:\PYTHON\PROJECTS\Bots\pentadabot_v2\data\pentada.db')
            cursor = conn.cursor()
            print("Customs value block successfully connected to SQLite | ", fullname, ' | ', date)
            query4 = "INSERT INTO cvalue ('userid', 'fullname', 'cncode', 'country', 'date') VALUES (?, ?, ?, ?, ?);"
            variables = (userid, fullname, cncode, country, date)
            cursor.execute(query4, variables)
            conn.commit()
            print("Record inserted successfully into cvalue table ", cursor.rowcount)
            print(userid, fullname, cncode, country, date)
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if (conn):
                conn.close()
                print("The SQLite connection is closed")

    else:
        await message.answer('❗️Очікую на коректне введення країни походження...')











#Customs payments calculation process
@dp.callback_query_handler(text_contains="payments_calc")
async def customs_calculator(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer('💵 <b>МИТНІ ПЛАТЕЖІ</b>')
    await call.message.answer('❗️Для попереднього розрахунку митних платежів заповніть наступну форму')