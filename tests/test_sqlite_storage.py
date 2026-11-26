import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from bot.sqlite_storage import SQLiteStorage
from bot.storage import default_state


class TestSQLiteStorage(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.db_path = str(Path(self.temp_dir.name) / "test.db")

        self.storage = SQLiteStorage(self.db_path)

        self.storage.persist_user(
            {
                "id": 123,
                "first_name": "Test",
            }
        )

    def test_default_state(self):
        self.assertEqual(
            self.storage.get_user_state(123),
            default_state(),
        )

    def test_save_user_state(self):
        state = default_state()
        state["current_state"] = "waiting_for_pizza_size"
        state["order_content"]["recipe"] = "pepperoni"

        self.storage.save_user_state(123, state)

        self.assertEqual(
            self.storage.get_user_state(123),
            state,
        )

    def test_state_after_restart(self):
        state = default_state()
        state["order_content"]["recipe"] = "pepperoni"
        state["current_state"] = "waiting_for_pizza_size"

        self.storage.save_user_state(123, state)

        new_storage = SQLiteStorage(self.db_path)

        self.assertEqual(
            new_storage.get_user_state(123),
            state,
        )

    def test_independent_users(self):
        self.storage.persist_user(
            {
                "id": 456,
                "first_name": "Second user",
            }
        )

        state = default_state()
        state["order_content"]["recipe"] = "pepperoni"

        self.storage.save_user_state(123, state)

        self.assertEqual(
            self.storage.get_user_state(456),
            default_state(),
        )

    def test_persist_user_preserves_state(self):
        state = default_state()
        state["order_content"]["recipe"] = "pepperoni"

        self.storage.save_user_state(123, state)

        self.storage.persist_user(
            {
                "id": 123,
                "first_name": "New name",
            }
        )

        self.assertEqual(
            self.storage.get_user_state(123),
            state,
        )


if __name__ == "__main__":
    unittest.main()
