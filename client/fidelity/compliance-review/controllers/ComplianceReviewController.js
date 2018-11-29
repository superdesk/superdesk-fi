import { get } from 'lodash';
import moment from 'moment';
import { getDateFilters } from 'superdesk-core/scripts/apps/search/directives/DateFilters';
import CompliantLifetimeComponent from '../components/CompliantLifetime';
import VersionCreatedComponent from '../components/VersionCreated';
import { getStatus } from '../compliance-status';

const filterToDaysDiff = (filter) => {
    switch (filter) {
        case 'before_next_month': return 30;
        case 'before_3_months_ahead': return 90;
        default: return 0;
    }
};

ComplianceReviewCtrl.$inject = ['$location', 'moment', 'gettext', '$scope'];
export function ComplianceReviewCtrl($location, moment, gettext, $scope) {
    const SUPERDESK = 'local';

    // old versions of corrected items can
    // have a date that doesn't match the filter
    const filterOldVersions = (items) => {
        const range = filterToDaysDiff(getFilterFromUrl());
        const now = moment();
        $scope.items._items = items.filter(({ archive_item }) => {
            const lifetime = moment(archive_item.extra.compliantlifetime);
            return lifetime.diff(now, 'days') < range;
        });
    };


    const watchItems = (items) => {
        if (items) {
            filterOldVersions(items._items);
            $scope.numberOfItems = items._items.length;
        }
    }

    const compliantFilter = getDateFilters(gettext).find(
        f => f.fieldname === 'extra.compliantlifetime',
    );
    this.filters = compliantFilter.predefinedFilters;
    this.activeFilter = 0;
    $scope.numberOfItems = 0;
    const sortString = 'extra.compliantlifetime:asc';

    $location.search('sort', sortString);

    // helper fns

    const filterExists = (key) => this.filters.some((f) => f.key === key);
    const getFilterIndex = (key) => this.filters.findIndex((f) => f.key === key);
    const setFilterInUrl = (filter) => $location.search('deadline', filter);
    const getFilterFromUrl = () => $location.search().deadline;
    const setDefaultFilter = () => setFilterInUrl(this.filters[0].key);

    if (filterExists(getFilterFromUrl())) {
        this.activeFilter = getFilterIndex(getFilterFromUrl());
    }

    // methods for view

    this.setFilter = (index) => {
        if (index < 0 || index >= this.filters.length) {
            console.warn('Filter does not exist. Index out of bounds.');
            return;
        }

        this.activeFilter = index;
        setFilterInUrl(this.filters[index].key);
    };

    // methods for parent directive

    this.repo = {
        published: true,
        search: SUPERDESK,
    };

    this.getSearch = () => {
        let deadline = getFilterFromUrl();

        if (!deadline || !filterExists(deadline)) {
            setDefaultFilter();
            deadline = getFilterFromUrl();
        }

        this.labelTo = `${compliantFilter.labelTo} ${this.filters[this.activeFilter].label}`;

        return {
            repo: 'published',
            'extra.compliantlifetime': deadline,
        };
    };

    this.customRender = {
        fields: {
            compliantlifetime: CompliantLifetimeComponent,
            versioncreated: VersionCreatedComponent,
        },
        getItemClass: getStatus,
    };

    $scope.$watch('items', watchItems);
}

export default angular.module('fidelity.compliance-review', ['superdesk.apps.authoring.widgets'])
    .config(['gettext', 'superdeskProvider', 'workspaceMenuProvider', 'config', function(gettext, superdesk, workspaceMenuProvider, config) {
            if (get(config, 'features.complianceReview', false)) {
                superdesk.activity('/compliance-review', {
                    description: gettext('Review published content'),
                    label: gettext('Compliance review'),
                    templateUrl: 'compliance-review.html',
                    sideTemplateUrl: 'scripts/apps/workspace/views/workspace-sidenav.html',
                    controller: ComplianceReviewCtrl,
                    controllerAs: 'search',
                });

                workspaceMenuProvider.item({
                    icon: 'archive',
                    href: '/compliance-review',
                    label: gettext('Compliance review'),
                });
            }
        },
    ])

    .controller('ComplianceReviewCtrl', ComplianceReviewCtrl)

    .run(['$templateCache', ($templateCache) => {
        $templateCache.put('compliance-review.html',require('../views/compliance-review.html'));
    }]);
