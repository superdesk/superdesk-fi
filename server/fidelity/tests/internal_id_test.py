#!/usr/bin/env python3
#
# This file is part of Superdesk.
#
# Copyright 2019 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license


import pytz
import fidelity.identifier_generator as id_generator

from datetime import datetime
from superdesk.tests import TestCase
from superdesk import get_resource_service
from settings import INTERNAL_ID_TPL as TEST_TPL


class InternalIdTestCase(TestCase):

    def setUp(self):
        self.app.config.update({
            "INTERNAL_ID_TPL": TEST_TPL,
            "INTERNAL_ID_SET_CUSTOM_FIELD_ID": "internal_id",
            "INTERNAL_ID_APPEND_CUSTOM_FIELDS_IDS": ['disclaimer'],
        })

    def setup_item(self):
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
        data = {
            "type": "text",
            "profile": "test_profile",
            "body_html": "<p>content</p>",
            "extra": {"disclaimer": "some disclaimer"},
        }
        item_id = archive_service.post([data])
        return archive_service.find_one(None, _id=item_id)

    def get_year(self):
        tz = pytz.timezone(self.app.config['DEFAULT_TIMEZONE'])
        now = datetime.now(tz=tz)
        return str(now.year)[-2:]

    def test_internal_id_on_new_item(self):
        """Check that an internal ID corresponding to template is built on item creation"""
        new_item = self.setup_item()
        expected_tpl = TEST_TPL.format(
            prefix="ED",
            year_short=self.get_year(),
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

    def test_internal_id_custom_desk_prefix(self):
        desk = {"name": "wpfh"}
        self.app.data.insert("desks", [desk])
        item = self.setup_item()

        # move to desk
        item["task"] = {"desk": desk["_id"]}
        id_generator.generate_id(None, item)
        self.assertEqual(item["extra"]["internal_id"], TEST_TPL.format(
            prefix="WPFH",
            year_short=self.get_year(),
            year_sequence=1,
        ))

        # move to different stage etc.
        id_generator.generate_id(None, item)
        self.assertEqual(item["extra"]["internal_id"], TEST_TPL.format(
            prefix="WPFH",
            year_short=self.get_year(),
            year_sequence=1,
        ))

        # move to different desk
        item["task"] = {}
        id_generator.generate_id(None, item)
        self.assertEqual(item["extra"]["internal_id"], TEST_TPL.format(
            prefix="ED",
            year_short=self.get_year(),
            year_sequence=2,
        ))
