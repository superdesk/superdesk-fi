# This file is part of Superdesk.
#
# Copyright 2013, 2020 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
import logging
from copy import deepcopy
from eve.utils import config
from typing import Tuple
from apps.tasks import send_to
from apps.archive.common import insert_into_versions
from apps.packages.package_service import get_item_ref
from superdesk import get_resource_service
from superdesk.errors import StopDuplication
from superdesk.metadata.packages import LINKED_IN_PACKAGES, PACKAGE, RESIDREF
from superdesk.publish.publish_queue import PUBLISHED_IN_PACKAGE
from superdesk.services import BaseService
from superdesk.metadata.item import (
    ITEM_STATE, ITEM_TYPE, PUBLISH_SCHEDULE, SCHEDULE_SETTINGS, PROCESSED_FROM, CONTENT_STATE, CONTENT_TYPE,
)


logger = logging.getLogger(__name__)


def create_de_item(archive_service: BaseService, item: dict) -> Tuple[str, dict]:
    """Duplicate item and return new id and updates to use for German item"""
    updates = {
        PUBLISH_SCHEDULE: item[PUBLISH_SCHEDULE],
        SCHEDULE_SETTINGS: item[SCHEDULE_SETTINGS],
        'language': 'de',
    }

    new_id = archive_service.duplicate_item(item, state='routed')
    updates[ITEM_STATE] = item.get(ITEM_STATE)
    updates[PROCESSED_FROM] = item[config.ID_FIELD]
    return new_id, updates


