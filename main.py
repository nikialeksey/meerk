# MIT License
#
# Copyright (c) 2018 Alexey Nikitin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import ConfigParser
import time
from datetime import datetime

import schedule
from slackclient import SlackClient

from meeker.caldav import DAVClient
from meeker.calendar import Calendar
from meeker.calendar import CalDavCalendar
from meeker.calendar import LoggableCalendar
from meeker.calendar import CompositeCalendar
from meeker.calendar import IcsCalendar
from meeker.status import SlackStatus
from meeker.status import Status
from meeker.status import CompositeStatus
from meeker.intervals import SimpleIntervals


def update_status(calendar, busy, available):
    # type: (Calendar, Status, Status) -> None
    if calendar.is_busy(datetime.now()):
        busy.sync()
    else:
        available.sync()


if __name__ == '__main__':
    intervals = SimpleIntervals()

    calendars = []
    busy_statuses = []
    available_statuses = []

    config = ConfigParser.ConfigParser()
    config.read('local.cfg')
    for section in config.sections():
        if section.startswith('caldav'):
            calendars.append(
                CalDavCalendar(
                    DAVClient(
                        config.get(section, 'url'),
                        username=config.get(section, 'username'),
                        password=config.get(section, 'password')
                    ),
                    intervals
                )
            )
        elif section.startswith('ics'):
            calendars.append(
                IcsCalendar(
                    config.get(section, 'url'),
                    intervals
                )
            )
        elif section.startswith('slack'):
            sc = SlackClient(config.get(section, 'token'))
            busy_statuses.append(
                SlackStatus(
                    sc,
                    config.get(section, 'busy_text'),
                    config.get(section, 'busy_emoji')
                )
            )
            available_statuses.append(
                SlackStatus(
                    sc,
                    config.get(section, 'available_text'),
                    config.get(section, 'available_emoji')
                )
            )

    calendar = LoggableCalendar(CompositeCalendar(calendars))
    calendar.sync()

    busy = CompositeStatus(busy_statuses)
    available = CompositeStatus(available_statuses)

    schedule.every(1).hours.do(calendar.sync)
    schedule.every(1).seconds.do(
        update_status,
        calendar,
        busy,
        available
    )

    while True:
        schedule.run_pending()
        time.sleep(1)
