import runpy
import sys

import pytest
from phue import PhueRegistrationException


def test_main_invocation_check_exits_with_status(freezer):
    # Choose a date far from both phases within 24h to force exit code 1
    freezer.move_to("2024-12-07")

    argv_backup = sys.argv[:]
    try:
        sys.argv = ["blood_moon/bm.py", "--check"]
        # Ensure a clean import state for runpy to avoid RuntimeWarning
        sys.modules.pop("blood_moon.bm", None)
        with pytest.raises(SystemExit) as exc:
            runpy.run_module("blood_moon.bm", run_name="__main__")
        assert exc.value.code == 1
    finally:
        sys.argv = argv_backup


def test_main_handles_phue_registration_exception(monkeypatch, capsys):
    # Patch the lamp connector so that the __main__ try/except branch is exercised
    import blood_moon.lamp as lamp

    monkeypatch.setattr(
        lamp,
        "connect_and_get_bridge",
        lambda: (_ for _ in ()).throw(
            PhueRegistrationException(101, "link button not pressed")
        ),
    )

    argv_backup = sys.argv[:]
    try:
        sys.argv = ["blood_moon/bm.py", "--sync"]
        # Ensure a clean import state for runpy to avoid RuntimeWarning
        sys.modules.pop("blood_moon.bm", None)
        # This should not raise, the exception is handled in __main__
        runpy.run_module("blood_moon.bm", run_name="__main__")
        out = capsys.readouterr().out
        assert "You are not registered with the Hue bridge yet" in out
    finally:
        sys.argv = argv_backup
