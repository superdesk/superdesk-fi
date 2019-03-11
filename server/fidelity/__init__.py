from superdesk import privilege


def init_app(app):
    for resource in ['archive', 'published', 'archive_autosave']:
        app.config['DOMAIN'][resource]['schema']['extra']['mapping']['properties'] = (
            {'compliantlifetime': {'type': 'date'}})

    privilege(name='fi_compliance_review', label='Compliance review',
              description='User can access compliance review.')

    privilege(name='fi_subject_matter_expert_review', label='Subject matter expert review page',
              description='User can access subject matter expert review page.')
