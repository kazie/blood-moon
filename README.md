# Blood Moon

![`python blood_moon/bm.py --help | python scripts/export_svg.py`](./help.svg)


## Description
**Blood Moon** is a script designed to control the lighting of a moon-themed lamp equipped with a Philips Hue light.
This script adjusts the lamp's color to a striking red when a full blood moon is near.


## Features
- Detects the closest full blood moon.
- Changes the lamp color to red during the full blood moon phase.
- Syncs with the Philips Hue system to ensure connectivity.
- Various command-line options to check, force a run, or use scheduled automation.

## Dependencies
This project requires Python 3.14 or newer, and the dependencies listed in [pyproject.toml](pyproject.toml) are managed by Poetry.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd blood_moon
   ```

2. **Install uv** (if not already installed):
   - `uv` for packages
   - `ruff` for formatting
   - `hatchling` for build system (`uv` does not support `run` itself)

3. **Install the Project Dependencies**:
   ```bash
   uv sync
   ```

4. **Environment Configuration**:
   Copy the `.env.example` file to `.env` and update it with your Philips Hue settings:
   ```properties
   HUE_BRIDGE_IP=your-hue-bridge-ip
   MOON_LAMP_NAME=Your Lamp Name
   ```

## Testing
You can run tests for the Blood Moon project using Poetry.  
The command to execute the tests is:

```bash
uv run build
```

This command will trigger the test suite configured in your development environment.
Ensure all tests pass to verify that the functionalities behave as expected.

## Usage
Run the script using one of its command-line options:
- **Check the moon phase**:
  ```bash
  uv run blood_moon --check
  ```
- **Force set the lamp**:
  ```bash
  uv run blood_moon --force-run
  ```
- **Sync with the Philips Hue bridge**:
  ```bash
  uv run blood_moon --sync
  ```
- **Run in scheduled mode**:
  ```bash
  uv run blood_moon --run-if-blood-moon-phase
  ```
