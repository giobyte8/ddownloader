import logging
from quart import Quart
from .api_hooks import hooks_api
from .app_sources import sources_app


logger = logging.getLogger(__name__)
app = Quart(__name__)
app.register_blueprint(hooks_api, url_prefix="/api/hooks")
app.register_blueprint(sources_app, url_prefix="/sources")


@app.route("/ping")
async def ping():
    logger.debug("Ping request received")
    return {"message": "pong"}
