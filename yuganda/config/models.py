# This is heavely inspired by Discord Coding Academy's Bracky Discord bot (https://gitlab.com/dcacademy/bracky).
import os
from typing import Type, TypeVar
import attr
import cattr

ThisImplT = TypeVar("ThisImplT")


class BaseConfig:
    @classmethod
    def from_dict(
        cls: Type[ThisImplT],
        obj: dict[str, any],
        converter: cattr.Converter = cattr.global_converter,
    ) -> ThisImplT:
        return converter.structure(obj, cls)

    def to_dict(self):
        assert attr.has(self.__class__)
        return attr.asdict(self)


@attr.s(frozen=True, auto_attribs=True)
class BotConfig(BaseConfig):
    """Some values related to the bot."""

    token: str = attr.ib(repr=False, factory=lambda: os.environ["YUGANDA_TOKEN"])
    starboard_threshold: int = 3


@attr.s(frozen=True, auto_attribs=True)
class LoggingConfig(BaseConfig):
    """Configuration values for the root logger (set via the basicConfig function)."""

    level: str = "INFO"
    log_format: str = "{asctime} | {levelname:^8} | {name} :: {message}"
    date_format: str = "%a, %d, %b %Y (%H:%M:%S)"


@attr.s(frozen=True, auto_attribs=True)
class EdgeDBConfig(BaseConfig):
    """
    All values needed to connect to an EdgeDB Database.
    The defaults will assume the bot is running on Docker.
    """

    password: str = attr.ib(repr=False, factory=lambda: os.environ["EDGEDB_PASSWORD"])
    host: str = "yuganda-db"
    port: int = 5656
    user: str = "edgedb"
    database: str = "edgedb"


@attr.s(frozen=True, auto_attribs=True)
class Config(BaseConfig):
    """Root configuration model."""

    bot: BotConfig
    logging: LoggingConfig = attr.ib(factory=LoggingConfig)
    database: EdgeDBConfig = attr.ib(factory=EdgeDBConfig)
