# -*- coding: utf-8 -*-

from openprocurement.api.constants import DOCUMENT_TYPES

DEFAULT_ASSET_TYPE = 'basic'

ASSET_STATUSES = ['draft', 'pending', "verification",
                  'active', 'deleted', 'complete']

STATUS_CHANGES = {
    "draft": {
        "editing_permissions": ["asset_owner", "Administrator"],
        "next_status": {
            "pending": ["asset_owner", "Administrator"]
        }
    },
    "pending": {
        "editing_permissions": ["asset_owner", "concierge", "Administrator"],
        "next_status": {
            "deleted": ["asset_owner", "Administrator"],
            "verification": ["concierge", "Administrator"]
        }
    },
    "verification": {
        "editing_permissions":  ["concierge", "Administrator"],
        "next_status": {
            "active": ["concierge", "Administrator"],
            "pending": ["concierge", "Administrator"]
        }
    },
    "active": {
        "editing_permissions": ["concierge", "Administrator"],
        "next_status": {
            "pending": ["concierge", "Administrator"],
            "complete": ["concierge", "Administrator"]
        }
    },
    "deleted": {
        "editing_permissions": [],
        "next_status": {}
    },
    "complete": {
        "editing_permissions": [],
        "next_status": {}
    }
}

ALLOWED_SCHEMA_PROPERIES_CODES = ['04']

