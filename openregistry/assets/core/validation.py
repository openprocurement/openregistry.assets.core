# -*- coding: utf-8 -*-
from functools import partial

from openprocurement.api.validation import (
    validate_accreditations,
    validate_change_status, # noqa forwarder import
    validate_data,
    validate_document_data, # noqa forwarded import
    validate_file_upload, # noqa forwarder import
    validate_items_uniq, # noqa forwarded import
    validate_decision_uniq, # noqa forwarded import
    validate_json_data,
    validate_patch_document_data, # noqa forwarded import
    validate_t_accreditation,
    validate_decision_post, # noqa forwarded import
    validate_decision_patch_data, # noqa forwarded import
    validate_decision_after_rectificationPeriod,
    validate_decision_update_in_not_allowed_status
)
from openprocurement.api.utils import (
    raise_operation_error,
    update_logging_context,
    get_resource_accreditation
)
from openprocurement.api.plugins.transferring.validation import (
    validate_accreditation_level
)


validate_decision_after_rectificationPeriod = partial(
    validate_decision_after_rectificationPeriod,
    parent_resource='asset'
)
validate_decision_update_in_not_allowed_status = partial(
    validate_decision_update_in_not_allowed_status,
    parent_resource='asset'
)


def validate_asset_data(request, error_handler, **kwargs):
    update_logging_context(request, {'asset_id': '__new__'})

    data = validate_json_data(request)

    model = request.asset_from_data(data, create=False)
    validate_accreditations(request, model, 'asset')
    data = validate_data(request, model, "asset", data=data)
    validate_t_accreditation(request, data, 'asset')


def validate_patch_asset_data(request, error_handler, **kwargs):
    data = validate_json_data(request)
    editing_roles = request.content_configurator.available_statuses[request.context.status]['editing_permissions']
    if request.authenticated_role not in editing_roles:
        msg = 'Can\'t update {} in current ({}) status'.format(request.validated['resource_type'],
                                                               request.context.status)
        raise_operation_error(request, error_handler, msg)
    default_status = type(request.asset).fields['status'].default
    if data.get('status') == default_status and data.get('status') != request.context.status:
        raise_operation_error(request, error_handler, 'Can\'t switch asset to {} status'.format(default_status))


def validate_data_by_model(request, error_handler, **kwargs):
    return validate_data(request, type(request.asset), data=validate_json_data(request))


def validate_asset_document_update_not_by_author_or_asset_owner(request, error_handler, **kwargs):
    if request.authenticated_role != (request.context.author or 'asset_owner'):
        request.errors.add('url', 'role', 'Can update document only author')
        request.errors.status = 403
        raise error_handler(request)


def validate_document_operation_in_not_allowed_asset_status(request, error_handler, **kwargs):
    status = request.validated['asset_status']
    if status != 'pending':
        raise_operation_error(request, error_handler,
                              'Can\'t update document in current ({}) asset status'.format(status))


def validate_asset_accreditation_level(request, **kwargs):
    levels = get_resource_accreditation(request, 'asset', request.context, 'create')
    validate_accreditation_level(request, request.validated['asset'], levels)
