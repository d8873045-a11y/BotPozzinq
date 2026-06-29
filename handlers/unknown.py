import logging
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config import UNKNOWN_TEXT
from keyboards import main_menu
from states import OrderStates

router = Router()
logger = logging.getLogger(__name__)


@router.message()
async def unknown_message(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == OrderStates.waiting_for_message.state:
        return

    logger.debug("Unknown message from user %s: %s", message.from_user.id, message.text)
    await message.answer(UNKNOWN_TEXT, reply_markup=main_menu())
