# -*- coding: utf-8 -*-
import os
import unittest
from openregistry.assets.core.tests.base import BaseAssetWebTest
from openregistry.api.tests.blanks.mixins import CoreResourceTestMixin


class AssetResourceTest(BaseAssetWebTest, CoreResourceTestMixin):
    relative_to = os.path.dirname(__file__)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AssetResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
