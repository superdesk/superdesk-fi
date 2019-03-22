import React from 'react';
import {getGenericListPageComponent, GenericListPageComponent} from 'superdesk-core/scripts/core/ui/components/ListPage/generic-list-page';
import {IFormField, IFormGroup} from 'superdesk-core/scripts/core/ui/components/generic-form/interfaces/form';
import {ListItemColumn, ListItem} from 'superdesk-core/scripts/core/components/ListItem';
import {gettext} from 'superdesk-core/scripts/core/utils';
import {getFormFieldPreviewComponent} from 'superdesk-core/scripts/core/ui/components/generic-form/form-field';
import {IKnowledgeBaseItem} from 'superdesk-core/scripts/superdesk-interfaces/KnowledgeBaseItem';
import {Positioner} from 'superdesk-ui-framework';
import {ListItemActionsMenu} from 'superdesk-core/scripts/core/components/ListItem';

const AnnotationsLibraryPageComponent = getGenericListPageComponent<IKnowledgeBaseItem>('concept_items');

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
                <button id={'knowledgebaseitem' + item._id}>
                    <i className="icon-dots-vertical" />
                </button>
                <Positioner
                    triggerSelector={'#knowledgebaseitem' + item._id}
                    placement="left-start"
                    className="dropdown2"
                >
                    <ul
                        className="dropdown__menu"
                        style={{display: 'block', position: 'static'}}
                    >
                        <li>
                            <div className="dropdown__menu-label">{gettext('Actions')}</div>
                        </li>
                        <li className="dropdown__menu-divider" />
                        <li>
                            <button
                                onClick={() => page.deleteItem(item) }
                                title="Edit"
                            >
                                <i className="icon-pencil" />
                                <span
                                    style={{display: 'inline'}}
                                >
                                    {gettext('Remove')}
                                </span>
                            </button>
                        </li>
                    </ul>
                </Positioner>
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