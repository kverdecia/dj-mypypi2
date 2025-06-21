from djmypypi2 import models
import cuid
import factory
import factory.fuzzy

from django.contrib.auth import get_user_model


User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.fuzzy.FuzzyText()

    email = factory.declarations.LazyAttribute(lambda obj: f'{obj.username}@{cuid.cuid()}.com')
    first_name = factory.declarations.LazyAttribute(lambda obj: obj.username.capitalize())
    last_name = factory.fuzzy.FuzzyText()

    class Meta:
        model = User


class PackageFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    version = factory.fuzzy.FuzzyText(length=6)
    user = factory.declarations.LazyAttribute(lambda obj: UserFactory())
    author = factory.fuzzy.FuzzyText()
    author_email = factory.declarations.LazyAttribute(lambda obj: f'{obj.author}@{cuid.cuid()}.com')
    maintainer = factory.fuzzy.FuzzyText()
    maintainer_email = factory.declarations.LazyAttribute(lambda obj: f'{obj.maintainer}@{cuid.cuid()}.com')
    summary = factory.fuzzy.FuzzyText()
    description = factory.fuzzy.FuzzyText()
    home_page = factory.declarations.LazyAttribute(lambda obj: f'https://github.com/{obj.user.username}/{obj.name}')
    license = factory.fuzzy.FuzzyText()
    classifiers = factory.fuzzy.FuzzyText()

    class Meta:
        model = models.Package


class VersionFactory(factory.django.DjangoModelFactory):
    package = factory.declarations.LazyAttribute(lambda obj: PackageFactory())
    version = factory.fuzzy.FuzzyInteger(0, 10)
    author = factory.fuzzy.FuzzyText()
    author_email = factory.declarations.LazyAttribute(lambda obj: f'{cuid.cuid()}@{cuid.cuid()}.com')
    maintainer = factory.fuzzy.FuzzyText()
    maintainer_email = factory.declarations.LazyAttribute(lambda obj: f'{cuid.cuid()}@{cuid.cuid()}.com')
    summary = factory.fuzzy.FuzzyText()
    description = factory.fuzzy.FuzzyText()
    home_page = factory.declarations.LazyAttribute(lambda obj: f'htts://{cuid.cuid()}.com')
    license = factory.fuzzy.FuzzyText()
    md5_digest = factory.fuzzy.FuzzyText()
    archive_name = factory.fuzzy.FuzzyText()

    class Meta:
        model = models.Version
