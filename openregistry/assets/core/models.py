# -*- coding: utf-8 -*-
from schematics.transforms import whitelist, blacklist, export_loop
from schematics.types.serializable import serializable
from schematics.types.compound import ModelType, DictType
from schematics.types import BaseType, StringType, IntType, MD5Type
from pyramid.security import Allow
from zope.interface import implementer

from openregistry.api.models.ocds import Organization, Document, Location, ItemClassification, Classification, Unit, Value, Address
from openregistry.api.models.schematics_extender import IsoDateTimeType, ListType
from openregistry.api.models.roles import schematics_embedded_role, schematics_default_role, plain_role, listing_role
from openregistry.api.models.common import BaseResourceItem

from openregistry.api.interfaces import IORContent


create_role = (blacklist('owner_token', 'owner', '_attachments', 'revisions', 'date', 'dateModified', 'doc_id', 'assetID', 'documents', 'status') + schematics_embedded_role)
edit_role = (blacklist('assetType', 'owner_token', 'owner', '_attachments', 'revisions', 'date', 'dateModified', 'doc_id', 'assetID', 'documents', 'mode') + schematics_embedded_role)
view_role = (blacklist('owner_token', '_attachments', 'revisions') + schematics_embedded_role)

Administrator_role = whitelist('status', 'mode')
bot_role = (whitelist('status', 'relatedLot'))


class IAsset(IORContent):
    """ Base asset marker interface """


def get_asset(model):
    while not IAsset.providedBy(model):
        model = model.__parent__
    return model


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
            # active role
            'active': view_role,
            'edit_active': whitelist(),
            'view': view_role,
            'listing': listing_role,
            'Administrator': Administrator_role,
            # complete role
            'complete': view_role,
            'edit_complete': blacklist('revisions'),
            # deleted role  # TODO: replace with 'delete' view for asset, temporary solution for tests
            'deleted': view_role,
            'edit_deleted': blacklist('revisions'),
            # bots_role
            'bot': bot_role,
            'default': schematics_default_role,
        }

    assetID = StringType()  # AssetID should always be the same as the OCID. It is included to make the flattened data structure more convenient.
    date = IsoDateTimeType()
    title = StringType(required=True)
    title_en = StringType()
    title_ru = StringType()
    description = StringType()
    description_en = StringType()
    description_ru = StringType()
    value = ModelType(Value)
    assetCustodian = ModelType(Organization, required=True)
    documents = ListType(ModelType(Document), default=list())  # All documents and attachments related to the asset.
    classification = ModelType(ItemClassification, required=True)
    additionalClassifications = ListType(ModelType(Classification), default=list())
    unit = ModelType(Unit)  # Description of the unit which the good comes in e.g. hours, kilograms
    quantity = IntType()  # The number of units required
    address = ModelType(Address)
    location = ModelType(Location)

    create_accreditation = 1
    edit_accreditation = 2

    def __local_roles__(self):
        roles = dict([('{}_{}'.format(self.owner, self.owner_token), 'asset_owner')])
        return roles

    def get_role(self):
        root = self.__parent__
        request = root.request
        if request.authenticated_role == 'Administrator':
            role = 'Administrator'
        elif request.authenticated_role == 'bot':
            role = 'bot'
        else:
            role = 'edit_{}'.format(request.context.status)
        return role

    def __acl__(self):
        acl = [
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'edit_asset'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'upload_asset_documents'),
        ]
        return acl


class Asset(BaseAsset):
    status = StringType(choices=['draft', 'pending', 'active', 'deleted', 'complete'], default="draft")
    relatedLot = MD5Type()

    create_accreditation = 1
    edit_accreditation = 2
