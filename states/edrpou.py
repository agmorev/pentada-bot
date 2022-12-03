from aiogram.dispatcher.filters.state import StatesGroup, State



class Edrpou(StatesGroup):
    edrpou_state = State()
    company_status = State()
    # details_state = State()