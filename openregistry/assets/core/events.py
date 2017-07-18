# -*- coding: utf-8 -*-


class AssetInitializeEvent(object):
    """ Asset initialization event. """

    def __init__(self, asset):
        self.asset = asset
