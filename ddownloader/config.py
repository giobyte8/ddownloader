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


def api_key_hooks():
    return os.getenv("API_KEY_HOOKS")


def ct_monitoring_enabled():
    return os.getenv("CT_MONITORING_ENABLED", "false").lower() == "true"


def ct_api_url():
    return os.getenv("CT_API_URL")


def ct_api_key():
    return os.getenv("CT_API_KEY")


def otel_svc_name():
    return os.getenv("OTEL_SERVICE_NAME", "ddownloader")
