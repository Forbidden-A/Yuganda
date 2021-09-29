from yuganda import Yuganda
import lightbulb
import logging

_LOGGER = logging.getLogger("yuganda.extensions.starboard")


class Starboard(lightbulb.Plugin):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
        _LOGGER.info("Loaded..")


def load(bot: Yuganda):
    bot.add_plugin(Starboard(bot))
