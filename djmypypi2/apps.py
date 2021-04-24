# -*- coding: utf-8
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DjMyPypi2Config(AppConfig):
    name = 'djmypypi2'
    verbose_name = _("PyPi Server")
    default_auto_field = 'django.db.models.BigAutoField'
