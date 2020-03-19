# This file is part of Superdesk.
#
# Copyright 2020 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from nose.tools import assert_raises
from superdesk.tests import TestCase
from superdesk.errors import StopDuplication
from superdesk.metadata.item import ITEM_STATE, CONTENT_STATE, PUBLISH_SCHEDULE, SCHEDULE_SETTINGS
from superdesk import get_resource_service
from fidelity.macros.set_german_and_publish import set_german_and_publish


class SetGermanAndPublishTest(TestCase):

    def test_set_german_and_publish(self):
        with self.app.app_context():
            with assert_raises(StopDuplication):
                item = {
                    "_id": "test_123",
                    "guid": "test_123",
                    "type": "text",
                    "language": "en",
                    PUBLISH_SCHEDULE: {},
                    SCHEDULE_SETTINGS: {},
                }
                set_german_and_publish(item)
            archive_service = get_resource_service('archive')
            new_item = archive_service.find_one(req=None, original_id='test_123')
            self.assertEqual(new_item['language'], 'de')
            self.assertEqual(new_item[ITEM_STATE], CONTENT_STATE.PUBLISHED)
