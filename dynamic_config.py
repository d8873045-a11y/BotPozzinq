import json
import os
from typing import Any

_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "config.json")

_DEFAULTS: dict[str, Any] = {
    "prices_items": [
        {"label": "1 поззинг", "rub": 150},
        {"label": "5 поззингов", "rub": 650},
        {"label": "10 поззингов", "rub": 1200},
    ],
    "reviews_url": "",
    "promo_url": "",
}


def _load() -> dict[str, Any]:
    if os.path.exists(_DATA_PATH):
        try:
            with open(_DATA_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                for key, val in _DEFAULTS.items():
                    if key not in data:
                        data[key] = val
                return data
        except Exception:
            pass
    return dict(_DEFAULTS)


def _save(data: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(_DATA_PATH), exist_ok=True)
    with open(_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_prices_items() -> list[dict]:
    return _load()["prices_items"]


def get_reviews_url() -> str:
    return _load().get("reviews_url", "")


def get_promo_url() -> str:
    return _load().get("promo_url", "")


def set_prices_items(items: list[dict]) -> None:
    data = _load()
    data["prices_items"] = items
    _save(data)


def set_reviews_url(url: str) -> None:
    data = _load()
    data["reviews_url"] = url
    _save(data)


def set_promo_url(url: str) -> None:
    data = _load()
    data["promo_url"] = url
    _save(data)


def build_prices_text() -> str:
    from config import RUB_TO_STARS
    items = get_prices_items()
    lines = ["💰 <b>Актуальные прайсы</b>\n"]
    for item in items:
        stars = int(item["rub"] * RUB_TO_STARS)
        lines.append(
            f"📌 {item['label']} — <b>{item['rub']} ₽</b> / <b>{stars} ⭐</b>"
        )
    lines.append("\n💳 Оплата: <b>СБЕР</b> или <b>Telegram Stars ⭐</b>")
    lines.append("\n<i>Актуальные цены уточняйте у администратора.</i>")
    return "\n".join(lines)
