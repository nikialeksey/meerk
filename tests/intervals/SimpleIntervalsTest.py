from datetime import datetime
from unittest import TestCase

import dateutil
from icalendar.cal import Component

from meerk.intervals import SimpleIntervals


class SimpleIntervalsTest(TestCase):
    def test_exdates(self):
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
        intervals = SimpleIntervals(dateutil.tz.gettz('UTC'))
        intervals.add(components, datetime(2018, 9, 15, 0, 0), datetime(2018, 9, 17, 0, 0))
        self.assertFalse(intervals.is_inside(datetime(2018, 9, 16, 23, 0)))

    def test_dtstart_equals_dtend(self):
        components = Component.from_ical(
            """
BEGIN:VEVENT
SUMMARY:empty
DTSTART;TZID=Asia/Barnaul:20180927T223000
DTEND;TZID=Asia/Barnaul:20180927T223000
DTSTAMP:20180927T163634Z
UID:ZpNblVw8yandex.ru
SEQUENCE:0
CATEGORIES:Events
CREATED:20180927T163531Z
LAST-MODIFIED:20180927T163531Z
TRANSP:OPAQUE
URL:https://calendar.yandex.ru/for/siberian.pro/event?event_id=685344091
END:VEVENT
            """
        ).walk()
        intervals = SimpleIntervals(dateutil.tz.gettz('UTC'))
        intervals.add(components, datetime(2018, 9, 26, 0, 0), datetime(2018, 9, 28, 0, 0))
        self.assertTrue(intervals.is_inside(datetime(2018, 9, 27, 15, 30)))

    def test_dtend_is_hidden(self):
        components = Component.from_ical(
            """
BEGIN:VEVENT
SUMMARY:Simple
DTSTART:20180926T170000Z
DTSTAMP:20180927T164741Z
UID:someuid
SEQUENCE:0
CREATED:20180927T164659Z
DESCRIPTION:
LAST-MODIFIED:20180927T164716Z
LOCATION:
STATUS:CONFIRMED
TRANSP:OPAQUE
END:VEVENT
            """
        ).walk()
        intervals = SimpleIntervals(dateutil.tz.gettz('UTC'))
        intervals.add(components, datetime(2018, 9, 26, 0, 0), datetime(2018, 9, 28, 0, 0))
        self.assertTrue(intervals.is_inside(datetime(2018, 9, 26, 17, 00)))

    def test_all_day_event(self):
        components = Component.from_ical(
            """
BEGIN:VEVENT
SUMMARY:all day
DTSTART;VALUE=DATE:20181007
DTEND;VALUE=DATE:20181008
DTSTAMP:20181007T043134Z
UID:iq6zz5Cdyandex.ru
SEQUENCE:0
CATEGORIES:events
CREATED:20181007T043121Z
LAST-MODIFIED:20181007T043121Z
TRANSP:OPAQUE
URL:https://calendar.yandex.ru/for/siberian.pro/event?event_id=696510765
END:VEVENT
            """
        ).walk()
        intervals = SimpleIntervals(dateutil.tz.gettz('UTC'))
        intervals.add(components, datetime(2018, 10, 6, 0, 0), datetime(2018, 10, 8, 0, 0))
        self.assertTrue(intervals.is_inside(datetime(2018, 10, 7, 17, 00)))

    def test_all_day_daily_event(self):
        components = Component.from_ical(
            """
BEGIN:VEVENT
SUMMARY:all day
DTSTART;VALUE=DATE:20181007
DTEND;VALUE=DATE:20181008
DTSTAMP:20181007T044204Z
UID:6uk40snnrfsarji6gitijk4k67@google.com
SEQUENCE:0
RRULE:FREQ=DAILY
CREATED:20181007T044142Z
DESCRIPTION:
LAST-MODIFIED:20181007T044142Z
LOCATION:
STATUS:CONFIRMED
TRANSP:TRANSPARENT
END:VEVENT
            """
        ).walk()
        intervals = SimpleIntervals(dateutil.tz.gettz('UTC'))
        intervals.add(components, datetime(2018, 10, 6, 0, 0), datetime(2018, 10, 10, 0, 0))
        self.assertTrue(intervals.is_inside(datetime(2018, 10, 9, 17, 00)))

    def test_all_day_daily_with_modification_event(self):
        components = Component.from_ical(
            """
BEGIN:VEVENT
SUMMARY:all day
DTSTART;VALUE=DATE:20181006
DTEND;VALUE=DATE:20181007
DTSTAMP:20181007T044526Z
UID:0q9s66jci35g6fmjq9bi3m8pbk@google.com
SEQUENCE:0
RRULE:FREQ=DAILY
EXDATE;VALUE=DATE:20181006
CREATED:20181007T044447Z
DESCRIPTION:
LAST-MODIFIED:20181007T044447Z
LOCATION:
STATUS:CONFIRMED
TRANSP:TRANSPARENT
END:VEVENT
            """
        ).walk()
        intervals = SimpleIntervals(dateutil.tz.gettz('UTC'))
        intervals.add(components, datetime(2018, 10, 6, 0, 0), datetime(2018, 10, 10, 0, 0))
        self.assertFalse(intervals.is_inside(datetime(2018, 10, 6, 17, 00)))
