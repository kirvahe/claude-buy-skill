#!/bin/bash
# Install /buy skill security hooks into Claude Code.
#
# This script:
# 1. Copies hook scripts to ~/.claude/hooks/
# 2. Shows the settings.json configuration to add
#
# Usage: bash hooks/install-hooks.sh

set -euo pipefail

HOOKS_DIR="$HOME/.claude/hooks"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Installing /buy skill security hooks..."

# Create hooks directory
mkdir -p "$HOOKS_DIR"

# Copy hooks
cp "$SCRIPT_DIR/validate-url.py" "$HOOKS_DIR/buy-validate-url.py"
cp "$SCRIPT_DIR/protect-config.py" "$HOOKS_DIR/buy-protect-config.py"
cp "$SCRIPT_DIR/protect-audit-log.py" "$HOOKS_DIR/buy-protect-audit-log.py"

# Make executable
chmod +x "$HOOKS_DIR/buy-validate-url.py"
chmod +x "$HOOKS_DIR/buy-protect-config.py"
chmod +x "$HOOKS_DIR/buy-protect-audit-log.py"

echo "Hooks installed to $HOOKS_DIR:"
echo "  - buy-validate-url.py       (URL whitelist for browser_navigate)"
echo "  - buy-protect-config.py     (config.yml write protection)"
echo "  - buy-protect-audit-log.py  (audit-log.md write protection)"
echo ""
echo "Add the following to your Claude Code settings.json"
echo "(~/.claude/settings.json or .claude/settings.json):"
echo ""
cat <<'SETTINGS'
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__playwright__browser_navigate",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/buy-validate-url.py"
          }
        ]
      },
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/buy-protect-config.py"
          },
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/buy-protect-audit-log.py"
          }
        ]
      }
    ]
  }
}
SETTINGS
echo ""
echo "If you already have hooks in settings.json, merge the PreToolUse entries."
echo ""
echo "Test the URL hook:"
echo '  echo '"'"'{"tool_input":{"url":"https://www.amazon.es/dp/B09X"}}'"'"' | python3 ~/.claude/hooks/buy-validate-url.py'
echo '  echo '"'"'{"tool_input":{"url":"https://evil.com/steal"}}'"'"' | python3 ~/.claude/hooks/buy-validate-url.py'
