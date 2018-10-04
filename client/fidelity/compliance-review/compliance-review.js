import {get} from 'lodash'
import {getDateFilters} from 'apps/search/directives/DateFilters'
import CompliantLifetimeComponent from './components/CompliantLifetime'
import VersionCreatedComponent from './components/VersionCreated'

ComplianceReviewCtrl.$inject = ['$location', 'config', 'moment'];
export function ComplianceReviewCtrl($location, config, moment) {
    const VIEW_DATE_FORMAT = config.view.dateformat;
    const SUPERDESK = 'local';

    const compliantFilter = getDateFilters(gettext)
        .find(f => f.fieldname === 'extra.compliantlifetime');
    this.filters = compliantFilter.predefinedFilters;
    this.activeFilter = 0;
    const sortString = 'extra.compliantlifetime:asc';

    $location.search('sort', sortString);

    // methods for view

    this.setFilter = (index) => {
        if (index < 0 || index >= this.filters.length) {
            console.warn('Filter does not exist. Index out of bounds.');
            return;
        }

        this.activeFilter = index;
        $location.search('deadline', this.filters[index].key);
    }

    // methods for parent directive

    this.repo = {
        published: true,
        search: SUPERDESK,
    };

    this.getSearch = () => {
        let deadline = $location.search()['deadline'];
        const filterExists = this.filters.some((f) => f.key === deadline);

        if (!filterExists) {
            deadline = this.filters[0].key; // first as default
            $location.search('deadline', deadline);
        }


        this.labelTo = `${compliantFilter.labelTo} ${this.filters[this.activeFilter].label}`;

        return {
            repo: 'published',
            'extra.compliantlifetime': deadline,
        }
    };

    this.customRender = {
        fields: {
            'compliantlifetime': CompliantLifetimeComponent,
            'versioncreated': VersionCreatedComponent,
        },
        getItemClass: (item) => {
            if (!get(item, 'archive_item.extra.compliantlifetime')) {
                return '';
            }

            const compliantDate = moment(item.archive_item.extra.compliantlifetime);
            const now = moment()
            const daysLeft = compliantDate.diff(now, 'days');
            const overdue = daysLeft < 0;

            return overdue ? 'overdue': '';
        }
    }
}

export default angular.module('fidelity.compliance-review', ['superdesk.apps.authoring.widgets'])
    .config(['superdeskProvider', 'workspaceMenuProvider', 'config', function(superdesk, workspaceMenuProvider, config) {
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
    }])

    .controller('ComplianceReviewCtrl', ComplianceReviewCtrl)

    .run(['$templateCache', ($templateCache) => {
        $templateCache.put('compliance-review.html', require('./views/compliance-review.html'));
    }])
;
