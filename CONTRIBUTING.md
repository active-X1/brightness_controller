# Contributing

```bash
git clone https://github.com/active-x1/brightness_controller.git
cd brightness_controller
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

```bash
pytest          # tests (no display or monitor needed)
ruff check .    # lint
ruff format .   # format
mypy            # type-check the core
```

## Guidelines

- Keep the app **desktop-only**. This is a small utility, not a framework.
- Anything that doesn't need a window belongs in `brightness_controller.core`
  and must not import `customtkinter`, so it stays testable without a display.
- `ui` should stay thin: render state, forward input to `core`.
- Add a test for every behaviour change in `core`, and a line in `CHANGELOG.md`
  for anything users will notice.
