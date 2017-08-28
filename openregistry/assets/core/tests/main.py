# -*- coding: utf-8 -*-
import unittest

from openregistry.assets.core.tests import asset, migration


def suite():
    tests = unittest.TestSuite()
    tests.addTest(asset.suite())
    tests.addTest(migration.suite())
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
