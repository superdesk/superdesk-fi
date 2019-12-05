# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2019 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from html import escape
from datetime import date, datetime
from superdesk.tests import TestCase
from superdesk import get_resource_service
from fidelity.compliance import ComplianceEOLCheck, DEFAULT_EOL_TEXT


class ComplianceCorrectionTestCase(TestCase):

    def test_compliant_correction_body(self):
        self.assertTrue(len(DEFAULT_EOL_TEXT.strip()) > 0)
        today = datetime.combine(date.today(), datetime.min.time())
        self.app.data.insert('archive', [
            {
                '_id': '123',
                'unique_name': '123',
                'guid': '123',
                'type': 'text',
                '_current_version': 1,
                'state': 'published',
                'body_text': 'original_text',
                'body_html': '<p>original_html</p>',
                'extra': {'compliantlifetime': today},
            },
        ])
        ComplianceEOLCheck().run()
        archive_service = get_resource_service('archive')
        item = archive_service.find_one(None, _id='123')
        self.assertTrue(item['body_text'].startswith(DEFAULT_EOL_TEXT))
        self.assertTrue(item['body_html'].startswith(
            '<div class="embed-block"><p class="compliance-notice">{DEFAULT_EOL_TEXT}</p></div>'.format(
                DEFAULT_EOL_TEXT=escape(DEFAULT_EOL_TEXT))))
        archive_versions_service = get_resource_service('archive_versions')
        version_item = archive_versions_service.find_one(None, guid='123', _current_version=2)
        self.assertIsNotNone(version_item)
