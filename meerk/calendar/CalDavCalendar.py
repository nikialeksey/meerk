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
from datetime import datetime
from datetime import timedelta

from icalendar import Event

from Calendar import Calendar
from meerk.caldav import DAVClient
from meerk.intervals import Intervals


class CalDavCalendar(Calendar):

    def __init__(self, dav, intervals):
        # type: (DAVClient, Intervals) -> CalDavCalendar
        self.dav = dav
        self.intervals = intervals

    def is_busy(self, time):
        # type: (datetime) -> bool
        return self.intervals.is_inside(time)

    def sync(self):
        # type: () -> None
        self.intervals.clear()
        start = datetime.now() - timedelta(days=1)
        end = datetime.now() + timedelta(days=1)
        calendars = self.dav.principal().calendars()
        for calendar in calendars:
            events = calendar.date_search(start, end)
            for event in events:
                self.intervals.add(Event.from_ical(event.data).walk(), start, end)
