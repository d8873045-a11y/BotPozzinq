import logging
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import dynamic_config
from config import ADMIN_IDS, RUB_TO_STARS
from keyboards import admin_menu_kb, main_menu
from states import AdminStates

router = Router()
logger = logging.getLogger(__name__)

PRICE_FORMAT_HELP = (
    "Отправь список цен в формате (каждая позиция с новой строки):\n\n"
    "<code>Название;цена_в_рублях</code>\n\n"
    "Например:\n"
    "<code>1 поззинг;100\n"
    "5 поззингов;450\n"
    "10 поззингов;850</code>\n\n"
    "Звёзды считаются автоматически (1 ₽ = 0.5 ⭐)."
)


def _is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext) -> None:
    if not _is_admin(message.from_user.id):
        await message.answer("⛔ Нет доступа.")
        return
    await state.clear()
    logger.info("Admin %s opened admin panel", message.from_user.id)
    await message.answer(
        "🔧 <b>Панель администратора</b>\n\nВыберите действие:",
        parse_mode="HTML",
        reply_markup=admin_menu_kb(),
    )


@router.callback_query(F.data == "admin:show")
async def cb_admin_show(call: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(call.from_user.id):
        await call.answer("⛔ Нет доступа.", show_alert=True)
        return

    items = dynamic_config.get_prices_items()
    reviews = dynamic_config.get_reviews_url() or "не задана"
    promo = dynamic_config.get_promo_url() or "не задана"

    lines = ["📊 <b>Текущие настройки</b>\n", "<b>Прайсы:</b>"]
    for item in items:
        stars = int(item["rub"] * RUB_TO_STARS)
        lines.append(f"  • {item['label']} — {item['rub']} ₽ / {stars} ⭐")
    lines.append(f"\n🔗 Ссылка на отзывы: {reviews}")
    lines.append(f"📢 Ссылка на ТГК: {promo}")

    await call.message.edit_text(
        "\n".join(lines),
        parse_mode="HTML",
        reply_markup=admin_menu_kb(),
    )
    await call.answer()


@router.callback_query(F.data == "admin:prices")
async def cb_admin_prices(call: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(call.from_user.id):
        await call.answer("⛔ Нет доступа.", show_alert=True)
        return
    await state.set_state(AdminStates.editing_prices)
    await call.message.answer(PRICE_FORMAT_HELP, parse_mode="HTML")
    await call.answer()


@router.callback_query(F.data == "admin:reviews_url")
async def cb_admin_reviews_url(call: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(call.from_user.id):
        await call.answer("⛔ Нет доступа.", show_alert=True)
        return
    await state.set_state(AdminStates.editing_reviews_url)
    current = dynamic_config.get_reviews_url() or "не задана"
    await call.message.answer(
        f"🔗 Текущая ссылка на отзывы: <code>{current}</code>\n\n"
        "Отправь новую ссылку (или <code>-</code> чтобы убрать):",
        parse_mode="HTML",
    )
    await call.answer()


@router.callback_query(F.data == "admin:promo_url")
async def cb_admin_promo_url(call: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(call.from_user.id):
        await call.answer("⛔ Нет доступа.", show_alert=True)
        return
    await state.set_state(AdminStates.editing_promo_url)
    current = dynamic_config.get_promo_url() or "не задана"
    await call.message.answer(
        f"📢 Текущая ссылка на ТГК: <code>{current}</code>\n\n"
        "Отправь новую ссылку (или <code>-</code> чтобы убрать):",
        parse_mode="HTML",
    )
    await call.answer()


@router.message(AdminStates.editing_prices)
async def receive_new_prices(message: Message, state: FSMContext) -> None:
    if not _is_admin(message.from_user.id):
        return

    raw = (message.text or "").strip()
    items = []
    errors = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(";")
        if len(parts) != 2:
            errors.append(f"❌ Неверный формат строки: <code>{line}</code>")
            continue
        label = parts[0].strip()
        try:
            rub = int(parts[1].strip())
            if rub <= 0:
                raise ValueError
        except ValueError:
            errors.append(f"❌ Неверная цена в строке: <code>{line}</code>")
            continue
        items.append({"label": label, "rub": rub})

    if errors:
        await message.answer(
            "⚠️ Найдены ошибки:\n" + "\n".join(errors) + "\n\nИсправь и отправь снова.\n\n" + PRICE_FORMAT_HELP,
            parse_mode="HTML",
        )
        return

    if not items:
        await message.answer("⚠️ Список цен пустой. Попробуй снова.\n\n" + PRICE_FORMAT_HELP, parse_mode="HTML")
        return

    dynamic_config.set_prices_items(items)
    await state.clear()

    preview_lines = ["✅ <b>Прайсы обновлены!</b>\n"]
    for item in items:
        stars = int(item["rub"] * RUB_TO_STARS)
        preview_lines.append(f"  • {item['label']} — {item['rub']} ₽ / {stars} ⭐")
    await message.answer("\n".join(preview_lines), parse_mode="HTML", reply_markup=admin_menu_kb())
    logger.info("Admin %s updated prices: %s", message.from_user.id, items)


@router.message(AdminStates.editing_reviews_url)
async def receive_reviews_url(message: Message, state: FSMContext) -> None:
    if not _is_admin(message.from_user.id):
        return
    url = (message.text or "").strip()
    if url == "-":
        url = ""
    dynamic_config.set_reviews_url(url)
    await state.clear()
    display = url or "убрана"
    await message.answer(
        f"✅ Ссылка на отзывы обновлена: <code>{display}</code>",
        parse_mode="HTML",
        reply_markup=admin_menu_kb(),
    )
    logger.info("Admin %s set reviews_url: %s", message.from_user.id, url)


@router.message(AdminStates.editing_promo_url)
async def receive_promo_url(message: Message, state: FSMContext) -> None:
    if not _is_admin(message.from_user.id):
        return
    url = (message.text or "").strip()
    if url == "-":
        url = ""
    dynamic_config.set_promo_url(url)
    await state.clear()
    display = url or "убрана"
    await message.answer(
        f"✅ Ссылка на ТГК обновлена: <code>{display}</code>",
        parse_mode="HTML",
        reply_markup=admin_menu_kb(),
    )
    logger.info("Admin %s set promo_url: %s", message.from_user.id, url)
