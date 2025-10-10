import os

from phue import Bridge, Light


def connect_and_get_bridge() -> Bridge:
    """Connect to the Hue bridge using the HUE_BRIDGE_IP env var.

    Will try to connect and register if no settings are found.
    """
    hue_ip = os.getenv("HUE_BRIDGE_IP")
    if hue_ip is None:
        raise ValueError("HUE_BRIDGE_IP not set")
    return Bridge(ip=hue_ip)


def get_moon_lamp(bridge: Bridge) -> Light:
    """Return the configured moon lamp light from the bridge by MOON_LAMP_NAME."""
    moon_name = os.getenv("MOON_LAMP_NAME")
    if moon_name is None:
        raise ValueError("MOON_LAMP_NAME not set")
    return bridge[moon_name]


def set_moon_lamp_red(lamp: Light):
    """Set the lamp to red if it is currently turned on."""
    if lamp.on is True:
        red_in_xy = [0.675, 0.322]
        lamp.xy = red_in_xy


def set_moon_lamp_teal(lamp: Light):
    """Set the lamp to teal if it is currently turned on."""
    if lamp.on is True:
        teal_in_xy = [0.17, 0.34]  # Teal coordinates for xy color space.
        lamp.xy = teal_in_xy
