import logging
import os
import hikari
import lightbulb
from asyncpg import Pool
from yuganda.config import Config, deserialise_raw_config, load_config_file
from yuganda.database import Database

__all__ = ["Yuganda"]

_LOGGER = logging.getLogger("yuganda")


class Yuganda(lightbulb.Bot):
    def __init__(self) -> None:

        self._database: Database
        self._extensions = [
            f"yuganda.extensions.{extension[:-3]}"
            for extension in os.listdir("yuganda/extensions")
            if extension.endswith(".py") and not extension.startswith("__init__")
        ]
        super().__init__(
            slash_commands_only=True,
            intents=hikari.Intents.ALL,
            token=self.config.bot.token,
        )

        subscriptions = {
            hikari.events.StartingEvent: self.on_starting,
            hikari.events.StartedEvent: self.on_started,
            hikari.events.ShardReadyEvent: self.on_shard_ready,
        }

        for event, callback in subscriptions.items():
            self.subscribe(event, callback)

    CONFIG_PATH = os.environ.get("YUGANDA_CONFIG_PATH") or "./config.yml"
    CONFIG_CACHE = deserialise_raw_config(load_config_file(CONFIG_PATH))

    @property
    def config(self) -> Config:
        if Yuganda.CONFIG_CACHE is None:
            Yuganda.CONFIG_CACHE = deserialise_raw_config(
                load_config_file(Yuganda.CONFIG_PATH)
            )
        return Yuganda.CONFIG_CACHE

    @property
    def database(self) -> Pool:
        if self._database is None:
            raise RuntimeError("Database is None.")
        return self._database

    async def on_starting(self, event: hikari.StartingEvent):
        _LOGGER.info("Bot is Starting..")
        _LOGGER.info("Connecting to database..")
        self._database = Database(self, Yuganda.CONFIG_CACHE.database)
        await self.database.initialise()
        _LOGGER.info("Loading extensions")
        for extension in self._extensions:
            _LOGGER.info("Loading extension: %s", extension)
            self.load_extension(extension)

    async def on_started(self, event: hikari.StartedEvent):
        pass

    async def on_shard_ready(self, event: hikari.ShardReadyEvent):
        pass
