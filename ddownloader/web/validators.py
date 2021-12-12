from flask_inputs.validators import ValidationError
from pathvalidate import is_valid_filepath


def safe_target_path(form, field):
    """Validates that value of target_path is a valid
    local file URL, and that it does not contains '..'
    """

    TARGET_PATH_FN = 'target_path'
    target_path: str = field.data.get(TARGET_PATH_FN, '')

    if not is_valid_filepath(target_path):
        raise ValidationError(f'{TARGET_PATH_FN} is not a valid file path')

    if '..' in target_path:
        raise ValidationError(f'{TARGET_PATH_FN} value is invalid')
