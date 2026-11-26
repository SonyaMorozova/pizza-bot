import os
import unittest
from unittest.mock import Mock, patch

os.environ.setdefault("TELEGRAM_TOKEN", "test-token")

from bot.storage import Storage, default_state
from bot.handlers.start_command import StartCommand
from bot.handlers.waiting_for_recipe import WaitingForRecipe
from bot.handlers.waiting_for_pizza_size import WaitingForPizzaSize
from bot.handlers.waiting_for_drink import WaitingForDrink


class TestHandlers(unittest.TestCase):

    def setUp(self):
        self.storage = Mock(spec=Storage)
        self.state = default_state()

    def make_callback(self, data):
        return {
            "callback_query": {
                "id": "callback-1",
                "from": {"id": 123},
                "data": data,
                "message": {
                    "message_id": 10,
                    "chat": {"id": 456},
                },
            }
        }

    @patch("bot.handlers.start_command.telegram_bot_api")
    def test_start_command(self, api):
        handler = StartCommand(self.storage)

        update = {
            "message": {
                "text": "/start",
                "from": {"id": 123},
                "chat": {"id": 456},
            }
        }

        self.assertTrue(
            handler.can_handle(update, self.state)
        )

        handler.handle(update, self.state)

        self.storage.save_user_state.assert_called_once_with(
            123, default_state()
        )

        api.send_message.assert_called_once()
        self.assertEqual(len(api.mock_calls), 1)

    @patch("bot.handlers.start_command.telegram_bot_api")
    def test_restart_order(self, api):
        handler = StartCommand(self.storage)

        self.state["current_state"] = "waiting_for_drink"
        self.state["order_content"]["recipe"] = "pepperoni"
        self.state["order_content"]["size"] = "large"

        update = {
            "message": {
                "text": "/start",
                "from": {"id": 123},
                "chat": {"id": 456},
            }
        }

        handler.handle(update, self.state)

        self.storage.save_user_state.assert_called_once_with(
            123, default_state()
        )

    @patch("bot.handlers.waiting_for_recipe.telegram_bot_api")
    def test_choose_recipe(self, api):
        handler = WaitingForRecipe(self.storage)
        update = self.make_callback("pepperoni")

        self.assertTrue(
            handler.can_handle(update, self.state)
        )

        handler.handle(update, self.state)

        self.assertEqual(
            self.state["order_content"]["recipe"],
            "pepperoni",
        )

        self.assertEqual(
            self.state["current_state"],
            "waiting_for_pizza_size",
        )

        self.storage.save_user_state.assert_called_once_with(
            123, self.state
        )

        self.assert_callback_calls(api)

    @patch("bot.handlers.waiting_for_pizza_size.telegram_bot_api")
    def test_choose_size(self, api):
        handler = WaitingForPizzaSize(self.storage)

        self.state["current_state"] = "waiting_for_pizza_size"
        self.state["order_content"]["recipe"] = "pepperoni"

        update = self.make_callback("large")

        self.assertTrue(
            handler.can_handle(update, self.state)
        )

        handler.handle(update, self.state)

        self.assertEqual(
            self.state["order_content"]["size"],
            "large",
        )

        self.assertEqual(
            self.state["current_state"],
            "waiting_for_drink",
        )

        self.storage.save_user_state.assert_called_once_with(
            123, self.state
        )

        self.assert_callback_calls(api)

    @patch("bot.handlers.waiting_for_drink.telegram_bot_api")
    def test_choose_drink(self, api):
        handler = WaitingForDrink(self.storage)

        self.state["current_state"] = "waiting_for_drink"
        self.state["order_content"]["recipe"] = "pepperoni"
        self.state["order_content"]["size"] = "large"

        update = self.make_callback("none")

        self.assertTrue(
            handler.can_handle(update, self.state)
        )

        handler.handle(update, self.state)

        self.assertEqual(
            self.state["order_content"]["drink"],
            "none",
        )

        self.assertEqual(
            self.state["current_state"],
            "order_finished",
        )

        self.storage.save_user_state.assert_called_once_with(
            123, self.state
        )

        self.assert_callback_calls(api)

        text = api.send_message.call_args.kwargs["text"]

        self.assertIn("Пепперони", text)
        self.assertIn("Большая", text)
        self.assertIn("Без напитка", text)

    def test_unknown_callback(self):
        handler = WaitingForRecipe(self.storage)
        update = self.make_callback("unknown")

        self.assertFalse(
            handler.can_handle(update, self.state)
        )

    def test_unknown_message(self):
        handler = StartCommand(self.storage)

        update = {
            "message": {
                "text": "Привет",
                "from": {"id": 123},
                "chat": {"id": 456},
            }
        }

        self.assertFalse(
            handler.can_handle(update, self.state)
        )

    def assert_callback_calls(self, api):
        api.delete_message.assert_called_once_with(
            chat_id=456,
            message_id=10,
        )

        api.send_message.assert_called_once()

        self.assertEqual(
            api.send_message.call_args.kwargs["chat_id"],
            456,
        )

        api.answer_callback_query.assert_called_once_with(
            callback_query_id="callback-1",
        )

        self.assertEqual(len(api.mock_calls), 3)


if __name__ == "__main__":
    unittest.main()