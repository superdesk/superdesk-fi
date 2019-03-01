import complianceReview from './compliance-review/controllers/ComplianceReviewController';
import subjectMatterExpertReview from './subject-matter-expert-review/controllers/subjectMatterExpertReviewController';
import ng from 'superdesk-core/scripts/core/services/ng';
import {AnnotationInputWithKnowledgeBase} from './annotations/AnnotationInputWithKnowledgeBase';

import './compliance-review/styles/compliance-review.scss';
import './subject-matter-expert-review/styles/subject-matter-expert-review.scss';

export default angular
    .module('fidelity.superdesk', [complianceReview.name, subjectMatterExpertReview.name])
    .run(['$templateCache', 'extensionPoints', ($templateCache, extensionPoints) => {
        $templateCache.put(
            'scripts/core/auth/login-modal.html',
            require('./login/login-modal.html')
        )

        ng.waitForServicesToBeAvailable()
            .then(() => {
                extensionPoints.register(
                    'authoring:editor3:annotations',
                    AnnotationInputWithKnowledgeBase,
                    {},
                    [],
                    () => {},
                );
            });
    }]);
