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
from datetime import date
from datetime import datetime

from icalendar.cal import Component
from intervaltree import IntervalTree, Interval

from Intervals import Intervals
import dateutil


class SimpleIntervals(Intervals):

    def __init__(self):
        self.tree = IntervalTree()

    def clear(self):
        # type: () -> None
        self.tree.clear()

    def add(self, components, start, end):
        # type: (list[Component], datetime, datetime) -> None
        for component in components:
            if component.name == 'VEVENT':
                dtstart = self.__without_tzinfo(component['dtstart'].dt)
                dtend = self.__without_tzinfo(component['dtend'].dt)
                if self.__is_intersect(start, end, dtstart, dtend):
                    if 'rrule' in component:
                        rrule = dateutil.rrule.rrulestr(
                            component['RRULE'].to_ical().decode('utf-8'),
                            dtstart=dtstart
                        )
                        rrule._until = end
                        duration = dtend - dtstart
                        for time in list(rrule):
                            self.tree.add(Interval(time, time + duration, component))
                    else:
                        self.tree.add(Interval(dtstart, dtend, component))

    def is_inside(self, time):
        # type: (datetime) -> bool
        return len(self.tree[time]) > 0

    def __is_intersect(self, a, b, c, d):
        # type: (datetime, datetime, datetime, datetime) -> bool
        return max(a, c) <= min(b, d)

    def __without_tzinfo(self, time):
        if type(time) == date:
            time = datetime.combine(time, datetime.min.time())
        if time.tzinfo is None:
            time.replace(tzinfo=dateutil.tz.gettz('UTC'))
        return time.astimezone(dateutil.tz.tzlocal()).replace(tzinfo=None)
