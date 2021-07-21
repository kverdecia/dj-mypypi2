import cuid

from django.urls import reverse, resolve
from django.test import TestCase

from djmypypi2 import models
from djmypypi2 import factories


class TestUrls(TestCase):
    def test_package_list_reverse(self):
        url = reverse('djmypypi2:package-list')
        self.assertEqual(url, '/mypypi2/')

    def test_package_list_resolve(self):
        view_name = resolve('/mypypi2/').view_name
        self.assertEqual(view_name, 'djmypypi2:package-list')

    def test_package_detail_reverse(self):
        package: models.Package = factories.PackageFactory()

        url = reverse('djmypypi2:package-detail', kwargs={'package_name': package.name})
        self.assertEqual(url, f'/mypypi2/{package.name}/')

    def test_package_detail_resolve(self):
        package: models.Package = factories.PackageFactory()

        view_name = resolve(f'/mypypi2/{package.name}/').view_name
        self.assertEqual(view_name, 'djmypypi2:package-detail')

    def test_download_reverse(self):
        version: models.Version = factories.VersionFactory()

        url = reverse('djmypypi2:download-package', kwargs={'archive_name': version.archive_name})
        self.assertEqual(url, f'/mypypi2/@download/{version.archive_name}')

    def test_download_resolve(self):
        version: models.Version = factories.VersionFactory()

        view_name = resolve(f'/mypypi2/@download/{version.archive_name}').view_name
        self.assertEqual(view_name, 'djmypypi2:download-package')