def set_german_and_publish(item, **kwargs):
    """
    Set item language to german and publish it
    """

    if item.get('language') != 'en':
        raise StopDuplication

    try:
        dest_desk_id = kwargs["dest_desk_id"]
        dest_stage_id = kwargs["dest_stage_id"]
    except KeyError:
        logger.warning(
            'missing "dest_desk_id" or "dest_stage_id", is this macro ({name}) used in Internal Destination?'
            .format(name=name))
        raise StopDuplication

    archive_service = get_resource_service('archive')
    archive_publish_service = get_resource_service('archive_publish')

    if item.get(ITEM_STATE) == CONTENT_STATE.PUBLISHED:
        new_id, updates = create_de_item(archive_service, item)

        if item[ITEM_TYPE] == CONTENT_TYPE.COMPOSITE:
            # we need to replace original items by duplicated one with german language.
            # Package item is processed after its content items have been duplicated
            # so we can retrieve them from group refs
            groups = item.get('groups', [])
            for group in groups:
                if group.get('id') != 'root':
                    refs = group.setdefault('refs', [])
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

        de_item_id = de_item[config.ID_FIELD]

        # "groups" is handled below
        fields_to_correct = (
            'abstract', 'annotations', 'anpa_category', 'anpa_take_key', 'archive_description', 'associations',
            'attachments', 'authors', 'body_footer', 'body_html', 'body_text', 'byline', 'company_codes', 'creditline',
            'dateline', 'description_text', 'deleted_groups', 'ednote', 'expiry', 'extra', 'fields_meta', 'genre',
            'headline', 'keywords', 'more_coming', 'place', 'profile', 'sign_off', 'signal', 'slugline',
            'sms_message', 'source', 'subject', 'urgency', 'word_count', 'priority'
        )

        for field in fields_to_correct:
            if item.get(field):
                de_item[field] = item[field]

        if item[ITEM_TYPE] == CONTENT_TYPE.COMPOSITE:
            # for a package, we need to synchronise references, in case of items have been added or removed from it
            de_item_groups = de_item['groups']

            # groups id to set of items id map for original items (root is skipped)
            ori_group_refs = {}
            for group in item.get('groups', []):
                if group.get('id') != 'root':
                    ori_refs = ori_group_refs[group['id']] = set()
                    refs = group.get('refs', [])
                    for ref in refs:
                        if ref.get(RESIDREF):
                            __, ref_item_id, __ = archive_service.packageService.get_associated_item(ref)
                            ori_refs.add(ref_item_id)

            # group id to dicts mapping from English item ID to their duplicated version in German
            # it is used to compare missing/new items below
            dup_group_en_de_map = {}
            for group in de_item.get('groups', []):
                if group.get('id') != 'root':
                    en_de_map = dup_group_en_de_map[group['id']] = {}
                    refs = group.get('refs', [])
                    for ref in refs:
                        if ref.get(RESIDREF):
                            ref_item, ref_item_id, __ = archive_service.packageService.get_associated_item(ref)
                            try:
                                en_de_map[ref_item['processed_from']] = ref_item_id
                            except KeyError:
                                logger.warning(
                                    'missing "processed_from" key in referenced item {ref_item_id} from package '
                                    '{item_id}'.format(
                                        ref_item_id=ref_item_id,
                                        item_id=ref_item[config.ID_FIELD]))
                                continue

            # we delete groups in German package which don't exist in English one
            groups_to_delete = []
            for deleted_group in dup_group_en_de_map.keys() - ori_group_refs.keys():
                for group in groups:
                    if group['id'] == deleted_group:
                        groups_to_delete.append(group)
                        break
                else:
                    logger.error("Internal error: group {group_id} should exist in German item {item_id}".format(
                        group_id=deleted_group,
                        item_id=de_item_id
                    ))
            for group in groups_to_delete:
                de_item_groups.remove(group)

            # now we synchronise items group by group
            for ori_group_id, ori_refs in ori_group_refs.items():
                for de_group in de_item_groups:
                    if de_group['id'] == ori_group_id:
                        en_de_map = dup_group_en_de_map[ori_group_id]
                        break
                else:
                    # the group doesn't exist in German package, we create it
                    ori_group = next(g for g in item['groups'] if g['id'] == ori_group_id)
                    de_group = {
                        'id': ori_group_id,
                        'role': ori_group['role'],
                        'refs': [],
                    }
                    de_item_groups.append(de_group)
                    de_group_root = next(g for g in de_item_groups if g['id'] == 'root')
                    de_group_root['refs'].append({"idRef": ori_group_id})
                    en_de_map = {}

                # we synchronise new items
                new_refs = ori_refs - en_de_map.keys()
                for new_ref in new_refs:
                    # we check if we have already a duplicate version of this item
                    dup_ref_item = archive_service.find_one(req=None, original_id=new_ref, language="de")
                    if dup_ref_item is None:
                        # we have to duplicate the item, basically reproducing what would happen
                        # with publish workflow
                        logger.info("creating German item for {item_id}".format(item_id=new_ref))
                        ori_ref_item = archive_service.find_one(req=None, guid=new_ref)
                        # we imitate internal destination
                        ori_ref_item_cpy = deepcopy(ori_ref_item)
                        send_to(ori_ref_item_cpy, desk_id=dest_desk_id, stage_id=dest_stage_id)
                        new_id, updates = create_de_item(archive_service, ori_ref_item_cpy)
                        dup_ref_item = archive_service.find_one(req=None, guid=new_id)
                        updates[LINKED_IN_PACKAGES] = dup_ref_item.setdefault(LINKED_IN_PACKAGES, [])
                        dup_ref_item[PUBLISHED_IN_PACKAGE] = updates[PUBLISHED_IN_PACKAGE] = de_item_id
                        updates[LINKED_IN_PACKAGES].append({PACKAGE: de_item_id})

                        archive_publish_service.patch(id=new_id, updates=updates)
                        insert_into_versions(id_=new_id)
                    else:
                        # the item already exists, let's update it
                        updates = {
                            LINKED_IN_PACKAGES: dup_ref_item.setdefault(LINKED_IN_PACKAGES, []),
                            PUBLISHED_IN_PACKAGE: de_item_id,
                        }
                        updates[LINKED_IN_PACKAGES].append({PACKAGE: de_item_id})
                        archive_service.system_update(id=dup_ref_item["guid"], updates=updates, original=dup_ref_item)

                    # we have the German item, now we create the ref to update German package
                    new_ref = get_item_ref(dup_ref_item)
                    new_ref['guid'] = new_ref[RESIDREF]
                    de_group['refs'].append(new_ref)

                # now we remove items removed from English version
                deleted_refs = en_de_map.keys() - ori_refs
                for deleted_ref in deleted_refs:
                    de_deleted_ref = en_de_map[deleted_ref]
                    for ref in de_group['refs']:
                        if ref.get('guid') == de_deleted_ref:
                            break
                    de_group['refs'].remove(ref)

        get_resource_service('archive_correct').patch(de_item[config.ID_FIELD], de_item)
        insert_into_versions(id_=de_item[config.ID_FIELD])

    # we don't want duplication, we stop here internal_destinations workflow
    raise StopDuplication


name = 'Set German and Publish'
label = name
callback = set_german_and_publish
access_type = 'frontend'
action_type = 'direct'
