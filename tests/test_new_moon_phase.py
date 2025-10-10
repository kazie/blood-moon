from datetime import datetime
from datetime import timedelta
from zoneinfo import ZoneInfo

from inline_snapshot import snapshot

from blood_moon.moon_phase import get_closest_new_moon, is_within


def test_get_next_new_moon_known_date(freezer):
    freezer.move_to("2025-10-21")
    next_phase = get_closest_new_moon()
    assert next_phase == snapshot(
        datetime(
            2025, 10, 21, 14, 25, 7, 590606, tzinfo=ZoneInfo(key="Europe/Stockholm")
        )
    )


def test_is_within_range(freezer):
    freezer.move_to("2025-10-20")
    next_phase = get_closest_new_moon()
    assert not is_within(check=next_phase, within=timedelta(seconds=24))
    assert not is_within(check=next_phase, within=timedelta(hours=24))
    assert is_within(check=next_phase, within=timedelta(days=24))


def test_is_within_close_before(freezer):
    freezer.move_to("2025-10-21T15:00:00+01:00")
    next_phase = get_closest_new_moon()
    assert is_within(check=next_phase, within=timedelta(hours=24))


def test_is_within_close_after(freezer):
    freezer.move_to("2025-10-21T15:00:00+01:00")
    next_phase = get_closest_new_moon()
    assert is_within(check=next_phase, within=timedelta(hours=24))


def test_is_within_too_early_before(freezer):
    freezer.move_to("2025-10-19T15:00:00+01:00")
    next_phase = get_closest_new_moon()
    assert not is_within(check=next_phase, within=timedelta(hours=24))


def test_is_within_too_late_after(freezer):
    freezer.move_to("2025-10-22T15:00:00+01:00")
    next_phase = get_closest_new_moon()
    assert not is_within(check=next_phase, within=timedelta(hours=24))
