#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest.mock import Mock, patch

import cuid

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase

from djmypypi2 import models
from djmypypi2 import factories


User = get_user_model()


class TestPackageModel(TestCase):
    def test_default_attributes(self):
        uid = cuid.cuid()
        with patch('cuid.cuid') as mocked_cuid:
            mocked_cuid.return_value = uid
            package = models.Package()
            mocked_cuid.assert_called_once()
            self.assertEqual(package.uid, uid)
            self.assertEqual(package.name, '')
            self.assertEqual(package.version, '')
            self.assertRaises(User.DoesNotExist, lambda: package.user)
            self.assertEqual(package.author, '')
            self.assertEqual(package.author_email, '')
            self.assertEqual(package.maintainer, '')
            self.assertEqual(package.maintainer_email, '')
            self.assertEqual(package.summary, '')
            self.assertEqual(package.description, '')
            self.assertEqual(package.home_page, '')
            self.assertEqual(package.license, '')
            self.assertEqual(package.classifiers, '')
            self.assertIsNone(package.last_uploaded)

    def test_method_str(self):
        package = models.Package()
        package.name = cuid.cuid()
        self.assertEqual(str(package), package.name)
        self.assertEqual(package.__str__(), package.name)

    def test_create_with_factory(self):
        factories.PackageFactory()

    def test_method_natural_key(self):
        package: models.Package = factories.PackageFactory()

        self.assertEqual(package.natural_key(), (package.uid,))

    def test_get_by_natural_key(self):
        package: models.Package = factories.PackageFactory()
        found = models.Package.objects.get_by_natural_key(*package.natural_key())

        self.assertEqual(package.pk, found.pk)

    def test_method_get_absolute_url(self):
        package: models.Package = factories.PackageFactory()

        url = reverse('djmypypi2:package-detail', kwargs={'package_name': package.name})
        self.assertEqual(package.get_absolute_url(), url)


class TestVersionModel(TestCase):
    def test_function_upload_version_to(self):
        mocked_version = Mock()
        package_name = cuid.cuid()
        file_name = f'{cuid.cuid()}.tar.gz'
        mocked_version.package.name = package_name
        self.assertEqual(models.upload_version_to(mocked_version, file_name),
            f'{package_name}/{file_name}')
        
    def test_default_attributes(self):
        version = models.Version()
        self.assertRaises(models.Package.DoesNotExist, lambda: version.package)
        self.assertEqual(version.version, '')
        self.assertEqual(version.author, '')
        self.assertEqual(version.author_email, '')
        self.assertEqual(version.maintainer, '')
        self.assertEqual(version.maintainer_email, '')
