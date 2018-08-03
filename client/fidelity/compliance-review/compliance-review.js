ComplianceReviewCtrl.$inject = ['$location', 'config', 'moment'];
export function ComplianceReviewCtrl($location, config, moment) {
    var VIEW_DATE_FORMAT = config.view.dateformat;

    const SUPERDESK = 'local';

    let deadline = $location.search()['deadline'];

    if(deadline !== 'month' && deadline !== 'week') {
        $location.search('deadline', 'month');
        deadline = $location.search()['deadline'];
    }

    // methods for view

    this.isActive = (deadline) => $location.search()['deadline'] === deadline;

    this.setDeadline = (deadline) => {
        $location.search('deadline', deadline);
    };

    // methods for parent directive

    this.repo = {
        published: true,
        search: SUPERDESK,
    };

    this.getSearch = () => {
        let deadline = $location.search()['deadline'];

        if(deadline !== 'month' && deadline !== 'week') {
            // in case page is changed, but it didn't finish removing old references yet
            return {};
        }

        const now = new Date();

        let dateFrom;
        if(deadline === 'week') {
            dateFrom = new Date(now.getFullYear() - 1, now.getMonth(), now.getDate() - 14);
        } else if(deadline === 'month') {
            dateFrom = new Date(now.getFullYear() - 1, now.getMonth(), now.getDate());
        }

        const dateTo = new Date(now.getFullYear() - 1, now.getMonth() + 1, now.getDate());

        // for displaying in the view
        this.dateFrom = moment(dateFrom).format(VIEW_DATE_FORMAT);
        this.dateTo = moment(dateTo).format(VIEW_DATE_FORMAT);

        return {
            firstpublishedfrom: moment(dateFrom).format(VIEW_DATE_FORMAT),
            firstpublishedto: moment(dateTo).format(VIEW_DATE_FORMAT),
        }
    };
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