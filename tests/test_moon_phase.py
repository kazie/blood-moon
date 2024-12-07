from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from ephem import UTC

from blood_moon.moon_phase import get_closest_full_moon, is_within


def test_get_next_full_moon_live():
    now = datetime.now(UTC)
    next_phase = get_closest_full_moon()
    assert next_phase > now


def test_get_next_full_moon_known_date(freezer):
    # 15 May 2022 (US) was a super blood blood_moon
    freezer.move_to("2022-05-15")
    next_phase = get_closest_full_moon()
    assert next_phase == datetime(
        2022, 5, 16, 6, 14, 7, 101064, tzinfo=ZoneInfo(key="Europe/Stockholm")
    )


def test_is_within_range(freezer):
    freezer.move_to("2024-12-07")
    next_phase = get_closest_full_moon()
    assert not is_within(check=next_phase, within=timedelta(seconds=24))
    assert not is_within(check=next_phase, within=timedelta(hours=24))
    assert is_within(check=next_phase, within=timedelta(days=24))


def test_is_within_close_before(freezer):
    freezer.move_to("2024-12-14T15:00:00+01:00")
    next_phase = get_closest_full_moon()
    assert is_within(check=next_phase, within=timedelta(hours=24))


def test_is_within_close_after(freezer):
    freezer.move_to("2024-12-15T15:00:00+01:00")
    next_phase = get_closest_full_moon()
    assert is_within(check=next_phase, within=timedelta(hours=24))


def test_is_within_too_early_before(freezer):
    freezer.move_to("2024-12-13T15:00:00+01:00")
    next_phase = get_closest_full_moon()
    assert not is_within(check=next_phase, within=timedelta(hours=24))


def test_is_within_too_late_after(freezer):
    freezer.move_to("2024-12-16T15:00:00+01:00")
    next_phase = get_closest_full_moon()
    assert not is_within(check=next_phase, within=timedelta(hours=24))
