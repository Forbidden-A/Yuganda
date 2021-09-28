# Heavily inspired by https://github.com/IkBenOlie5/Kangakari/
import logging
from yuganda.config.models import PostgresConfig
import asyncpg
from lightbulb import Bot
import typing
import functools
import asyncio
import hikari

_LOGGER = logging.getLogger()

_any_callable = typing.Callable[..., typing.Any]


class Database:
    def __init__(self, bot: Bot, config: PostgresConfig):
        self.config = config
        self.bot = bot
        self._connected = asyncio.Event()
        self._pool: asyncpg.Pool

    @property
    def is_connected(self):
        return self._connected.is_set()

    @property
    def pool(self):
        assert self._connected, "Database is not connected."
        return self._pool

    async def initialise(self):
        assert not self.is_connected, "Already connected and initialised."
        _LOGGER.info("Creating data pool")
        self._pool = await asyncpg.create_pool(**self.config.to_dict())
        _LOGGER.info("Syncing and executing schemas")
        # TODO: Execute schema and sync.
        self._connected.set()

    async def close(self):
        assert self.is_connected, "Database is not connected."
        await self.pool.close()
        del self._pool
        self._connected.clear()
        _LOGGER.info("Closed the database.")

    def in_transaction(c: _any_callable) -> _any_callable:
        @functools.wraps(c)
        async def wrap(self, *args, **kwargs):
            assert self.is_connected, "Database is not connected."
            con: asyncpg.Connection
            async with self._pool.acquire() as con:
                async with con.transaction():
                    await c(self, *args, con=con, **kwargs)

        return wrap

    # ! Example
    @in_transaction
    async def get_guild(self, guild_id: hikari.Snowflakeish, con: asyncpg.Connection):
        _LOGGER.info("works ig")
        _LOGGER.info(str(guild_id))
        _LOGGER.info(str(con))
        # return con.fetchrow(r"SELECT * FROM guilds WHERE guild_id = $1", int(guild_id))
