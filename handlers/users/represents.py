from aiogram import types
from loader import dp, bot

from keyboards.inline import represent_markup


@dp.message_handler(text="🏪 Представники")
async def bot_represents(message: types.Message):
    await message.answer('<b>ПРЕДСТАВНИКИ НА КОРДОНІ</b>')
    await message.answer('Оберіть суміжну країну на кордоні, де знаходяться необхідні пункти пропуску''',
                         reply_markup=represent_markup)

@dp.callback_query_handler(text_contains="represent_pl")
async def poland_represents(call: types.CallbackQuery):
    poland = "\n".join(
        [
            '<u>🚚 <b>АВТОМОБІЛЬНІ ПУНКТИ</b></u>',
            '📌Ягодин – Дорогуск',
            '📌Краківець – Корчова',
            '📌Рава-Руська – Хребенне',
            '📌Шегині – Медика',
            '📌Устилуг – Зосін',
            '',
            '<u>🚂 <b>ЗАЛІЗНИЧНІ ПУНКТИ</b></u>',
            '📌Ягодин - Дорогуск (станція Ягодин)',
            '📌Володимир-Волинський - Хрубешув (станція Ізов)',
            '📌Рава-Руська - Хребенне, Верхрата (станція Рава-Руська)',
            '📌Мостиська - Пшемисль (станції Мостиська, Мостиська II)'
        ]
    )
    await call.answer(cache_time=60)
    await call.message.answer('🇵🇱 <b>ПОЛЬЩА</b>')
    await call.message.answer(poland)

@dp.callback_query_handler(text_contains="represent_sk")
async def slovakia_represents(call: types.CallbackQuery):
    slovakia = "\n".join(
        [
            '<u>🚚 <b>АВТОМОБІЛЬНІ ПУНКТИ</b></u>',
            '📌Ужгород – Вишнє-Нємецьке',
            '',
            '<u>🚂 <b>ЗАЛІЗНИЧНІ ПУНКТИ</b></u>',
            '📌Чоп - Чієрна над Тисою (станція Чоп)',
            '📌Павлове - Матьовце (станція Ужгород)'
        ]
    )
    await call.answer(cache_time=60)
    await call.message.answer('🇸🇰 <b>СЛОВАЧЧИНА</b>')
    await call.message.answer(slovakia)

@dp.callback_query_handler(text_contains="represent_hu")
async def hungary_represents(call: types.CallbackQuery):
    hungary = "\n".join(
        [
            '<u>🚚 <b>АВТОМОБІЛЬНІ ПУНКТИ</b></u>',
            '📌Чоп – Захонь (Chop – Zahon)',
            '',
            '<u>🚂 <b>ЗАЛІЗНИЧНІ ПУНКТИ</b></u>',
            '📌Чоп - Захонь (станція Чоп)',
            '📌Соловка - Еперєшке (станція Батєве)'
        ]
    )
    await call.answer(cache_time=60)
    await call.message.answer('🇭🇺 <b>УГОРЩИНА</b>')
    await call.message.answer(hungary)

@dp.callback_query_handler(text_contains="represent_ro")
async def romania_represents(call: types.CallbackQuery):
    romania = "\n".join(
        [
            '<u>🚚 <b>АВТОМОБІЛЬНІ ПУНКТИ</b></u>',
            '📌Порубне – Сірет',
            '📌Дякове – Халмеу',
            '',
            '<u>🚂 <b>ЗАЛІЗНИЧНІ ПУНКТИ</b></u>',
            '📌Вадул-Сірет - Вікшани (станція Вадул-Сірет)',
            '📌Дякове - Халмеу (станція Дякове)'
        ]
    )
    await call.answer(cache_time=60)
    await call.message.answer('🇷🇴 <b>РУМУНІЯ</b>')
    await call.message.answer(romania)

@dp.callback_query_handler(text_contains="represent_md")
async def moldova_represents(call: types.CallbackQuery):
    moldova = "\n".join(
        [
            '<u>🚚 <b>АВТОМОБІЛЬНІ ПУНКТИ</b></u>',
            '📌Могилів-Подільский – Отач',
            '📌Маяки – Удобне – Паланки',
            '📌Платонове – Гоянул Ноу',
            '📌Кучурган – Первомайськ',
            '📌Старокозаче – Тудора',
            '📌Рені – Джюрджюлешть',
            '📌Сокиряни – Окниця',
            '📌Кельменці – Ларга)',
            '📌Россошани – Брічень)',
            '📌Мамалига – Крива',
            '',
            '<u>🚂 <b>ЗАЛІЗНИЧНІ ПУНКТИ</b></u>',
            '📌Могилів-Подільский – Волчинець (станція Могилів-Подільский)',
            '📌Кучурган - Новосавицьке (станція Кучурган)',
            '📌Рені - Джюрджюлешть (станція Рені)',
            '📌Мамалига - Крива (станція Мамалига)',
            '📌Кельменці - Ларга (станція Ларга)',
            '📌Сокиряни - Окниця (станція Сокиряни)',
            '📌Слобідка - Кобасна (станція Слобідка)'
        ]
    )
    await call.answer(cache_time=60)
    await call.message.answer('🇲🇩 <b>МОЛДОВА</b>')
    await call.message.answer(moldova)

