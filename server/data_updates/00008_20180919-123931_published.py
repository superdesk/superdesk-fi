# -*- coding: utf-8; -*-
# This file is part of Superdesk.
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
#
# Author  : pablopunk
# Creation: 2018-09-19 12:39

from superdesk.commands.data_updates import DataUpdate
from superdesk import get_resource_service
from datetime import date
from bson import ObjectId


def add_years(d, years):
    d = d.replace(hour=0, minute=0, second=0)
    try:
        return d.replace(year=d.year + years)
    except ValueError:
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))


class DataUpdate(DataUpdate):

    resource = 'published'

    def forwards(self, mongodb_collection, mongodb_database):
        archive_service = get_resource_service('archive')
        published_service = get_resource_service(self.resource)

        for item in published_service.get(req=None, lookup=None):
            published_date = item.get('firstpublished')

            if published_date is not None:
                compliant_lifetime = add_years(published_date, 1)

                extra = item.get('extra', {})
                extra['compliantlifetime'] = compliant_lifetime

                published_service.system_update(ObjectId(item['_id']), {'extra': extra}, item)

                archive_item = archive_service.find_one(req=None, _id=item['item_id'])
                if archive_item:
                    archive_service.system_update(archive_item['_id'], {'extra': extra}, archive_item)

    def backwards(self, mongodb_collection, mongodb_database):
        pass

