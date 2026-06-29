from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from config import BTN_PRICES, BTN_REVIEWS, BTN_ORDER, BTN_BACK


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=BTN_PRICES),
                KeyboardButton(text=BTN_REVIEWS),
            ],
            [
                KeyboardButton(text=BTN_ORDER),
            ],
        ],
        resize_keyboard=True,
        persistent=True,
    )


def back_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BTN_BACK)]],
        resize_keyboard=True,
    )


def payment_choice_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💳 Оплата через СБЕР")],
            [KeyboardButton(text="⭐ Оплата звёздами")],
            [KeyboardButton(text=BTN_BACK)],
        ],
        resize_keyboard=True,
    )


def stars_prices_kb(items: list[dict]) -> InlineKeyboardMarkup:
    from config import RUB_TO_STARS
    buttons = []
    for i, item in enumerate(items):
        stars = int(item["rub"] * RUB_TO_STARS)
        buttons.append([
            InlineKeyboardButton(
                text=f"{item['label']} — {stars} ⭐",
                callback_data=f"stars_buy:{i}",
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def admin_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✏️ Изменить прайсы", callback_data="admin:prices")],
            [InlineKeyboardButton(text="🔗 Ссылка на отзывы", callback_data="admin:reviews_url")],
            [InlineKeyboardButton(text="📢 Ссылка на ТГК", callback_data="admin:promo_url")],
            [InlineKeyboardButton(text="📊 Текущие настройки", callback_data="admin:show")],
        ]
    )
