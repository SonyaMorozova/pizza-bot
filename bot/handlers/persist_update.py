from bot import updated_logger
from bot.handler import Handler, HandlerStatus


class PersistUpdate(Handler):
    def can_handle(self, update: dict, state: dict) -> bool:
        return True

    def handle(self, update: dict, state: dict) -> HandlerStatus:
        updated_logger.persist_update(update)
        return HandlerStatus.CONTINUE
