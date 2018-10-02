
def init_app(app):
    for resource in ['archive', 'published', 'archive_autosave']:
        app.config['DOMAIN'][resource]['schema']['extra']['mapping']['properties'] = (
            {'compliantlifetime': {'type': 'datetime'}})
