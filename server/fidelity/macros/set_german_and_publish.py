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
from superdesk.metadata.packages import LINKED_IN_PACKAGES, PACKAGE, RESIDREF
from superdesk.publish.publish_queue import PUBLISHED_IN_PACKAGE
from apps.archive.common import insert_into_versions
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
    archive_publish_service = get_resource_service('archive_publish')

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
            # we need to replace original items by duplicated one with german language.
            # Package item is processed after its content items have been duplicated
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
                            ref["_current_version"] = new_item["_current_version"]
                            new_item_updates = {
                                LINKED_IN_PACKAGES: new_item.get(LINKED_IN_PACKAGES, []),
                                PUBLISHED_IN_PACKAGE: new_id,
                            }
                            new_item_updates[LINKED_IN_PACKAGES].append({PACKAGE: new_id})
                            archive_publish_service.patch(id=new_item[config.ID_FIELD], updates=new_item_updates)
                            insert_into_versions(id_=new_item[config.ID_FIELD])
            updates["groups"] = groups
            archive_publish_service.patch(id=new_id, updates=updates)
        elif len(item.get(LINKED_IN_PACKAGES, [])) > 0:
            # if item is in a package, we don't want to publish it now.
            # it will be published when the package item will go through this macro, at the end.
            archive_service.patch(id=new_id, updates=updates)
            insert_into_versions(id_=new_id)
        else:
            # this is a single item, not part of package
            archive_publish_service.patch(id=new_id, updates=updates)
            insert_into_versions(id_=new_id)
    elif item.get(ITEM_STATE) == CONTENT_STATE.CORRECTED:
        de_item = archive_service.find_one(req=None, processed_from=item[config.ID_FIELD])

        if not de_item:
            raise StopDuplication

        # "groups" and "deleted_groups" are not included here as it is tricky to replicate the correction
        # because references in the "German" (duplicated) item are not the same as the one in the "English"
        # (original) one.
        fields_to_correct = (
            'abstract', 'annotations', 'anpa_category', 'anpa_take_key', 'archive_description', 'associations',
            'attachments', 'authors', 'body_footer', 'body_html', 'body_text', 'byline', 'company_codes', 'creditline',
            'dateline', 'description_text', 'ednote', 'expiry', 'extra', 'fields_meta', 'genre',
            'headline', 'keywords', 'more_coming', 'place', 'profile', 'sign_off', 'signal', 'slugline',
            'sms_message', 'source', 'subject', 'urgency', 'word_count', 'priority'
        )

        for field in fields_to_correct:
            if item.get(field):
                de_item[field] = item[field]

        get_resource_service('archive_correct').patch(de_item[config.ID_FIELD], de_item)
        insert_into_versions(id_=de_item[config.ID_FIELD])

    # we don't want duplication, we stop here internal_destinations workflow
    raise StopDuplication


name = 'Set German and Publish'
label = name
callback = set_german_and_publish
access_type = 'frontend'
action_type = 'direct'
