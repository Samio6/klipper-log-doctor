# Klipper Log Doctor

Klipper Log Doctor is a beginner-friendly, local, read-only analyzer for Klipper `klippy.log` files. It looks for a small set of known error messages and explains what they may mean.

> **Important:** This project is an early prototype. Its findings are diagnostic hints, not a definitive diagnosis. It does not replace Klipper documentation or safe hardware troubleshooting.

## Project goals

- Read Klipper log files locally.
- Highlight recognizable errors and show their line numbers.
- Explain likely causes and safe next checks in plain language.
- Keep user data private: no log uploads, telemetry, or network calls.
- Never control a printer or modify printer configuration.

## Current status

Version: **0.1.0 — first command-line prototype**

Initial detection rules:
- MCU shutdown messages
- MCU communication and protocol errors
- Configuration parsing errors
- Heater verification and ADC range errors
- Printer firmware restart markers

The rules are intentionally conservative and will expand as we add real-world examples and tests.

## Install from a local clone

Requires Python 3.10 or newer.

```bash
git clone https://github.com/Samio6/klipper-log-doctor.git
cd klipper-log-doctor
python -m pip install .
```

## Analyze a log

```bash
klipper-log-doctor /path/to/klippy.log
```

On Windows, use a path such as:

```powershell
klipper-log-doctor "C:\Users\YourName\Downloads\klippy.log"
```

The program only reads the file. It does not edit it or communicate with the printer.

## Run tests

```bash
python -m pip install pytest
python -m pytest
```

## Privacy and safety

- Log contents are processed on the computer running the tool.
- No network requests are made by the analyzer.
- The tool does not execute commands on the printer.
- The tool does not edit configuration files.
- Before sharing a log publicly, remove IP addresses, serial numbers, hostnames, usernames, and other private information.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).
