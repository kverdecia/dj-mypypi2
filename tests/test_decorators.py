import base64
from unittest.mock import Mock, MagicMock, patch

import cuid

import django.contrib.auth
from django.test import RequestFactory, TestCase

from djmypypi2 import decorators


class TestBasicAuthDecorator(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.mocked_view = Mock().view
        self.decorated_view = decorators.basic_authentication(self.mocked_view)

    @patch('django.contrib.auth.login')
    @patch('django.contrib.auth.authenticate')
    def test_authorization_not_provided(self, authenticate_mock: MagicMock, login_mock: MagicMock):
        request = self.factory.post('/mypypi2/@upload')
        self.decorated_view(request)
        self.mocked_view.assert_called_with(request)
        authenticate_mock.assert_not_called()
        login_mock.assert_not_called()

    @patch('django.contrib.auth.login')
    @patch('django.contrib.auth.authenticate')
    def test_authorization_not_basic_auth(self, authenticate_mock: MagicMock, login_mock: MagicMock):
        request = self.factory.post('/mypypi2/@upload', HTTP_AUTHORIZATION=cuid.cuid())
        self.decorated_view(request)
        self.mocked_view.assert_called_with(request)
        authenticate_mock.assert_not_called()
        login_mock.assert_not_called()

    @patch('django.contrib.auth.login')
    @patch('django.contrib.auth.authenticate')
    def test_authorization_basic_auth_wrong_format(self, authenticate_mock: MagicMock, login_mock: MagicMock):
        header = f'Basic {cuid.cuid()}'
        request = self.factory.post('/mypypi2/@upload', HTTP_AUTHORIZATION=header)
        self.decorated_view(request)
        self.mocked_view.assert_called_with(request)
        authenticate_mock.assert_not_called()
        login_mock.assert_not_called()

    @patch('django.contrib.auth.login')
    @patch('django.contrib.auth.authenticate')
    def test_authorization_basic_auth_wrong_format2(self, authenticate_mock: MagicMock, login_mock: MagicMock):
        text = cuid.cuid().encode('utf-8')
        b64 = base64.b64encode(text).decode('ascii')
        header = f'Basic {b64}'
        request = self.factory.post('/mypypi2/@upload', HTTP_AUTHORIZATION=header)
        self.decorated_view(request)
        self.mocked_view.assert_called_with(request)
        authenticate_mock.assert_not_called()
        login_mock.assert_not_called()

    @patch('django.contrib.auth.login')
    @patch('django.contrib.auth.authenticate')
    def test_authorization_basic_auth_ok(self, authenticate_mock: MagicMock, login_mock: MagicMock):
        username = cuid.cuid()
        password = cuid.cuid()
        text = f'{username}:{password}'.encode('utf-8')
        b64 = base64.b64encode(text).decode('ascii')
        header = f'Basic {b64}'
        request = self.factory.post('/mypypi2/@upload', HTTP_AUTHORIZATION=header)
        authenticate_mock.return_value = Mock()
        self.decorated_view(request)
        self.mocked_view.assert_called_with(request)
        authenticate_mock.assert_called_once_with(request, username=username, password=password)
        login_mock.assert_called_once_with(request, authenticate_mock.return_value)
