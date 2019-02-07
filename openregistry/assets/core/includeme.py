# -*- coding: utf-8 -*-
import logging
from pyramid.interfaces import IRequest

from openregistry.assets.core.utils import (
    extract_asset,
    isAsset,
    register_assetType,
    asset_from_data,
    SubscribersPicker,
    get_evenly_plugins,
)
from openprocurement.api.interfaces import IContentConfigurator
from openprocurement.api.plugins.related_processes import add_related_processes_views
from openprocurement.api.utils import get_plugin_aliases
from openregistry.assets.core.adapters import AssetConfigurator
from openregistry.assets.core.constants import ENDPOINTS
from openregistry.assets.core.models import IAsset
from openregistry.assets.core.traversal import factory
from openregistry.assets.core.views.related_processes import AssetsRelatedProcessesResource


LOGGER = logging.getLogger(__name__)


def includeme(config, plugin_map):
    from openregistry.assets.core.design import add_design
    add_design()
    config.add_request_method(extract_asset, 'asset', reify=True)

    # assetType plugins support
    config.registry.assetTypes = {}
    config.add_route_predicate('_internal_type', isAsset)
    config.add_subscriber_predicate('_internal_type', SubscribersPicker)
    config.add_request_method(asset_from_data)
    config.add_directive('add_assetType',
                         register_assetType)
    config.scan("openregistry.assets.core.views")
    config.scan("openregistry.assets.core.subscribers")
    config.registry.registerAdapter(AssetConfigurator, (IAsset, IRequest),
                                    IContentConfigurator)
    config.registry.asset_type_configurator = {}

    LOGGER.info("Included openprocurement.assets.core plugin", extra={'MESSAGE_ID': 'included_plugin'})

    # Aliases information
    LOGGER.info('Start aliases')
    get_plugin_aliases(plugin_map.get('plugins', {}))
    LOGGER.info('End aliases')

    # add accreditation
    config.registry.accreditation['asset'] = {}

    # search for plugins
    get_evenly_plugins(config, plugin_map['plugins'], 'openregistry.assets.core.plugins')

    # add related processes views
    add_related_processes_views(config, ENDPOINTS['assets'], factory, AssetsRelatedProcessesResource)
