from click.testing import CliRunner

import blood_moon.bm as bm


def test_help_shown_without_args():
    runner = CliRunner()
    result = runner.invoke(bm.blood_moon, [])
    assert result.exit_code == 0
    # rich-click formats help without the plain 'Options:' header, but always shows 'Usage:'
    assert "Usage:" in result.output


def test_check_mode_when_not_within_any(freezer):
    # A date far from both full and new moon within 24h
    freezer.move_to("2024-12-07")
    runner = CliRunner()
    result = runner.invoke(bm.blood_moon, ["--check"])
    assert result.exit_code == 1
    assert "Closest full moon is at" in result.output
    assert "Closest new moon is at" in result.output


def test_sync_calls_connect_and_reports(mocker):
    runner = CliRunner()
    mock_connect = mocker.patch("blood_moon.bm.connect_and_get_bridge")

    result = runner.invoke(bm.blood_moon, ["--sync"])

    assert result.exit_code == 0
    mock_connect.assert_called_once()
    assert "Hue connection synced" in result.output


def test_force_red_invokes_setter(mocker):
    runner = CliRunner()
    mocker.patch("blood_moon.bm.connect_and_get_bridge")
    fake_lamp = object()
    mocker.patch("blood_moon.bm.get_moon_lamp", return_value=fake_lamp)
    mock_set_red = mocker.patch("blood_moon.bm.set_moon_lamp_red")

    result = runner.invoke(bm.blood_moon, ["--force-red"])

    assert result.exit_code == 0
    mock_set_red.assert_called_once_with(fake_lamp)
    assert "now be red" in result.output


def test_force_teal_invokes_setter(mocker):
    runner = CliRunner()
    mocker.patch("blood_moon.bm.connect_and_get_bridge")
    fake_lamp = object()
    mocker.patch("blood_moon.bm.get_moon_lamp", return_value=fake_lamp)
    mock_set_teal = mocker.patch("blood_moon.bm.set_moon_lamp_teal")

    result = runner.invoke(bm.blood_moon, ["--force-teal"])

    assert result.exit_code == 0
    mock_set_teal.assert_called_once_with(fake_lamp)
    assert "now be teal" in result.output


def test_scheduled_run_sets_red_when_full_moon_near(freezer, mocker):
    # Within 24h of known full moon around 2024-12-14/15
    freezer.move_to("2024-12-14T15:00:00+01:00")
    runner = CliRunner()

    mocker.patch("blood_moon.bm.connect_and_get_bridge")
    fake_lamp = object()
    mocker.patch("blood_moon.bm.get_moon_lamp", return_value=fake_lamp)
    mock_set_red = mocker.patch("blood_moon.bm.set_moon_lamp_red")
    mock_set_teal = mocker.patch("blood_moon.bm.set_moon_lamp_teal")

    result = runner.invoke(bm.blood_moon, ["--run-if-moon-phase"])

    assert result.exit_code == 0
    mock_set_red.assert_called_once_with(fake_lamp)
    mock_set_teal.assert_not_called()


def test_scheduled_run_sets_teal_when_new_moon_near(freezer, mocker):
    # Within 24h of known new moon 2025-10-21
    freezer.move_to("2025-10-21T15:00:00+01:00")
    runner = CliRunner()

    mocker.patch("blood_moon.bm.connect_and_get_bridge")
    fake_lamp = object()
    mocker.patch("blood_moon.bm.get_moon_lamp", return_value=fake_lamp)
    mock_set_red = mocker.patch("blood_moon.bm.set_moon_lamp_red")
    mock_set_teal = mocker.patch("blood_moon.bm.set_moon_lamp_teal")

    result = runner.invoke(bm.blood_moon, ["--run-if-moon-phase"])

    assert result.exit_code == 0
    mock_set_teal.assert_called_once_with(fake_lamp)
    mock_set_red.assert_not_called()


def test_scheduled_run_when_not_within_any_reports_and_exits_0(freezer, mocker):
    freezer.move_to("2024-12-07")
    runner = CliRunner()

    # Ensure we do not attempt to connect to the bridge in this branch
    mock_connect = mocker.patch("blood_moon.bm.connect_and_get_bridge")

    result = runner.invoke(bm.blood_moon, ["--run-if-moon-phase"])

    assert result.exit_code == 0
    mock_connect.assert_not_called()
    # Output should mention both phases
    assert "The blood moon" in result.output
    assert "new moon" in result.output


def test_scheduled_run_reports_full_already_risen_and_new_not_arrived_yet(
    freezer, mocker
):
    # Freeze time and craft phase times so that:
    # - Full moon is in the past (>24h): triggers "already risen" branch.
    # - New moon is in the future (>24h): triggers "has not arrived yet" branch.
    from datetime import datetime, timedelta
    from zoneinfo import ZoneInfo

    freezer.move_to("2025-01-10T12:00:00+01:00")
    tz = ZoneInfo("Europe/Stockholm")

    full_when = datetime.now(tz) - timedelta(days=2)
    new_when = datetime.now(tz) + timedelta(days=2)

    mocker.patch("blood_moon.bm.get_closest_full_moon", return_value=full_when)
    mocker.patch("blood_moon.bm.get_closest_new_moon", return_value=new_when)
    mock_connect = mocker.patch("blood_moon.bm.connect_and_get_bridge")

    runner = CliRunner()
    result = runner.invoke(bm.blood_moon, ["--run-if-moon-phase"])

    assert result.exit_code == 0
    mock_connect.assert_not_called()
    assert "has already risen" in result.output
    assert "has not arrived yet" in result.output
