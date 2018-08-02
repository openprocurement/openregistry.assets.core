# -*- coding: utf-8 -*-
from schematics.transforms import whitelist, blacklist
from schematics.types import StringType, MD5Type, ValidationError
from schematics.types.compound import ModelType
from pyramid.security import Allow
from zope.interface import implementer

from openprocurement.api.models.common import (
    sensitive_embedded_role,
    BaseResourceItem,
    Classification,
    Address,
    Location,
    Period  # noqa forwarded import
)
from openprocurement.api.interfaces import IORContent
from openprocurement.api.models.ocds import (
    Organization,
    Document,
    ItemClassification,
    Unit,
    Value,
    DecimalType,
    Item,
    Debt,  # noqa forwarded import
)
from openprocurement.api.models.registry_models import (
    LokiDocument,  # noqa forwarded import
    LokiItem,  # noqa forwarded import
    AssetHolder,  # noqa forwarded import
    AssetCustodian,  # noqa forwarded import
    Decision,  # noqa forwarded import
)
from openprocurement.api.models.roles import (
    schematics_embedded_role, schematics_default_role, plain_role, listing_role
)
from openprocurement.api.models.schematics_extender import IsoDateTimeType, ListType
from openprocurement.api.validation import (
    validate_items_uniq,  # noqa forwarded import
    koatuu_validator  # noqa forwarded import
)
from openprocurement.schemas.dgf.schemas_store import SchemaStore

from schematics_flexible.schematics_flexible import FlexibleModelType

from openregistry.assets.core.constants import ASSET_STATUSES, ALLOWED_SCHEMA_PROPERIES_CODES, SANDBOX_MODE

assets_embedded_role = sensitive_embedded_role

create_role = (
        blacklist(
            'owner_token',
            'owner',
            '_attachments',
            'revisions',
            'date',
            'dateModified',
            'doc_id',
            'assetID',
            'documents',
            'status',
            'sandboxParameters',
        ) + assets_embedded_role
)
edit_role = (blacklist('assetType', 'owner_token', 'owner', '_attachments', 'revisions', 'date', 'dateModified', 'doc_id', 'assetID', 'documents', 'mode') + assets_embedded_role)
view_role = (blacklist('owner_token', '_attachments', 'revisions') + assets_embedded_role)

Administrator_role = whitelist('status', 'mode', 'relatedLot')
concierge_role = (whitelist('status', 'relatedLot'))


class IAsset(IORContent):
    """ Base asset marker interface """


def get_asset(model):
    while not IAsset.providedBy(model):
        model = model.__parent__
    return model


def validate_schema_properties(data, new_schema_properties):
    """ Raise validation error if code in schema_properties mismatch
        with classification id """
    if new_schema_properties:
        if not data['classification']['id'].startswith(new_schema_properties['code']):
            raise ValidationError("classification id mismatch with schema_properties code")
        elif not any([new_schema_properties['code'].startswith(prefix) for prefix in ALLOWED_SCHEMA_PROPERIES_CODES]):
            raise ValidationError("schema_properties code must be one of {}.".format(repr(ALLOWED_SCHEMA_PROPERIES_CODES)))


class Item(Item):
    def validate_schema_properties(self, data, new_schema_properties):
        validate_schema_properties(data, new_schema_properties)


@implementer(IAsset)
class BaseAsset(BaseResourceItem):
    class Options:
        roles = {
            'create': create_role,
            # draft role
            'draft': view_role,
            'edit_draft': edit_role,
            'plain': plain_role,
            'edit': edit_role,
            # pending role
            'edit_pending': edit_role,
            'pending': view_role,
            # verification role
            'verification': view_role,
            'edit_verification': whitelist(),
            # active role
            'active': view_role,
            'edit_active': whitelist(),
            'view': view_role,
            'listing': listing_role,
            'Administrator': Administrator_role,
            # complete role
            'complete': view_role,
            'edit_complete': whitelist(),
            # deleted role  # TODO: replace with 'delete' view for asset, temporary solution for tests
            'deleted': view_role,
            'edit_deleted': whitelist(),
            # concierge_role
            'concierge': concierge_role,
            'default': schematics_default_role,
        }

    status = StringType(choices=ASSET_STATUSES, default="draft")
    relatedLot = MD5Type(serialize_when_none=False)
    _internal_type = None

    assetID = StringType()  # AssetID should always be the same as the OCID. It is included to make the flattened data structure more convenient.
    date = IsoDateTimeType()
    title = StringType(required=True)
    title_en = StringType()
    title_ru = StringType()
    description = StringType()
    description_en = StringType()
    description_ru = StringType()
    assetCustodian = ModelType(Organization, required=True)
    documents = ListType(ModelType(Document), default=list())  # All documents and attachments related to the asset.

    create_accreditation = 1
    edit_accreditation = 2

    if SANDBOX_MODE:
        sandboxParameters = StringType()

    def __init__(self, *args, **kwargs):
        super(BaseAsset, self).__init__(*args, **kwargs)
        self.doc_type = "Asset"

    def __local_roles__(self):
        roles = dict([('{}_{}'.format(self.owner, self.owner_token), 'asset_owner')])
        return roles

    def get_role(self):
        root = self.__parent__
        request = root.request
        if request.authenticated_role == 'Administrator':
            role = 'Administrator'
        elif request.authenticated_role == 'concierge':
            role = 'concierge'
        else:
            role = 'edit_{}'.format(request.context.status)
        return role

    def __acl__(self):
        acl = [
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'edit_asset'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'upload_asset_documents'),
        ]
        return acl

    def validate_relatedLot(self, data, lot):
        if data['status'] == 'active' and not lot:
            raise ValidationError(u'This field is required.')

    def validate_sandbox_parameters(self):
        if self.mode and self.mode == 'test' and self.sandboxParameters:
            raise ValidationError(u"procurementMethodDetails should be used with mode test")


class Asset(BaseAsset):
    value = ModelType(Value)
    classification = ModelType(ItemClassification, required=True)
    additionalClassifications = ListType(ModelType(Classification), default=list())
    unit = ModelType(Unit)  # Description of the unit which the good comes in e.g. hours, kilograms
    quantity = DecimalType()  # The number of units required
    address = ModelType(Address)
    location = ModelType(Location)
    schema_properties = FlexibleModelType(SchemaStore())

    def validate_schema_properties(self, data, new_schema_properties):
        validate_schema_properties(data, new_schema_properties)
