from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


login_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔐 Увійти...", callback_data='login'),
        ],
        [
            InlineKeyboardButton(text="📄 Заявка на підключення", callback_data='signin'),
        ],
    ],
)

client_cabinet_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📑 Заявки", callback_data='orders'),
        ],
        [
            InlineKeyboardButton(text="📊 Звіти", callback_data='reports'),
        ],
        [
            InlineKeyboardButton(text="🏦 Реквізити гаранта", callback_data='requisits'),
        ],
        [
            InlineKeyboardButton(text="👨‍💻 Контактні особи", callback_data='officials'),
        ],
    ],
)

order_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📝 Оформити заявку онлайн", url='https://docs.google.com/forms/d/e/1FAIpQLSfGdRHW5FzDVcPqTCnwVkKf57ryfD3llzfqnDbcWTThDU3eSQ/viewform?usp=sf_link'),
        ],
        [
            InlineKeyboardButton(text="📥 Завантажити бланк заявки", callback_data='order_download'),
        ],
        [
            InlineKeyboardButton(text="📤 Відправити готову заявку", callback_data='order_send'),
        ],
    ],
)

client_report_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📑 Перевірити статус декларації", url='https://cabinet.customs.gov.ua/ccdcheck'),
        ],
        [
            InlineKeyboardButton(text="📈 2021", callback_data='report_2021'),
            InlineKeyboardButton(text="📊 2022", callback_data='report_2022'),
        ],
        [
            InlineKeyboardButton(text="🧾 Поточний місяць", callback_data='report_month'),
        ],
        [
            InlineKeyboardButton(text="🧾 Минула доба", callback_data='report_yesterday'),
            InlineKeyboardButton(text="🧾 Поточна доба", callback_data='report_today'),
        ],
    ],
)

# CABINET ADMIN MARKUP
admin_cabinet_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📑 Заявки", callback_data='orders'),
            InlineKeyboardButton(text="📊 Звіти", callback_data='reports'),
        ],
        [
            InlineKeyboardButton(text="🪤 Ризики 🛠", callback_data='risks'),
        ],
        [
            InlineKeyboardButton(text="🗂 Інформація з ЄДР", callback_data='edr_info')
        ],
        [
            InlineKeyboardButton(text="📨 Розсилки", callback_data='notifications'),
        ],
        [
            InlineKeyboardButton(text="🏦 Реквізити гаранта", callback_data='requisits'),
        ],
        [
            InlineKeyboardButton(text="👨‍💻 Контактні особи", callback_data='officials'),
        ],
    ],
)

admin_report_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📑 Перевірити статус декларації", url='https://cabinet.customs.gov.ua/ccdcheck'),
        ],
        [
            InlineKeyboardButton(text="⚠️ Одночасно видані гарантії", callback_data='report_simissued'),
        ],
        [
            InlineKeyboardButton(text="⌛️ Завершення терміну дії гарантій", callback_data='report_expiration'),
        ],
        [
            InlineKeyboardButton(text="📈 2021", callback_data='admin_report_2021'),
            InlineKeyboardButton(text="📊 2022", callback_data='admin_report_2022'),
        ],
        [
            InlineKeyboardButton(text="🧾 Поточний місяць", callback_data='admin_report_month'),
        ],
        [
            InlineKeyboardButton(text="🧾 Минула доба", callback_data='admin_report_yesterday'),
            InlineKeyboardButton(text="🧾 Поточна доба", callback_data='admin_report_today'),
        ],
    ],
)

admin_notifications_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📩 Направлення повідомлення", callback_data='usersend'),
        ],
        [
            InlineKeyboardButton(text="✉️ Розсилка користувачам бота", callback_data='telesend'),
        ],
        [
            InlineKeyboardButton(text="📧 Розсилка електронною поштою 🛠", callback_data='emailsend'),
        ],
    ],
)
