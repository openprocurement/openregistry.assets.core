# -*- coding: utf-8 -*-
import logging

from openprocurement.api.migration import (
    BaseMigrationsRunner,  # noqa: forwarded import
    BaseMigrationStep,  # noqa: forwarded import
)
LOGGER = logging.getLogger(__name__)


def migrate_data(registry, destination=None):
    pass
