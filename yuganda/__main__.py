import logging
import os

from attr import setters
from yuganda.database import initialise_database

from hikari.events.lifetime_events import StartingEvent
from yuganda.config.models import Config
from yuganda.config.load import deserialise_raw_config, load_config_file
from hikari.intents import Intents
import lightbulb
import edgedb

CONFIG_PATH = os.environ.get("YUGANDA_CONFIG_PATH") or "./config.yml"
CONFIG_CACHE = deserialise_raw_config(load_config_file(CONFIG_PATH))

logging.basicConfig(
    level=CONFIG_CACHE.logging.level,
    style="{",
    format=CONFIG_CACHE.logging.log_format,
    datefmt=CONFIG_CACHE.logging.date_format,
)

_LOGGER = logging.getLogger("yuganda")


class Yuganda(lightbulb.Bot):
    def __init__(self) -> None:
        self._data_pool: edgedb.AsyncIOPool
        super().__init__(
            slash_commands_only=True, intents=Intents.ALL, token=self.config.bot.token
        )

    @property
    def config(self) -> Config:
        global CONFIG_CACHE
        return CONFIG_CACHE or (
            CONFIG_CACHE := deserialise_raw_config(load_config_file(CONFIG_PATH))
        )

    @property
    def data_pool(self) -> edgedb.AsyncIOPool:
        if self._data_pool is None:
            raise RuntimeError("Data Pool is None.")
        return self._data_pool

    @data_pool.setter
    def data_pool(self, pool: edgedb.AsyncIOPool):
        self._data_pool = pool


async def on_starting(event: StartingEvent):
    _LOGGER.info("Bot is Starting..")
    print(event.app.config)
    _LOGGER.info("Creating a connection pool to database..")
    event.app.data_pool = await initialise_database(CONFIG_CACHE.database)


def main():
    bot = Yuganda()

    bot.subscribe(StartingEvent, on_starting)
    bot.run()


if __name__ == "__main__":
    main()
