import CompliantLifetimeComponent from './components/CompliantLifetime'
import VersionCreatedComponent from './components/VersionCreated'
import {get} from 'lodash'

ComplianceReviewCtrl.$inject = ['$location', 'config', 'moment'];
export function ComplianceReviewCtrl($location, config, moment) {
    var VIEW_DATE_FORMAT = config.view.dateformat;

    const SUPERDESK = 'local';
    const deadlinePeriod = 'months';
    const deadlineOptions = [1, 3];
    const sortString = 'extra.compliantlifetime:asc';

    let deadline = $location.search()['deadline'];

    if(!deadlineOptions.includes(deadline)) {
        $location.search('deadline', deadlineOptions[0]);
        $location.search('sort', sortString);
        deadline = $location.search()['deadline'];
    }

    // methods for view

    this.isActive = (deadline) => parseInt($location.search()['deadline']) === deadline

    this.setDeadline = (deadline) => {
        $location.search('deadline', deadline);
        $location.search('sort', sortString);
    };

    // methods for parent directive

    this.repo = {
        published: true,
        search: SUPERDESK,
    };

    this.getSearch = () => {
        let deadline = parseInt($location.search()['deadline']);

        if (isNaN(deadline)) {
            this.setDeadline(deadlineOptions[0]);
            deadline = parseInt($location.search()['deadline']);
        }

        this.dateTo = moment().add(deadline, deadlinePeriod).format(VIEW_DATE_FORMAT);

        return {
            repo: 'published',
            'extra.compliantlifetimeto': this.dateTo,
        }
    };

    this.customRender = {
        fields: {
            'compliantlifetime': CompliantLifetimeComponent,
            'versioncreated': VersionCreatedComponent,
        },
        getItemClass: (item) => {
            if (!get(item, 'archive_item.extra.comliantlifetime')) {
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
    .config(['superdeskProvider', 'workspaceMenuProvider', function(superdesk, workspaceMenuProvider) {
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
    }])

    .controller('ComplianceReviewCtrl', ComplianceReviewCtrl)

    .run(['$templateCache', ($templateCache) => {
        $templateCache.put('compliance-review.html', require('./views/compliance-review.html'));
    }])
;
