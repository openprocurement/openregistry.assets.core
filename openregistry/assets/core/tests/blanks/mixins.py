# -*- coding: utf-8 -*-

from openprocurement.api.tests.base import snitch
from openprocurement.api.tests.blanks.mixins import (
    ResourceTestMixin,  # noqa forwarded import
    ResourceDocumentTestMixin  # noqa forwarded import
)
from .asset import (
    # AssetResourceTest
    patch_asset,
    asset_concierge_patch,
    administrator_change_delete_status,
    administrator_change_complete_status,
    # AssetTest
    simple_add_asset,
    # AssetWorkflowTest
    change_draft_asset,
    change_pending_asset,
    change_verification_asset,
    change_active_asset,
    change_deleted_asset,
    change_complete_asset,
    patch_decimal_quantity,
)


class BaseAssetResourceTestMixin(object):
    """ Mixin with common tests for Basic Asset and Compound Asset
    """
    test_08_patch_asset = snitch(patch_asset)
    test_09_asset_concierge_patch = snitch(asset_concierge_patch)
    test_10_administrator_change_delete_status = snitch(administrator_change_delete_status)
    test_11_administrator_change_complete_status = snitch(administrator_change_complete_status)

    test_simple_add_test = snitch(simple_add_asset)

    test_12_check_draft_asset = snitch(change_draft_asset)
    test_13_check_pending_asset = snitch(change_pending_asset)
    test_14_check_verification_asset = snitch(change_verification_asset)
    test_15_check_active_asset = snitch(change_active_asset)
    test_16_check_deleted_asset = snitch(change_deleted_asset)
    test_17_check_complete_asset = snitch(change_complete_asset)

class AssetResourceTestMixin(BaseAssetResourceTestMixin):
    """ Mixin with common tests for Basic Asset and Compound Asset
    """
    test_18_patch_patch_decimal_quantity = snitch(patch_decimal_quantity)
