import logging
from quart import Quart, request, jsonify


logger = logging.getLogger(__name__)
app = Quart(__name__)


@app.route("/ping")
async def ping():
    logger.debug("Ping request received")
    return {"message": "pong"}