@dp.callback_query_handler(text_contains="represent_by")
async def belorus_represents(call: types.CallbackQuery):
    belorus = "\n".join(
        [
            '<u>🚚 <b>АВТОМОБІЛЬНІ ПУНКТИ</b></u>',
            '📌Доманове – Мокрани',
            '📌Виступовичі – Нова Рудня',
            '📌Нові Яриловичі – Нова Гута',
            '📌Городище – Верхній Теребежів',
            '',
            '<u>🚂 <b>ЗАЛІЗНИЧНІ ПУНКТИ</b></u>',
            '📌Горностаївка - Терюха (пункт контролю на станції Чернігів)',
            '📌Удрицьк - Горинь (пункт контролю на станції Сарни)',
            '📌Виступовичі - Словечно (пункт контролю на станції Коростень)',
            '📌Заболоття - Хотислав (пункт контролю на станції Ковель)',
            '📌Щорс - Терехівка (пункт контролю на станції Щорс)'
        ]
    )
    await call.answer(cache_time=60)
    await call.message.answer('🇧🇾 <b>БІЛОРУСЬ</b>')
    await call.message.answer(belorus)

@dp.callback_query_handler(text_contains="represent_ru")
async def russia_represents(call: types.CallbackQuery):
    russia = "\n".join(
        [
            '<u>🚚 <b>АВТОМОБІЛЬНІ ПУНКТИ</b></u>',
            '📌Грем’яч – Погар',
            '📌Сеньківка – Нові Юрковичі/Веселівка',
            '📌Бачівськ – Троєборне',
            '📌Юнакіївка – Суджа',
            '📌Танюшівка – Ровеньки',
            '📌Просяне – Бугайовка',
            '',
            '<u>🚂 <b>ЗАЛІЗНИЧНІ ПУНКТИ</b></u>',
            "📌Куп'янськ пункт контролю (станція Тополі)",
            '📌Хутір-Михайлівський пункт контролю (станція Зернове)',
            '📌Харків - Сортувальний пункт контролю (станція Козача Лопань)'
        ]
    )
    await call.answer(cache_time=60)
    await call.message.answer('🇷🇺 <b>РОСІЯ</b>')
    await call.message.answer(russia)

@dp.callback_query_handler(text_contains="represent_sea")
async def seaport_represents(call: types.CallbackQuery):
    seaport = "\n".join(
        [
            '⚓️Іллічівський морський торговельний порт',
            '⚓️Морський торговельний порт «Южний»',
            '⚓️Ренійський морський порт',
            '⚓️Дніпро-Бузький морський торговельний порт',
            '⚓️Спеціальний порт «Октябрьский»',
            '⚓️Одеський морський торговельний порт',
            '⚓️Ізмаїльський морський торговельний порт',
            '⚓️Миколаївський морський торговельний порт',
            '⚓️Миколаївський річковий порт',
            '⚓️Білгород-Дністровський морський торговельний порт',
            '⚓️Маріупольський морський торговельний порт',
            '⚓️Бердянський морський торговельний порт)',
            '⚓️Херсонський річковий порт',
            '⚓️Херсонський морський торговельний порт'
        ]
    )
    await call.answer(cache_time=60)
    await call.message.answer('🚢 <b>МОРСЬКІ ПУНКТИ</b>')
    await call.message.answer(seaport)

@dp.callback_query_handler(text_contains="represent_air")
async def airport_represents(call: types.CallbackQuery):
    airport = "\n".join(
        [
            '🛫Маріуполь – аеропорт',
            '🛫Донецьк – аеропорт',
            '🛫Рівне – аеропорт',
            '🛫Ужгород – аеропорт',
            '🛫Івано-Франківськ – аеропорт',
            '🛫Хмельницький – аеропорт',
            '🛫Одеса – аеропорт',
            '🛫Миколаїв – аеропорт',
            '🛫Аеропорт "Кульбакіне"',
            '🛫Запоріжжя – аеропорт',
            '🛫Дніпропетровськ – аеропорт',
            '🛫Кривий Ріг – аеропорт',
            '🛫Черкаси – аеропорт',
            '🛫Київ – аеропорт',
            '🛫Аеродром "Гостомель"',
            '🛫Бориспіль – аеропорт'
        ]
    )
    await call.answer(cache_time=60)
    await call.message.answer('✈️ <b>ПОВІТРЯНІ ПУНКТИ</b>')
    await call.message.answer(airport)