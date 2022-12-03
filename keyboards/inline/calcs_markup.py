from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

calcs_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💶 Вартість фінансової гарантії", callback_data='warranty_calc'),
        ],
        [
            InlineKeyboardButton(text="💵 Розрахунок митних платежів", url='https://qdpro.com.ua/uk/export/calc'),
        ],
        [
            InlineKeyboardButton(text="💵 Розрахунок митних платежів для авто", url='https://qdpro.com.ua/uk/export/calc/cars'),
        ],
        [
            InlineKeyboardButton(text="💵 Розрахунок митної вартості для авто", url='https://calc.customs.gov.ua'),
        ],
        [
            InlineKeyboardButton(text="💲 Показники митної вартості", callback_data='customs_value'),
        ],
    ],
)

vehicle_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🚚 Автомобільний", callback_data='auto'),
            InlineKeyboardButton(text="🚂 Залізничний", callback_data='railway'),
        ],
        [
            InlineKeyboardButton(text="🚢 Морський", callback_data='sea'),
            InlineKeyboardButton(text="⛽️ Трубопровідний", callback_data='pipeline'),
        ],
    ],
)