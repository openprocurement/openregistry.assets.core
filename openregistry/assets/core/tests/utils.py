from openregistry.assets.core.utils import generate_asset_id
from openregistry.assets.core.tests.base import BaseAssetWebTest
from openprocurement.api.utils import get_now


class AssetUtilTest(BaseAssetWebTest):
    def setUp(self):
        self.database = self.db
        self.base_asset_prefix = 'UA-AR-DGF'

    def test_generate_id(self):
        result = generate_asset_id(get_now(), self.db)
        key = get_now().date().isoformat()
        index = self.db.get(key, 1)
        mock_id = '{}-{:04}-{:02}-{:02}-{:06}{}'.format(
            self.base_asset_prefix,
            get_now().year,
            get_now().month,
            get_now().day,
            index,
            ''
        )
        self.assertEqual(result, mock_id)
