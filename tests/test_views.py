from http import HTTPStatus
from io import StringIO

import cuid

from django.urls import reverse
from django.http import Http404, request
from django.test import RequestFactory, TestCase

from djmypypi2 import models
from djmypypi2 import factories
from djmypypi2 import views


class TestPackageListView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse('djmypypi2:package-list')

    def test_view(self):
        package1: models.Package = factories.PackageFactory()
        package2: models.Package = factories.PackageFactory()
        package3: models.Package = factories.PackageFactory()

        view = views.PackageListView.as_view()
        request = self.factory.get(self.url)
        response = view(request)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, f'<a href="{package1.get_absolute_url()}">{package1.name}</a>')
        self.assertContains(response, f'<a href="{package2.get_absolute_url()}">{package2.name}</a>')
        self.assertContains(response, f'<a href="{package3.get_absolute_url()}">{package3.name}</a>')


class TestPackageDetailView(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_package_not_found(self):
        package_name = cuid.cuid()

        url = reverse('djmypypi2:package-detail', kwargs={'package_name': package_name})
        view = views.PackageDetailView.as_view()
        request = self.factory.get(url)
        self.assertRaises(Http404, view, request, package_name=package_name)

    def test_ok(self):
        package: models.Package = factories.PackageFactory()
        with self.settings(DEFAULT_FILE_STORAGE='tests.mock_storage.StorageMock'):
            version1: models.Version = factories.VersionFactory(package=package)
            version1.archive.save(version1.archive_name, StringIO(cuid.cuid()), save=True)
            version2: models.Version = factories.VersionFactory(package=package)
            version2.archive.save(version2.archive_name, StringIO(cuid.cuid()), save=True)
        url = reverse('djmypypi2:package-detail', kwargs={'package_name': package.name})
        view = views.PackageDetailView.as_view()
        request = self.factory.get(url)
        response = view(request, package_name=package.name)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, package.name)
        self.assertContains(response, package.summary)
        self.assertContains(response, version1.archive_name)
        self.assertContains(response, version2.archive_name)
