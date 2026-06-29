import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import dynamic_config
from config import BTN_PRICES
from keyboards import main_menu

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.text == BTN_PRICES)
async def show_prices(message: Message, state: FSMContext) -> None:
    await state.clear()
    logger.info("User %s requested prices", message.from_user.id)
    await message.answer(
        dynamic_config.build_prices_text(),
        parse_mode="HTML",
        reply_markup=main_menu(),
    )
