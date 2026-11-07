"""
Executive Audit & Status Dashboard
Provides Governing Officer Tarwater with a real-time system overview.
Governing Authority: Governing Officer Tarwater
"""

import os
import json
import yaml
from pathlib import Path

CONFIG_PATH = "governance_config.yaml"
REGISTRY_PATH = "sub_repositories.json"
AUDIT_LOG_PATH = "executive_audit.log"


def print_banner():
    print("=" * 65)
    print(" 🛡️  AUTONOMOUS SYSTEM GOVERNANCE & CONTROL DASHBOARD")
    print(" Governing Authority: Governing Officer Tarwater")
    print("=" * 65)


def show_system_status():
    print_banner()

    # 1. Load Policy
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            policy = yaml.safe_load(f)
        
        meta = policy.get("system_metadata", {})
        safeguards = policy.get("architectural_safeguards", {})
        override = policy.get("communication_and_oversight", {}).get("emergency_override", {})

        print(f"\n[SYSTEM METADATA]")
        print(f"  • Repository: {meta.get('repository_name')}")
        print(f"  • Version:    {meta.get('version')}")
        print(f"  • Executive:  {meta.get('executive_agent')}")

        print(f"\n[QUALITY BASELINE & SAFEGUARDS]")
        quality = safeguards.get("quality_baseline", {})
        scaling = safeguards.get("modular_scaling", {})
        print(f"  • Min Test Coverage Required: {quality.get('min_test_coverage_percent')}%")
        print(f"  • Max Cyclomatic Complexity:  {quality.get('max_cyclomatic_complexity')}")
        print(f"  • Modular Isolation Threshold: {scaling.get('complexity_threshold_for_isolation')}")

        print(f"\n[EMERGENCY OVERRIDE STATUS]")
        kill_switch = override.get("global_kill_switch", False)
        status_str = "🔴 ENGAGED (SYSTEM HALTED)" if kill_switch else "🟢 DISENGAGED (SYSTEM ACTIVE)"
        print(f"  • Global Kill Switch: {status_str}")
    else:
        print("\n[!] Warning: governance_config.yaml not found.")

    # 2. Load Sub-Repository Registry
    print(f"\n[SPAWNED SUB-REPOSITORIES]")
    if os.path.exists(REGISTRY_PATH):
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            registry = json.load(f)
        sub_repos = registry.get("sub_repositories", [])
        if sub_repos:
            for repo in sub_repos:
                print(f"  • {repo['repository']} (Source: {repo['source_module']}, CC: {repo['trigger_complexity']})")
                print(f"    URL: {repo['url']}")
        else:
            print("  • No sub-repositories spawned yet (all modules within complexity limits).")
    else:
        print("  • Registry initialized (no sub-repos yet).")

    # 3. Recent Executive Audit Log Entries
    print(f"\n[RECENT EXECUTIVE AUDIT LOGS]")
    if os.path.exists(AUDIT_LOG_PATH):
        with open(AUDIT_LOG_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
            recent = lines[-5:] # Last 5 entries
            for line in recent:
                try:
                    entry = json.loads(line.strip())
                    print(f"  [{entry['timestamp']}] {entry['action']}: {entry['detail']}")
                except Exception:
                    pass
    else:
        print("  • No executive override actions recorded.")

    print("\n" + "=" * 65)


if __name__ == "__main__":
    show_system_status()
