import logging
from datetime import timedelta
from quart import Quart
from ddownloader import config as cfg
from .api_hooks import hooks_api
from .app_sources import sources_app
from .auth_app import auth_app


logger = logging.getLogger(__name__)
app = Quart(
    __name__,
    static_folder="static",
    static_url_path="/static",
)

app.secret_key = cfg.secret_key()
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(
    days=cfg.session_lifetime_days()
)
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = cfg.app_env() in ["prod", "production"]
app.config["SESSION_COOKIE_HTTPONLY"] = True

app.register_blueprint(hooks_api, url_prefix="/api/hooks")
app.register_blueprint(sources_app, url_prefix="/sources")
app.register_blueprint(auth_app)


@app.route("/ping")
async def ping():
    logger.debug("Ping request received")
    return {"message": "pong"}
