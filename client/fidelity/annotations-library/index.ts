import {reactToAngular1} from 'superdesk-ui-framework';
import {AnnotationsLibraryPage} from './AnnotationsLibraryPage';

const styles = 'display: flex; height: 100%; padding-top: 48px';

export default angular.module('fidelity.annotations-library', [])
    .component('sdAnnotationsLibraryPage', reactToAngular1(AnnotationsLibraryPage, [], [], styles))
    .config(['gettext', 'superdeskProvider', function(gettext, superdesk) {
            superdesk.activity('/annotations-library', {
                label: gettext('Annotations library'),
                category: superdesk.MENU_MAIN,
                adminTools: false,
                template: '<sd-annotations-library-page></<sd-annotations-library-page>',
                sideTemplateUrl: 'scripts/apps/workspace/views/workspace-sidenav.html',
            });
        },
    ]);
