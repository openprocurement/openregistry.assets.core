# -*- coding: utf-8 -*-
from datetime import datetime

from openprocurement.api.tests.base import (
    BaseResourceWebTest,
    snitch,  # noqa forwarded import
    DumpsTestAppwebtest,  # noqa forwarded import
    PrefixedRequestClass  # noqa forwarded import
)
from openprocurement.api.tests.blanks.json_data import (
    test_document_data,  # noqa forwarded import
    test_asset_basic_data,  # noqa forwarded import
    test_asset_basic_data_with_schema,  # noqa forwarded import
    test_asset_claimrights_data,  # noqa forwarded import
    test_asset_compound_data  # noqa forwarded import
)


now = datetime.now()


class BaseAssetWebTest(BaseResourceWebTest):

    resource_name = 'assets'
