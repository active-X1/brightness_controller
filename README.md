<div align="center">

# 💡 Brightness Controller

**A lightweight desktop utility for controlling your screen brightness.**

![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)
![Platforms](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)
![License: MIT](https://img.shields.io/badge/license-MIT-green)
![Code style: Ruff](https://img.shields.io/badge/code%20style-ruff-261230)

</div>

A small, modern desktop app built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
and [screen-brightness-control](https://github.com/Crozzers/screen_brightness_control).
Drag a slider, see the level, done. It can also start with your computer.

## Features

- **Instant brightness control** with a slider and a live percentage readout.
- **Launch at startup**: on first run the app asks whether it should start when you sign in.
  You can change your mind any time with the *Launch at startup* switch.
- **System / Light / Dark themes**, remembered between runs.
- **Smooth and safe**: slider changes are throttled so the window never lags on slow hardware,
  and problems (e.g. a monitor that can't be controlled) show a message instead of crashing.
- **Tiny**: two dependencies, no background services, no admin rights needed.

## Requirements

- Python **3.10 or newer**
- **Windows** or **Linux**. macOS is not supported by the underlying brightness library.
- A display that supports software brightness control. Laptop panels usually do;
  external monitors generally need **DDC/CI** enabled in their on-screen menu.

## Installation

```bash
git clone https://github.com/active-x1/brightness_controller.git
cd brightness_controller
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install .
```

> **Linux:** if Tkinter is missing, install it with `sudo apt install python3-tk` (Debian/Ubuntu)
> or `sudo dnf install python3-tkinter` (Fedora). Some Linux setups also need permission to change
> backlight values; see the
> [screen-brightness-control docs](https://crozzers.github.io/screen_brightness_control/) for details.

## Usage

```bash
brightness-controller              # or: python -m brightness_controller
```

| Option | Description |
| --- | --- |
| `--minimized` | Start minimised. This is what the startup entry uses. |
| `-V`, `--version` | Show the version. |

### Launch at startup

The first time you open the app it asks:

> **Launch at startup?** Would you like Brightness Controller to start automatically (minimised) when you sign in?

Answering **No thanks** means you won't be asked again. Closing the question with the window's X
button means it will be asked again next time. Either way, the **Launch at startup** switch in the
main window turns it on or off at any time.

| OS | What is created | Removed when switched off |
| --- | --- | --- |
| Windows | A value in `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` | ✅ |
| Linux | `~/.config/autostart/brightness-controller.desktop` | ✅ |

Both are per-user, so no administrator rights are needed. Settings are stored in
`%APPDATA%\BrightnessController\settings.json` on Windows and
`~/.config/brightness-controller/settings.json` on Linux.

## Project structure

```text
brightness_controller/
├── src/brightness_controller/
│   ├── core/                  # No UI imports: easy to test without a display
│   │   ├── brightness.py      #   BrightnessService: read/set brightness, friendly errors
│   │   ├── settings.py        #   JSON settings (theme, startup-prompt answered)
│   │   └── autostart.py       #   Launch at startup: Windows registry / Linux autostart
│   ├── ui/
│   │   ├── main_window.py     #   Slider, theme switch, startup switch
│   │   ├── startup_prompt.py  #   One-time "Launch at startup?" dialog
│   │   └── about_dialog.py
│   ├── main.py                # CLI entry point (--minimized, --version)
│   └── __main__.py            # python -m brightness_controller
├── tests/
├── .github/workflows/ci.yml
├── pyproject.toml
├── CHANGELOG.md
├── CONTRIBUTING.md
└── LICENSE
```

`core` never imports the UI, and the UI never talks to hardware, the registry or the file system
directly. It goes through `BrightnessService`, `SettingsStore` and `Autostart`, which can each be
replaced by a fake in tests.

## Development

```bash
pip install -e ".[dev]"
pytest            # tests (no display or monitor needed)
ruff check .      # lint
ruff format .     # format
mypy              # type-check the core
```

### Building a standalone executable

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name BrightnessController --paths src --collect-all customtkinter src/brightness_controller/__main__.py
```

The result is in `dist/`. A built executable registers *itself* for startup, so the
launch-at-startup switch keeps working. Attach it to a GitHub Release.

## License

Released under the [MIT License](LICENSE). Created by Cyrus Akacha Cyprian.
