import logging

from superdesk import privilege


logging.getLogger(__name__).setLevel(logging.INFO)


# extra fields to be indexed in elastic
# to be able to use the for filtering
EXTRA_FIELDS = [
    'compliantlifetime',
    'validsince',
    'validuntil',
]


def init_app(app):
    for resource in ['archive', 'published', 'archive_autosave', 'items']:
        for field in EXTRA_FIELDS:
            props = app.config['DOMAIN'][resource]['schema']['extra']['mapping'].setdefault('properties', {})
            props[field] = {'type': 'date'}

    privilege(name='fi_compliance_review', label='Compliance review',
              description='User can access compliance review.')

    privilege(name='fi_subject_matter_expert_review', label='Fidelity SME Review ',
              description='User can access subject matter expert review page.')
