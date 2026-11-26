from bot import pizza_menu, telegram_bot_api
from bot.handler import Handler, HandlerStatus
from bot.storage import Storage, default_state


class StartCommand(Handler):
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def can_handle(self, update: dict, state: dict) -> bool:
        if "message" not in update:
            return False

        return update["message"].get("text") == "/start"

    def handle(self, update: dict, state: dict) -> HandlerStatus:
        message = update["message"]
        user_id = message["from"]["id"]

        new_state = default_state()
        self._storage.save_user_state(user_id, new_state)

        telegram_bot_api.send_message(
            chat_id=message["chat"]["id"],
            text=pizza_menu.MSG_CHOOSE_RECIPE,
            reply_markup=pizza_menu.recipes_keyboard(),
        )

        return HandlerStatus.STOP
