import logging
import edgedb
from yuganda.config.models import EdgeDBConfig

_LOGGER = logging.getLogger()


async def initialise_database(config: EdgeDBConfig):
    # edgedb://user:pass@host:port/database?option=value
    dns = f"edgedb://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}"
    data_pool = await edgedb.asyncio_pool.create_async_pool(dns)
    return data_pool
