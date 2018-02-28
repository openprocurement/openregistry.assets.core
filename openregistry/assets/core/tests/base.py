# -*- coding: utf-8 -*-
from datetime import datetime

from openprocurement.api.tests.base import BaseResourceWebTest


now = datetime.now()


class BaseAssetWebTest(BaseResourceWebTest):

    resource_name = 'assets'
