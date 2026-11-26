from bot.handler import Handler, HandlerStatus
from bot.storage import Storage, user_from_update


class PersistUser(Handler):
    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def can_handle(self, update: dict, state: dict) -> bool:
        return True

    def handle(self, update: dict, state: dict) -> HandlerStatus:
        user = user_from_update(update)

        if user is not None:
            self._storage.persist_user(user)

        return HandlerStatus.CONTINUE
