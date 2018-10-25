import React from 'react'
import moment from 'moment'
import ng from 'core/services/ng'
import {get} from 'lodash'

export default ({ item }) => {
    if (!get(item, 'archive_item.extra.compliantlifetime')) {
        return (<div></div>);
    }

    const compliantDate = moment(item.archive_item.extra.compliantlifetime);
    const now = moment()
    const {dateformat} = ng.get('config').view;
    const compliantDateFormatted = compliantDate.format(dateformat)

    let daysLeft = compliantDate.diff(now, 'days');
    const overdue = daysLeft < 0;
    daysLeft = overdue ? -daysLeft : daysLeft;
    const leftWords = overdue ? gettext('days overdue') : gettext('days left');
    const leftString = `${daysLeft} ${leftWords}`;

    return (
        <span className="state-label compliance-date">
            <span>{compliantDateFormatted}</span>
            <span> ({leftString})</span>
        </span>
    );
}
