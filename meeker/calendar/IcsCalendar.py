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
import urllib2
from datetime import datetime
from datetime import timedelta

from icalendar import Calendar as iCalendar

from Calendar import Calendar
from meeker.intervals import Intervals


class IcsCalendar(Calendar):

    def __init__(self, url, intervals):
        # type: (str, Intervals) -> IcsCalendar
        self.url = url
        self.intervals = intervals

    def is_busy(self, time):
        # type: (datetime) -> bool
        return self.intervals.is_inside(time)

    def sync(self):
        # type: () -> None
        response = urllib2.urlopen(self.url)
        ical = response.read()
        self.intervals.clear()
        self.intervals.add(
            iCalendar.from_ical(ical).walk(),
            datetime.now() - timedelta(days=1),
            datetime.now() + timedelta(days=1)
        )
