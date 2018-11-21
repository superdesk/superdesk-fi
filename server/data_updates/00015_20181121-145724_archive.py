# -*- coding: utf-8; -*-
# This file is part of Superdesk.
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
#
# Author  : Jérôme
# Creation: 2018-11-21 14:57

from superdesk.commands.data_updates import DataUpdate


class DataUpdate(DataUpdate):
    """This migration add "translated_from" field to all items translated using manual duplication"""
    resource = 'archive'

    def forwards(self, collection, database):
        modified_count = 0
        for item in collection.find(
            {
                'language': {'$ne': None},
                'original_id': {'$ne': None},
                'translated_from': None}):
            duplicated_id = item['original_id']
            # duplicated item is the original item of the translation,
            # but it may not be the first item (i.e. original story)
            duplicated_item = collection.find_one({'_id': duplicated_id})

            if duplicated_item is None:
                print("Missing original item: {duplicated_id}".format(duplicated_id=duplicated_id))
                continue

            duplicated_lang = duplicated_item.get('language')

            if duplicated_lang and duplicated_lang != item['language']:
                # we go back up to first item to find the right translation_id
                source_item = duplicated_item
                while True:
                    source_id = source_item.get('original_id')
                    if source_id is None:
                        break
                    source_item = collection.find_one({'_id': source_id})
                    if source_item is None:
                        break

                if source_item is None:
                    print("Missing source item: {source_id}".format(source_id=source_id))
                    continue

                # at this point, source_item is the original article (the first item, before any translation)
                source_id = source_item['_id']
                translation_id = source_item.get('translation_id', source_id)

                up_result = collection.update_one(
                    {'_id': item['_id']},
                    {'$set': {
                        'translation_id': translation_id,
                        'translated_from': duplicated_id}})
                modified_count += up_result.modified_count

                # original item must have a translation_id too
                if 'translation_id' not in duplicated_item:
                    up_result = collection.update_one(
                        {'_id': duplicated_item['_id']},
                        {'$set': {
                            'translation_id': translation_id}})
                    modified_count += up_result.modified_count

        if modified_count:
            print("{modified_count} item(s) modified".format(modified_count=modified_count))

    def backwards(self, mongodb_collection, mongodb_database):
        # We can't go backward as we can't distinguish which items have been translated using manual duplication
        # from the ones which have been translated using "translate to".
        pass
