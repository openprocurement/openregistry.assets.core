# -*- coding: utf-8 -*-
from openprocurement.api.tests.blanks.json_data import (
    test_document_data,  # noqa forwarded import
    test_organization,  # noqa forwarded import
    test_item_data_with_schema,  # noqa forwarded import
    schema_properties, # noqa forwarded import
    test_loki_item_data, # noqa forwarded import
    test_organization_loki, # noqa forwarded import
)

test_related_process_data = {
    'relatedProcessID': '1' * 32,
    'type': 'asset',
}
