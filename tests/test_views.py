from http import HTTPStatus
from io import StringIO
import base64
import hashlib

import cuid

from django.urls import reverse
from django.http import Http404
from django.test import RequestFactory, TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

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


class TestUploadView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.username = cuid.cuid()
        self.password = cuid.cuid()
        user_passwd = f'{self.username}:{self.password}'.encode('utf-8')
        b64 = base64.b64encode(user_passwd).decode('ascii')
        self.authorization_header = f'Basic {b64}'

        name = cuid.cuid()
        version = '1.0.0'
        self.content = cuid.cuid().encode('utf-8')
        self.archive_name = f'{name}-{version}.tar.gz'
        md5_digest = str(hashlib.md5(self.content))
        self.url = reverse('djmypypi2:upload-package')
        self.params = {
            'content': SimpleUploadedFile(self.archive_name, self.content, content_type='application/tar+gzip'),
            'name': name,
            'version': version,
            'author': cuid.cuid(),
            'author_email': f'{cuid.cuid()}@{cuid.cuid()}.com',
            'maintainer': cuid.cuid(),
            'maintainer_email': f'{cuid.cuid()}@{cuid.cuid()}.com',
            'summary': cuid.cuid(),
            'description': cuid.cuid(),
            'home_page': f'https://{cuid.cuid()}.com',
            'license': cuid.cuid(),
            'classifiers': '\n'.join([cuid.cuid(), cuid.cuid()]),
            'md5_digest': md5_digest,
        }

        content_type = ContentType.objects.get_for_model(models.Package)
        self.permission_add_package = Permission.objects.get(
            codename='add_package',
            content_type=content_type,
        )


    def test_unauthenticated(self):
        response = self.client.post(self.url, self.params)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_wrong_authentication(self):
        response = self.client.post(self.url, self.params,
            HTTP_AUTHORIZATION=self.authorization_header)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_user_has_not_permission(self):
        user = User()
        user.username = self.username
        user.set_password(self.password)
        user.save()
        response = self.client.post(self.url, self.params,
            HTTP_AUTHORIZATION=self.authorization_header)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_user_has_permission(self):
        with self.settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage'):
            user = User()
            user.username = self.username
            user.set_password(self.password)
            user.save()
            user.user_permissions.add(self.permission_add_package)
            response = self.client.post(self.url, self.params,
                HTTP_AUTHORIZATION=self.authorization_header)
            self.assertEqual(response.status_code, HTTPStatus.OK)
            version: models.Version = models.Version.objects.first()
            package: models.Package = version.package
            self.assertEqual(package.name, self.params['name'])
            self.assertEqual(package.user, user)
            self.assertEqual(package.version, self.params['version'])
            self.assertEqual(version.version, self.params['version'])
            self.assertEqual(package.author, self.params['author'])
            self.assertEqual(version.author, self.params['author'])
            self.assertEqual(package.author_email, self.params['author_email'])
            self.assertEqual(version.author_email, self.params['author_email'])
            self.assertEqual(package.maintainer, self.params['maintainer'])
            self.assertEqual(version.maintainer, self.params['maintainer'])
            self.assertEqual(package.maintainer_email, self.params['maintainer_email'])
            self.assertEqual(version.maintainer_email, self.params['maintainer_email'])
            self.assertEqual(package.summary, self.params['summary'])
            self.assertEqual(version.summary, self.params['summary'])
            self.assertEqual(package.description, self.params['description'])
            self.assertEqual(version.description, self.params['description'])
            self.assertEqual(package.home_page, self.params['home_page'])
            self.assertEqual(version.home_page, self.params['home_page'])
            self.assertEqual(package.license, self.params['license'])
            self.assertEqual(version.license, self.params['license'])
            self.assertEqual(package.classifiers, self.params['classifiers'])
            self.assertEqual(version.classifiers, self.params['classifiers'])
            self.assertEqual(version.md5_digest, self.params['md5_digest'])
            self.assertEqual(version.archive_name, self.archive_name)
            self.assertEqual(version.archive.read(), self.content)
