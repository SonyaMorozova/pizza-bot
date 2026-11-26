from abc import ABC, abstractmethod


def default_state() -> dict:
    return {
        "current_state": "waiting_for_recipe",
        "order_content": {
            "recipe": None,
            "size": None,
            "drink": None,
        },
    }


def user_from_update(update: dict):
    for key in ("message", "callback_query"):
        if key in update:
            return update[key].get("from")
    return None


def user_id_from_update(update: dict):
    user = user_from_update(update)
    if user is None:
        return None
    return int(user["id"])


class Storage(ABC):

    @abstractmethod
    def persist_user(self, user: dict) -> None:
        pass

    @abstractmethod
    def get_user_state(self, user_id: int) -> dict:
        pass

    @abstractmethod
    def save_user_state(self, user_id: int, state: dict) -> None:
        pass