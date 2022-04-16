import datetime
from dateutil.relativedelta import relativedelta
from django import template
import pytz
from django.utils import timezone


utc = pytz.timezone('Europe/Moscow')

register = template.Library()


def normalized(self):
    """
    Return a version of this object represented entirely using integer
    values for the relative attributes.

    """
    # Cascade remainders down (rounding each to roughly nearest microsecond)
    days = int(self.days)

    hours_f = round(self.hours + 24 * (self.days - days), 11)
    hours = int(hours_f)

    minutes_f = round(self.minutes + 60 * (hours_f - hours), 10)
    minutes = int(minutes_f)

    seconds_f = round(self.seconds + 60 * (minutes_f - minutes), 8)
    seconds = int(seconds_f)

    microseconds = round(self.microseconds + 1e6 * (seconds_f - seconds))

    # Constructor carries overflow back up with call to _fix()
    return self.__class__(years=self.years, months=self.months,
                          days=days, hours=hours, minutes=minutes,
                          seconds=seconds, microseconds=microseconds,
                          leapdays=self.leapdays, year=self.year,
                          month=self.month, day=self.day,
                          weekday=self.weekday, hour=self.hour,
                          minute=self.minute, second=self.second,
                          microsecond=self.microsecond)


@register.filter(name='time_difference')
def time_difference(value):
    """
    Returns time difference between two dates in seconds/minutes/hours and etc
    based on time gap.
    """
    global utc
    d2 = utc.localize(datetime.datetime.now())
    d1 = value

    diff = relativedelta(d2, d1)
    tda = [diff.years, diff.months, diff.days, diff.hours, diff.minutes, diff.seconds]
    appendixes = [
        ['seconds', 'second'],
        ['minutes', 'minute'],
        ['hours', 'hour'],
        ['days', 'day'],
        ['months', 'month'],
        ['years', 'year'],
                  ]

    filtered_tda = list(filter(lambda x: x != 0, (map(int, tda))))
    if filtered_tda:
        value = filtered_tda[0]
        appendix = appendixes[len(filtered_tda) - 1][int(filtered_tda[0] <= 1)]
        return '{value} {appendix} ago'.format(value=value, appendix=appendix)
    else:
        return 'now'


@register.filter(name='add_id')
def add_id(value, arg):
    """
    Adds html id to an object
    """
    return value.as_widget(attrs={'id': arg})


@register.filter(name='add_text')
def add_text(value, arg):
    """
    Adds text after object
    """
    arg += '' if value == 1 else 's'
    return '{value} {arg}'.format(value=value, arg=arg)
