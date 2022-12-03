from aiogram.dispatcher.filters.state import StatesGroup, State



class Signin(StatesGroup):
    company_state = State()
    name_state = State()
    email_state = State()