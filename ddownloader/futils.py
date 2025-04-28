import os


class DirNotFoundError(Exception):
    """Custom exception for directory not found errors."""


class FileNotFoundError(Exception):
    """Custom exception for file not found errors."""


def assert_dir_exists(path: str) -> None:
    """Asserts that the directory exists.

    Args:
        path (str): The path to the directory.

    Raises:
        DirNotFoundError: If the directory does not exist.
    """
    if not os.path.isdir(path):
        raise DirNotFoundError(f"Directory '{path}' does not exist.")


def assert_file_exists(path: str) -> None:
    """Asserts that the file exists.

    Args:
        path (str): The path to the file.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File '{path}' does not exist.")
