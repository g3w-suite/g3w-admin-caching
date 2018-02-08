#G3W-ADMIN-CACHING
G3W-ADMIN-CACHING module for caching layers data by tilestache (http://tilestache.org/).


Requirements
------------

* tilestache

Installation
------------

Add like git submodule from main g3w-admin directory

```bash
git submodule add -f https://<user>@bitbucket.org/gis3w/g3w-admin-caching.git g3w-admin/caching
```

Install pip requirements.txt:

```bash
pip install g3w-admin/caching/requirements.txt
```

Add caching module to G3W_LOCAL_MORE_APPS config value inside local_settings.py:

```python
G3WADMIN_LOCAL_MORE_APPS = [
    ...
    'caching',
    ...
]
```


Apply migrations:

```bash
    ./manage.py migrate caching
```

Add tilestache to django settings file

```python
...
TILESTACHE_CACHE_NAME = 'default'
TILESTACHE_CACHE_TYPE = 'Disk' # or 'Memcache'
TILESTACHE_CACHE_DISK_PATH = '/tmp/tilestache_cache/'
...
```