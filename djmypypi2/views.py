"Views for a python package index"
from django.views.generic import ListView, DetailView
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
