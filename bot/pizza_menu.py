import json

RECIPES = [
    ("margherita", "Маргарита"),
    ("pepperoni", "Пепперони"),
    ("four_cheese", "Четыре сыра"),
    ("hawaiian", "Гавайская"),
    ("napoletano", "Неаполитанская"),
]

SIZES = [
    ("small", "Маленькая"),
    ("medium", "Средняя"),
    ("large", "Большая"),
]

DRINKS = [
    ("juice", "Сок"),
    ("mors", "Морс"),
    ("tea", "Чай"),
    ("cola", "Кола"),
    ("none", "Без напитка"),
]

_LABELS = {key: label for options in (RECIPES, SIZES, DRINKS) for key, label in options}

MSG_CHOOSE_RECIPE = "Собери пиццу. Выбери рецепт:"
MSG_CHOOSE_SIZE = "Выбери размер:"
MSG_CHOOSE_DRINK = "Выбери напиток:"
MSG_ORDER_FINISHED_HINT = "Заказ уже оформлен. Нажми /start, чтобы начать новый."


def label_for(option_id: str) -> str:
    return _LABELS.get(option_id, option_id)


def _keyboard(options: list[tuple[str, str]]) -> str:
    return json.dumps(
        {
            "inline_keyboard": [
                [{"text": label, "callback_data": key}] for key, label in options
            ]
        },
        ensure_ascii=False,
    )


def recipes_keyboard() -> str:
    return _keyboard(RECIPES)


def sizes_keyboard() -> str:
    return _keyboard(SIZES)


def drinks_keyboard() -> str:
    return _keyboard(DRINKS)


def format_order_summary(order_content: dict) -> str:
    recipe = label_for(order_content["recipe"])
    size = label_for(order_content["size"])
    drink = label_for(order_content["drink"])

    return (
        "Заказ принят:\n"
        f"• Рецепт: {recipe}\n"
        f"• Размер: {size}\n"
        f"• Напиток: {drink}\n\n"
        "Новый заказ: /start"
    )
