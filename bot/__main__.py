from bot import long_polling
from bot.dispatcher import Dispatcher
from bot.handlers import get_handlers
from bot.sqlite_storage import SQLiteStorage


def main() -> None:
    try:
        storage = SQLiteStorage()

        dispatcher = Dispatcher(storage)
        dispatcher.add_handlers(*get_handlers(storage))

        long_polling.start_long_polling(dispatcher)

    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == "__main__":
    main()