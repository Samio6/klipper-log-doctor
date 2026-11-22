from klipper_log_doctor.analyzer import analyze_text


def test_detects_mcu_shutdown_with_line_number():
    findings = analyze_text(
        "Starting Klippy\nMCU 'mcu' shutdown: Timer too close\n"
    )

    assert len(findings) == 1
    assert findings[0].rule_id == "MCU_SHUTDOWN"
    assert findings[0].line_number == 2
    assert findings[0].severity == "error"


def test_detects_configuration_error():
    findings = analyze_text("Unknown config file section 'printer'")

    assert len(findings) == 1
    assert findings[0].rule_id == "CONFIG_ERROR"


def test_no_findings_for_unrelated_text():
    assert analyze_text("Starting Klippy\nPrinter is ready\n") == []


def test_returns_multiple_findings_in_log_order():
    findings = analyze_text(
        "MCU 'mcu' shutdown: test\n"
        "Lost communication with MCU 'toolhead'\n"
    )

    assert [item.rule_id for item in findings] == [
        "MCU_SHUTDOWN",
        "PROTOCOL_ERROR",
    ]
