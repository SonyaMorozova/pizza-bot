from abc import ABC, abstractmethod


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