# -*- coding: utf-8 -*-
"Model definition for the python package index"
import os.path
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models

from . import uids


class UIDManager(models.Manager):
    def get_by_natural_key(self, uid):
        return self.get(uid=uid)


class Package(models.Model):
    "Model for saving packages"
    objects = UIDManager()

    uid = models.CharField(_("UID"), max_length=40, default=uids.get_uid, editable=False, unique=True)
    name = models.CharField(_("Name"), max_length=100, unique=True)
    version = models.CharField(_("Version"), max_length=20)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"),
        on_delete=models.CASCADE, related_name='python_packages') # pylint: disable=bad-continuation

    author = models.CharField(_("Author"), max_length=100, blank=True, default='')
    author_email = models.CharField(_("Author email"), max_length=100, blank=True, default='')
    maintainer = models.CharField(_("Maintainer"), max_length=100, blank=True, default='')
    maintainer_email = models.CharField(_("Maintainer email"), max_length=100,
        blank=True, default='') # pylint: disable=bad-continuation

    summary = models.TextField(_("Summary"), blank=True, default='')
    description = models.TextField(_("Description"), blank=True, default='')
    home_page = models.URLField(_("Homepage"), max_length=255, blank=True, default='')
    license = models.TextField(_("License"), max_length=20, blank=True, default='')
    classifiers = models.TextField(_("Classifiers"), blank=True, default='')

    last_uploaded = models.DateTimeField(_("Last uploaded"), auto_now=True)

    class Meta:
        verbose_name = _("Package")
        verbose_name_plural = _("Packages")

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.uid,)
