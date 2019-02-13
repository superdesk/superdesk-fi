# -*- coding: utf-8; -*-
# This file is part of Superdesk.
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
#
# Author  : Pablo Varela
# Creation: 2019-02-12 11:59

from superdesk.commands.data_updates import DataUpdate
from superdesk import get_resource_service
from eve.utils import ParsedRequest
from bson import ObjectId


class DataUpdate(DataUpdate):

    resource = 'published'

    def forwards(self, mongodb_collection, mongodb_database):
        archive_service = get_resource_service('archive')
        published_service = get_resource_service(self.resource)
        templates_service = get_resource_service('content_templates')

        templates = list(templates_service.get(req=None, lookup={
            'template_name': 'article'
        }))
        if len(templates) != 1:
            return
        article_template_id = templates[0].get('_id')

        req = ParsedRequest()
        req.max_results = 50
        for page in range(1, 200): # 10k limit
            req.page = page
            items = list(published_service.get(req=req, lookup=None))
            if not items:
                break
            for item in items:
                if ObjectId(item.get('template')) != article_template_id:
                    extra = item.get('extra')
                    if extra is not None:
                        extra.pop('compliantlifetime', None)
                        published_service.system_update(ObjectId(item['_id']), {'extra': extra}, item)

                        archive_item = archive_service.find_one(req=None, _id=item.get('item_id'))
                        if archive_item:
                            archive_service.system_update(archive_item.get('_id'), {'extra': extra}, archive_item)

    def backwards(self, mongodb_collection, mongodb_database):
        pass
