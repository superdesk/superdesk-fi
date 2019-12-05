# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2019 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import logging
from datetime import date, datetime
from html import escape
from flask import current_app as app
from eve.utils import config
import superdesk
from superdesk.celery_app import celery
from apps.archive.common import insert_into_versions
from superdesk.editor_utils import EditorContent

logger = logging.getLogger(__name__)
DEFAULT_EOL_TEXT = "This content is no longer updated by Fidelity International"


class ComplianceEOLCheck(superdesk.Command):
    """Check compliance items which have reached end-of-life and correct them

    If items have just reached end of life (i.e. they expire "today"), they
    will be corrected and setting's ``COMPLIANCE_EOL_TEXT`` will be added at
    beginning of the body.

    Example:
    ::

        $ python manage.py compliance:eol_check

    """

    def run(self):
        logger.info("running compliance end-of-life check")
        archive_service = superdesk.get_resource_service('archive')
        correct_service = superdesk.get_resource_service('archive_correct')
        today = datetime.combine(date.today(), datetime.min.time())
        cursor = archive_service.find({
            "extra.compliantlifetime": today,
        })
        eol_text = app.config.get('COMPLIANCE_EOL_TEXT', DEFAULT_EOL_TEXT)
        nb_corrected = 0
        nb_failed = 0
        for item in cursor:
            updates = {}
            item_id = item[config.ID_FIELD]
            if 'body_text' in item:
                updates['body_text'] = "{eol_text}\n{body_text}".format(
                    eol_text=eol_text,
                    body_text=item['body_text'])
            if 'body_html' in item:
                html = '<p class="compliance-notice">{eol_text}</p>'.format(
                    eol_text=escape(eol_text),
                )
                body_editor = EditorContent.create(item, 'body_html')
                body_editor.prepend('embed', html)
                body_editor.update_item()
                updates['body_html'] = item['body_html']
            try:
                correct_service.patch(item_id, updates)
            except Exception as e:
                logger.warning(
                    "the item {item_id} reached compliance end-of-life, but it cannot "
                    "be corrected: {e}".format(item_id=item_id, e=e))
                nb_failed += 1
                continue
            else:
                try:
                    insert_into_versions(item_id)
                except Exception as e:
                    logger.error(
                        "the item {item_id} could not be inserted into versions: {e}"
                        .format(item_id=item_id, e=e))

            # archive_service.update(item_id, updates, item)
            logger.info("item {item_id} reached compliance end-of-life, it has been corrected".format(item_id=item_id))
            nb_corrected += 1

        logger.info("{nb_corrected} article(s) have been corrected due to compliance eol reached".format(
            nb_corrected=nb_corrected))
        if nb_failed > 0:
            logger.warning(
                "{nb_failed} article(s) could *NOT* be corrected despite reaching "
                "compliance end of life".format(nb_failed=nb_failed))


@celery.task(soft_time_limit=300)
def eol_check():
    ComplianceEOLCheck().run()


superdesk.command('compliance:eol_check', ComplianceEOLCheck())
