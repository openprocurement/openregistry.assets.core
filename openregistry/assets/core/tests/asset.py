# -*- coding: utf-8 -*-
import os
import unittest
from openregistry.assets.core.tests.base import BaseAssetWebTest
from openprocurement.api.tests.blanks.mixins import CoreResourceTestMixin


class AssetResourceTest(BaseAssetWebTest, CoreResourceTestMixin):
    relative_to = os.path.dirname(__file__)


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AssetResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
