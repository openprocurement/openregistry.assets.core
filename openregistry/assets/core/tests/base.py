# -*- coding: utf-8 -*-
from datetime import datetime
from copy import deepcopy
from uuid import uuid4

from openprocurement.api.tests.base import (
    BaseResourceWebTest,
    snitch,  # noqa forwarded import
    DumpsTestAppwebtest,  # noqa forwarded import
    PrefixedRequestClass,  # noqa forwarded import
    create_blacklist, # noqa forwarded import
)
from openprocurement.api.tests.blanks.json_data import (
    test_document_data,  # noqa forwarded import
    test_asset_basic_data,  # noqa forwarded import
    test_asset_basic_data_with_schema,  # noqa forwarded import
    test_asset_claimrights_data,  # noqa forwarded import
    test_asset_compound_data,  # noqa forwarded import
    test_asset_compound_data_060,  # noqa forwarded import
    test_asset_compound_data_341  # noqa forwarded import
)


now = datetime.now()

from openprocurement.api.tests.base import MOCK_CONFIG as BASE_MOCK_CONFIG
from openregistry.assets.core.tests.fixtures import PARTIAL_MOCK_CONFIG
from openprocurement.api.utils import connection_mock_config

MOCK_CONFIG = connection_mock_config(PARTIAL_MOCK_CONFIG, ('plugins',), BASE_MOCK_CONFIG)


class BaseAssetWebTest(BaseResourceWebTest):

    resource_name = 'assets'
    mock_config = MOCK_CONFIG

class AssetTransferWebTest(BaseAssetWebTest):
    initial_lots = None

    def setUp(self):
        super(AssetTransferWebTest, self).setUp()   
        self.create_resource()
        self.asset_blank = self.app.RequestClass.blank
        self.app.RequestClass.blank = self._blank
        self.not_used_transfer = self.create_transfer()

    def tearDown(self):
        self.app.RequestClass.blank = self.asset_blank
        super(AssetTransferWebTest, self).tearDown()

    def get_asset(self, asset_id):
        response = self.app.get('/assets/{}'.format(asset_id))
        return response.json

    def create_transfer(self):
        test_transfer_data = {}
        response = self.app.post_json('/transfers', {"data": test_transfer_data})
        return response.json

    def use_transfer(self, transfer, asset_id, origin_transfer):
        req_data = {"data": {"id": transfer['data']['id'],
                             'transfer': origin_transfer}}

        self.app.post_json('/assets/{}/ownership'.format(asset_id), req_data)
        response = self.app.get('/transfers/{}'.format(transfer['data']['id']))
        return response.json
    
    def add_lots_to_asset(self, asset, need_lots=None):
        lots = []
        for i in need_lots:
            lot = deepcopy(i)
            lot['id'] = uuid4().hex
            lots.append(lot)
        asset['lots']  = lots
        for i, item in enumerate(asset['items']):
            item['relatedLot'] = lots[i % len(lots)]['id']
    
    def create_asset_unit(self, auth=None, data=None, lots=None):
        auth_switch = False

        if auth:
            current_auth = self.app.authorization
            self.app.authorization = auth
            auth_switch = True
        if not data:
            data = deepcopy(self.initial_data)
        if lots:
            self.add_lots_to_asset(data, lots)
        elif self.initial_lots:
            self.add_lots_to_asset(data, self.initial_lots)
        response = self.app.post_json('/assets', {'data': data})
        asset = response.json
        if auth_switch:
            self.app.authorization = current_auth
        return asset

    def set_asset_mode(self, asset_id, mode):
        current_auth = self.app.authorization

        self.app.authorization = ('Basic', ('administrator', ''))
        response = self.app.patch_json('/assets/{}'.format(asset_id),
                                       {'data': {'mode': mode}})
        self.app.authorization = current_auth
        return response
