# -*- coding: utf-8 -*-
"Admin interface for models of package dj-mypypi"
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from . import models


class VersionInline(admin.TabularInline):
    "Admin interface for version model."
    fields = ('version', 'archive_name', 'archive', 'md5_digest', 'uploaded')
    readonly_fields = fields
    model = models.Version


@admin.register(models.Package)
class PackageAdmin(admin.ModelAdmin):
    "Admin interface for the package model"
    list_display = ('name', 'version', 'author', 'author_email', 'license', 'last_uploaded')

    fieldsets = (
        (None, {
            'fields': ('name', 'version', 'summary', 'user', 'last_uploaded'),
        }),
        (_("Maintainance"), {
            'fields': ('author', 'author_email', 'maintainer', 'maintainer_email')
        }),
        (_("Description"), {
            'fields': ('description', 'home_page', 'license', 'classifiers')
        }),
    )

    readonly_fields = ('name', 'version', 'summary', 'user', 'last_uploaded',
        'author', 'author_email', 'maintainer', 'maintainer_email',  # pylint: disable=bad-continuation
        'description', 'home_page', 'license', 'classifiers')  # pylint: disable=bad-continuation

    inlines = [VersionInline]

    def has_add_permission(self, request):
        return False

    def has_view_permission(self, request, obj=None):
        if not super().has_view_permission(request, obj):
            return False
        return True
