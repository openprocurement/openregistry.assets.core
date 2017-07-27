# -*- coding: utf-8 -*-
from schematics.transforms import whitelist, blacklist, export_loop
from schematics.types import BaseType, StringType, IntType, MD5Type
from schematics.types.compound import ModelType, DictType
from couchdb_schematics.document import SchematicsDocument
from pyramid.security import Allow
from zope.interface import implementer
from schematics.types.serializable import serializable

from openregistry.api.models import (
    Revision, Organization, Model, schematics_embedded_role,
    IsoDateTimeType, ListType, Document as BaseDocument,
    Location, schematics_default_role, ItemClassification,
    Classification, Unit, Value
)

from openregistry.api.interfaces import IORContent


create_role = (blacklist('owner_token', 'owner', '_attachments', 'revisions', 'date', 'dateModified', 'doc_id', 'assetID', 'documents', 'status') + schematics_embedded_role)
edit_role = (blacklist('status', 'assetType', 'owner_token', 'owner', '_attachments', 'revisions', 'date', 'dateModified', 'doc_id', 'assetID', 'documents', 'mode') + schematics_embedded_role)
view_role = (blacklist('owner_token', '_attachments', 'revisions') + schematics_embedded_role)

Administrator_role = whitelist('status', 'mode')


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
    assetCustodian = ModelType(Organization)
    documents = ListType(ModelType(Document), default=list())  # All documents and attachments related to the asset.
    classification = ModelType(ItemClassification)
    additionalClassifications = ListType(ModelType(Classification), default=list())
    unit = ModelType(Unit)  # Description of the unit which the good comes in e.g. hours, kilograms
    quantity = IntType()  # The number of units required
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
    status = StringType(choices=['draft', 'pending', 'active', 'deleted'], default='pending')
    relatedLot = MD5Type()

    create_accreditation = 1
    edit_accreditation = 2
