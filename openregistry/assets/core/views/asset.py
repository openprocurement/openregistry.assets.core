# -*- coding: utf-8 -*-
from openprocurement.api.validation import (
    validate_change_status,
)
from openprocurement.api.utils import (
    json_view,
    context_unpack,
    APIResource,
)

from openregistry.assets.core.validation import (
    validate_patch_asset_data,
    validate_data_by_model
)
from openregistry.assets.core.utils import (
    save_asset, apply_patch, opassetsresource
)
from openregistry.assets.core.interfaces import IAssetManager

patch_asset_validators = (
    validate_patch_asset_data,
    validate_change_status,
    validate_data_by_model
)


@opassetsresource(name='Asset',
                  path='/assets/{asset_id}',
                  description="Open Contracting compatible data exchange format.")
class AssetResource(APIResource):

    @json_view(permission='view_asset')
    def get(self):
        asset_data = self.context.serialize(self.context.status)
        return {'data': asset_data}

    @json_view(content_type="application/json",
               validators=patch_asset_validators,
               permission='edit_asset')
    def patch(self):
        self.request.registry.getAdapter(
            self.context,
            IAssetManager
        ).change_asset(self.request)
        asset = self.context
        if asset.status == 'active' and self.request.validated['data'].get('status') == 'pending':
            self.request.validated['data']['relatedLot'] = None
            self.request.validated['asset'].relatedLot = None
        apply_patch(self.request, src=self.request.validated['asset_src'])
        self.LOGGER.info(
            'Updated asset {}'.format(asset.id),
            extra=context_unpack(self.request, {'MESSAGE_ID': 'asset_patch'})
        )
        return {'data': asset.serialize(asset.status)}
