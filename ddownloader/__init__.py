import logging
import ddownloader.config as cfg
from logging.handlers import RotatingFileHandler
from ddownloader import futils


_LOGGER_NAME = 'ddownloader'


class ShortenedNameFormatter(logging.Formatter):
    """
    Custom formatter that shortens logger names (package names) in log messages
    so that it shows the most relevant parts only and fits in a given lenght.

    Also the log level is padded with spaces when necessary so that it always
    uses same length
    """

    def __init__(self, fmt=None, datefmt=None, style='%'):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self._max_length = 30

    def format(self, record):
        """
        Formats the log record, shortening the logger name.
        """
        record.shortname = self.shorten_logger_name(record.name, self._max_length)
        record.levelname = record.levelname.ljust(7)
        return super().format(record)

    @staticmethod
    def shorten_logger_name(name, max_length=30):
        """
        Shortens a logger name (e.g., 'com.example.app.MyClass') to a maximum length,
        preserving the class name and shortening package names as much as possible
        within the given length.  It will show full package names if space is available.

        Args:
            name: The logger name (e.g., 'com.example.app.MyClass').
            max_length: The maximum length of the shortened name.

        Returns:
            The shortened logger name (e.g., 'c.e.app.MyClass' or 'com.example.app.MyClass').
        """
        if len(name) <= max_length:
            return name.ljust(max_length)

        parts = name.split('.')
        if len(parts) <= 1:
            return name.ljust(max_length)  # No shortening needed

        class_name = parts[-1]
        shortened_parts = []
        available_length = max_length - len(class_name) - 1  # -1 for the dot before class name
        if available_length <= 0:
            return class_name.ljust(max_length)

        total_shortened_length = 0
        for i, part in enumerate(parts[:-1]):
            if total_shortened_length + len(part) + (len(parts) -1 -i) <= available_length:
                shortened_parts.append(part + ".")
                total_shortened_length += len(part) + 1
            else:
                shortened_parts.append(part[0] + ".")
                total_shortened_length += 2

        shortened_name = ''.join(shortened_parts) + class_name

        if len(shortened_name) > max_length:
            return class_name.ljust(max_length)
        else:
            return shortened_name.ljust(max_length)


#################################################
# Setup logging to console

_ch = logging.StreamHandler()
_ch.setFormatter(ShortenedNameFormatter(
    fmt='%(asctime)s - %(shortname)s - %(levelname)s - %(message)s',

    # Consider longer format for prod: '%Y-%m-%d %H:%M:%S'
    datefmt='%b %d %H:%M:%S',
    style='%'
))

# Set up "ddownloader.*" loggers level
dl_logger = logging.getLogger(_LOGGER_NAME)
dl_logger.setLevel(cfg.log_level())
dl_logger.addHandler(_ch)


#################################################
# Setup logging to file

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


#################################################
# Logger for Quart access and error logs

quart_logger = logging.getLogger("quart.app")
quart_logger.setLevel(logging.INFO)

# Ensure the logs directory exists
futils.mkdirs(cfg.logs_path())

# Create a RotatingFileHandler
file_handler = RotatingFileHandler(
    filename=f"{ cfg.logs_path() }/quart_app.log",
    maxBytes=50 * 1024 * 1024,  # 50MB
    backupCount=5
)

# Reuse the ShortenedNameFormatter instance
file_handler.setFormatter(_ch.formatter)

# Remove other handlers and add the file handler
quart_logger.handlers = []
quart_logger.addHandler(file_handler)
