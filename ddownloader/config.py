import logging
import os
from dotenv import load_dotenv

load_dotenv()


def app_env():
    return os.getenv("APP_ENV", "prod")


def app_port():
    return os.getenv("APP_PORT")


def db_host():
    return os.getenv("DB_HOST")


def db_port():
    return os.getenv("DB_PORT")


def db_user():
    return os.getenv("DB_USERNAME")


def db_password():
    return os.getenv("DB_PASSWORD")


def db_name():
    return os.getenv("DB_NAME")


def galleries_path():
    return os.getenv("GALLERIES_PATH")


def config_path():
    return os.getenv("CONFIG_PATH", "config")


def runtime_path():
    return os.path.join(config_path(), "runtime")


def logs_path():
    """
    Path to directory for log files.

    Returns:
        str: Path to logs directory.
    """
    return os.path.join(runtime_path(), "logs")


def log_level():
    raw_level = os.getenv("LOG_LEVEL", "INFO").upper()

    if raw_level == "DEBUG":
        return logging.DEBUG
    elif raw_level == "INFO":
        return logging.INFO
    elif raw_level == "WARNING":
        return logging.WARNING
    elif raw_level == "ERROR":
        return logging.ERROR
    elif raw_level == "CRITICAL":
        return logging.CRITICAL

    else:
        raise logging.INFO


def api_key_hooks():
    return os.getenv("API_KEY_HOOKS")


def secret_key():
    return os.getenv("SECRET_KEY")


def web_auth_username():
    return os.getenv("WEB_AUTH_USERNAME")


def web_auth_password_hash():
    return os.getenv("WEB_AUTH_PASSWORD_HASH")


def session_lifetime_days():
    return int(os.getenv("SESSION_LIFETIME_DAYS", "7"))


def ct_monitoring_enabled():
    return os.getenv("CT_MONITORING_ENABLED", "false").lower() == "true"


def ct_api_url():
    return os.getenv("CT_API_URL")


def ct_api_key():
    return os.getenv("CT_API_KEY")

def app_base_url():
    return os.getenv("APP_BASE_URL", "http://localhost:5002")


def otel_svc_name():
    return os.getenv("OTEL_SERVICE_NAME", "ddownloader")
