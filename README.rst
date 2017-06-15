==================
G3W-ADMIN-CACHING
==================

G3W-ADMIN-CACHING module for caching layers data by tilestache (http://tilestache.org/).

Requirements
------------

* tilestache

Installation
------------

Add like git submodule from main g3w-admin directory

::

     git submodule add -f https://<user>@bitbucket.org/gis3w/g3w-admin-caching.git g3w-admin/caching


Install pip requirements.txt:

::

    pip install g3w-admin/caching/requirements.txt

Add caching module to G3W_LOCAL_MORE_APPS config value inside local_settings.py:

::

    G3WADMIN_LOCAL_MORE_APPS = [
        ...
        'caching'
        ...
    ]



Apply migrations:

To build cadastre_config on to 'default' database:

::

    ./manage.py migrate cadastre



