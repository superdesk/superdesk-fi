# -*- coding: utf-8; -*-
# This file is part of Superdesk.
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
#
# Author  : petr
# Creation: 2017-11-23 11:43

from superdesk.commands.data_updates import DataUpdate


class DataUpdate(DataUpdate):

    resource = 'vocabularies'

    def forwards(self, mongodb_collection, mongodb_database):
        _ids = ['categories', 'author']
        return mongodb_collection.delete_many({'_id': {'$in': _ids}})

    def backwards(self, mongodb_collection, mongodb_database):
        pass
