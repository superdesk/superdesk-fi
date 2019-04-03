import React from "react";
import {Item, Column, Row} from "superdesk-core/scripts/core/ui/components/List";
import {UserHtmlSingleLine} from "superdesk-core/scripts/core/helpers/UserHtmlSingleLine";
import {IKnowledgeBaseItem} from "superdesk-core/scripts/superdesk-interfaces/KnowledgeBaseItem";

interface IProps {
    onSelect(item: IKnowledgeBaseItem): void;
    onCancel(): void;
    backButton: JSX.Element;
    items: Array<IKnowledgeBaseItem>;
}

export class AnnotationSelectList extends React.Component<IProps> {
    render() {
        return (
            <div>
                <div style={{maxHeight: '20rem', overflow: 'auto', paddingTop: 15}}>
                    {this.props.items.map((item, i) => (
                        <Item key={i} onClick={() => this.props.onSelect(item)}>
                            <Column grow>
                                <Row><strong>{item.name}</strong></Row>
                                <Row>
                                    <span className="sd-overflow-ellipsis sd-list-item--element-grow">
                                        <UserHtmlSingleLine html={item.definition_html} />
                                    </span>
                                </Row>
                            </Column>
                        </Item>
                    ))}
                </div>
                {this.props.backButton}
            </div>
        );
    }
}
