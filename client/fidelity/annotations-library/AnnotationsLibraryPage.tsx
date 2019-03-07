import React from 'react';
import {KnowledgeBasePage, IKnowledgeBaseItem} from 'superdesk-core/scripts/apps/knowledge-base/knowledge-base-page';
import {IFormField, IFormGroup} from 'superdesk-core/scripts/apps/knowledge-base/generic-form/interfaces/form';
import {ListItemColumn} from 'superdesk-core/scripts/core/components/ListItem';
import {gettext} from 'superdesk-core/scripts/core/utils';
import {getFormFieldPreviewComponent} from 'superdesk-core/scripts/apps/knowledge-base/generic-form/form-field';

const nameField: IFormField = {
    label : gettext('Name'),
    type: 'text_single_line',
    field: 'name',
};
const languageField: IFormField = {
    label : gettext('Language'),
    type: 'vocabulary_single_value',
    field: 'language',
    component_parameters: {
        vocabulary_id: 'languages',
    },
};
const definitionField: IFormField = {
    label : gettext('Definition'),
    type: 'text_single_line',
    field: 'definition',
};

const formConfig: IFormGroup = {
    direction: 'vertical',
    type: 'inline',
    form: [
        nameField,
        languageField,
        definitionField,
    ],
};

const renderConceptItemRow = (item: IKnowledgeBaseItem) => {
    return (
        <React.Fragment>
            <ListItemColumn>
                {getFormFieldPreviewComponent(item, nameField)}
            </ListItemColumn>
            <ListItemColumn>
                {getFormFieldPreviewComponent(item, languageField)}
            </ListItemColumn>
            <ListItemColumn ellipsisAndGrow noBorder>
                {getFormFieldPreviewComponent(item, definitionField)}
            </ListItemColumn>
        </React.Fragment>
    );
};

export class AnnotationsLibraryPage extends React.Component {
    render() {
        return (
            <KnowledgeBasePage
                formConfig={formConfig}
                renderConceptItemRow={renderConceptItemRow}
            />
        );
    }
}