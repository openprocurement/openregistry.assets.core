from openprocurement.api.plugins.transferring.validation import (
    validate_ownership_data
)
from openprocurement.api.utils import (
    json_view, context_unpack, APIResource
)
from openregistry.assets.core.plugins.transferring.validation import (
    validate_change_ownership_accreditation
)
from openregistry.assets.core.utils import (
    save_asset,
    opassetsresource,
    # get_asset_route_name,
    ROUTE_PREFIX
)


@opassetsresource(name='Asset ownership',
                  path='/assets/{asset_id}/ownership',
                  description='Assets Ownership')
class AssetOwnership(APIResource):
    @json_view(permission='create_asset',
               validators=(validate_ownership_data,
                           validate_change_ownership_accreditation))
    def post(self):
        asset = self.request.validated['asset']
        asset_path = "Asset"
        location = self.request.route_path(asset_path, asset_id=asset.id)
        location = location[len(ROUTE_PREFIX):]  # strips /api/<version>
        ownership_changed = self.request.change_ownership(location)

        if ownership_changed and save_asset(self.request):
            self.LOGGER.info(
                'Updated ownership of asset {}'.format(asset.id),
                extra=context_unpack(
                    self.request, {'MESSAGE_ID': 'asset_ownership_update'}
                )
            )

            return {'data': self.request.context.serialize('view')}

