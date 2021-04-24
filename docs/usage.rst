=====
Usage
=====

To use django app implementing pypi in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'djmypypi2.apps.DjMyPypi2Config',
        ...
    )

Add django app implementing pypi's URL patterns:

.. code-block:: python

    from djmypypi2 import urls as djmypypi2_urls


    urlpatterns = [
        ...
        url(r'^', include(djmypypi2_urls)),
        ...
    ]
