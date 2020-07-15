#!/usr/bin/env python3
# This file is part of Superdesk.
#
# Copyright 2018 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

"""Unit tests for Qumu module"""

import sys
import re
from unittest import skipIf
from superdesk.tests import TestCase
from superdesk.editor_utils import Editor3Content
from fidelity.qumu import qumu_embed_pre_process


class QumuTestCase(TestCase):

    def build_item(self, draftjs_data, field='body_html'):
        return {
            'fields_meta': {
                field: {
                    'draftjsState': [draftjs_data],
                },
            },
        }

    @skipIf(
        sys.version_info[:2] <= (3, 5),
        "Python 3.5 doesn't keep dict key insertion order, making this test fail"
    )
    def test_qumu_embed_pre_process(self):
        """Check that Qumu embed is pre-processed, with json dump and selector added

        cf. SDESK-4939 and SDFID-5
        """
        self.app.config['EMBED_PRE_PROCESS'] = [qumu_embed_pre_process]
        draftjs_data = {
            "blocks": [
                {
                    "key": "d60k5",
                    "text": " ",
                    "type": "unstyled",
                    "depth": 0,
                    "inlineStyleRanges": [],
                    "entityRanges": [],
                    "data": {"MULTIPLE_HIGHLIGHTS": {}},
                },
                {
                    "key": "dusi6",
                    "text": " ",
                    "type": "atomic",
                    "depth": 0,
                    "inlineStyleRanges": [],
                    "entityRanges": [{"offset": 0, "length": 1, "key": 0}],
                    "data": {},
                },
                {
                    "key": "dr7r5",
                    "text": "",
                    "type": "unstyled",
                    "depth": 0,
                    "inlineStyleRanges": [],
                    "entityRanges": [],
                    "data": {},
                },
            ],
            "entityMap": {
                "0": {
                    "type": "EMBED",
                    "mutability": "MUTABLE",
                    "data": {
                        "data": {
                            "html": '<script type="text/javascript" src="https://video.fidelity.tv/widgets/application'
                                    '.js"></script> <script type="text/javascript"> KV.widget({   "guid": "LS80jXTAMH9'
                                    '",   "type": "thumbnail",   "playerType": "full",   "size": 10 }); </script>'
                        }
                    },
                }
            },
        }
        item = self.build_item(draftjs_data)
        body_editor = Editor3Content(item)
        body_editor.update_item()
        expected = (
            '<div class="embed-block"><script type="text/javascript" src="https://video.fidelity.tv/widgets/application'
            '.js"></script><script type="text/javascript"> KV.widget({"guid": "LS80jXTAMH9", "type": "thumbnail", "play'
            'erType": "full", "size": 10, "selector": "qumu-UUID_RE"}); </script><div id="qumu-UUID_RE"></div></div>'
        )

        # we have to use a regex because the UUID of the selector is not predictable
        expected_re = re.escape(expected).replace("UUID_RE", '[-0-9a-f]+')
        self.assertIsNotNone(re.match(expected_re, item['body_html']))
