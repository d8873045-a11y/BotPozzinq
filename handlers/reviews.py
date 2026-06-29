import logging
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

import dynamic_config
from config import REVIEWS_NO_LINK_TEXT, BTN_REVIEWS
from keyboards import main_menu

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.text == BTN_REVIEWS)
async def show_reviews(message: Message, state: FSMContext) -> None:
    await state.clear()
    logger.info("User %s requested reviews", message.from_user.id)

    reviews_url = dynamic_config.get_reviews_url()
    if reviews_url:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📖 Читать отзывы", url=reviews_url)]
            ]
        )
        await message.answer(
            "⭐ <b>Отзывы наших клиентов</b>\n\nНажми кнопку ниже, чтобы посмотреть:",
            parse_mode="HTML",
            reply_markup=kb,
        )
        await message.answer("Главное меню 👇", reply_markup=main_menu())
    else:
        await message.answer(REVIEWS_NO_LINK_TEXT, reply_markup=main_menu())
