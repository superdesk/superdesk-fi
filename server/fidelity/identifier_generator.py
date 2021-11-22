# This file is part of Superdesk.
#
# Copyright 2019 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import logging
import pytz
import superdesk.signals as signals
from datetime import datetime
from superdesk import app, get_resource_service

logger = logging.getLogger(__name__)

DEFAULT_PREFIX = "ED"


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
    prefix = get_prefix(item)
    if extra.get(set_field_id) and prefix in extra[set_field_id]:
        return
    sequences_service = get_resource_service('sequences')
    sequence_key = 'fidelity_internal_id_{year}'.format(year=now.year) if prefix == DEFAULT_PREFIX else \
        'fidelity_internal_id_{year}_{desk}'.format(year=now.year, desk=prefix)
    sequence_number = sequences_service.get_next_sequence_number(sequence_key)
    internal_id = template.format(
        prefix=prefix,
        year_short=str(now.year)[-2:],
        year_sequence=sequence_number,
    )
    extra[set_field_id] = internal_id
    for field_id in app.config['INTERNAL_ID_APPEND_CUSTOM_FIELDS_IDS']:
        if field_id in profile['schema']:
            extra[field_id] = extra.setdefault(field_id, '') + '<br>' + internal_id


def get_prefix(item):
    try:
        desk_id = item["task"]["desk"]
    except KeyError:
        pass
    else:
        desk = get_resource_service("desks").find_one(req=None, _id=desk_id)
        if desk and desk.get("name").upper() in app.config["INTERNAL_ID_DESK_MAP"]:
            return app.config["INTERNAL_ID_DESK_MAP"][desk["name"].upper()]
    return DEFAULT_PREFIX


def init_app(app):
    signals.item_create.connect(generate_id)
    signals.item_move.connect(generate_id)
