from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="ℹ️ Інфо"),
            KeyboardButton(text="💼 Кабінет"),
        ],
        [
            KeyboardButton(text="🧮 Калькулятори"),
            KeyboardButton(text="🏪 Представники"),
        ],
        [
            KeyboardButton(text="🤝 Оферта"),
            KeyboardButton(text="☎️ Контакти"),
        ],
    ],
    resize_keyboard=True
)