import subprocess


def build():
    print("🐶🧹 Formatting code with ruff")
    subprocess.run("ruff format .", check=True, shell=True)
    print("🐶🔬 Checking code with ruff")
    subprocess.run("ruff check .", check=True, shell=True)
    print("🎰 Checking __slots__ with slotscheck")
    subprocess.run("slotscheck blood_moon/", check=True, shell=True)
    print("🧪 Running tests with pytest")
    subprocess.run("pytest --cov=blood_moon .", check=True, shell=True)


def blood_moon():
    subprocess.run(
        "python blood_moon/bm.py --run-if-moon-phase", check=True, shell=True
    )


def help_svg():
    """Export the CLI help to an SVG (help.svg) using the rich console renderer.

    Run this inside the uv environment via: `uv run help_svg`.
    """
    # Pipeline the help text into the SVG exporter script
    subprocess.run(
        "python blood_moon/bm.py --help | python scripts/export_svg.py",
        check=True,
        shell=True,
    )
