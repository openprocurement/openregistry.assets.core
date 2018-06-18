# -*- coding: utf-8 -*-
from datetime import datetime

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
