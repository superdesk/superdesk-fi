# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2019 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import re
import json
import uuid
import logging
from functools import partial

logger = logging.getLogger(__name__)
QUMU_RE = re.compile(r'KV\.widget\(({.*})\)')


def qumu_config_modifier(match, selector):
    conf_json = json.loads(match.group(1))
    conf_json['selector'] = selector
    return "KV.widget({})".format(json.dumps(conf_json))


def qumu_embed_pre_process(data):
    """dump QUMU config json as string + add selector"""
    try:
        html = data['html']
    except KeyError:
        logging.error('missing "html" key in data: {data}'.format(
            data=data))
        return

    if not QUMU_RE.search(html):
        # this is not a QUMU embed
        return

    try:
        selector = "qumu-{}".format(uuid.uuid4())
        final_div = '<div id="{selector}"></div>'.format(selector=selector)
        data['html'] = QUMU_RE.sub(
            partial(qumu_config_modifier, selector=selector),
            html,
            count=1
        ) + final_div
    except Exception as e:
        logger.warning("Invalid QUMU embed: {e}\n{data}".format(e=e, data=data))
