#!/usr/bin/env python3
"""PreToolUse hook: block Write/Edit to config.yml during skill execution.

Makes config immutability structural, not instruction-based. No prompt injection
can modify config.yml through Claude Code tool calls when this hook is active.

Install: copy to ~/.claude/hooks/ and add to settings.json (see install-hooks.sh).
"""
import json
import os
import sys


PROTECTED_PATTERNS = [
    os.path.expanduser("~/.claude/skills/buy/config.yml"),
]


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

    # Only intercept Write and Edit tools
    if tool_name not in ("Write", "Edit"):
        sys.exit(0)

    file_path = data.get("tool_input", {}).get("file_path", "")
    if not file_path:
        sys.exit(0)

    # Normalize path
    file_path = os.path.realpath(os.path.expanduser(file_path))

    for protected in PROTECTED_PATTERNS:
        protected = os.path.realpath(os.path.expanduser(protected))
        if file_path == protected:
            deny(
                f"BLOCKED: Cannot modify protected config file '{file_path}'. "
                "Config changes require manual editing outside Claude Code."
            )

    # Not a protected file — allow
    sys.exit(0)


if __name__ == "__main__":
    main()
