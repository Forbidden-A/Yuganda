import logging
from yuganda import Yuganda


def main():
    logging.basicConfig(
        level=Yuganda.CONFIG_CACHE.logging.level,
        style="{",
        format=Yuganda.CONFIG_CACHE.logging.log_format,
        datefmt=Yuganda.CONFIG_CACHE.logging.date_format,
    )

    bot = Yuganda()

    bot.run()


if __name__ == "__main__":
    main()
