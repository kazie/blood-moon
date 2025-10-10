import pytest

from blood_moon.lamp import (
    connect_and_get_bridge,
    get_moon_lamp,
    set_moon_lamp_red,
    set_moon_lamp_teal,
)

# Mock environment variables
MOCK_HUE_BRIDGE_IP = "hue-bridge-ip"
MOCK_MOON_LAMP_NAME = "blood_moon-test-lamp"


@pytest.fixture(autouse=True)
def set_env_vars(monkeypatch):
    monkeypatch.setenv("HUE_BRIDGE_IP", MOCK_HUE_BRIDGE_IP)
    monkeypatch.setenv("MOON_LAMP_NAME", MOCK_MOON_LAMP_NAME)


def test_connect_and_get_bridge(mocker):
    mock_bridge = mocker.patch("blood_moon.lamp.Bridge")
    bridge_instance = mock_bridge.return_value

    bridge = connect_and_get_bridge()

    mock_bridge.assert_called_once_with(ip=MOCK_HUE_BRIDGE_IP)
    assert bridge == bridge_instance


def test_connect_and_get_bridge_with_no_env_vars(monkeypatch):
    monkeypatch.delenv("HUE_BRIDGE_IP")
    with pytest.raises(ValueError, match="HUE_BRIDGE_IP not set"):
        connect_and_get_bridge()


def test_get_moon_lamp(mocker):
    # Create a mock Bridge object using the mocker fixture
    mock_bridge = mocker.MagicMock()
    mock_light = mocker.MagicMock()
    mock_bridge.__getitem__.return_value = mock_light

    # Call the function under test
    moon_lamp = get_moon_lamp(mock_bridge)

    # Assert that the bridge is accessed with the correct lamp name
    mock_bridge.__getitem__.assert_called_once_with(MOCK_MOON_LAMP_NAME)
    # Ensure the moon_lamp returned is the mock_light object
    assert moon_lamp == mock_light


def test_get_moon_lamp_with_no_env_vars(monkeypatch, mocker):
    monkeypatch.delenv("MOON_LAMP_NAME")
    with pytest.raises(ValueError, match="MOON_LAMP_NAME not set"):
        get_moon_lamp(mocker.Mock())


def test_set_moon_lamp_red_when_on(mocker):
    mock_light = mocker.Mock()
    mock_light.on = True
    # Use PropertyMock to monitor the .xy property
    xy_property = mocker.PropertyMock()
    type(mock_light).xy = xy_property

    set_moon_lamp_red(mock_light)

    xy_property.assert_called_once_with([0.675, 0.322])


def test_no_set_moon_lamp_red_when_off(mocker):
    mock_light = mocker.Mock()
    mock_light.on = False
    # Use PropertyMock to monitor the .xy property
    xy_property = mocker.PropertyMock()
    type(mock_light).xy = xy_property

    set_moon_lamp_red(mock_light)

    assert not mock_light.xy.called


def test_set_moon_lamp_teal_when_on(mocker):
    mock_light = mocker.Mock()
    mock_light.on = True
    # Use PropertyMock to monitor the .xy property
    xy_property = mocker.PropertyMock()
    type(mock_light).xy = xy_property

    set_moon_lamp_teal(mock_light)

    xy_property.assert_called_once_with([0.17, 0.34])


def test_no_set_moon_lamp_teal_when_off(mocker):
    mock_light = mocker.Mock()
    mock_light.on = False
    # Use PropertyMock to monitor the .xy property
    xy_property = mocker.PropertyMock()
    type(mock_light).xy = xy_property

    set_moon_lamp_teal(mock_light)

    assert not mock_light.xy.called
