from flask_inputs.validators import ValidationError
from pathlib import Path
from pathvalidate import is_valid_filepath

from ddownloader.config_loader import downloads_dir


def safe_target_path(form, field):
    """Validates that value of relative_target_path is a valid
    local file URL, and that it does not contains '..'
    """

    TARGET_PATH_FN = 'relative_target_path'
    target_path: str = field.data.get(TARGET_PATH_FN, '')

    if not is_valid_filepath(target_path):
        raise ValidationError(f'{TARGET_PATH_FN} is not a valid file path')

    if '..' in target_path:
        raise ValidationError(f'{TARGET_PATH_FN} value is invalid')

def target_path_not_exists(form, field):
    """Validates that value of relative_target_path will not override
    an already existent file
    """
    TARGET_PATH_FN = 'relative_target_path'
    target_path: str = field.data.get(TARGET_PATH_FN, '')

    dest_file = Path(downloads_dir(), target_path)
    if dest_file.exists():
        raise ValidationError(f'Given {TARGET_PATH_FN} already exists')
