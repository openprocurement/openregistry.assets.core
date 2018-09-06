# -*- coding: utf-8 -*-
from openprocurement.api.validation import (
    validate_accreditation_level
)
from openprocurement.api.utils import (
   get_resource_accreditation
)


def validate_change_ownership_accreditation(request, **kwargs):
    levels = get_resource_accreditation(request, 'asset', request.context, 'create')
    err_msg = 'Broker Accreditation level does not permit ownership change'
    validate_accreditation_level(request, request.validated['asset'], levels, err_msg)
