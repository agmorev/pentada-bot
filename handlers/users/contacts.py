from aiogram import types
from loader import dp, bot


@dp.message_handler(text="☎️ Контакти")
async def bot_contacts(message: types.Message):
    address = "\n".join(
        [
            'ПОВНЕ ТОВАРИСТВО "ПЕНТАДА ТРАНС" ТОВ «ПЕНТАДА ГРУПП» І КОМПАНІЯ',
            'Код ЄДРПОУ: 36701373',
            '',
            'Юридична адреса:',
            '🗺 04080, м. Київ, вул. Хвойки Вікентія, 21, офіс 360'
        ]
    )
    phones = "\n".join(
        [
            'Оформлення фінансових гарантій (24/7):',
            '☎️ +38 (067) 447 60 66 (оператори)',
            '📧 zayavka_gd@pentada-trans.com',
            '',
            'Інші питання:',
            '☎️ +38 (067) 476 97 80',
            '☎️ +38 (067) 476 97 91',
            '☎️ +38 (067) 321 36 65',
            '📧 office@pentada-trans.com',
            '',
            'Наша веб-сторінка:',
            '💻 http://www.pentada-trans.com/',
            '',
            'Ми в соцмережах:',
            'Facebook: https://www.facebook.com/pentadatrans/',
            
        ]
    )
    await message.answer('<b>КОНТАКТНА ІНФОРМАЦІЯ</b>')
    await message.answer(address)
    await message.answer_location(50.4854543,30.4863925)
    await message.answer(phones)