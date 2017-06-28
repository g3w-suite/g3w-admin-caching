from django.apps import AppConfig
import os
import logging



class CachingConfig(AppConfig):

    name = 'caching'
    verbose_name = 'Caching'

    def ready(self):

        # import signal handlers
        import caching.receivers

        # init tilestache config.obj
        logger = logging.getLogger('g3wadmin.debug')
        logger.debug('PID APPS {}'.format(os.getpid()))
        from .utils import TilestacheConfig
        self.tilestache_cfg = TilestacheConfig()
        self.tilestache_cfg.save_hash_file()



