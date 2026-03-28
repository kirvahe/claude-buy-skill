#!/usr/bin/env python3
"""PreToolUse hook: block Write/Edit to audit-log.md during skill execution.

The audit log must be append-only. This hook blocks Write and Edit tool calls
targeting audit-log.md. Appends via Bash (echo >>) are still allowed since
Bash uses a different tool name.

Install: copy to ~/.claude/hooks/ and add to settings.json (see install-hooks.sh).
"""
import json
import os
import sys


def deny(reason: str) -> None:
    result = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }
    print(json.dumps(result))
    sys.exit(0)


def main() -> None:
    data = json.load(sys.stdin)
    tool_name = data.get("tool_name", "")

    if tool_name not in ("Write", "Edit"):
        sys.exit(0)

    file_path = data.get("tool_input", {}).get("file_path", "")
    if not file_path:
        sys.exit(0)

    basename = os.path.basename(file_path)
    if basename == "audit-log.md":
        deny(
            f"BLOCKED: Cannot overwrite audit log '{file_path}'. "
            "Audit log is append-only. Use Bash with 'echo >>' to append entries."
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
