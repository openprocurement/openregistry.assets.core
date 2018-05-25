from pyramid.exceptions import URLDecodeError
from pyramid.compat import decode_path_info
from cornice.resource import resource
from schematics.exceptions import ModelValidationError
from pkg_resources import get_distribution
from couchdb.http import ResourceConflict
from logging import getLogger
from functools import partial
from time import sleep


from openprocurement.api.utils import (
    error_handler,
    update_logging_context,
    set_modetest_titles,
    get_revision_changes,
    context_unpack,
    get_now,
    apply_data_patch,
    prepare_revision,
    raise_operation_error, # noqa forwarded import
    calculate_business_date, # noqa forwarded import
    get_file, # noqa forwarded import
    update_file_content_type, # noqa forwarded import
    json_view, # noqa forwarded import
    APIResource, # noqa forwarded import

)

from openregistry.assets.core.constants import DEFAULT_ASSET_TYPE

from openregistry.assets.core.traversal import factory

PKG = get_distribution(__package__)
LOGGER = getLogger(PKG.project_name)


opassetsresource = partial(resource,
                           error_handler=error_handler,
                           factory=factory)


def generate_asset_id(ctime, db, server_id=''):
    key = ctime.date().isoformat()
    assetIDdoc = 'assetID_' + server_id if server_id else 'assetID'
    while True:
        try:
            assetID = db.get(assetIDdoc, {'_id': assetIDdoc})
            index = assetID.get(key, 1)
            assetID[key] = index + 1
            db.save(assetID)
        except ResourceConflict:  # pragma: no cover
            pass
        except Exception:  # pragma: no cover
            sleep(1)
        else:
            break
    return 'UA-AR-DGF-{:04}-{:02}-{:02}-{:06}{}'.format(ctime.year,
                                                 ctime.month,
                                                 ctime.day,
                                                 index,
                                                 server_id and '-' + server_id)


def extract_asset(request):
    try:
        # empty if mounted under a path in mod_wsgi, for example
        path = decode_path_info(request.environ['PATH_INFO'] or '/')
    except KeyError:
        path = '/'
    except UnicodeDecodeError as e:
        raise URLDecodeError(e.encoding, e.object, e.start, e.end, e.reason)

    asset_id = ""
    # extract asset id
    parts = path.split('/')
    if len(parts) < 4 or parts[3] != 'assets':
        return

    asset_id = parts[4]
    return extract_asset_adapter(request, asset_id)


def extract_asset_adapter(request, asset_id):
    db = request.registry.db
    doc = db.get(asset_id)
    if doc is None or doc.get('doc_type') != 'Asset':
        request.errors.add('url', 'asset_id', 'Not Found')
        request.errors.status = 404
        raise error_handler(request)

    return request.asset_from_data(doc)


def get_asset_types(registry, internal_types):
    asset_types = [
        at for at, it in registry.asset_type_configurator.items() if it in internal_types
    ]
    return asset_types


def asset_from_data(request, data, raise_error=True, create=True):
    assetType = data.get('assetType')
    if not assetType:
        asset_types = get_asset_types(request.registry, (DEFAULT_ASSET_TYPE,))
        assetType = asset_types[0] if asset_types else DEFAULT_ASSET_TYPE
    model = request.registry.assetTypes.get(assetType)
    if model is None and raise_error:
        request.errors.add('body', 'assetType', 'Not implemented')
        request.errors.status = 415
        raise error_handler(request)
    update_logging_context(request, {'asset_type': assetType})
    if model is not None and create:
        model = model(data)
    return model


def apply_patch(request, data=None, save=True, src=None):
    data = request.validated['data'] if data is None else data
    patch = data and apply_data_patch(src or request.context.serialize(), data)
    if patch:
        request.context.import_data(patch)
        if save:
            return save_asset(request)


class isAsset(object):
    """ Route predicate. """

    def __init__(self, val, config):
        self.val = val

    def text(self):
        return 'assetType = %s' % (self.val,)

    phash = text

    def __call__(self, context, request):
        if request.asset is not None:
            asset_type = getattr(request.asset, 'assetType', None)
            return request.registry.asset_type_configurator.get(asset_type) == self.val
        return False


def register_assetType(config, model, asset_type):
    """Register a assetType.
    :param config:
        The pyramid configuration object that will be populated.
    :param model:
        The asset model class
    :param asset_type
        Asset type associated with internal_type
    """
    config.registry.assetTypes[asset_type] = model
    config.registry.asset_type_configurator[asset_type] = model._internal_type


class SubscribersPicker(isAsset):
    """ Subscriber predicate. """

    def __call__(self, event):
        if event.asset is not None:
            asset_type = getattr(event.asset, 'assetType', None)
            return event.asset._internal_type == self.val
        return False


def asset_serialize(request, asset_data, fields):
    asset = request.asset_from_data(asset_data, raise_error=False)
    if asset is None:
        return dict([(i, asset_data.get(i, '')) for i in ['assetType', 'dateModified', 'id']])
    return dict([(i, j) for i, j in asset.serialize(asset.status).items() if i in fields])


def save_asset(request):
    asset = request.validated['asset']
    if asset.mode == u'test':
        set_modetest_titles(asset)
    patch = get_revision_changes(asset.serialize("plain"), request.validated['asset_src'])
    if patch:
        revision = prepare_revision(asset, patch, request.authenticated_userid)
        asset.revisions.append(type(asset).revisions.model_class(revision))
        old_dateModified = asset.dateModified
        if getattr(asset, 'modified', True):
            asset.dateModified = get_now()
        try:
            asset.store(request.registry.db)
        except ModelValidationError, e:
            for i in e.message:
                request.errors.add('body', i, e.message[i])
            request.errors.status = 422
        except ResourceConflict, e:  # pragma: no cover
            request.errors.add('body', 'data', str(e))
            request.errors.status = 409
        except Exception, e:  # pragma: no cover
            request.errors.add('body', 'data', str(e))
        else:
            LOGGER.info('Saved asset {}: dateModified {} -> {}'.format(asset.id, old_dateModified and old_dateModified.isoformat(), asset.dateModified.isoformat()),
                        extra=context_unpack(request, {'MESSAGE_ID': 'save_asset'}, {'RESULT': asset.rev}))
            return True

