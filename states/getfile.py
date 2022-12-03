from aiogram.dispatcher.filters.state import StatesGroup, State



class Getfile(StatesGroup):
    load_state = State()


class GetEdrFile(StatesGroup):
    load_state = State()
