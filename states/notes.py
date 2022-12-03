from aiogram.dispatcher.filters.state import StatesGroup, State



class Telesend(StatesGroup):
    message_state = State()


class Usersend(StatesGroup):
    userid_state = State()
    message_state = State()