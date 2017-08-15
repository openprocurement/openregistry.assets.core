# -*- coding: utf-8 -*-
from openregistry.api.validation import validate_data, validate_json_data
from openregistry.api.utils import update_logging_context, raise_operation_error


def validate_asset_data(request, error_handler, **kwargs):
    update_logging_context(request, {'asset_id': '__new__'})

    data = validate_json_data(request)

    model = request.asset_from_data(data, create=False)
    if not any([request.check_accreditation(acc) for acc in iter(str(model.create_accreditation))]):
        request.errors.add('body', 'accreditation',
                           'Broker Accreditation level does not permit asset creation')
        request.errors.status = 403
        raise error_handler(request)

    data = validate_data(request, model, data=data)
    if data and data.get('mode', None) is None and request.check_accreditation('t'):
        request.errors.add('body', 'mode', 'Broker Accreditation level does not permit asset creation')
        request.errors.status = 403
        raise error_handler(request)


def validate_patch_asset_data(request, error_handler, **kwargs):
    data = validate_json_data(request)
    can_edit = request.content_configurator.available_statuses[request.context.status]['editing_permissions']
    if request.authenticated_role not in can_edit:
        msg = 'Can\'t update {} in current ({}) status'.format(request.validated['resource_type'],
                                                               request.context.status)
        raise_operation_error(request, error_handler, msg)
    default_status = type(request.asset).fields['status'].default
    if data.get('status') == default_status and data.get('status') != request.context.status:
        raise_operation_error(request, error_handler, 'Can\'t switch asset to {} status'.format(default_status))
    return validate_data(request, type(request.asset), True, data)


def validate_asset_document_update_not_by_author_or_asset_owner(request, error_handler, **kwargs):
    if request.authenticated_role != (request.context.author or 'asset_owner'):
        request.errors.add('url', 'role', 'Can update document only author')
        request.errors.status = 403
        raise error_handler(request)
