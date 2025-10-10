from datetime import datetime, timedelta
from typing import Final
from zoneinfo import ZoneInfo

import ephem
from ephem import UTC

_SWE: Final[ZoneInfo] = ZoneInfo("Europe/Stockholm")
_TZ = _SWE


def get_closest_full_moon() -> datetime:
    """
    Get the closest full moon to the current date and time.
    Return the closest full moon as a datetime object, in your local timezone.

    - If the closest full moon is tomorrow, display that information.
    - If the closest full moon was yesterday, display that information.
    """
    now = datetime.now(tz=_TZ)
    when_previous = ephem.previous_full_moon(date=now).datetime().replace(tzinfo=UTC)
    when_next = ephem.next_full_moon(date=now).datetime().replace(tzinfo=UTC)
    # Calculate time deltas
    delta_previous = now - when_previous
    delta_next = now - when_next

    # Return the closest date
    if abs(delta_previous) < abs(delta_next):
        return when_previous.astimezone(_TZ)
    else:
        return when_next.astimezone(_TZ)


def get_closest_new_moon() -> datetime:
    """
    Get the closest new moon to the current date and time.
    Return the closest new moon as a datetime object, in your local timezone.

    - If the closest new moon is tomorrow, display that information.
    - If the closest new moon was yesterday, display that information.
    """
    now = datetime.now(tz=_TZ)
    when_previous = ephem.previous_new_moon(date=now).datetime().replace(tzinfo=UTC)
    when_next = ephem.next_new_moon(date=now).datetime().replace(tzinfo=UTC)
    # Calculate time deltas
    delta_previous = now - when_previous
    delta_next = now - when_next

    # Return the closest date
    if abs(delta_previous) < abs(delta_next):
        return when_previous.astimezone(_TZ)
    else:
        return when_next.astimezone(_TZ)


def is_within(check: datetime, within: timedelta) -> bool:
    now = datetime.now(tz=_TZ)
    between = abs(now - check)
    # return if within positive timedelta
    return between <= within
