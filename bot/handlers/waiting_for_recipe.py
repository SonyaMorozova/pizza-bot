from bot import pizza_menu, telegram_bot_api
from bot.handler import Handler, HandlerStatus
from bot.storage import Storage

_VALID = {key for key, _ in pizza_menu.RECIPES}


class WaitingForRecipe(Handler):
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def can_handle(self, update: dict, state: dict) -> bool:
        if state.get("current_state") != "waiting_for_recipe":
            return False

        if "callback_query" not in update:
            return False

        cq = update["callback_query"]

        return cq.get("data") in _VALID and cq.get("message") is not None

    def handle(self, update: dict, state: dict) -> HandlerStatus:
        cq = update["callback_query"]
        chat_id = cq["message"]["chat"]["id"]
        message_id = cq["message"]["message_id"]

        recipe = cq["data"]

        state["order_content"]["recipe"] = recipe
        state["current_state"] = "waiting_for_pizza_size"

        self._storage.save_user_state(cq["from"]["id"], state)

        telegram_bot_api.delete_message(
            chat_id=chat_id,
            message_id=message_id,
        )

        telegram_bot_api.send_message(
            chat_id=chat_id,
            text=pizza_menu.MSG_CHOOSE_SIZE,
            reply_markup=pizza_menu.sizes_keyboard(),
        )

        telegram_bot_api.answer_callback_query(
            callback_query_id=cq["id"],
        )

        return HandlerStatus.STOP
