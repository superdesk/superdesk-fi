import React from 'react'
import moment from 'moment'
import ng from 'core/services/ng'

export default ({ item }) => {
    const {archive_item} = item;
    const compliantDate = moment(archive_item.extra.compliantlifetime);
    const now = moment()
    const {dateformat} = ng.get('config').view;
    const compliantDateFormatted = compliantDate.format(dateformat)

    let daysLeft = compliantDate.diff(now, 'days');
    const overdue = daysLeft < 0;
    daysLeft = overdue ? -daysLeft : daysLeft;
    const leftWords = overdue ? gettext('days overdue') : gettext('days left');
    const leftString = `${daysLeft} ${leftWords}`;

    return (
        <div>
            <time>{compliantDateFormatted}</time>
            <time> ({leftString})</time>
        </div>
    );
}
