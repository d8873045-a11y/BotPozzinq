import os

BOT_TOKEN: str = os.environ["BOT_TOKEN"]

ADMIN_IDS: list[int] = [8714651484, 6069318420]

STARS_RECEIVER_ID: int = 8962183816

WELCOME_TEXT: str = (
    "👋 Привет! Добро пожаловать!\n\n"
    "🎯 Здесь можно быстро и удобно заказать <b>поззинги</b> — "
    "просто выбери нужное в меню ниже.\n\n"
    "💬 Смотри прайсы, читай отзывы или сразу оформляй заказ — "
    "всё в пару нажатий."
)

ORDER_PROMPT_TEXT: str = (
    "📝 Оставьте сообщение ниже и укажите свой юзернейм 👇\n\n"
    "<i>Например: Хочу заказать 5 поззингов. Мой username: @ваш_ник</i>"
)

ORDER_CONFIRM_TEXT: str = (
    "✅ Заявка отправлена!\n\n"
    "Мы свяжемся с вами в ближайшее время 🙌"
)

REVIEWS_NO_LINK_TEXT: str = "📝 Ссылка на отзывы будет добавлена позже."

UNKNOWN_TEXT: str = "🤔 Не понял тебя. Воспользуйся кнопками меню ниже 👇"

BTN_PRICES: str = "💰 Прайсы"
BTN_REVIEWS: str = "⭐ Отзывы"
BTN_ORDER: str = "🛒 Заказать поззинги"
BTN_BACK: str = "↩️ Назад"
BTN_PAY_SBER: str = "💳 Оплата через СБЕР"
BTN_PAY_STARS: str = "⭐ Оплата звёздами"

RUB_TO_STARS: float = 0.5
