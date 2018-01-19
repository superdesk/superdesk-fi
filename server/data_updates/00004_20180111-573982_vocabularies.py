# -*- coding: utf-8; -*-
# This file is part of Superdesk.
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
#

from superdesk.commands.data_updates import DataUpdate
from superdesk.vocabularies.commands import UpdateVocabulariesInItemsCommand
from apps.prepopulate.app_initialize import AppInitializeWithDataCommand


class DataUpdate(DataUpdate):

    resource = 'vocabularies'

    def forwards(self, mongodb_collection, mongodb_database):
        AppInitializeWithDataCommand().run(entity_name='vocabularies')
        UpdateVocabulariesInItemsCommand().run()

    def backwards(self, mongodb_collection, mongodb_database):
        pass
