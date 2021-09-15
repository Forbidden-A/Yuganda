import logging
import edgedb
from yuganda.config.models import EdgeDBConfig

_LOGGER = logging.getLogger()


async def initialise_database(config: EdgeDBConfig):
    # edgedb://user:pass@host:port/database?option=value
    data_pool = edgedb.asyncio_pool.create_async_pool(**config.to_dict())
    return data_pool
