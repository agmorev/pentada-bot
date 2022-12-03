from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


info_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📰 Новини", callback_data='news'),
        ],
        [
            InlineKeyboardButton(text="⚖️ Законодавство", callback_data='laws'),
            InlineKeyboardButton(text="🔠 Термінологія", callback_data='termins'),
        ],
        [
            InlineKeyboardButton(text="📚 Документи ЗЕД", url='https://www.qdpro.com.ua/uk/export/catalogue'),
        ],
        [
            InlineKeyboardButton(text="🗂 УКТЗЕД", url='https://www.qdpro.com.ua/uk/export/uktzed'),
            InlineKeyboardButton(text="📗 Митний тариф", url='https://cabinet.customs.gov.ua/tnvinfo'),
        ],
        [
            InlineKeyboardButton(text="🏢 Митні органи", url='https://qdpro.com.ua/uk/direct/8'),
            InlineKeyboardButton(text="🗺 Митна мапа", url='https://map.customs.gov.ua/?locationTypes=1'),
        ],
        [
            InlineKeyboardButton(text="📊 Митна статистика", url='https://bi.customs.gov.ua/uk/trade/'),
        ],
        [
            InlineKeyboardButton(text="🔎 Інформація про контрагента", callback_data='edrpou'),
        ],
        [
            InlineKeyboardButton(text="🗄 Суб'єкти ЗЕД", callback_data='zed'),
            InlineKeyboardButton(text="🗃 Митні брокери", callback_data='broker'),
        ],
        [
            InlineKeyboardButton(text="💱 Курси валют", url='https://qdpro.com.ua/uk/export/nbulist'),
        ],
    ],
)

edr_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="❌ Припинено", callback_data='stopped'),
        ],
        [
            InlineKeyboardButton(text="✔️ Зареєстровано", callback_data='registered'),
        ],
        [
            InlineKeyboardButton(text="⭕️ В стані припинення", callback_data='stopping'),
        ],
        [
            InlineKeyboardButton(text="⚠️ Порушено справу про банкрутство", callback_data='bankruptcy'),
        ],
        [
            InlineKeyboardButton(text="🚫 Свідоцтво недійсне", callback_data='invalid'),
        ],
        [
            InlineKeyboardButton(text="🆘 В стані санації", callback_data='sanitation'),
        ],
        [
            InlineKeyboardButton(text="⛔️ Скасовано", callback_data='canceled'),
        ],
        [
            InlineKeyboardButton(text="💯 Всі", callback_data='all'),
        ],
    ],
)