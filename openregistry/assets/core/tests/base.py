# -*- coding: utf-8 -*-
from datetime import datetime

from openprocurement.api.tests.base import (
    BaseResourceWebTest,
    snitch,
    DumpsTestAppwebtest,
    PrefixedRequestClass
)


now = datetime.now()


class BaseAssetWebTest(BaseResourceWebTest):

    resource_name = 'assets'
