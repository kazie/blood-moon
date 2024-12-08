from datetime import UTC, datetime, timedelta

import rich_click as click
from click import get_current_context
from dotenv import load_dotenv
from phue import PhueRegistrationException
from rich.console import Console

from blood_moon import moon_phase
from blood_moon.lamp import connect_and_get_bridge, get_moon_lamp, set_moon_lamp_red
from blood_moon.moon_phase import get_closest_full_moon, is_within

load_dotenv()

# Set up rich-click to be the default formatter
click.rich_click.USE_RICH_MARKUP = True
# Create a console instance for rich output
console = Console(record=True)
# Force colors
click.rich_click.COLOR_SYSTEM = "truecolor"


@click.command()
@click.option(
    "-r",
    "--run-if-blood-moon-phase",
    "scheduled_run",
    default=False,
    flag_value=True,
    type=bool,
    help="Turns on the [red]red[/red] blood moon if it is currently close to a full blood_moon.",
)
@click.option(
    "-c",
    "--check",
    "check",
    default=False,
    flag_value=True,
    type=bool,
    help="Returns if would set lamp or not, but won't actually set it",
)
@click.option(
    "-s",
    "--sync",
    "sync",
    default=False,
    flag_value=True,
    type=bool,
    help="Use this to check if hue connection is working, or to sync once pressed hue button",
)
@click.option(
    "-f",
    "--force-run",
    "force",
    default=False,
    flag_value=True,
    type=bool,
    help="Will set the lamp colour to [bold red]red[/bold red] right away, but only if lamp is on",
)
def blood_moon(**kwargs):
    """
    A simple program to steer your blood_moon light.
    When you are close to a [bold]full blood_moon[/bold], your [underline]blood_moon[/underline] will turn [bold red]red[/bold red].

    This only happens when a current full blood_moon is within 24 hours (before or after) the current time, and your lamp is already turned on.
    """
    load_dotenv()
    when = moon_phase.get_closest_full_moon()
    ctx = get_current_context()
    match kwargs:
        case {"check": True}:
            within = is_within(check=when, within=timedelta(hours=24))
            console.print(
                f"Closest full blood_moon is at [bright_cyan]{when}[/bright_cyan], thus we would {"" if within else "[bold red]not[/bold red]"} activate right now."
            )
            ctx.exit(0 if within else 1)
        case {"sync": True}:
            connect_and_get_bridge()
            console.print(
                "Hue connection synced, you are [underline]good to go[/underline]"
            )
            ctx.exit(0)
        case {"scheduled_run": True}:
            next_full_moon = get_closest_full_moon()
            is_soon = is_within(check=next_full_moon, within=timedelta(hours=24))
            if not is_soon:
                now = datetime.now(UTC)
                if next_full_moon < now:
                    console.print(
                        f"The blood moon has already risen, and rose at [bright_cyan]{next_full_moon}[/bright_cyan]"
                    )
                    ctx.exit(0)
                else:
                    console.print(
                        f"The blood moon has not risen yet, next full blood_moon is at [bright_cyan]{next_full_moon}[/bright_cyan]"
                    )
                    ctx.exit(0)
            bridge = connect_and_get_bridge()
            moon = get_moon_lamp(bridge)
            set_moon_lamp_red(moon)
            ctx.exit(0)
        case {"force": True}:
            bridge = connect_and_get_bridge()
            moon = get_moon_lamp(bridge)
            set_moon_lamp_red(moon)
            console.print("If on, the blood_moon should [red]now be red[/red]")
            ctx.exit(0)
        case _:
            console.print(ctx.get_help())
            ctx.exit(0)


if __name__ == "__main__":
    try:
        blood_moon()
    except PhueRegistrationException as e:
        ctx = get_current_context()
        console.print(
            "You are not registered with the Hue bridge yet, press [bold]the button[/bold] on your bridge, and try again"
        )
