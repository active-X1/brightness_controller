# Brightness Controller

A lightweight Python desktop app for controlling screen brightness through a modern CustomTkinter interface.

## Features

- Adjust screen brightness with a slider
- Display current brightness level
- Toggle app appearance between Light and Dark themes
- View About dialog with app details

## Requirements

- Python 3.10+ (or compatible)
- `customtkinter`
- `screen_brightness_control`

## Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd Advance
   ```
2. Install dependencies:
   ```bash
   pip install customtkinter screen_brightness_control
   ```

## Usage

Run the app from the `Brightness` folder:

```bash
python Brightness/brightness.py
```

## Notes

- The app reads the current screen brightness on startup and updates the slider accordingly.
- Brightness changes are applied immediately when the slider is moved.
- Theme selection uses CustomTkinter appearance modes.

## About

This app demonstrates a small Python GUI utility for system brightness control.
It is built with `customtkinter` for the interface and `screen_brightness_control` for monitor brightness management.
