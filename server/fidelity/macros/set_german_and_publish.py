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
from superdesk.metadata.packages import RESIDREF
from eve.utils import config
from superdesk.metadata.item import (
    ITEM_STATE, ITEM_TYPE, PUBLISH_SCHEDULE, SCHEDULE_SETTINGS, PROCESSED_FROM, CONTENT_STATE, CONTENT_TYPE,
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

        if item[ITEM_TYPE] == CONTENT_TYPE.COMPOSITE:
            # we need to replace original items by duplicated one with german language
            # package item is processed after its content items have been duplicated
            # so we can retrieve them from group refs
            groups = item.get('groups', [])
            for group in groups:
                if group.get('id') != 'root':
                    refs = group.get('refs', [])
                    for ref in refs:
                        if ref.get(RESIDREF):
                            __, ref_item_id, __ = archive_service.packageService.get_associated_item(ref)
                            new_item = archive_service.find_one(req=None, original_id=ref_item_id)
                            if new_item is None:
                                logger.warning(
                                    "no duplicated item found for {ref_item_id}".format(ref_item_id=ref_item_id))
                                continue
                            ref[RESIDREF] = ref['guid'] = new_item['guid']
                            ref["_current_version"] = new_item["version"]
            updates["groups"] = groups

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
