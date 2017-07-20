# -*- coding: utf-8 -*-
from openregistry.api.validation import validate_data, validate_json_data
from openregistry.api.utils import update_logging_context,  raise_operation_error


def validate_asset_data(request, error_handler, **kwargs):
    update_logging_context(request, {'asset_id': '__new__'})

    data = validate_json_data(request)

    model = request.asset_from_data(data, create=False)
    if not any([request.check_accreditation(acc) for acc in iter(str(model.create_accreditation))]):
        request.errors.add('assetType', 'accreditation',
                           'Broker Accreditation level does not permit asset creation')
        request.errors.status = 403
        raise error_handler(request.errors)

    data = validate_data(request, model, data=data)
    if data and data.get('mode', None) is None and request.check_accreditation('t'):
        request.errors.add('assetType', 'mode', 'Broker Accreditation level does not permit asset creation')
        request.errors.status = 403
        raise error_handler(request)


def validate_patch_asset_data(request, error_handler, **kwargs):
    data = validate_json_data(request)
    if request.context.status != 'draft':
        return validate_data(request, type(request.asset), True, data)
    default_status = type(request.asset).fields['status'].default
    if data.get('status') != default_status:
        raise_operation_error(request, error_handler, 'Can\'t update asset in current (draft) status')
    request.validated['data'] = {'status': default_status}
    request.context.status = default_status



def validate_asset_status_update_in_terminated_status(request, error_handler, **kwargs):
    asset = request.context
    if request.authenticated_role != 'Administrator' and asset.status in ['active', 'deleted']:
        raise_operation_error(request, error_handler, 'Can\'t update asset in current ({}) status'.format(asset.status))