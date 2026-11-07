"""
Autonomous Refactoring & Modular Scaling Engine
Enforces Article II & III of the Autonomous System Foundational Constitution.
Governing Authority: Governing Officer Tarwater
"""

import os
import json
import yaml
import logging
import subprocess
from datetime import datetime, timezone

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

CONFIG_PATH = "governance_config.yaml"


def load_governance_policy(path: str = CONFIG_PATH) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def check_emergency_override(policy: dict) -> None:
    """Article III.2: Halts all execution if Governing Officer Tarwater triggers the kill switch."""
    override_cfg = policy["communication_and_oversight"]["emergency_override"]
    env_kill_switch = os.getenv("TARWATER_KILL_SWITCH", "false").lower() == "true"

    if override_cfg.get("global_kill_switch") or env_kill_switch:
        logging.critical("EMERGENCY OVERRIDE ACTIVE: Execution halted by Governing Officer Tarwater.")
        raise SystemExit(1)


def send_webhook_alert(policy: dict, event_type: str, details: dict) -> None:
    """Article III.1: Dispatches real-time audit logs and alerts to Governing Officer Tarwater."""
    notif_cfg = policy["communication_and_oversight"]["notifications"]
    if not notif_cfg.get("webhook_alerts_enabled"):
        return

    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "recipient": notif_cfg["notify_target"],
        "event": event_type,
        "details": details
    }

    webhook_url = os.getenv("TARWATER_WEBHOOK_URL")
    if webhook_url:
        # Placeholder for HTTP POST request (e.g., requests.post(webhook_url, json=payload))
        logging.info(f"Webhook dispatched to {webhook_url}: {json.dumps(payload)}")
    else:
        logging.info(f"[AUDIT LOG - WEBHOOK QUEUED]: {json.dumps(payload)}")


def commit_with_audit_tag(tag: str, message: str) -> None:
    """Article II.2: Commits autonomous actions with mandatory constitutional audit tags."""
    full_message = f"{tag} {message}"
    logging.info(f"Committing change: {full_message}")
    subprocess.run(["git", "add", "."], check=False)
    subprocess.run(["git", "commit", "-m", full_message], check=False)


def evaluate_and_enforce(metrics: dict) -> None:
    """
    Evaluates CI/CD telemetry against governance_config.yaml thresholds
    and triggers refactoring PRs or sub-repository isolation.
    """
    policy = load_governance_policy()
    check_emergency_override(policy)

    safeguards = policy["architectural_safeguards"]
    min_cov = safeguards["quality_baseline"]["min_test_coverage_percent"]
    max_cc = safeguards["quality_baseline"]["max_cyclomatic_complexity"]
    spawn_cc = safeguards["modular_scaling"]["complexity_threshold_for_isolation"]

    tests_passed = metrics.get("tests_passed", True)
    coverage = metrics.get("test_coverage", 100.0)
    complexity = metrics.get("max_module_complexity", 1)
    target_module = metrics.get("target_module", "core_module")

    # 1. Check Modular Isolation Threshold (Article II.2 & IV.1)
    if complexity >= spawn_cc and safeguards["modular_scaling"]["dynamic_repo_spawning_enabled"]:
        new_repo_name = f"autonomous-sub-{target_module.replace('_', '-')}"
        logging.warning(f"Complexity ({complexity}) exceeded isolation limit ({spawn_cc}). Spawning {new_repo_name}.")
        commit_with_audit_tag("[SPAWN-REPO]", f"Isolated {target_module} into modular repo {new_repo_name}")
        send_webhook_alert(policy, "SUB_REPO_SPAWNED", {
            "module": target_module,
            "new_repository": new_repo_name,
            "complexity": complexity
        })
        return

    # 2. Check Quality Baseline & Trigger Self-Refactoring (Article II.2)
    if not tests_passed or coverage < min_cov or complexity > max_cc:
        reason = []
        if not tests_passed:
            reason.append("unit/integration test failure")
        if coverage < min_cov:
            reason.append(f"coverage {coverage}% < {min_cov}%")
        if complexity > max_cc:
            reason.append(f"complexity {complexity} > {max_cc}")

        reason_str = ", ".join(reason)
        logging.warning(f"Quality baseline breached ({reason_str}). Triggering autonomous refactor PR.")
        commit_with_audit_tag("[REFACTOR]", f"Autonomous refactor PR generated for {target_module}: {reason_str}")
        send_webhook_alert(policy, "AUTONOMOUS_REFACTOR_TRIGGERED", {
            "module": target_module,
            "reasons": reason,
            "requires_approval_from": policy["operational_mandate"]["require_final_approval_from"]
        })
    else:
        logging.info("All CI/CD metrics comply with Constitutional Quality Baseline.")


if __name__ == "__main__":
    # Simulated CI/CD telemetry run
    sample_ci_metrics = {
        "target_module": "task_scheduler",
        "tests_passed": True,
        "test_coverage": 81.5,
        "max_module_complexity": 9
    }
    evaluate_and_enforce(sample_ci_metrics)
