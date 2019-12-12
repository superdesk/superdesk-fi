#!/usr/bin/env python3
#
# This file is part of Superdesk.
#
# Copyright 2019 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from datetime import datetime
import pytz
from superdesk.tests import TestCase
from superdesk import get_resource_service

TEST_TPL = "ED{year_short} - {year_sequence:04}"


class InternalIdTestCase(TestCase):

    def setUp(self):
        self.app.config.update({
            "INTERNAL_ID_TPL": TEST_TPL,
            "INTERNAL_ID_SET_CUSTOM_FIELD_ID": "internal_id",
            "INTERNAL_ID_APPEND_CUSTOM_FIELDS_IDS": ['disclaimer'],
        })

    def test_internal_id_on_new_item(self):
        """Check that an internal ID corresponding to template is built on item creation"""
        tz = pytz.timezone(self.app.config['DEFAULT_TIMEZONE'])
        now = datetime.now(tz=tz)
        self.app.data.insert(
            "content_types",
            [
                {
                    "_id": "test_profile",
                    "schema": {
                        "headline": {"default": "default_headline"},
                        "internal_id": {"type": "text", "required": False, "enabled": True, "nullable": True},
                        "disclaimer": {"type": "text", "required": False, "enabled": True, "nullable": True},
                    },
                }
            ],
        )
        archive_service = get_resource_service('archive')
        item_id = archive_service.post([{
            "type": "text",
            "profile": "test_profile",
            "body_html": "<p>content</p>",
            "extra": {"disclaimer": "some disclaimer"},
        }])[0]
        new_item = archive_service.find_one(None, _id=item_id)
        expected_tpl = TEST_TPL.format(
            year_short=str(now.year)[-2:],
            year_sequence=1,
        )
        self.assertEqual(
            new_item['extra']['internal_id'],
            expected_tpl
        )
        self.assertEqual(
            new_item['extra']['disclaimer'],
            "some disclaimer<br>{}".format(expected_tpl)
        )

    def test_internal_id_not_set(self):
        """Check that an internal ID is not added if it is not present in profile's schema"""
        self.app.config.update({
            "INTERNAL_ID_TPL": TEST_TPL,
            "INTERNAL_ID_SET_CUSTOM_FIELD_ID": "internal_id",
            "INTERNAL_ID_APPEND_CUSTOM_FIELDS_IDS": ['disclaimer'],
        })
        self.app.data.insert(
            "content_types",
            [
                {
                    "_id": "test_profile",
                    "schema": {
                        "headline": {"default": "default_headline"},
                    },
                }
            ],
        )
        archive_service = get_resource_service('archive')
        item_id = archive_service.post([{
            "type": "text",
            "profile": "test_profile",
            "body_html": "<p>content</p>",
        }])[0]
        new_item = archive_service.find_one(None, _id=item_id)
        self.assertNotIn('internal_id', new_item.get('extra', {}))
