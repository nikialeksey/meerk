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
# todo #14:30m Disable pylint skippinf for this file
# pylint: skip-file
import collections
from datetime import date
from datetime import datetime
from datetime import tzinfo
from typing import List

import dateutil.rrule
import dateutil.tz
from icalendar.cal import Component

from .CalEventsIntervals import CalEventsIntervals
from .TimeIntervals import TimeIntervals
from .InMemoryTimeIntervals import InMemporyTimeIntervals


class SimpleCalEventsIntervals(CalEventsIntervals):

    def __init__(
            self,
            tzlocal: tzinfo,
            intervals: TimeIntervals = InMemporyTimeIntervals()
    ) -> None:
        self.tzlocal = tzlocal
        self.intervals = intervals

    def clear(self):
        self.intervals.clear()

    def add(self, components: List[Component], start: datetime, end: datetime):
        for component in components:
            if component.name == 'VEVENT':
                raw_dtstart = component['dtstart']
                dtstart = self.__without_tzinfo(raw_dtstart.dt)
                dtend = self.__without_tzinfo(component.get('dtend', raw_dtstart).dt)
                if self.__is_intersect(start, end, dtstart, dtend):
                    if 'rrule' in component:
                        rrule = dateutil.rrule.rrulestr(
                            component['RRULE'].to_ical().decode('utf-8'),
                            dtstart=dtstart
                        )
                        rrule._until = end
                        duration = dtend - dtstart
                        excludes = set()
                        if 'exdate' in component:
                            if isinstance(component['exdate'], collections.Iterable):
                                for exdates in component['exdate']:
                                    for exdate in exdates.dts:
                                        excludes.add(self.__without_tzinfo(exdate.dt).date())
                            else:
                                for exdate in component['exdate'].dts:
                                    excludes.add(self.__without_tzinfo(exdate.dt).date())
                        for time in filter(lambda time: time.date() not in excludes, list(rrule)):
                            self.intervals.add(time, time + duration, component)
                    else:
                        self.intervals.add(dtstart, dtend, component)

    def is_inside(self, time: datetime) -> bool:
        return self.intervals.is_inside(time)

    def __is_intersect(self, a: datetime, b: datetime, c: datetime, d: datetime) -> bool:
        return max(a, c) <= min(b, d)

    def __without_tzinfo(self, dt):
        if type(dt) == date:
            dt = datetime.combine(dt, datetime.min.time())
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=dateutil.tz.gettz('UTC'))
        return dt.astimezone(self.tzlocal).replace(tzinfo=None)
