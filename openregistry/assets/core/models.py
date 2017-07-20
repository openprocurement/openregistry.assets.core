# -*- coding: utf-8 -*-
from schematics.transforms import whitelist, blacklist, export_loop
from schematics.types import StringType, BaseType
from schematics.types.compound import ModelType, DictType
from couchdb_schematics.document import SchematicsDocument
from pyramid.security import Allow
from zope.interface import implementer
from schematics.types.serializable import serializable

from openregistry.api.models import (
    Revision, Organization, Model, Period, schematics_embedded_role,
    IsoDateTimeType, ListType, Document as BaseDocument,
    Location, Value, schematics_default_role,
    Address
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
    title = StringType(required=True)
    title_en = StringType()
    title_ru = StringType()
    documents = ListType(ModelType(Document), default=list())  # All documents and attachments related to the asset.
    description = StringType()
    description_en = StringType()
    description_ru = StringType()
    date = IsoDateTimeType()
    dateModified = IsoDateTimeType()
    assetID = StringType()  # AssetID should always be the same as the OCID. It is included to make the flattened data structure more convenient.
    owner = StringType()
    owner_token = StringType()
    mode = StringType(choices=['test'])

    _attachments = DictType(DictType(BaseType), default=dict())  # couchdb attachments
    revisions = ListType(ModelType(Revision), default=list())

    def __repr__(self):
        return '<%s:%r@%r>' % (type(self).__name__, self.id, self.rev)

    def __local_roles__(self):
        roles = dict([('{}_{}'.format(self.owner, self.owner_token), 'asset_owner')])
        return roles

    @serializable(serialized_name='id')
    def doc_id(self):
        """A property that is serialized by schematics exports."""
        return self._id

    def import_data(self, raw_data, **kw):
        """
        Converts and imports the raw data into the instance of the model
        according to the fields in the model.
        :param raw_data:
            The data to be imported.
        """
        data = self.convert(raw_data, **kw)
        del_keys = [k for k in data.keys() if data[k] == self.__class__.fields[k].default or data[k] == getattr(self, k)]
        for k in del_keys:
            del data[k]

        self._data.update(data)
        return self


class Asset(BaseAsset):
    status = StringType(choices=['draft', 'pending', 'active', 'deleted'], default='pending')

    create_accreditation = 1
    edit_accreditation = 2

    __name__ = ''

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