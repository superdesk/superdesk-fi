import moment from 'moment';
import {get} from 'lodash';

export const SOON_DAYS = 31;

export const getStatus = (item) => {
    if (!get(item, 'archive_item.extra.compliantlifetime')) {
        return '';
    }

    const compliantDate = moment(item.archive_item.extra.compliantlifetime);
    const now = moment();
    const daysLeft = compliantDate.diff(now, 'days');

    if (daysLeft < 0) {
        return 'overdue';
    } else if (daysLeft < SOON_DAYS) {
        return 'soon';
    }

    return '';
}
