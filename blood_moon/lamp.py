import os

from phue import Bridge, Light


def connect_and_get_bridge() -> Bridge:
    hue_ip = os.getenv("HUE_BRIDGE_IP")
    if hue_ip is None:
        raise ValueError("HUE_BRIDGE_IP not set")
    # Will try to connect, and register if no settings found
    return Bridge(ip=hue_ip)


def get_moon_lamp(bridge: Bridge) -> Light:
    moon_name = os.getenv("MOON_LAMP_NAME")
    if moon_name is None:
        raise ValueError("MOON_LAMP_NAME not set")
    return bridge[moon_name]


def set_moon_lamp_red(lamp: Light):
    if lamp.on is True:
        red_in_xy = [0.675, 0.322]
        lamp.xy = red_in_xy
