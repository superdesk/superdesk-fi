# -*- coding: utf-8; -*-
# This file is part of Superdesk.
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
#
# Author  : petr
# Creation: 2022-02-16 14:22

import fidelity

from superdesk.commands.data_updates import BaseDataUpdate


class DataUpdate(BaseDataUpdate):

    resource = 'vocabularies'

    def forwards(self, mongodb_collection, mongodb_database):
        mongodb_collection.find_one_and_update({
            '_id': fidelity.DISCLAIMER,
        }, {
            '$set': {
                'field_type': 'custom',
                'custom_field_type': 'predefined-text',
                'custom_field_config': {'allowSwitchingToFreeText': True},
            },
            '$unset': {
                'field_options': 1,
            },
        })

    def backwards(self, mongodb_collection, mongodb_database):
        mongodb_collection.find_one_and_update({
            '_id': fidelity.DISCLAIMER,
        }, {
            '$set': {
                'field_type': 'text',
                'field_options': {},
            },
            '$unset': {
                'custom_field_type': 1,
                'custom_field_config': 1,
            },
        })
