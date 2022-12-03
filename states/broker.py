from aiogram.dispatcher.filters.state import StatesGroup, State



class Broker(StatesGroup):
    broker_state = State()
    
    