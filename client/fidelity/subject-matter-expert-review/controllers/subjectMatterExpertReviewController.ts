import {reactToAngular1} from 'superdesk-core/node_modules/superdesk-ui-framework';
import {SubjectMatterExpertReview} from '../components/subjectMatterExpertReview';

subjectMatterExpertReviewCtrl.$inject = [];
export function subjectMatterExpertReviewCtrl() {
    
}

export default angular.module('fidelity.subject-matter-expert-review', ['superdesk.apps.authoring.widgets'])
    .component('sdSubjectMatterExpertReview', reactToAngular1(SubjectMatterExpertReview))
    .config(['gettext', 'superdeskProvider', 'workspaceMenuProvider', 'config', function(gettext, superdesk, workspaceMenuProvider, config) {
            superdesk.activity('/subject-matter-expert-review', {
                description: '',
                label: gettext('Subject matter expert review'),
                template: '<sd-subject-matter-expert-review></sd-subject-matter-expert-review>',
                sideTemplateUrl: 'scripts/apps/workspace/views/workspace-sidenav.html',
                controller: subjectMatterExpertReviewCtrl,
                controllerAs: 'search',
            });
        },
    ]);
