import pytest
from flask_inputs.validators import ValidationError
from unittest.mock import Mock

from ddownloader.web.validators import safe_target_path


def test_safe_target_path_not_string():
    mock_field = Mock()

    mock_field.data = {'target_path': 45}
    with pytest.raises(ValidationError):
        safe_target_path(None, mock_field)

    mock_field.data['target_path'] = []
    with pytest.raises(ValidationError):
        safe_target_path(None, mock_field)


def test_safe_target_path_empty():
    mock_field = Mock()

    mock_field.data = {'target_path': ' '}
    with pytest.raises(ValidationError):
        safe_target_path(None, mock_field)

    mock_field.data['target_path'] = ''
    with pytest.raises(ValidationError):
        safe_target_path(None, mock_field)


def test_safe_target_path_double_dot():
    mock_field = Mock()

    mock_field.data = {'target_path': '../System32/test.sh'}
    with pytest.raises(ValidationError):
        safe_target_path(None, mock_field)

    mock_field.data = {'target_path': '/System32/test.sh'}
    with pytest.raises(ValidationError):
        safe_target_path(None, mock_field)


def test_safe_target_path():
    mock_field = Mock()

    # Try with a valid paths, exception must not be raised

    mock_field.data = {'target_path': 'System32/test.sh'}
    safe_target_path(None, mock_field)

    mock_field.data = {'target_path': 'test.sh'}
    safe_target_path(None, mock_field)
    
    mock_field.data['target_path'] = 'nrhioervfhuoefrvuhgi452'
    safe_target_path(None, mock_field)

    mock_field.data['target_path'] = '9/8/7/6/5/4/3/'
    safe_target_path(None, mock_field)
