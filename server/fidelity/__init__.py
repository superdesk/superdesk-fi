from superdesk import privilege


def init_app(app):
    for resource in ['archive', 'published', 'archive_autosave']:
        app.config['DOMAIN'][resource]['schema']['extra']['mapping']['properties'] = (
            {'compliantlifetime': {'type': 'date'}})

    privilege(name='fi_compliance_review', label='Fidelity compliance review',
              description='User can access compliance review.')
