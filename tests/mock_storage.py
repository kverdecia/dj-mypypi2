from unittest.mock import MagicMock
from django.core.files.storage import Storage


def _generate_filename(filename):
    return filename


def _save(name, content, max_length):
    return name


def StorageMock(*args, mocked_url=None, **kwargs):
    result = MagicMock(spec=Storage, name='StorageMock')
    result.generate_filename = _generate_filename
    result.save = MagicMock(side_effect=_save)
    result.url = MagicMock(name='url')
    result.url.return_value = mocked_url or '/example.com/generated_filename.png'
    return result
