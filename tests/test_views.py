from http import HTTPStatus
from io import StringIO

import cuid

from django.urls import reverse
from django.http import Http404
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
        with self.settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage'):
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
        url1 = reverse('djmypypi2:download-package', kwargs={'archive_name': version1.archive_name})
        self.assertContains(response, url1)
        self.assertContains(response, version2.archive_name)
        url2 = reverse('djmypypi2:download-package', kwargs={'archive_name': version2.archive_name})
        self.assertContains(response, url2)


class TestDownloadArchiveView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_not_found(self):
        archive_name = cuid.cuid()
        url = reverse('djmypypi2:download-package', kwargs={'archive_name': archive_name})
        request = self.factory.get(url)
        self.assertRaises(Http404, views.download_package, request, archive_name)

    def test_ok(self):
        with self.settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage'):
            archive = StringIO(cuid.cuid())
            version: models.Version = factories.VersionFactory()
            version.archive.save(version.archive_name, archive, save=True)
            archive.seek(0)
            url = reverse('djmypypi2:download-package', kwargs={'archive_name': version.archive_name})
            response = self.client.get(url)
            for chunk in response.streaming_content:
                content = chunk.decode('utf-8')
                break
            self.assertEqual(archive.getvalue(), content)
