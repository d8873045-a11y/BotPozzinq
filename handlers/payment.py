import logging
from datetime import datetime, timezone

from aiogram import Router, F, Bot
from aiogram.types import (
    Message,
    CallbackQuery,
    LabeledPrice,
    PreCheckoutQuery,
)

import dynamic_config
from config import ADMIN_IDS, STARS_RECEIVER_ID, RUB_TO_STARS
from keyboards import stars_prices_kb, main_menu

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data.startswith("stars_buy:"))
async def cb_stars_buy(call: CallbackQuery, bot: Bot) -> None:
    index = int(call.data.split(":")[1])
    items = dynamic_config.get_prices_items()

    if index >= len(items):
        await call.answer("Позиция не найдена.", show_alert=True)
        return

    item = items[index]
    stars = int(item["rub"] * RUB_TO_STARS)

    if stars < 1:
        await call.answer("Слишком маленькая сумма для оплаты звёздами.", show_alert=True)
        return

    await bot.send_invoice(
        chat_id=call.from_user.id,
        title=f"Заказ: {item['label']}",
        description=f"{item['label']} — оплата Telegram Stars",
        payload=f"order:{index}",
        currency="XTR",
        prices=[LabeledPrice(label=item["label"], amount=stars)],
        provider_token="",
    )
    await call.answer()


@router.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery) -> None:
    await query.answer(ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message, bot: Bot) -> None:
    payment = message.successful_payment
    user = message.from_user
    name = user.full_name or "нет имени"
    username = f"@{user.username}" if user.username else "нет username"
    stars = payment.total_amount
    payload = payment.invoice_payload
    now = datetime.now(timezone.utc).strftime("%d.%m.%Y %H:%M:%S UTC")

    items = dynamic_config.get_prices_items()
    try:
        index = int(payload.split(":")[1])
        item_label = items[index]["label"] if index < len(items) else payload
    except Exception:
        item_label = payload

    notify_text = (
        "⭐ <b>Оплата звёздами получена!</b>\n\n"
        "👤 <b>Покупатель:</b>\n"
        f"  Имя: {name}\n"
        f"  Username: {username}\n"
        f"  ID: <code>{user.id}</code>\n\n"
        f"🛒 <b>Товар:</b> {item_label}\n"
        f"💫 <b>Сумма:</b> {stars} ⭐\n\n"
        f"🕐 <b>Время:</b> {now}"
    )

    notify_ids = set(ADMIN_IDS) | {STARS_RECEIVER_ID}
    for uid in notify_ids:
        try:
            await bot.send_message(uid, notify_text, parse_mode="HTML")
        except Exception as exc:
            logger.error("Failed to notify %s about payment: %s", uid, exc)

    logger.info("Stars payment from %s: %s stars for %s", user.id, stars, item_label)

    await message.answer(
        f"✅ <b>Оплата прошла успешно!</b>\n\n"
        f"Вы оплатили: <b>{item_label}</b> ({stars} ⭐)\n\n"
        "Мы свяжемся с вами в ближайшее время 🙌",
        parse_mode="HTML",
        reply_markup=main_menu(),
    )
