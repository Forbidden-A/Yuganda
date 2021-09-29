# Heavily inspired by https://github.com/IkBenOlie5/Kangakari/
import logging
from yuganda.config import PostgresConfig
from yuganda.resources import get_resource

import asyncpg
from lightbulb import Bot
import typing
import functools
import asyncio
import hikari

__all__ = ["Database"]

_LOGGER = logging.getLogger("yuganda.database")

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
        self._connected.set()
        con: asyncpg.Connection
        async with self.pool.acquire() as con:
            async with con.transaction():
                schema: str
                with get_resource("schema.sql") as fp:
                    schema = fp.read()
                await con.execute(schema)

    async def close(self):
        assert self.is_connected, "Database is not connected."
        await self.pool.close()
        del self._pool
        self._connected.clear()
        _LOGGER.info("Closed the database.")

    @staticmethod
    def in_transaction(c: _any_callable) -> _any_callable:
        @functools.wraps(c)
        async def wrap(self, *args, **kwargs):
            assert self.is_connected, "Database is not connected."
            con: asyncpg.Connection
            async with self._pool.acquire() as con:
                async with con.transaction():
                    await c(self, *args, con=con, **kwargs)

        return wrap

    @in_transaction
    async def get_starred_message(
        self, message_id: hikari.Snowflakeish, con: asyncpg.Connection
    ):
        return dict(
            await con.fetchrow(
                r"SELECT * FROM yuganda.starred_messages WHERE message_id = $1",
                int(message_id),
            )
        )

    @in_transaction
    async def create_starred_message(
        self,
        message_id: hikari.Snowflakeish,
        followup_id: hikari.Snowflakeish,
        stars: int,
        con: asyncpg.Connection,
    ):
        await con.execute(
            r"INSERT INTO yuganda.starred_messages (message_id, followup_id, stars) VALUES ($1, $2, $3)",
            int(message_id),
            int(followup_id),
            stars,
        )

    @in_transaction
    async def update_starred_message(
        self, message_id: hikari.Snowflakeish, stars: int, con: asyncpg.Connection
    ):
        await con.execute(
            r"UPDATE yuganda.starred_messages SET stars = $2 WHERE message_id = $1",
            int(message_id),
            stars,
        )

    @in_transaction
    async def update_guild_options(
        self,
        guild_id: hikari.Snowflakeish,
        starboard_id: hikari.Snowflakeish,
        con: asyncpg.Connection,
    ):
        await con.execute(
            r"UPDATE yuganda.guild_options SET starboard_id = $2 WHERE guild_id = $1",
            int(guild_id),
            int(starboard_id) if starboard_id is not None else None,
        )

    @in_transaction
    async def insert_guild_options(
        self,
        guild_id: hikari.Snowflakeish,
        con: asyncpg.Connection,
        starboard_id: typing.Optional[hikari.Snowflakeish] = None,
    ):
        await con.execute(
            r"INSERT INTO yuganda.guild_options (guild_id, starboard_id) VALUES ($1, $2)",
            int(guild_id),
            int(starboard_id) if starboard_id is not None else None,
        )

    @in_transaction
    async def get_guild_options(
        self, guild_id: hikari.Snowflakeish, con: asyncpg.Connection
    ):
        return dict(
            await con.fetchrow(
                r"SELECT * FROM yuganda.guild_options WHERE guild_id = $1",
                int(guild_id),
            )
        )
