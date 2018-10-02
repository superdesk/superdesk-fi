#!/usr/bin/env python
# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import os
from pathlib import Path
from superdesk.default_settings import INSTALLED_APPS


def env(variable, fallback_value=None):
    env_value = os.environ.get(variable, '')
    if len(env_value) == 0:
        return fallback_value
    else:
        if env_value == "__EMPTY__":
            return ''
        else:
            return env_value


ABS_PATH = str(Path(__file__).resolve().parent)

init_data = Path(ABS_PATH) / 'data'
if init_data.exists():
    INIT_DATA_PATH = init_data

INSTALLED_APPS.extend([
    'apps.languages',
    'superdesk.auth.saml',
    'fidelity',
])

RENDITIONS = {
    'picture': {
        'thumbnail': {'width': 220, 'height': 120},
        'viewImage': {'width': 640, 'height': 640},
        'baseImage': {'width': 1400, 'height': 1400},
    },
    'avatar': {
        'thumbnail': {'width': 60, 'height': 60},
        'viewImage': {'width': 200, 'height': 200},
    }
}

WS_HOST = env('WSHOST', '0.0.0.0')
WS_PORT = env('WSPORT', '5100')

LOG_CONFIG_FILE = env('LOG_CONFIG_FILE', 'logging_config.yml')

REDIS_URL = env('REDIS_URL', 'redis://localhost:6379')
if env('REDIS_PORT'):
    REDIS_URL = env('REDIS_PORT').replace('tcp:', 'redis:')
BROKER_URL = env('CELERY_BROKER_URL', REDIS_URL)

SECRET_KEY = env('SECRET_KEY', '')

LEGAL_ARCHIVE = True

#: Defines default value for genre to be set for manually created articles
DEFAULT_GENRE_VALUE_FOR_MANUAL_ARTICLES = env('DEFAULT_GENRE_VALUE_FOR_MANUAL_ARTICLES', [])
DEFAULT_URGENCY_VALUE_FOR_MANUAL_ARTICLES = 1

DEFAULT_LANGUAGE = 'en'

LANGUAGES = [
    {'language': 'en', 'label': 'English', 'source': True, 'destination': True},
    {'language': 'fr', 'label': 'French', 'source': True, 'destination': True},
    {'language': 'de', 'label': 'German', 'source': True, 'destination': True},
    {'language': 'es', 'label': 'Spanish', 'source': True, 'destination': True},
    {'language': 'it', 'label': 'Italian', 'source': True, 'destination': True},
    {'language': 'sv', 'label': 'Swedish', 'source': True, 'destination': True},
    {'language': 'nb', 'label': 'Norwegian', 'source': True, 'destination': True},
    {'language': 'pl', 'label': 'Polish', 'source': True, 'destination': True},
    {'language': 'zh-cn', 'label': 'Simplified Chinese', 'source': True, 'destination': True},
    {'language': 'zh-hk', 'label': 'Traditional Chinese (HK)', 'source': True, 'destination': True},
    {'language': 'ja', 'label': 'Japanese', 'source': True, 'destination': True},
    {'language': 'ko', 'label': 'Korean', 'source': True, 'destination': True},
    {'language': 'zh-tw', 'label': 'Traditional Chinese (TW)', 'source': True, 'destination': True},
    {'language': 'nl', 'label': 'Dutch', 'source': True, 'destination': True}
]

SAML_PATH = env('SAML_PATH', os.path.join(ABS_PATH, 'saml'))

SCHEMA = {
    'composite': {
        'slugline': {'required': True},
        'language': {'required': True},
        'subject': {'type': 'list'},
    },
}

EDITOR = {
    'composite': {
        'slugline': {'order': 1, 'sdWidth': 'half'},
        'language': {'order': 2, 'sdWidth': 'half'},
        'subject_custom': {'order': 3, 'sdWidth': 'half'},
    },
}

OVERRIDE_EDNOTE_FOR_CORRECTIONS = False
