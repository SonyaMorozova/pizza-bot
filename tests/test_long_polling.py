import json
import os
import unittest
from unittest.mock import Mock, patch

os.environ.setdefault("TELEGRAM_TOKEN", "test-token")

from bot.dispatcher import Dispatcher
from bot.long_polling import start_long_polling


class TestLongPolling(unittest.TestCase):

    def setUp(self):
        self.dispatcher = Mock(spec=Dispatcher)

    @patch("bot.long_polling.telegram_bot_api.get_updates")
    def test_polling_parameters(self, get_updates):
        get_updates.side_effect = KeyboardInterrupt

        with self.assertRaises(KeyboardInterrupt):
            start_long_polling(self.dispatcher)

        params = get_updates.call_args.kwargs

        self.assertEqual(params["offset"], 0)

        self.assertTrue(5 <= params["timeout"] <= 60)
        self.assertTrue(1 <= params["limit"] <= 100)

        self.assertCountEqual(
            json.loads(params["allowed_updates"]),
            ["message", "callback_query"],
        )

    @patch("bot.long_polling.telegram_bot_api.get_updates")
    def test_dispatch_update(self, get_updates):
        update = {"update_id": 10}

        get_updates.side_effect = [
            [update],
            KeyboardInterrupt,
        ]

        with self.assertRaises(KeyboardInterrupt):
            start_long_polling(self.dispatcher)

        self.dispatcher.dispatch.assert_called_once_with(
            update
        )

    @patch("bot.long_polling.telegram_bot_api.get_updates")
    def test_offset_update(self, get_updates):
        get_updates.side_effect = [
            [
                {"update_id": 10},
                {"update_id": 11},
            ],
            KeyboardInterrupt,
        ]

        with self.assertRaises(KeyboardInterrupt):
            start_long_polling(self.dispatcher)

        calls = get_updates.call_args_list

        self.assertEqual(calls[0].kwargs["offset"], 0)
        self.assertEqual(calls[1].kwargs["offset"], 12)

        self.assertEqual(
            self.dispatcher.dispatch.call_count, 2
        )


if __name__ == "__main__":
    unittest.main()