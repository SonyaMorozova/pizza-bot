import unittest
from unittest.mock import Mock

from bot.dispatcher import Dispatcher
from bot.handler import Handler, HandlerStatus
from bot.storage import Storage, default_state


class TestDispatcher(unittest.TestCase):
    def setUp(self):
        self.storage = Mock(spec=Storage)
        self.state = default_state()

        self.storage.get_user_state.return_value = self.state

        self.dispatcher = Dispatcher(self.storage)

        self.update = {
            "message": {
                "text": "/start",
                "from": {"id": 123},
                "chat": {"id": 456},
            }
        }

    def test_get_user_state(self):
        self.dispatcher.dispatch(self.update)

        self.storage.get_user_state.assert_called_once_with(123)

    def test_matching_handler(self):
        handler = Mock(spec=Handler)
        handler.can_handle.return_value = True
        handler.handle.return_value = HandlerStatus.STOP

        self.dispatcher.add_handlers(handler)
        self.dispatcher.dispatch(self.update)

        handler.can_handle.assert_called_once_with(self.update, self.state)

        handler.handle.assert_called_once_with(self.update, self.state)

    def test_skip_handler(self):
        handler = Mock(spec=Handler)
        handler.can_handle.return_value = False

        self.dispatcher.add_handlers(handler)
        self.dispatcher.dispatch(self.update)

        handler.handle.assert_not_called()

    def test_continue_dispatching(self):
        first = Mock(spec=Handler)
        first.can_handle.return_value = True
        first.handle.return_value = HandlerStatus.CONTINUE

        second = Mock(spec=Handler)
        second.can_handle.return_value = True
        second.handle.return_value = HandlerStatus.STOP

        self.dispatcher.add_handlers(first, second)
        self.dispatcher.dispatch(self.update)

        first.handle.assert_called_once()
        second.handle.assert_called_once()

    def test_stop_dispatching(self):
        first = Mock(spec=Handler)
        first.can_handle.return_value = True
        first.handle.return_value = HandlerStatus.STOP

        second = Mock(spec=Handler)

        self.dispatcher.add_handlers(first, second)
        self.dispatcher.dispatch(self.update)

        first.handle.assert_called_once()
        second.can_handle.assert_not_called()
        second.handle.assert_not_called()

    def test_update_without_user(self):
        self.dispatcher.dispatch({})

        self.storage.get_user_state.assert_not_called()


if __name__ == "__main__":
    unittest.main()
