import logging
from quart import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from .auth import SESSION_KEY, verify_credentials

auth_app = Blueprint("auth", __name__)
logger = logging.getLogger(__name__)


def _safe_next_url(next_url: str | None) -> str:
    """Only allow redirecting to relative, in-app paths.

    Guards against open-redirect attacks via a crafted ``next`` value.
    """
    if next_url and next_url.startswith("/") and not next_url.startswith("//"):
        return next_url

    return url_for("sources.all")


@auth_app.route("/login", methods=["GET"])
async def login():
    if session.get(SESSION_KEY):
        return redirect(_safe_next_url(request.args.get("next")))

    return await render_template(
        "login.html",
        next=request.args.get("next", ""),
    )


@auth_app.route("/login", methods=["POST"])
async def login_submit():
    form = await request.form
    username = form.get("username", "")
    password = form.get("password", "")
    next_url = form.get("next", "")

    if verify_credentials(username, password):
        session.clear()
        session[SESSION_KEY] = True
        session.permanent = True
        return redirect(_safe_next_url(next_url))

    logger.warning("Failed web login attempt for username: %s", username)
    return await render_template(
        "login.html",
        next=next_url,
        username=username,
        error="Invalid username or password.",
    ), 401


@auth_app.route("/logout", methods=["GET"])
async def logout():
    session.clear()
    return redirect(url_for("auth.login"))
