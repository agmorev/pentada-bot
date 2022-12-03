from aiogram import types
from loader import dp, bot
from aiogram.types import ContentType


@dp.message_handler(content_types=ContentType.DOCUMENT)
async def load_file(message: types.Message):
    await message.document.download()
    order_fileid = message.document.file_id
    order_filename = message.document.file_name
    print(order_fileid)
    print(order_filename)

@dp.message_handler()
async def bot_echo(message: types.Message):
    await message.answer(message.text)