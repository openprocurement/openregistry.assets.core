# -*- coding: utf-8 -*-
import logging
from pyramid.interfaces import IRequest
from openregistry.assets.core.utils import (
    extract_asset, isAsset, register_assetType,
    asset_from_data, SubscribersPicker
)
from openregistry.assets.core.models import IAsset
from openprocurement.api.app import get_evenly_plugins
from openprocurement.api.interfaces import IContentConfigurator
from openregistry.assets.core.adapters import AssetConfigurator

LOGGER = logging.getLogger(__name__)


def includeme(config, plugin_map):
    from openregistry.assets.core.design import add_design
    add_design()
    config.add_request_method(extract_asset, 'asset', reify=True)

    # assetType plugins support
    config.registry.assetTypes = {}
    config.add_route_predicate('assetType', isAsset)
    config.add_subscriber_predicate('assetType', SubscribersPicker)
    config.add_request_method(asset_from_data)
    config.add_directive('add_assetType',
                         register_assetType)
    config.scan("openregistry.assets.core.views")
    config.scan("openregistry.assets.core.subscribers")
    config.registry.registerAdapter(AssetConfigurator, (IAsset, IRequest),
                                    IContentConfigurator)


    LOGGER.info("Included openprocurement.assets.core plugin", extra={'MESSAGE_ID': 'included_plugin'})

    # search for plugins
    get_evenly_plugins(config, plugin_map['plugins'], 'openprocurement.assets.core.plugins')
