# -*- coding: utf-8 -*-

from openregistry.api.tests.base import snitch


from .asset import (
    patch_asset,
    asset_concierge_patch,
    administrator_change_delete_status,
    administrator_change_complete_status
)


class AssetResourceTestMixin(object):
    """ Mixin with common tests for Basic Asset and Compound Asset
    """
    test_08_patch_asset = snitch(patch_asset)
    test_09_asset_concierge_patch = snitch(asset_concierge_patch)
    test_10_administrator_change_delete_status = snitch(administrator_change_delete_status)
    test_11_administrator_change_complete_status = snitch(administrator_change_complete_status)
