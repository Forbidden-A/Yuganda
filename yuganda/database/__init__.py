import logging
from yuganda.config.models import PostgresConfig
import asyncpg

_LOGGER = logging.getLogger()


async def initialise_database(config: PostgresConfig):
    data_pool = asyncpg.create_pool(**config.to_dict())
    return data_pool
