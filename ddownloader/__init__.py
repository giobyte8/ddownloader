import logging

_LOGGER_NAME = 'ddownloader'
_FORMATTER = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


logger = logging.getLogger(_LOGGER_NAME)
logger.setLevel(logging.DEBUG)

# Console handler setup
_ch = logging.StreamHandler()
_ch.setLevel(logging.DEBUG)
_ch.setFormatter(_FORMATTER)
logger.addHandler(_ch)

# TODO Setup an appropriate mechanism
# Rotating file handler setup
#futils.ensure_dir_existence(cfg.logs_path())
# _fh = RotatingFileHandler(
#     os.path.join(cfg.logs_path(), _LOG_FILENAME),
#     maxBytes=1024 * 1024 * 50,
#     backupCount=5,
#     encoding='utf-8'
# )
# _fh.setLevel(file_level)
# _fh.setFormatter(_FORMATTER)
#logger.addHandler(_fh)