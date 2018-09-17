# Meerk

[![Mit License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/nikialeksey/meerk/blob/master/LICENSE)
![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg)
[![PyPI version](https://badge.fury.io/py/meerk.svg)](https://badge.fury.io/py/meerk)

Simple bot which notifies your chats that you are in a meeting

## How to run

Clone project:

```bash
git clone https://github.com/nikialeksey/meerk.git
```

Install dependencies and

```bash
pip install -r requirements.txt
```

[Configure](https://github.com/nikialeksey/meerk#how-to-configure) and run:

```bash
python main.py
```

Or you can use it as library for your service or app, see example in 
[`main.py`](https://github.com/nikialeksey/meerk/blob/master/main.py).

## How to configure

In order to configure you need to make a copy of file 
[`local.cfg_template`](https://github.com/nikialeksey/meerk/blob/master/local.cfg_template) with name `local.cfg`
and change content of it. 

### CalDav calendars

To add calendar supports [CalDav](https://en.wikipedia.org/wiki/CalDAV)
format you need to uncomment 
[`caldav-calendar`](https://github.com/nikialeksey/meerk/blob/master/local.cfg_template#L1-L4) section
and fill with your personal data. If you have a multiple calendars supports [CalDav](https://en.wikipedia.org/wiki/CalDAV)
you may create a new section in `local.cfg` with the same fields and section name prefix `caldav`, 
but with other data, for example:

```ini
[caldav-another]
url: <another caldav url>
username: <another caldav username>
password: <another caldav password>
```

### Ics calendars

To add calendar using [`ics`](https://en.wikipedia.org/wiki/ICalendar) file you need to uncomment
[`ics-calendar`](https://github.com/nikialeksey/meerk/blob/master/local.cfg_template#L6-L7) section and fill with
your public [`ics`](https://en.wikipedia.org/wiki/ICalendar) file link. Again, if you have a few 
[`ics`](https://en.wikipedia.org/wiki/ICalendar) calendars, you may create a few sections in `local.cfg` with section 
name prefix `ics`, for example:

```ini
[ics-another]
url: <another ics url>

[ics-yet-another]
url: <yet another ics url>
```

### Slack

It supports only slack, but you can contribute for more chats. To configure slack, you guessed it, you need to 
uncomment [`slack-app`](https://github.com/nikialeksey/meerk/blob/master/local.cfg_template#L9-L14) section and fill,
for example:

```ini
[slack-app]
token: xoxp-3165681461-*****6099680-*****3333042-*****007685996b538e88cbe92a6098b
busy_text: I am in a meeting
busy_emoji: :shushing_face:
available_text: Android development 09.00 - 17.00
available_emoji: :computer:
```

## How it works

**Meerk** periodically synchronizes specified in `local.cfg` calendars and periodically verifies if there is a 
meeting now, then update chat status to **Busy**, else **Available**. 

## Thanks

Thanks to [@tobixen](https://github.com/tobixen) and his project [caldav](https://github.com/python-caldav/caldav). I 
[use it in the **Meerk**](https://github.com/nikialeksey/meerk/tree/master/meerk/caldav) temporary. When 
[#11](https://github.com/python-caldav/caldav/issues/11) appears in release build I get rid of the immediate code of
project [caldav](https://github.com/python-caldav/caldav) and will be use as dependency or write my own 
[CalDav](https://en.wikipedia.org/wiki/CalDAV) implementation.