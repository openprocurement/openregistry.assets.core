from openregistry.assets.core.tests.base import snitch
from openregistry.assets.core.tests.plugins.transferring.blanks.resource_blanks import (
    change_resource_ownership,
    resource_location_in_transfer,
    already_applied_transfer,
    half_applied_transfer,
    new_owner_can_change,
    old_owner_cant_change,
    broker_not_accreditation_level,
    level_permis,
    switch_mode,
    create_asset_by_concierge
)

class AssetOwnershipChangeTestCaseMixin(object):

    first_owner = 'broker'
    second_owner = 'broker1'
    test_owner = 'broker1t'
    invalid_owner = 'broker3'
    initial_auth = ('Basic', (first_owner, ''))

    test_change_resource_ownership = snitch(change_resource_ownership)
    test_resource_location_in_transfer = snitch(resource_location_in_transfer)
    test_already_applied_transfer = snitch(already_applied_transfer)
    test_half_applied_transfer = snitch(half_applied_transfer)
    test_new_owner_can_change = snitch(new_owner_can_change)
    test_old_owner_cant_change = snitch(old_owner_cant_change)
    test_broker_not_accreditation_level = snitch(broker_not_accreditation_level)
    test_level_permis = snitch(level_permis)
    test_switch_mode = snitch(switch_mode)
    test_create_asset_by_concierge = snitch(switch_mode)
