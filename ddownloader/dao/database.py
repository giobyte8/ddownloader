import ddownloader.config as cfg
import logging
from tortoise import Tortoise


logger = logging.getLogger(__name__)


async def init():
    logger.debug("Initializing Tortoise ORM")
    pg_url = (
        f"psycopg://{ cfg.db_user() }:{ cfg.db_password() }@"
        f"{ cfg.db_host() }:{ cfg.db_port() }/{ cfg.db_name() }"
    )

    await Tortoise.init(
        db_url=pg_url,
        modules={"models": ["ddownloader.dao.tortoise.models"]},
        _enable_global_fallback=True,
    )


async def shutdown():
    logger.debug("Shutting down Tortoise ORM")
    await Tortoise.close_connections()
