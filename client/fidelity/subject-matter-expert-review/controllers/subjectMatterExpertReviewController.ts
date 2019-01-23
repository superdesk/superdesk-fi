import {hideSideMenu, unhideSideMenu, hideTopMenu, unhideTopMenu} from 'core/helpers/for-extensions';

const subjectMatterExpertReviewDeskId = "5c0f7018149f1171135c77ec";
const cssClassNameForView = 'fi_subject-matter-expert-review-page';

function closeAuthoring() {
    return angular.element(document.querySelector('[sd-authoring]')).scope().close();
}

function isWidgetVisible(widget) {
    const allowedWidgetIds = ['find-replace', 'comments', 'inline-comments'];

    return Promise.resolve(allowedWidgetIds.includes(widget._id));
}

subjectMatterExpertReviewCtrl.$inject = [
    '$scope',
    'search',
    'api',
    'gettext',
    'authoringWorkspace',
    'superdeskFlags',
    'archiveService',
    'desks',
    'notify',
    'modal',
    '$location',
];

let previousWorkspaceFlagValue;

export function subjectMatterExpertReviewCtrl(
    $scope,
    search,
    api,
    gettext,
    authoringWorkspace,
    superdeskFlags,
    archiveService,
    desks,
    notify,
    modal,
    $location,
) {

    function addCustomAuthoringButtons() {
        authoringWorkspace.authoringTopBarAdditionalButtons['subject-matter-expert-view--finish-review'] = {
            label: gettext('Finish review'),
            class: 'btn btn--sd-green',
            onClick: (item) => {
                const currentDeskId = item.task.desk;

                modal.confirm(gettext('You will no longer be able to edit the item once the review is finished. Continue?'))
                    .then(() => archiveService.getVersions(item, desks, 'versions'))
                    .then((versions) => {
                        // getting the version of the item just before it was moved to subject matter review desk
                        const {desk: originDesk, stage: originStage} = versions.find((item) => item.task.desk !== currentDeskId).task;

                        closeAuthoring()
                            .then(
                                () => api.save('move', {}, {task: {desk: originDesk, stage: originStage}, allPackageItems: true}, item)
                            )
                            .then(() => {
                                notify.success(gettext('The review is finished.'));
                            });
                    });
            },
        };

        authoringWorkspace.authoringTopBarButtonsToHide['article-edit--topbar--minimize'] = true;
        authoringWorkspace.authoringTopBarButtonsToHide['article-edit--topbar--actions'] = true;
        authoringWorkspace.authoringTopBarButtonsToHide['article-edit--topbar--sendto-publish'] = true;
    }

    function removeCustomAuthoringButtons() {
        delete authoringWorkspace.authoringTopBarAdditionalButtons['subject-matter-expert-view--finish-review'];

        delete authoringWorkspace.authoringTopBarButtonsToHide['article-edit--topbar--minimize'];
        delete authoringWorkspace.authoringTopBarButtonsToHide['article-edit--topbar--actions'];
        delete authoringWorkspace.authoringTopBarButtonsToHide['article-edit--topbar--sendto-publish'];
    }

    function onInitialize() {
        const queryParams = $location.search();

        if (queryParams['item'] != null && queryParams['action'] === 'edit') {
            superdeskFlags.flags.hideMonitoring = true;
        }

        document.body.classList.add(cssClassNameForView);

        hideSideMenu();
        hideTopMenu();
        addCustomAuthoringButtons();
        authoringWorkspace.addWidgetVisibilityCheckerFunction(isWidgetVisible);


        previousWorkspaceFlagValue = superdeskFlags.flags.workqueue;

        $scope.$applyAsync(() => {
            superdeskFlags.flags.workqueue = false;
        });
    }

    function onDestroy() {
        unhideSideMenu();
        unhideTopMenu();
        removeCustomAuthoringButtons();
        authoringWorkspace.removeWidgetVisibilityCheckerFunction(isWidgetVisible);

        document.body.classList.remove(cssClassNameForView);


        $scope.$applyAsync(() => {
            superdeskFlags.flags.workqueue = previousWorkspaceFlagValue;
        });
    }
    
    onInitialize();
    
    $scope.$on('$destroy', onDestroy);

    $scope.customDataSource = {
        getItems: (from, pageSize) => {
            const criteria = search.query({desk: `["${subjectMatterExpertReviewDeskId}"]`}).getCriteria(true);
    
            criteria.source.from = from;
            criteria.source.size = pageSize;
    
            return api.query('search', criteria);
        },
        getItem: (item) => {
            const criteria = search.query({desk: `["${subjectMatterExpertReviewDeskId}"]`}).getCriteria(true);
            const criteriaSingle = search.getSingleItemCriteria(item, criteria);
    
            return api.query('search', criteriaSingle);
        }
    };

    $scope.onMonitoringItemSelect = function(item, event) {
        superdeskFlags.flags.hideMonitoring = true;
        authoringWorkspace.edit(item);
    }

    $scope.onMonitoringItemDoubleClick = function(item) {
        // double click disabled
    }
}

export default angular.module('fidelity.subject-matter-expert-review', ['superdesk.apps.authoring.widgets'])
    .config(['gettext', 'superdeskProvider', function(gettext, superdesk) {
            superdesk.activity('/subject-matter-expert-review', {
                description: '',
                label: gettext('Subject matter expert review'),
                template: require('../views/subject-matter-expert-review.html'),
                sideTemplateUrl: 'scripts/apps/workspace/views/workspace-sidenav.html',
                controller: subjectMatterExpertReviewCtrl,
                privileges: {fi_subject_matter_expert_review: 1},
            });
        },
    ]);
