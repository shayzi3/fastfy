import pytz

from datetime import datetime


moscow_timezone = pytz.timezone(zone="Europe/Moscow")


def moscow_datetime() -> datetime:
     return datetime.now(tz=moscow_timezone)