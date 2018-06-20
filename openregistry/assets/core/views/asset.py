# -*- coding: utf-8 -*-
from openprocurement.api.validation import (
    validate_change_status,
)

from openregistry.assets.core.events import AssetInitializeEvent
from openregistry.assets.core.design import (
    FIELDS, VIEW_MAP, CHANGES_VIEW_MAP, FEED
)
from openprocurement.api.utils import (
    get_now, generate_id, json_view, set_ownership,
    context_unpack, APIResourceListing, APIResource
)

from openregistry.assets.core.validation import (
    validate_asset_data,
    validate_patch_asset_data,
    validate_data_by_model
)
from openregistry.assets.core.utils import (
    save_asset,
    apply_patch,
    opassetsresource,
    asset_serialize,
    generate_asset_id
)
from openregistry.assets.core.interfaces import IAssetManager

patch_asset_validators = (
    validate_patch_asset_data,
    validate_change_status,
    validate_data_by_model
)


@opassetsresource(name='Assets',
                  path='/assets',
                  description="Open Contracting compatible data exchange format.")
class AssetsResource(APIResourceListing):

    def __init__(self, request, context):
        super(AssetsResource, self).__init__(request, context)
        # params for listing
        self.VIEW_MAP = VIEW_MAP
        self.CHANGES_VIEW_MAP = CHANGES_VIEW_MAP
        self.FEED = FEED
        self.FIELDS = FIELDS
        self.serialize_func = asset_serialize
        self.object_name_for_listing = 'Assets'
        self.log_message_id = 'asset_list_custom'

    @json_view(content_type="application/json", permission='create_asset', validators=(validate_asset_data,))
    def post(self):
        """This API request is targeted to creating new Asset."""
        self.request.registry.getAdapter(
            self.request.validated['asset'],
            IAssetManager
        ).create_asset(self.request)

        asset_id = generate_id()
        asset = self.request.validated['asset']
        asset.id = asset_id
        if not asset.get('assetID'):
            asset.assetID = generate_asset_id(get_now(), self.db, self.server_id)
        self.request.registry.notify(AssetInitializeEvent(asset))
        if self.request.json_body['data'].get('status') == 'draft':
            asset.status = 'draft'
        acc = set_ownership(asset, self.request)
        self.request.validated['asset'] = asset
        self.request.validated['asset_src'] = {}
        if save_asset(self.request):
            self.LOGGER.info('Created asset {} ({})'.format(asset_id, asset.assetID),
                             extra=context_unpack(self.request, {'MESSAGE_ID': 'asset_create'}, {'asset_id': asset_id, 'assetID': asset.assetID}))
            self.request.response.status = 201
            self.request.response.headers[
                'Location'] = self.request.route_url('Asset', asset_id=asset_id)
            return {
                'data': asset.serialize(asset.status),
                'access': acc
            }


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

