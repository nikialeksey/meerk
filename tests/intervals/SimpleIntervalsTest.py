from datetime import datetime
from unittest import TestCase

from icalendar.cal import Component

from meerk.intervals import SimpleIntervals


class SimpleIntervalsTest(TestCase):
    def test_exdates(self):
        intervals = SimpleIntervals()
        components = Component.from_ical(
            """
BEGIN:VEVENT
SUMMARY:asd
DTSTART;TZID=Asia/Barnaul:20180916T230000
DTEND;TZID=Asia/Barnaul:20180916T235900
DTSTAMP:20180917T165114Z
UID:P6nNfouJyandex.ru
SEQUENCE:2
RRULE:FREQ=DAILY;INTERVAL=1
EXDATE;TZID=Asia/Barnaul:20180917T230000
EXDATE;TZID=Asia/Barnaul:20180916T230000
CATEGORIES:Events
CREATED:20180917T162723Z
LAST-MODIFIED:20180917T162741Z
TRANSP:OPAQUE
URL:https://calendar.yandex.ru/for/siberian.pro/event?event_id=673628779
END:VEVENT
            """
        ).walk()
        intervals.add(components, datetime(2018, 9, 15, 0, 0), datetime(2018, 9, 17, 0, 0))
        self.assertFalse(intervals.is_inside(datetime(2018, 9, 16, 23, 0)))
