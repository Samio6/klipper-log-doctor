"""Small, explainable rules for common Klipper log errors."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class Finding:
    """A diagnostic finding tied to a line in the log."""

    rule_id: str
    title: str
    severity: str
    explanation: str
    next_steps: tuple[str, ...]
    line_number: int
    matched_text: str


@dataclass(frozen=True)
class Rule:
    rule_id: str
    title: str
    severity: str
    pattern: re.Pattern[str]
    explanation: str
    next_steps: tuple[str, ...]


RULES: tuple[Rule, ...] = (
    Rule(
        rule_id="MCU_SHUTDOWN",
        title="MCU shutdown",
        severity="error",
        pattern=re.compile(r"MCU .* shutdown|Shutdown due to", re.IGNORECASE),
        explanation="Klipper stopped because a micro-controller reported a shutdown condition. Nearby log lines usually contain the specific cause.",
        next_steps=(
            "Read several lines before and after this message for the detailed shutdown reason.",
            "Check wiring, connectors, power, and the component named in the surrounding messages.",
            "Do not repeatedly restart until the underlying cause is understood.",
        ),
    ),
    Rule(
        rule_id="PROTOCOL_ERROR",
        title="MCU communication or protocol error",
        severity="error",
        pattern=re.compile(r"protocol error|Unable to .* communicate with MCU|Lost communication with MCU", re.IGNORECASE),
        explanation="The host and a micro-controller may have lost communication or disagreed about the expected protocol.",
        next_steps=(
            "Check the MCU USB or serial connection and its power supply.",
            "Review recent firmware or configuration changes.",
            "Inspect earlier log lines for the first communication failure.",
        ),
    ),
    Rule(
        rule_id="CONFIG_ERROR",
        title="Configuration error",
        severity="error",
        pattern=re.compile(r"Error loading template|Option .* is not valid|Unknown config file section|Unable to parse", re.IGNORECASE),
        explanation="Klipper reported a configuration parsing or validation problem.",
        next_steps=(
            "Read the complete error message; it often names the section or option.",
            "Check spelling, indentation, and whether the option is supported by your Klipper version.",
            "Back up the configuration before making changes.",
        ),
    ),
    Rule(
        rule_id="THERMAL_VERIFY",
        title="Temperature verification failed",
        severity="error",
        pattern=re.compile(r"Heater .* not heating at expected rate|ADC out of range", re.IGNORECASE),
        explanation="A temperature sensor or heater did not behave as Klipper expected. This can indicate a wiring, sensor, heater, or power problem.",
        next_steps=(
            "Stop heating and inspect the sensor and heater wiring with power disconnected.",
            "Check that the configured sensor type matches the installed sensor.",
            "Do not bypass the thermal safety check.",
        ),
    ),
    Rule(
        rule_id="RESTART_REQUIRED",
        title="Klipper restart marker",
        severity="warning",
        pattern=re.compile(r"Firmware restart|Restarting printer", re.IGNORECASE),
        explanation="The log contains a restart marker. This is often informational; inspect nearby lines to determine why it occurred.",
        next_steps=(
            "Review the surrounding lines for the event that triggered the restart.",
            "If this repeats unexpectedly, look for the first error before the restart marker.",
        ),
    ),
)


def analyze_text(text: str) -> list[Finding]:
    """Analyze log text and return matching findings in log order."""
    findings: list[Finding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for rule in RULES:
            if rule.pattern.search(line):
                findings.append(
                    Finding(
                        rule_id=rule.rule_id,
                        title=rule.title,
                        severity=rule.severity,
                        explanation=rule.explanation,
                        next_steps=rule.next_steps,
                        line_number=line_number,
                        matched_text=line.strip(),
                    )
                )
    return findings


def analyze_file(path: str | Path) -> list[Finding]:
    """Read a log file without modifying it and analyze its contents."""
    log_path = Path(path)
    text = log_path.read_text(encoding="utf-8", errors="replace")
    return analyze_text(text)
