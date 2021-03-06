# Generated by Django 3.2 on 2021-04-24 06:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djmypypi2.uids


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(default=djmypypi2.uids.get_uid, editable=False, max_length=40, unique=True, verbose_name='UID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('version', models.CharField(max_length=20, verbose_name='Version')),
                ('author', models.CharField(blank=True, default='', max_length=100, verbose_name='Author')),
                ('author_email', models.CharField(blank=True, default='', max_length=100, verbose_name='Author email')),
                ('maintainer', models.CharField(blank=True, default='', max_length=100, verbose_name='Maintainer')),
                ('maintainer_email', models.CharField(blank=True, default='', max_length=100, verbose_name='Maintainer email')),
                ('summary', models.TextField(blank=True, default='', verbose_name='Summary')),
                ('description', models.TextField(blank=True, default='', verbose_name='Description')),
                ('home_page', models.URLField(blank=True, default='', max_length=255, verbose_name='Homepage')),
                ('license', models.TextField(blank=True, default='', max_length=20, verbose_name='License')),
                ('classifiers', models.TextField(blank=True, default='', verbose_name='Classifiers')),
                ('last_uploaded', models.DateTimeField(auto_now=True, verbose_name='Last uploaded')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='python_packages', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Package',
                'verbose_name_plural': 'Packages',
            },
        ),
    ]
