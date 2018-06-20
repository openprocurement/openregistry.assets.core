import mock

from openregistry.assets.core.utils import generate_asset_id
from openregistry.assets.core.tests.base import BaseAssetWebTest
from openprocurement.api.utils import get_now


@mock.patch('openregistry.assets.core.utils.project_configurator', autospec=True)
class AssetUtilTest(BaseAssetWebTest):

    def setUp(self):
        self.database = self.db

    def test_generate_id(self, mock_project_configurator):
        test_prefix = 'TEST-ID'
        mock_project_configurator.ASSET_PREFIX = test_prefix
        result = generate_asset_id(get_now(), self.db)

        key = get_now().date().isoformat()
        index = self.db.get(key, 1)
        mock_id = '{}-{:04}-{:02}-{:02}-{:06}{}'.format(
            test_prefix,
            get_now().year,
            get_now().month,
            get_now().day,
            index,
            ''
        )
        self.assertEqual(result, mock_id)
