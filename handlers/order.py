import logging
from datetime import datetime, timezone

from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import dynamic_config
from config import ADMIN_IDS, ORDER_PROMPT_TEXT, ORDER_CONFIRM_TEXT, BTN_ORDER, BTN_BACK
from keyboards import main_menu, back_menu, payment_choice_kb, stars_prices_kb
from states import OrderStates

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.text == BTN_ORDER)
async def ask_payment_method(message: Message, state: FSMContext) -> None:
    await state.set_state(OrderStates.choosing_payment)
    logger.info("User %s choosing payment method", message.from_user.id)
    await message.answer(
        "🛒 <b>Как хотите оплатить?</b>\n\n"
        "💳 <b>СБЕР</b> — вы пишете заявку, мы присылаем реквизиты\n"
        "⭐ <b>Telegram Stars</b> — моментальная оплата прямо в Telegram",
        parse_mode="HTML",
        reply_markup=payment_choice_kb(),
    )


@router.message(OrderStates.choosing_payment, F.text == "💳 Оплата через СБЕР")
async def choose_sber(message: Message, state: FSMContext) -> None:
    await state.set_state(OrderStates.waiting_for_message)
    await message.answer(
        ORDER_PROMPT_TEXT,
        parse_mode="HTML",
        reply_markup=back_menu(),
    )


@router.message(OrderStates.choosing_payment, F.text == "⭐ Оплата звёздами")
async def choose_stars(message: Message, state: FSMContext) -> None:
    await state.clear()
    items = dynamic_config.get_prices_items()
    if not items:
        await message.answer("❌ Прайсы не настроены. Обратитесь к администратору.", reply_markup=main_menu())
        return
    await message.answer(
        "⭐ <b>Выберите позицию для оплаты звёздами:</b>",
        parse_mode="HTML",
        reply_markup=stars_prices_kb(items),
    )
    await message.answer("Главное меню доступно ниже 👇", reply_markup=main_menu())


@router.message(F.text == BTN_BACK)
async def go_back(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Главное меню 👇", reply_markup=main_menu())


@router.message(OrderStates.waiting_for_message)
async def receive_order(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.clear()

    user = message.from_user
    name = user.full_name or "нет имени"
    username = f"@{user.username}" if user.username else "нет username"
    user_id = user.id
    text = message.text or "(нет текста)"
    now = datetime.now(timezone.utc).strftime("%d.%m.%Y %H:%M:%S UTC")

    owner_msg = (
        "📬 <b>Новая заявка на поззинги</b>\n\n"
        "👤 <b>От пользователя:</b>\n"
        f"  Имя: {name}\n"
        f"  Username: {username}\n"
        f"  ID: <code>{user_id}</code>\n\n"
        "💬 <b>Сообщение:</b>\n"
        f"{text}\n\n"
        f"🕐 <b>Время:</b>\n{now}"
    )

    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, owner_msg, parse_mode="HTML")
        except Exception as exc:
            logger.error("Failed to send order to admin %s: %s", admin_id, exc)

    logger.info("Order from user %s sent to all admins", user_id)
    await message.answer(ORDER_CONFIRM_TEXT, reply_markup=main_menu())
