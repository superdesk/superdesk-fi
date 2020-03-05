# This file is part of Superdesk.
#
# Copyright 2013, 2020 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
import logging
from superdesk import get_resource_service
from superdesk.errors import StopDuplication
from eve.utils import config
from superdesk.metadata.item import ITEM_STATE, PUBLISH_SCHEDULE, SCHEDULE_SETTINGS, PROCESSED_FROM


logger = logging.getLogger(__name__)


def set_german_and_publish(item, **kwargs):
    """Set item language to german and publish it"""
    updates = {
        PUBLISH_SCHEDULE: item[PUBLISH_SCHEDULE],
        SCHEDULE_SETTINGS: item[SCHEDULE_SETTINGS],
        'language': 'de',
    }
    archive_service = get_resource_service('archive')
    new_id = archive_service.duplicate_content(item, state='routed')
    updates[ITEM_STATE] = item.get(ITEM_STATE)
    updates[PROCESSED_FROM] = item[config.ID_FIELD]

    get_resource_service('archive_publish').patch(id=new_id, updates=updates)

    # we don't want duplication, we stop here internal_destinations workflow
    raise StopDuplication


name = 'Set German and Publish'
label = name
callback = set_german_and_publish
access_type = 'frontend'
action_type = 'direct'
