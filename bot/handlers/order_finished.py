from bot import pizza_menu, telegram_bot_api
from bot.handler import Handler, HandlerStatus


class OrderFinished(Handler):
    def can_handle(self, update: dict, state: dict) -> bool:
        return (
            state.get("current_state") == "order_finished"
            and "callback_query" in update
        )

    def handle(self, update: dict, state: dict) -> HandlerStatus:
        cq = update["callback_query"]
        telegram_bot_api.answer_callback_query(callback_query_id=cq["id"])
        message = cq.get("message")
        if message is not None:
            telegram_bot_api.send_message(
                chat_id=message["chat"]["id"],
                text=pizza_menu.MSG_ORDER_FINISHED_HINT,
            )
        return HandlerStatus.STOP
