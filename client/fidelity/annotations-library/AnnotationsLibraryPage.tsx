import React from 'react';
import {getGenericListPageComponent, GenericListPageComponent} from 'superdesk-core/scripts/core/ui/components/ListPage/generic-list-page';
import {IFormField, IFormGroup, FormFieldType} from 'superdesk-core/scripts/core/ui/components/generic-form/interfaces/form';
import {ListItemColumn, ListItem} from 'superdesk-core/scripts/core/components/ListItem';
import {gettext} from 'superdesk-core/scripts/core/utils';
import {getFormFieldPreviewComponent} from 'superdesk-core/scripts/core/ui/components/generic-form/form-field';
import {IKnowledgeBaseItem} from 'superdesk-core/scripts/superdesk-interfaces/KnowledgeBaseItem';
import {ListItemActionsMenu} from 'superdesk-core/scripts/core/components/ListItem';

const AnnotationsLibraryPageComponent = getGenericListPageComponent<IKnowledgeBaseItem>('concept_items');

export const nameField: IFormField = {
    label : gettext('Name'),
    type: FormFieldType.textSingleLine,
    field: 'name',
    required: true,
};
const languageField: IFormField = {
    label : gettext('Language'),
    type: FormFieldType.vocabularySingleValue,
    field: 'language',
    component_parameters: {
        vocabulary_id: 'languages',
    },
    required: true,
};
const definitionField: IFormField = {
    label : gettext('Definition'),
    type: FormFieldType.textEditor3,
    field: 'definition_html',
    required: true,
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

const renderRow = (key: string, item: IKnowledgeBaseItem, page: GenericListPageComponent<IKnowledgeBaseItem>) => {
    return (
        <ListItem key={key} onClick={() => page.openPreview(item._id)}>
            <ListItemColumn>
                {getFormFieldPreviewComponent(item, nameField)}
            </ListItemColumn>
            <ListItemColumn>
                {getFormFieldPreviewComponent(item, languageField)}
            </ListItemColumn>
            <ListItemColumn ellipsisAndGrow noBorder>
                {getFormFieldPreviewComponent(item, definitionField)}
            </ListItemColumn>
            <ListItemActionsMenu>
                <div style={{display: 'flex'}}>
                    <button
                        onClick={(e) =>  {
                            e.stopPropagation();
                            page.startEditing(item._id);
                        }}
                        title={gettext('Edit')}
                    >
                        <i className="icon-pencil" />
                    </button>

                    <button
                        onClick={(e) => {
                            e.stopPropagation();
                            page.deleteItem(item);
                        }}
                        title={gettext('Remove')}
                    >
                        <i className="icon-trash" />
                    </button>
                </div>
            </ListItemActionsMenu>
        </ListItem>
    );
};

export class AnnotationsLibraryPage extends React.Component {
    render() {
        return (
            <AnnotationsLibraryPageComponent
                formConfig={formConfig}
                renderRow={renderRow}
                newItemTemplate={{cpnat_type: 'cpnat:abstract'}}
            />
        );
    }
}