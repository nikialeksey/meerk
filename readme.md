# Meerk

**Meerk** - **MEE**ting ma**RK**  

Simple bot which notifies your chats that you are in a meeting

## How to run

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
