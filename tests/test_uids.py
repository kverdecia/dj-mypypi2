from unittest.mock import patch

import cuid

from django.test import TestCase

from djmypypi2 import uids


class TestUids(TestCase):
    def test_function_get_uid(self):
        uid = cuid.cuid()
        with patch('cuid.cuid') as mocked_cuid:
            mocked_cuid.return_value = uid
            self.assertEqual(uids.get_uid(), uid)
            mocked_cuid.assert_called_once()
