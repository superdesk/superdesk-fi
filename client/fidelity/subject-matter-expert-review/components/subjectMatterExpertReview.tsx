import React from 'react';
import { connectServices } from 'superdesk-core/scripts/core/helpers/ReactRenderAsync';
import { ItemList } from 'superdesk-core/scripts/apps/search/components/ItemList';

interface IProps {
    // services
    monitoringState?: any;
    contentApiSearch?: any;
    search: any;
}

interface IState {
    itemsById: any;
    itemsList: any;
}

export class SubjectMatterExpertReviewComponent extends React.Component<IProps, IState> {
    constructor(props) {
        super(props);

        this.state = {
            itemsList: [],
            itemsById: {},
        };
    }
    componentDidMount() {
        const { contentApiSearch, search } = this.props;

        const criteria = contentApiSearch.getCriteria();

        return contentApiSearch.query(criteria).then((items) => {
            const itemsById = {};
            const itemsList = [];

            items._items.forEach((item) => {
                var itemId = search.generateTrackByIdentifier(item);
                itemsList.push(itemId);
                itemsById[itemId] = item;
            });

            this.setState({
                itemsById,
                itemsList
            });
        });
    }
    render() {
        if (this.state.itemsList.length < 1) {
            return <div>loading...</div>;
        }

        return (
            <div id="subject-matter">
                <div className="subnav subnav--absolute">
                    <header className="search-page-header">
                        <div style={{ display: 'flex', alignItems: 'center', width: '100%', marginRight: '20px' }}>
                            <span className="subnav__page-title">
                                {gettext('Subject matter expert review page')}
                            </span>
                        </div>
                    </header>
                </div>
                <section className="search main-section search-page-container">
                    <div className="archive-content">
                        {/* TODO: fix spacing */}
                        <br />
                        <br />
                        <br />
                        <br />
                        <br />

                        <div className="preview-layout closed">
                            <div className="list-pane">
                                <div id="content-list" className="content">
                                    <div className="shadow-list-holder">
                                        <ItemList
                                            scope={{}}
                                            desksById={{}}
                                            highlightsById={{}}
                                            ingestProvidersById={{}}
                                            markedDesksById={{}}
                                            profilesById={{}}
                                            usersById={{}}
                                            narrow={false}
                                            swimlane={false}
                                            handleItemsChange={() => { }}
                                            itemsList={this.state.itemsList}
                                            itemsById={this.state.itemsById}
                                            view={'compact'}
                                            elementForListeningKeyEvents={$('div')}
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        );
    }
}


export const SubjectMatterExpertReview = connectServices<IProps>(
    SubjectMatterExpertReviewComponent,
    [
        'monitoringState',
        'contentApiSearch',
        'search',
    ],
);
