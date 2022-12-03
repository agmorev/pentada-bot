from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

represent_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🗺 Мапа митної інфраструктури", url='https://map.customs.gov.ua/?locationTypes=1'),
        ],
        [
            InlineKeyboardButton(text="⏱ Час очікування в пунктах пропуску", url='https://dpsu.gov.ua/ua/map/'),
        ],
        [
            InlineKeyboardButton(text="🇵🇱 Польща", callback_data='represent_pl'),
            InlineKeyboardButton(text="🇸🇰 Словаччина", callback_data='represent_sk'),
            InlineKeyboardButton(text="🇭🇺 Угорщина", callback_data='represent_hu'),
        ],
        [
            InlineKeyboardButton(text="🇷🇴 Румунія", callback_data='represent_ro'),
            InlineKeyboardButton(text="🇲🇩 Молдова", callback_data='represent_md'),
            InlineKeyboardButton(text="🇧🇾 Білорусь", callback_data='represent_by'),
        ],
        [
            InlineKeyboardButton(text="🇷🇺 Росія", callback_data='represent_ru'),
            InlineKeyboardButton(text="🚢 Морські", callback_data='represent_sea'),
            InlineKeyboardButton(text="🛩 Повітряні", callback_data='represent_air'),
        ],
    ],
)