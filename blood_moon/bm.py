from datetime import UTC, datetime, timedelta

import rich_click as click
from click import get_current_context
from dotenv import load_dotenv
from phue import PhueRegistrationException
from rich.console import Console

from blood_moon.lamp import (
    connect_and_get_bridge,
    get_moon_lamp,
    set_moon_lamp_red,
    set_moon_lamp_teal,
)
from blood_moon.moon_phase import get_closest_full_moon, get_closest_new_moon, is_within

load_dotenv()

# Set up rich-click to be the default formatter
click.rich_click.TEXT_MARKUP = "rich"
# Create a console instance for rich output
console = Console(record=True)
# Force colors
click.rich_click.COLOR_SYSTEM = "truecolor"


@click.command()
@click.option(
    "-r",
    "--run-if-moon-phase",
    "scheduled_run",
    default=False,
    flag_value=True,
    type=bool,
    help="Scheduled run: if near a full moon turns [red]red[/red]; if near a new moon turns [cyan]teal[/cyan].",
)
@click.option(
    "-c",
    "--check",
    "check",
    default=False,
    flag_value=True,
    type=bool,
    help="Show whether we'd set the lamp to [red]red[/red] (full moon) or [cyan]teal[/cyan] (new moon) right now, without actually changing it.",
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
    "-fr",
    "--force-red",
    "force_red",
    default=False,
    flag_value=True,
    type=bool,
    help="Will set the lamp colour to [bold red]red[/bold red] right away, but only if lamp is on",
)
@click.option(
    "-ft",
    "--force-teal",
    "force_teal",
    default=False,
    flag_value=True,
    type=bool,
    help="Will set the lamp colour to [bold cyan]teal[/bold cyan] right away, but only if lamp is on",
)
def blood_moon(**kwargs):
    """
    A simple program to steer your moon light.

    - Near a [bold]full moon[/bold] (within 24 hours), your [underline]moon[/underline] will turn [bold red]red[/bold red].
    - Near a [bold]new moon[/bold] (within 24 hours), it will turn [cyan]teal[/cyan].

    The lamp color is only changed if the lamp is already turned on.
    """
    load_dotenv()
    ctx = get_current_context()
    match kwargs:
        case {"check": True}:
            full_when = get_closest_full_moon()
            full_within = is_within(check=full_when, within=timedelta(hours=24))
            new_when = get_closest_new_moon()
            new_within = is_within(check=new_when, within=timedelta(hours=24))
            console.print(
                f"Closest full moon is at [bright_cyan]{full_when}[/bright_cyan], thus we would {'' if full_within else '[bold red]not[/bold red]'} activate [red]red[/red] right now."
            )
            console.print(
                f"Closest new moon is at [bright_cyan]{new_when}[/bright_cyan], thus we would {'' if new_within else '[bold red]not[/bold red]'} activate [cyan]teal[/cyan] right now."
            )
            ctx.exit(0 if (full_within or new_within) else 1)
        case {"sync": True}:
            connect_and_get_bridge()
            console.print(
                "Hue connection synced, you are [underline]good to go[/underline]"
            )
            ctx.exit(0)
        case {"scheduled_run": True}:
            full_when = get_closest_full_moon()
            full_within = is_within(check=full_when, within=timedelta(hours=24))
            new_when = get_closest_new_moon()
            new_within = is_within(check=new_when, within=timedelta(hours=24))
            if not (full_within or new_within):
                now = datetime.now(UTC)
                # Inform about next occurrences
                if full_when < now:
                    console.print(
                        f"The blood moon has already risen, and rose at [bright_cyan]{full_when}[/bright_cyan]"
                    )
                else:
                    console.print(
                        f"The blood moon has not risen yet, next full moon is at [bright_cyan]{full_when}[/bright_cyan]"
                    )
                if new_when < now:
                    console.print(
                        f"The new moon has already passed at [bright_cyan]{new_when}[/bright_cyan]"
                    )
                else:
                    console.print(
                        f"The new moon has not arrived yet, next new moon is at [bright_cyan]{new_when}[/bright_cyan]"
                    )
                ctx.exit(0)
            bridge = connect_and_get_bridge()
            moon = get_moon_lamp(bridge)
            if full_within:
                set_moon_lamp_red(moon)
            elif new_within:
                set_moon_lamp_teal(moon)
            ctx.exit(0)
        case {"force_red": True}:
            bridge = connect_and_get_bridge()
            moon = get_moon_lamp(bridge)
            set_moon_lamp_red(moon)
            console.print("If on, the blood_moon should [red]now be red[/red]")
            ctx.exit(0)
        case {"force_teal": True}:
            bridge = connect_and_get_bridge()
            moon = get_moon_lamp(bridge)
            set_moon_lamp_teal(moon)
            console.print("If on, the blood_moon should now be teal")
            ctx.exit(0)
        case _:
            console.print(ctx.get_help())
            ctx.exit(0)


if __name__ == "__main__":
    try:
        blood_moon()
    except PhueRegistrationException:
        console.print(
            "You are not registered with the Hue bridge yet, press [bold]the button[/bold] on your bridge, and try again"
        )
