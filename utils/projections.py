from ModestMaps.Core import Point


class CustomGridProjection(object):
    def __init__(self, xyz, srs):
        self.xyz = xyz
        self.srs = srs
        self.tilesize = 256
        self.resolutions = [2**(x+1) for x in list(reversed(range(15)))] + [1.0/2**x for x in range(10)]
        '''
        self.resolutions = [32768, 16384, 8192, 4096, 2048, 1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.0078125, 0.00390625, 0.001953125]
        queste risoluzioni sono quelle usate anche client su un extent [0,0,8388608,8388608], ovvero origin [0,0], tile 256px e risoluzione 32768
        '''
    def coordinateProj(self, coord):
        tile_meters = self.tilesize * self.resolutions[coord.zoom]
        row = (2**coord.zoom - coord.row) if self.xyz else coord.row
        px = coord.column * tile_meters
        py = row * tile_meters
        return Point(px, py)


class CustomXYZGridProjection(CustomGridProjection):
    def __init__(self, srs):
        CustomGridProjection.__init__(self, True, srs)


class CustomTMSGridProjection(CustomGridProjection):
    def __init__(self, srs):
        CustomGridProjection.__init__(self, False, srs)