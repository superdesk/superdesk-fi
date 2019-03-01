import React from 'react';
import {NavTabs} from 'superdesk-core/scripts/core/ui/components';
import {IKnowledgeBaseItem} from 'superdesk-core/scripts/apps/knowledge-base/knowledge-base-page';
import {connectCrudManager, ICrudManager} from 'superdesk-core/scripts/core/helpers/CrudManager';
import {gettext} from 'superdesk-core/scripts/core/utils';
import {IPropsAnnotationInputComponent} from 'superdesk-core/scripts/core/editor3/components/annotations/AnnotationInput';

import {AnnotationsSelect} from './AnnotationsSelect';

interface IProps extends IPropsAnnotationInputComponent {
    // connected
    conceptItems?: ICrudManager<IKnowledgeBaseItem>;
}

class AnnotationInputWithKnowledgeBaseComponent extends React.Component<IProps> {
    private tabsRef: NavTabs;

    componentDidMount() {
        this.props.conceptItems.read(1, null, {'name': this.props.annotationText})
            .then(() => {
                if (this.props.conceptItems._meta.total < 1) {
                    // go to new annotation tab if there aren't existing ones to select from
                    this.tabsRef.selectTabByIndex(1);
                }
            });
    }

    render() {
        if (this.props.conceptItems._items == null) {
            return null; // loading
        }

        const tabs = [
            {
                label: gettext('Annotation library'),
                render: () => (
                    <AnnotationsSelect
                        annotationText={this.props.annotationText}
                        onApplyAnnotation={this.props.onApplyAnnotation}
                        annotationTypeSelect={this.props.annotationTypeSelect}
                        onCancel={this.props.onCancel}
                        conceptItems={this.props.conceptItems}
                    />
                ),
            },
            {
                label: gettext('New annotation'),
                render: () => <div style={{marginTop: 15}}>{this.props.annotationInputComponent}</div>,
            },
        ];

        return (
            <NavTabs
                tabs={tabs}
                active={0}
                ref={(r) => {
                    this.tabsRef = r;
                }}
            />
        );
    }
}

export const AnnotationInputWithKnowledgeBase = connectCrudManager<IProps, IKnowledgeBaseItem>(
    AnnotationInputWithKnowledgeBaseComponent,
    'conceptItems',
    'concept_items',
);
