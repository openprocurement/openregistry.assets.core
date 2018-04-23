from pyramid.interfaces import IRequest
from openregistry.assets.core.utils import (
    extract_asset, isAsset, register_assetType,
    asset_from_data, SubscribersPicker
)
from openprocurement.api.interfaces import IContentConfigurator
from openprocurement.api.utils import configure_plugins
from openregistry.assets.core.models import IAsset
from openregistry.assets.core.adapters import AssetConfigurator


def includeme(config, plugin_config):
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

    # search for plugins
    if plugin_config and plugin_config.get('plugins'):
        for name in plugin_config['plugins']:
            package_config = plugin_config['plugins'][name]
            configure_plugins(
                config, {name: package_config},
                'openregistry.assets.core.plugins', name
            )
