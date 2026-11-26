import json
import os
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs

os.environ.setdefault("TELEGRAM_TOKEN", "test-token")

from bot import telegram_bot_api


class TestTelegramBotAPI(unittest.TestCase):
    @patch("bot.telegram_bot_api.urllib.request.urlopen")
    def test_api_request(self, urlopen):
        urlopen.return_value.__enter__.return_value.read.return_value = json.dumps(
            {"ok": True, "result": {}}
        ).encode()

        with patch.object(telegram_bot_api, "TOKEN", "test-token"):
            with patch.object(
                telegram_bot_api,
                "BASE_URL",
                "https://test-api.example",
            ):
                telegram_bot_api.api_request(
                    "sendMessage",
                    chat_id=123,
                    text="Hello",
                )

        urlopen.assert_called_once()

        url = urlopen.call_args.args[0]

        self.assertEqual(
            url,
            "https://test-api.example/bottest-token/sendMessage",
        )

        data = urlopen.call_args.kwargs["data"]
        params = parse_qs(data.decode())

        self.assertEqual(params["chat_id"], ["123"])
        self.assertEqual(params["text"], ["Hello"])

    @patch("bot.telegram_bot_api.api_request")
    def test_get_updates(self, request):
        updates = [{"update_id": 10}]

        request.return_value = {
            "ok": True,
            "result": updates,
        }

        result = telegram_bot_api.get_updates(offset=0)

        request.assert_called_once_with(
            "getUpdates",
            offset=0,
        )

        self.assertEqual(result, updates)

    @patch("bot.telegram_bot_api.api_request")
    def test_send_message(self, request):
        telegram_bot_api.send_message(
            chat_id=123,
            text="Hello",
        )

        request.assert_called_once_with(
            "sendMessage",
            chat_id=123,
            text="Hello",
        )

    @patch("bot.telegram_bot_api.api_request")
    def test_delete_message(self, request):
        telegram_bot_api.delete_message(
            chat_id=123,
            message_id=10,
        )

        request.assert_called_once_with(
            "deleteMessage",
            chat_id=123,
            message_id=10,
        )

    @patch("bot.telegram_bot_api.api_request")
    def test_answer_callback_query(self, request):
        telegram_bot_api.answer_callback_query(
            callback_query_id="callback-1",
        )

        request.assert_called_once_with(
            "answerCallbackQuery",
            callback_query_id="callback-1",
        )


if __name__ == "__main__":
    unittest.main()
