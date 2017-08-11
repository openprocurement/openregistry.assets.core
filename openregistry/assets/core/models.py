# -*- coding: utf-8 -*-
from schematics.transforms import whitelist, blacklist, export_loop
from schematics.types import BaseType, StringType, IntType, MD5Type
from schematics.types.compound import ModelType, DictType, ListType
from couchdb_schematics.document import SchematicsDocument
from pyramid.security import Allow
from zope.interface import implementer
from schematics.types.serializable import serializable

from openregistry.api.models.ocds import Organization, Revision, Document as BaseDocument, Location, ItemClassification, Classification, Unit, Unit, Value, Address
from openregistry.api.models.schematics_extender import Model, IsoDateTimeType
from openregistry.api.models.roles import schematics_embedded_role, schematics_default_role, plain_role, listing_role

from openregistry.api.interfaces import IORContent


create_role = (blacklist('owner_token', 'owner', '_attachments', 'revisions', 'date', 'dateModified', 'doc_id', 'assetID', 'documents', 'status') + schematics_embedded_role)
edit_role = (blacklist('status', 'assetType', 'owner_token', 'owner', '_attachments', 'revisions', 'date', 'dateModified', 'doc_id', 'assetID', 'documents', 'mode') + schematics_embedded_role)
view_role = (blacklist('owner_token', '_attachments', 'revisions') + schematics_embedded_role)

Administrator_role = whitelist('status', 'mode')
bot_role = (whitelist('status'))


class IAsset(IORContent):
    """ Base asset marker interface """


def get_asset(model):
    while not IAsset.providedBy(model):
        model = model.__parent__
    return model


class Document(BaseDocument):
    documentOf = StringType(required=True, choices=['asset'], default='asset')


@implementer(IAsset)
class BaseAsset(SchematicsDocument, Model):
    class Options:
        roles = {
            'create': create_role,
            # draft role
            'draft': view_role,
            'edit_draft': edit_role,
            'plain': plain_role,
            'edit': edit_role,
            # pending role
            'edit_pending': blacklist('revisions'),
            'pending': view_role,
            # active role
            'active': view_role,
            'edit_active': whitelist(),
            'view': view_role,
            'listing': listing_role,
            'Administrator': Administrator_role,
            # deleted role  # TODO: replace with 'delete' view for asset, temporary solution for tests
            'deleted': view_role,
            'edit_deleted': blacklist('revisions'),
            # bots_role
            'bot1': bot_role,
            'default': schematics_default_role,
        }

    assetID = StringType()  # AssetID should always be the same as the OCID. It is included to make the flattened data structure more convenient.
    owner = StringType()
    owner_token = StringType()
    mode = StringType(choices=['test'])
    date = IsoDateTimeType()
    dateModified = IsoDateTimeType()
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

    _attachments = DictType(DictType(BaseType), default=dict())  # couchdb attachments
    revisions = ListType(ModelType(Revision), default=list())

    create_accreditation = 1
    edit_accreditation = 2


    __name__ = ''

    def __repr__(self):
        return '<%s:%r@%r>' % (type(self).__name__, self.id, self.rev)

    def __local_roles__(self):
        roles = dict([('{}_{}'.format(self.owner, self.owner_token), 'asset_owner')])
        return roles

    @serializable(serialized_name='id')
    def doc_id(self):
        """A property that is serialized by schematics exports."""
        return self._id

    def get_role(self):
        root = self.__parent__
        request = root.request
        if request.authenticated_role == 'Administrator':
            role = 'Administrator'
        elif request.authenticated_role == 'bot1':
            role = 'bot1'
        else:
            role = 'edit_{}'.format(request.context.status)
        return role

    def __acl__(self):
        acl = [
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'edit_asset'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'upload_asset_documents'),
        ]
        return acl

    def __local_roles__(self):
        roles = dict([('{}_{}'.format(self.owner, self.owner_token), 'asset_owner')])
        return roles


class Asset(BaseAsset):
    status = StringType(choices=['draft', 'pending', 'active', 'deleted', 'complete'], default='pending')
    relatedLot = MD5Type()

    create_accreditation = 1
    edit_accreditation = 2
