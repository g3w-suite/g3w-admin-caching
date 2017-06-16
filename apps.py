from django.apps import AppConfig

# init tilestache config.obj
tilestache_cfg = None


class CachingConfig(AppConfig):

    name = 'caching'
    verbose_name = 'Caching'

    def ready(self):

        # import signal handlers
        import caching.receivers

        # init tilestache config.obj
        from .utils import TilestacheConfig
        caching.utils.tilestache_cfg = TilestacheConfig("caching/tilestache.cfg")



