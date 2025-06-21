import binascii
import functools
import base64

from django.contrib import auth

from . import models


def basic_authentication(func):
    "Decorator for http basic authentication on views."
    @functools.wraps(func)
    def _basic_authentication(request, *args, **kwargs):
        header_value = request.META.get('HTTP_AUTHORIZATION')
        if not header_value:
            return func(request, *args, **kwargs)
        if not header_value.startswith('Basic '):
            return func(request, *args, **kwargs)
        try:
            decoded_value = base64.b64decode(header_value[6:]).decode('utf8')
        except binascii.Error:
            return func(request, *args, **kwargs)
        value_items = decoded_value.split(':')
        if len(value_items) != 2:
            return func(request, *args, **kwargs)
        username, password = value_items
        if username == '__token__':
            try:
                token = models.Token.objects.get(token=password)
                user = token.user
            except models.Token.DoesNotExist:
                user = None
        else:
            user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        return func(request, *args, **kwargs)
    return _basic_authentication
