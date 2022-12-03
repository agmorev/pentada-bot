from utils.set_bot_commands import set_default_commands

import os
from loader import bot
from data import config
import logging

logging.basicConfig(level=logging.INFO)

async def on_shutdown(dp):
    logging.info(dp)

async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await set_default_commands(dp)

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)



# from aiogram.utils.executor import start_webhook
# from loader import bot
# from data.config import WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT
# # from loader import SSL_CERTIFICATE, ssl_context, bot
# from utils.set_bot_commands import set_default_commands


# async def on_startup(dp):
#     await bot.set_webhook(
#         url=WEBHOOK_URL
#         # certificate=SSL_CERTIFICATE
#     )
#     import filters
#     import middlewares
#     filters.setup(dp)
#     middlewares.setup(dp)

#     from utils.notify_admins import on_startup_notify
#     await on_startup_notify(dp)
#     await set_default_commands(dp)


# if __name__ == '__main__':
#     from handlers import dp

#     start_webhook(
#         dispatcher=dp,
#         webhook_path=WEBHOOK_PATH,
#         on_startup=on_startup,
#         skip_updates=True,
#         host=WEBAPP_HOST,
#         port=WEBAPP_PORT,
#         # ssl_context=ssl_context
#     )