# -*- coding: utf-8 -*-

from pyramid.security import (
    ALL_PERMISSIONS,
    Allow,
    Deny,
    Everyone,
)
from openregistry.api.traversal import get_item


class Root(object):
    __name__ = None
    __parent__ = None
    __acl__ = [
        (Allow, Everyone, ALL_PERMISSIONS),
        (Allow, Everyone, 'view_listing'),
        (Allow, Everyone, 'view_asset'),
        (Allow, 'g:brokers', 'create_asset'),
        (Allow, 'g:Administrator', 'edit_asset'),
        (Allow, 'g:admins', ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request
        self.db = request.registry.db


def factory(request):
    request.validated['asset_src'] = {}
    root = Root(request)
    if not request.matchdict or not request.matchdict.get('asset_id'):
        return root
    request.validated['asset_id'] = request.matchdict['asset_id']
    asset = request.asset
    asset.__parent__ = root
    request.validated['asset'] = request.validated['db_doc'] = asset
    request.validated['asset_status'] = asset.status
    if request.method != 'GET':
        request.validated['asset_src'] = asset.serialize('plain')
    if request.matchdict.get('document_id'):
        return get_item(asset, 'document', request)
    request.validated['id'] = request.matchdict['asset_id']
    return asset
