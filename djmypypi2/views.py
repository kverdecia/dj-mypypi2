"Views for a python package index"
from django.http import FileResponse
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from . import models


class PackageListView(ListView):
    "Python package index view"
    template_name = 'djmypypi2/package-list.html'
    queryset = models.Package.objects.order_by('name')


class PackageDetailView(DetailView):
    "Python package view"
    template_name = 'djmypypi2/package-detail.html'
    model = models.Package
    slug_field = 'name'
    slug_url_kwarg = 'package_name'


def download_package(request, archive_name) -> FileResponse:
    "Handler to download a package"
    version = get_object_or_404(models.Version, archive_name=archive_name)
    version.archive.open()
    return FileResponse(version.archive, as_attachment=True, filename=archive_name)
