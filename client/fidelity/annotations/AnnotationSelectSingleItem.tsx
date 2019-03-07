import React from "react";
import {IKnowledgeBaseItem} from 'superdesk-core/scripts/apps/knowledge-base/knowledge-base-page';
import {gettext} from 'superdesk-core/scripts/core/utils';

interface IProps {
    item: IKnowledgeBaseItem;
    annotationTypeSelect: JSX.Element;
    onBack(): void;
    onApplyAnnotation(html: string): void;
}

export class AnnotationSelectSingleItem extends React.Component<IProps> {
    render() {
        return (
            <div>
                <div style={{marginTop: 20}}>
                    {this.props.annotationTypeSelect}
                </div>
                <h3 style={{marginTop: 15}}>{this.props.item.name}</h3>
                <div
                    style={{maxHeight: '15rem', overflow: 'auto', marginTop: 15}}
                    dangerouslySetInnerHTML={{__html: this.props.item.definition}}
                />
                <div className="space-between" style={{marginTop: 15}}>
                    <button className="btn btn--primary" onClick={this.props.onBack}>
                        {gettext('Back to results')}
                    </button>
                    <button
                        className="btn btn--primary"
                        onClick={() => this.props.onApplyAnnotation(this.props.item.definition)}
                    >
                        {gettext('Use this')}
                    </button>
                </div>
            </div>
        );
    }
}
