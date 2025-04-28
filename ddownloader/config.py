import os
from dotenv import load_dotenv

load_dotenv()


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
