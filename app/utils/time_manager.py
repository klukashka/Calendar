from datetime import datetime
import pytz


def utc_cur_time() -> datetime:
    """Return current time in UTC"""
    utc_time = datetime.now(pytz.utc)
    naive_utc_time = utc_time.replace(microsecond=0, tzinfo=None)
    return naive_utc_time


def localize(dt: datetime, tz: str) -> datetime:
    """Convert aware datetime to necessary time zone"""
    local_tz = pytz.timezone(tz)
    try:
        in_utc_time = pytz.utc.localize(dt)
        local_time = in_utc_time.astimezone(local_tz)
        return local_time
    except ValueError as e:
        raise ValueError(f"Failed to convert {dt}. Expected aware datetime") from e
    except Exception as e:
        raise Exception(f"Failed to convert {dt}.") from e


def convert_to_utc(dt: str, tz: str) -> datetime:
    """Convert naive-datetime to aware-datetime in a specific timezone"""
    formatted_datetime = datetime.strptime(dt, DATE_TIME_FORMAT)  # Adjust format as necessary
    # Get the local timezone using pytz
    local_timezone = pytz.timezone(tz)
    # Localize the naive datetime to the local timezone
    local_datetime = local_timezone.localize(formatted_datetime)
    # Convert to UTC
    utc_datetime = local_datetime.astimezone(pytz.utc)
    utc_naive = utc_datetime.replace(tzinfo=None)
    return utc_naive
