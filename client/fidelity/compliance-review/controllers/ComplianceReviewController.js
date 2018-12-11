import { get } from 'lodash';
import CompliantLifetimeComponent from '../components/CompliantLifetime';
import VersionCreatedComponent from '../components/VersionCreated';
import { getStatus } from '../compliance-status';


ComplianceReviewCtrl.$inject = ['$location', 'gettext', '$scope'];
export function ComplianceReviewCtrl($location, gettext, $scope) {
    const SUPERDESK = 'local';

    const sortString = 'extra.compliantlifetime:asc';

    $location.search('sort', sortString);

    this.complianceFilters = {
        before_next_month: {
            days: 30,
            label: gettext('Next Month')
        },
        before_3_months_ahead: {
            days: 90,
            label: gettext('Next 3 Months')
        }
    };

    // helper fns

    const filterExists = (key) => this.complianceFilters.hasOwnProperty(key)
    const setFilterInUrl = (filter) => $location.search('deadline', filter);
    const getFilterFromUrl = () => $location.search().deadline;
    const defaultFilter = () => Object.keys(this.complianceFilters)[0];

    // methods for view

    this.setFilter = (filter) => {
        if (filterExists(filter)) {
            if ($scope.items && $scope.items._meta && $scope.items._meta.total) {
                delete $scope.items._meta.total
            }
            this.activeFilter = filter;
            setFilterInUrl(filter);
        }
    };

    // methods for parent directive

    this.repo = {
        published: true,
        search: SUPERDESK,
    };

    if (filterExists(getFilterFromUrl())) {
        this.activeFilter = getFilterFromUrl();
    } else {
        this.setFilter(defaultFilter())
    }

    this.getSearch = () => {
        let deadline = getFilterFromUrl();

        if (!deadline || !filterExists(deadline)) {
            this.setFilter(defaultFilter());
            deadline = getFilterFromUrl();
        }

        this.labelTo = `${gettext('Need review before')} ${this.complianceFilters[this.activeFilter].label}`;

        return {
            repo: 'published',
            'extra.compliantlifetime': deadline,
            ignoreKilled: true,
            onlyLastPublished: true,
            type: '["text"]',
        };
    };

    this.customRender = {
        fields: {
            compliantlifetime: CompliantLifetimeComponent,
            versioncreated: VersionCreatedComponent,
        },
        getItemClass: getStatus,
    };

    $scope.$watch('view', () => $scope.view = 'compact') // force compact view
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
