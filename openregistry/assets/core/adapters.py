# -*- coding: utf-8 -*-
from openprocurement.api.adapters import ContentConfigurator
from openprocurement.api.utils import error_handler


class AssetConfigurator(ContentConfigurator):
    """ Asset configuration adapter """

    name = "Asset Configurator"
    model = None


class AssetManagerAdapter(object):
    name = "Asset Manager"
    context = None

    def __init__(self, context):
        self.context = context

    def _validate(self, request, validators):
        kwargs = {'request': request, 'error_handler': error_handler}
        for validator in validators:
            validator(**kwargs)

    def create_asset(self, request):
        pass

    def change_asset(self, request):
        pass