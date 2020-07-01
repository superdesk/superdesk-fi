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
from superdesk.metadata.item import (
    ITEM_STATE, PUBLISH_SCHEDULE, SCHEDULE_SETTINGS, PROCESSED_FROM, CONTENT_STATE
)


logger = logging.getLogger(__name__)


def set_german_and_publish(item, **kwargs):
    """
    Set item language to german and publish it
    """

    if item.get('language') != 'en':
        raise StopDuplication

    archive_service = get_resource_service('archive')

    if item.get(ITEM_STATE) == CONTENT_STATE.PUBLISHED:
        updates = {
            PUBLISH_SCHEDULE: item[PUBLISH_SCHEDULE],
            SCHEDULE_SETTINGS: item[SCHEDULE_SETTINGS],
            'language': 'de',
        }

        new_id = archive_service.duplicate_item(item, state='routed')
        updates[ITEM_STATE] = item.get(ITEM_STATE)
        updates[PROCESSED_FROM] = item[config.ID_FIELD]

        get_resource_service('archive_publish').patch(id=new_id, updates=updates)
    elif item.get(ITEM_STATE) == CONTENT_STATE.CORRECTED:
        de_item = archive_service.find_one(req=None, processed_from=item[config.ID_FIELD])

        if not de_item:
            raise StopDuplication

        fields_to_correct = (
            'abstract', 'annotations', 'anpa_category', 'anpa_take_key', 'archive_description', 'associations',
            'attachments', 'authors', 'body_footer', 'body_html', 'body_text', 'byline', 'company_codes', 'creditline',
            'dateline', 'deleted_groups', 'description_text', 'ednote', 'expiry', 'extra', 'fields_meta', 'genre',
            'groups', 'headline', 'keywords', 'more_coming', 'place', 'profile', 'sign_off', 'signal', 'slugline',
            'sms_message', 'source', 'subject', 'urgency', 'word_count', 'priority'
        )

        for field in fields_to_correct:
            if item.get(field):
                de_item[field] = item[field]

        get_resource_service('archive_correct').patch(de_item[config.ID_FIELD], de_item)

    # we don't want duplication, we stop here internal_destinations workflow
    raise StopDuplication


name = 'Set German and Publish'
label = name
callback = set_german_and_publish
access_type = 'frontend'
action_type = 'direct'
