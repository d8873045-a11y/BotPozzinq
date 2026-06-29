from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    choosing_payment = State()
    waiting_for_message = State()


class AdminStates(StatesGroup):
    menu = State()
    editing_prices = State()
    editing_reviews_url = State()
    editing_promo_url = State()
