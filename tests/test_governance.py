"""
Foundational Unit Test Suite for Autonomous Governance Core
Verifies Constitutional Overrides, Policy Loading, and Telemetry Scanning.
Governing Authority: Governing Officer Tarwater
"""

import os
import pytest
from refactor_engine import load_governance_policy, check_emergency_override
from telemetry_scanner import discover_python_modules, scan_cyclomatic_complexity


def test_policy_loads_correctly():
    """Verifies governance_config.yaml loads and enforces Tarwater's authority."""
    policy = load_governance_policy()
    assert policy["system_metadata"]["governing_officer"] == "Tarwater"
    assert policy["architectural_safeguards"]["quality_baseline"]["min_test_coverage_percent"] >= 80.0
    assert policy["architectural_safeguards"]["quality_baseline"]["max_cyclomatic_complexity"] <= 15


def test_emergency_kill_switch_halts_execution(monkeypatch):
    """Article III.2: Ensures TARWATER_KILL_SWITCH immediately halts all system execution."""
    policy = load_governance_policy()
    monkeypatch.setenv("TARWATER_KILL_SWITCH", "true")

    with pytest.raises(SystemExit) as exc_info:
        check_emergency_override(policy)
    assert exc_info.value.code == 1


def test_emergency_kill_switch_allows_normal_run(monkeypatch):
    """Ensures system proceeds normally when kill switch is disengaged."""
    policy = load_governance_policy()
    policy["communication_and_oversight"]["emergency_override"]["global_kill_switch"] = False
    monkeypatch.setenv("TARWATER_KILL_SWITCH", "false")

    # Should complete without raising SystemExit
    check_emergency_override(policy)


def test_telemetry_discovers_core_modules():
    """Verifies telemetry_scanner locates core Python files and measures complexity."""
    modules = discover_python_modules(".")
    assert "refactor_engine.py" in modules
    assert "override_control.py" in modules
    assert "telemetry_scanner.py" in modules

    report = scan_cyclomatic_complexity("override_control.py")
    assert report["file"] == "override_control.py"
    assert report["max_complexity"] >= 1
