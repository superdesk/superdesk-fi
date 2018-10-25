import complianceReview from './compliance-review/controllers/ComplianceReviewController';
import './compliance-review/styles/compliance-review.scss';

export default angular.module('fidelity.superdesk', [complianceReview.name]);
