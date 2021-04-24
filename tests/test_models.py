#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest.mock import patch

import cuid

from django.test import TestCase
from django.contrib.auth import get_user_model

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
