"""
Emergency Override & Executive Administrative Control Interface
Enforces Article I.1, Article III.2, and Article IV.2 of the Constitution.
Exclusive Authority: Governing Officer Tarwater
"""

import os
import sys
import yaml
import json
import logging
import subprocess
from datetime import datetime, timezone

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

CONFIG_PATH = "governance_config.yaml"
AUDIT_LOG_PATH = "executive_audit.log"


def load_policy() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_policy(policy: dict) -> None:
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(policy, f, sort_keys=False)


def record_executive_action(action: str, detail: str) -> None:
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "authority": "Governing Officer Tarwater",
        "action": action,
        "detail": detail
    }
    with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    logging.info(f"EXECUTIVE AUDIT RECORDED: {action} - {detail}")


def verify_authority() -> None:
    """Validates executive override token before executing administrative actions."""
    expected_token = os.getenv("TARWATER_ADMIN_TOKEN")
    provided_token = os.getenv("EXECUTIVE_SESSION_TOKEN")

    if not expected_token or provided_token != expected_token:
        logging.error("UNAUTHORIZED: Executive actions require Governing Officer Tarwater's valid token.")
        sys.exit(1)


def engage_kill_switch(halt: bool = True) -> None:
    """Article III.2: Immediately halts or resumes all autonomous agent operations."""
    verify_authority()
    policy = load_policy()
    policy["communication_and_oversight"]["emergency_override"]["global_kill_switch"] = halt
    save_policy(policy)

    state = "ENGAGED (SYSTEM HALTED)" if halt else "DISENGAGED (SYSTEM ACTIVE)"
    record_executive_action("EMERGENCY_KILL_SWITCH", f"Global kill switch set to {halt} - {state}")
    print(f"[TARWATER OVERRIDE] Global kill switch is now {state}.")


def rollback_repository(commit_hash: str) -> None:
    """Article III.2: Rolls back the repository state to a verified commit hash."""
    verify_authority()
    policy = load_policy()
    if not policy["communication_and_oversight"]["emergency_override"].get("allow_instant_rollback"):
        logging.error("Rollback is disabled in governance_config.yaml.")
        sys.exit(1)

    logging.warning(f"Initiating executive rollback to commit: {commit_hash}")
    subprocess.run(["git", "reset", "--hard", commit_hash], check=True)
    record_executive_action("EXECUTIVE_ROLLBACK", f"Repository hard-reset to commit {commit_hash}")
    print(f"[TARWATER OVERRIDE] Repository rolled back to {commit_hash}.")


def amend_threshold(section: str, key: str, new_value) -> None:
    """Article IV.2: Direct constitutional threshold amendment by Governing Officer Tarwater."""
    verify_authority()
    policy = load_policy()

    if section not in policy["architectural_safeguards"]:
        logging.error(f"Invalid safeguard section: {section}")
        sys.exit(1)

    old_value = policy["architectural_safeguards"][section].get(key)
    policy["architectural_safeguards"][section][key] = new_value
    save_policy(policy)

    record_executive_action(
        "CONSTITUTIONAL_AMENDMENT",
        f"Updated architectural_safeguards.{section}.{key}: {old_value} -> {new_value}"
    )
    print(f"[TARWATER AMENDMENT] {section}.{key} updated from {old_value} to {new_value}.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python override_control.py halt")
        print("  python override_control.py resume")
        print("  python override_control.py rollback <commit_hash>")
        print("  python override_control.py amend <section> <key> <value>")
        sys.exit(1)

    command = sys.argv[1].lower()
    if command == "halt":
        engage_kill_switch(True)
    elif command == "resume":
        engage_kill_switch(False)
    elif command == "rollback" and len(sys.argv) == 3:
        rollback_repository(sys.argv[2])
    elif command == "amend" and len(sys.argv) == 5:
        raw_val = sys.argv[4]
        try:
            parsed_val = json.loads(raw_val)
        except json.JSONDecodeError:
            parsed_val = raw_val
        amend_threshold(sys.argv[2], sys.argv[3], parsed_val)
    else:
        print("Invalid command or arguments.")
        sys.exit(1)
