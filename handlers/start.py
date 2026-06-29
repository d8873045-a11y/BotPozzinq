import logging
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config import WELCOME_TEXT
from keyboards import main_menu

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    logger.info("User %s started the bot", message.from_user.id)
    await message.answer(
        WELCOME_TEXT,
        parse_mode="HTML",
        reply_markup=main_menu(),
    )
