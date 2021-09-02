import logging
import os
from yuganda.config.models import Config
from yuganda.config.load import deserialise_raw_config, load_config_file
from hikari.events.shard_events import ShardReadyEvent
from hikari.intents import Intents
import lightbulb

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
        super().__init__(
            slash_commands_only=True, intents=Intents.ALL, token=self.config.bot.token
        )

    @property
    def config(self) -> Config:
        global CONFIG_CACHE
        return CONFIG_CACHE or (
            CONFIG_CACHE := deserialise_raw_config(load_config_file(CONFIG_PATH))
        )


async def on_ready(event: ShardReadyEvent):
    _LOGGER.info(
        "Bot is ready at shard %s with user %s", event.shard.id, event.my_user.username
    )


def main():
    bot = Yuganda()

    bot.subscribe(ShardReadyEvent, on_ready)
    bot.run()


if __name__ == "__main__":
    main()
