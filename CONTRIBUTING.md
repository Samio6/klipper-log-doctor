# Contributing

Thanks for helping improve Klipper Log Doctor.

## Development setup

1. Install Python 3.10 or newer.
2. Clone this repository.
3. From the repository folder, create and activate a virtual environment.
4. Install the project and pytest:

```bash
python -m pip install -e .
python -m pip install pytest
```

## Run the tests

```bash
python -m pytest
```

## Project principles

- Analyze log files locally and read-only.
- Never modify printer configuration or send commands to a printer.
- Do not upload logs or other user data.
- Explain findings in plain language and avoid claiming certainty when a log is incomplete.
- Add a test for each new detection rule.

Before sharing a log in an issue, remove IP addresses, serial numbers, hostnames, usernames, and other private information.
