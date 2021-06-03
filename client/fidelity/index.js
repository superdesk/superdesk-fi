import complianceReview from './compliance-review/controllers/ComplianceReviewController';
import subjectMatterExpertReview from './subject-matter-expert-review/controllers/subjectMatterExpertReviewController';
import {startApp} from 'superdesk-core/scripts/index';
import annotationsLibraryExtension from 'superdesk-core/scripts/extensions/annotationsLibrary/dist/src/extension';
import samsExtension from 'superdesk-core/scripts/extensions/sams/dist/src/extension';
import {SamsAttachmentsWidget} from 'superdesk-core/scripts/extensions/sams/dist/src/apps/samsAttachmentsWidget';

import './compliance-review/styles/compliance-review.scss';
import './subject-matter-expert-review/styles/subject-matter-expert-review.scss';

setTimeout(() => {
    startApp(
        [annotationsLibraryExtension, samsExtension],
        {AuthoringAttachmentsWidget: SamsAttachmentsWidget},
    );
});

export default angular
    .module('fidelity.superdesk', [complianceReview.name, subjectMatterExpertReview.name])
    .run(['$templateCache', ($templateCache) => {
        $templateCache.put(
            'scripts/core/auth/login-modal.html',
            require('./login/login-modal.html')
        )
    }]);
