# This file is part of Superdesk.
#
# Copyright 2019 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import logging
import pytz
from datetime import datetime
from superdesk import app, get_resource_service
from superdesk.signals import item_create

logger = logging.getLogger(__name__)


def generate_id(sender, item, **kwargs):
    content_types_service = get_resource_service('content_types')
    try:
        profile = content_types_service.find_one(None, _id=item['profile'])
    except KeyError:
        return
    if profile is None:
        logger.warning("Can't find profile {profile}".format(profile=item['profile']))
        return
    set_field_id = app.config['INTERNAL_ID_SET_CUSTOM_FIELD_ID']
    if set_field_id not in profile['schema']:
        return
    extra = item.setdefault('extra', {})
    tz = pytz.timezone(app.config['DEFAULT_TIMEZONE'])
    now = datetime.now(tz=tz)
    template = app.config['INTERNAL_ID_TPL']
    sequences_service = get_resource_service('sequences')
    sequence_key = 'fidelity_internal_id_{year}'.format(year=now.year)
    sequence_number = sequences_service.get_next_sequence_number(sequence_key)
    internal_id = template.format(
        year_short=str(now.year)[-2:],
        year_sequence=sequence_number,
    )
    extra[set_field_id] = internal_id
    for field_id in app.config['INTERNAL_ID_APPEND_CUSTOM_FIELDS_IDS']:
        if field_id in profile['schema']:
            extra[field_id] = extra.setdefault(field_id, '') + '<br>' + internal_id


def init_app(app):
    item_create.connect(generate_id)
