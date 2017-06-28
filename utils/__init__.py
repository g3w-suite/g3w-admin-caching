from django.conf import settings
from django.apps import apps
from django.http.request import QueryDict
from django.core.urlresolvers import reverse
from TileStache import parseConfig
from TileStache.Config import _parseConfigLayer
from TileStache.Caches import Disk
from caching.models import G3WCachingLayer
from django.apps import apps
from django.core.cache import cache
import shutil
import os
import fcntl
import logging

logger = logging.getLogger('g3wadmin.debug')


def get_config():
    """
    Get global config tielstache object
    :return:
    """
    logger.debug('PID {}'.format(os.getpid()))
    # check if file has exixst
    tilestache_cfg = apps.get_app_config('caching').tilestache_cfg
    logger.debug('ID Tielstache_cfg: {}'.format(id(tilestache_cfg)))

    if os.path.exists(tilestache_cfg.file_hash_name):
        cid = tilestache_cfg.read_hash_file()
        logger.debug('Read hash file: {}'.format(cid))
        if cid != tilestache_cfg.get_cache_hash():
            tilestache_cfg = TilestacheConfig()
            tilestache_cfg.set_cache_hash(cid)
            apps.get_app_config('caching').tilestache_cfg = tilestache_cfg
            logger.debug('Cache hush: {}'.format(tilestache_cfg.get_cache_hash()))
        else:
            logger.debug('Diverso')

    return tilestache_cfg

class TilestacheConfig(object):

    config_dict = dict()
    file_hash_name = 'tilestache_hash_file.txt'
    cache_key = 'tilestache_cfg_id'

    def __init__(self):

        self.cache_dict = self.init_cache_dict()
        self.config_dict.update({'cache': self.cache_dict})
        self.config = parseConfig(self.config_dict)
        try:
            self.init_layers()
        except:
            pass

    def init_cache_dict(self):

        if settings.TILESTACHE_CACHE_TYPE == 'Disk':
            return {
                'name': 'Disk',
                'path': getattr(settings, 'TILESTACHE_CACHE_DISK_PATH', 'tmp/tilestache_g3wsuite'),
                'umask': getattr(settings, 'TILESTACHE_CACHE_DISK_UMASK', '0000')
            }
        else:
            return {
                'name': 'Test'
            }

    def init_layers(self):
        """
        Add layers to tilestache config obj on startup
        :return:
        """

        # get caching layers activated
        caching_layers = G3WCachingLayer.objects.all()
        for caching_layer in caching_layers:
            self.add_layer(str(caching_layer), caching_layer)

    def build_layer_dict(self, caching_layer):

        #get layer object
        Layer = apps.get_app_config(caching_layer.app_name).get_model('layer')
        layer = Layer.objects.get(pk=caching_layer.layer_id)

        # build template
        base_tamplate = reverse('ows', kwargs={
            'group_slug': '0', # avoid a query
            'project_type': str(caching_layer.app_name),
            'project_id': str(layer.project.pk)
        })

        # build query dict fo tilestache
        q = QueryDict('', mutable=True)
        q['SERVICE'] = 'WMS'
        q['VERSION'] = '1.1.1'
        q['REQUEST'] = 'GetMap'
        q['BBOX'] = '$xmin,$ymin,$xmax,$ymax'
        q['SRS'] = '$srs'
        q['FORMAT'] = 'image/png'
        q['TRANSPARENT'] = 'true'
        q['LAYERS'] = layer.name
        q['WIDTH'] = '$width'
        q['HEIGHT'] = '$height'


        # build dict
        layer_dict = {
            'provider': {
                'name': 'url template',
                'template': '{}{}?{}'.format(settings.TILESTACHE_LAYERS_HOST, base_tamplate, q.urlencode(safe='$'))
            },
            'projection': 'caching.utils.projections:CustomXYZGridProjection(\'EPSG:{}\')'.
                format(layer.project.group.srid.auth_srid)
        }

        return layer_dict

    def add_layer(self, layer_key_name, caching_layer):
        """
        Add layer to tilestache config
        :param layer_key_name:
        :param layer_dict:
        :return:
        """
        self.config.layers[layer_key_name] = _parseConfigLayer(self.build_layer_dict(caching_layer), self.config,
                                                               dirpath='.')

    def remove_layer(self, layer_key_name):
        """
        Remove layer from tilestache config obj
        :param layer_key_name:
        :return: None
        """
        del(self.config.layers[layer_key_name])


    def erase_cache_layer(self, layer_key_name):
        """
        Delete cache by provder cache
        :param layer_key_name:
        :return:
        """

        if isinstance(self.config.cache, Disk):
            shutil.rmtree("{}/{}".format(self.config.cache.cachepath, layer_key_name), ignore_errors=True)

        # todo: for other cache type

    def set_cache_hash(self, cid):
        cache.set(self.cache_key, cid, None)

    def get_cache_hash(self):
        return cache.get(self.cache_key)

    def reset_cache_hash(self):
        cache.delete(self.cache_key)

    def save_hash_file(self, force=False):
        """
        Write has file for check tilestache config between processes
        :param force:
        :return:
        """

        cid = id(self)
        '''
        f = open(self.file_hash_name, 'w+')
        f.write(str(cid))
        f.close()
        '''

        with open(self.file_hash_name, "w") as f:
            logger.debug('PID salvo file')
            fcntl.flock(f, fcntl.LOCK_EX)
            f.write(str(cid))
            fcntl.flock(f, fcntl.LOCK_UN)

        self.set_cache_hash(cid)

    def read_hash_file(self):

        if os.path.exists(self.file_hash_name):
            f = open(self.file_hash_name, 'r')
            id = f.read()
            f.close()
            return int(id) if id else None
        else:
            return None



