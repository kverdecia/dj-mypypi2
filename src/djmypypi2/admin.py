# -*- coding: utf-8 -*-
"Admin interface for models of package dj-mypypi"
from typing import Any
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _
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
        (_("Maintenance"), {
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


@admin.register(models.Token)
class TokenAdmin(admin.ModelAdmin):
    "Admin interface for the token model"
    list_display = ('uid', 'name')

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).filter(user=request.user)

    def get_fields(self, request: HttpRequest, obj: models.Token | None = None) -> list[str | list[str] | tuple[str, ...] | tuple[()]] | tuple[str | list[str] | tuple[str, ...] | tuple[()], ...] | tuple[()]:
        if obj is None:
            return ('name',)
        return ('uid', 'name', 'token')

    def get_readonly_fields(self, request: HttpRequest, obj: models.Token | None = None) -> list[str] | tuple[str, ...] | tuple[()]:
        if obj:
            return ('uid', 'token')
        return super().get_readonly_fields(request, obj)

    def save_model(self, request: HttpRequest, obj: models.Token, form: Any, change: Any) -> None:
        obj.user = request.user
        return super().save_model(request, obj, form, change)
