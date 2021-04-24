=============================
django app implementing pypi
=============================

.. image:: https://badge.fury.io/py/dj-mypypi2.svg
    :target: https://badge.fury.io/py/dj-mypypi2

.. image:: https://travis-ci.org/kverdecia/dj-mypypi2.svg?branch=master
    :target: https://travis-ci.org/kverdecia/dj-mypypi2

.. image:: https://codecov.io/gh/kverdecia/dj-mypypi2/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/kverdecia/dj-mypypi2

django app implementing pypi server

Documentation
-------------

The full documentation is at https://dj-mypypi2.readthedocs.io.

Quickstart
----------

Install django app implementing pypi::

    pip install dj-mypypi2

Add it to your `INSTALLED_APPS`:

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

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
