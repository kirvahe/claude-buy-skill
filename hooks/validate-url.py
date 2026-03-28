#!/usr/bin/env python3
"""PreToolUse hook: validate browser_navigate URLs against the /buy skill whitelist.

Deterministic URL validation immune to prompt injection. Checks:
- HTTPS-only scheme
- No userinfo (user:pass@host)
- No non-standard ports
- No non-ASCII/IDN hostnames
- Hostname must match whitelist (exact or www. subdomain)
- URL path must not match banned patterns

Install: copy to ~/.claude/hooks/ and add to settings.json (see install-hooks.sh).
Test: echo '{"tool_input":{"url":"https://www.amazon.es/dp/X"}}' | python3 validate-url.py
"""
import json
import sys
import os
import re
from typing import Optional
from urllib.parse import urlparse

# --- Service domains (always allowed, exact match only) ---
SERVICE_DOMAINS = {
    "camelcamelcamel.com",
    "www.camelcamelcamel.com",
    "idealo.es",
    "www.idealo.es",
    "nytimes.com",
    "www.nytimes.com",
    "seriouseats.com",
    "www.seriouseats.com",
    "reddit.com",
    "www.reddit.com",
    "lens.google.com",
    "www.google.com",
}

# --- Default store domains (ES preset) ---
DEFAULT_STORE_DOMAINS = {
    "amazon.es",
    "decantalo.com",
    "zara.com",
    "elcorteingles.es",
    "temu.com",
    "mediamarkt.es",
    "uniqlo.com",
    "leroymerlin.es",
    "ikea.com",
}

# --- Always-banned URL path patterns (all modes) ---
ALWAYS_BANNED_PATHS = [
    "/account/settings",
    "/account/security",
    "/password",
    "/wallet",
    "/saved-cards",
    "/payment-methods",
    "/manage-subscription",
    "/gp/css/",
    "/ap/signin",
    "/address",
    "/gift-card",
    "/returns",
    "/gp/r.html",
]

# --- Checkout paths (banned in RESEARCH and CART modes) ---
CHECKOUT_BANNED_PATHS = [
    "/checkout",
    "/payment",
    "/pay/",
    "/billing",
    "/gp/buy/",
    "/cart/proceed",
    "/order/confirm",
    "/place-order",
    "/cesta/",
    "/tramitar",
    "/compra/",
    "/finalizar",
    "/pedido/",
    "/orden/",
    "/pago/",
    "/resumen-pedido/",
    "/m/checkout/",
    "/carrito/tramitar/",
]


def deny(reason: str) -> None:
    """Output deny decision and exit. Uses hookSpecificOutput wrapper (required)."""
    result = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }
    print(json.dumps(result))
    sys.exit(0)


def allow() -> None:
    """Output allow decision and exit."""
    result = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
        }
    }
    print(json.dumps(result))
    sys.exit(0)


def load_config_domains() -> set:
    """Load store domains from config.yml if available."""
    config_path = os.path.expanduser("~/.claude/skills/buy/config.yml")
    if not os.path.exists(config_path):
        return set()

    domains = set()
    try:
        with open(config_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("domain:"):
                    domain = line.split(":", 1)[1].strip().strip("'\"")
                    if domain:
                        domains.add(domain)
    except (IOError, OSError):
        pass
    return domains


def load_security_mode() -> str:
    """Read security_mode from config.yml. Defaults to RESEARCH (safest)."""
    config_path = os.path.expanduser("~/.claude/skills/buy/config.yml")
    if not os.path.exists(config_path):
        return "research"

    try:
        with open(config_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("security_mode:"):
                    return line.split(":", 1)[1].strip().strip("'\"").lower()
    except (IOError, OSError):
        pass
    return "research"


def hostname_matches_whitelist(hostname: str, whitelist: set[str]) -> bool:
    """Check if hostname exactly matches or is a subdomain of a whitelisted domain."""
    if hostname in whitelist:
        return True
    for allowed in whitelist:
        if hostname.endswith("." + allowed):
            return True
    return False


def path_matches_banned(url_path: str, patterns: list) -> Optional[str]:
    """Check if URL path contains any banned pattern. Returns matched pattern or None."""
    path_lower = url_path.lower()
    for pattern in patterns:
        if pattern.lower() in path_lower:
            return pattern
    return None


def main() -> None:
    data = json.load(sys.stdin)
    url = data.get("tool_input", {}).get("url", "")

    if not url:
        deny("BLOCKED: browser_navigate called with empty URL")

    # --- Parse URL ---
    parsed = urlparse(url)

    # --- Scheme validation ---
    if parsed.scheme.lower() != "https":
        deny(f"BLOCKED: Only https:// is allowed. Got: {parsed.scheme}:// in {url}")

    # --- Userinfo check ---
    if parsed.username or parsed.password or "@" in (parsed.netloc.split(":")[0] if ":" in parsed.netloc else parsed.netloc):
        if "@" in parsed.netloc:
            deny(f"BLOCKED: URL contains userinfo component: {url}")

    # --- Extract hostname ---
    hostname = (parsed.hostname or "").lower()
    if not hostname:
        deny(f"BLOCKED: Could not extract hostname from URL: {url}")

    # --- Non-ASCII / IDN check ---
    try:
        hostname.encode("ascii")
    except UnicodeEncodeError:
        deny(f"BLOCKED: Non-ASCII (IDN) hostname: {hostname}")

    # --- Port check ---
    if parsed.port is not None and parsed.port != 443:
        deny(f"BLOCKED: Non-standard port {parsed.port} in URL: {url}")

    # --- Build whitelist ---
    store_domains = DEFAULT_STORE_DOMAINS | load_config_domains()
    all_domains = SERVICE_DOMAINS | store_domains

    # --- Hostname whitelist check ---
    # Service domains: exact match only
    service_match = hostname in SERVICE_DOMAINS
    # Store domains: exact match or subdomain
    store_match = hostname_matches_whitelist(hostname, store_domains)

    if not service_match and not store_match:
        deny(
            f"BLOCKED: Domain '{hostname}' is not in the allowed list. "
            f"Whitelisted: {', '.join(sorted(all_domains))}"
        )

    # --- Banned path check (always banned) ---
    url_path = parsed.path or "/"
    matched = path_matches_banned(url_path, ALWAYS_BANNED_PATHS)
    if matched:
        deny(f"BLOCKED: Banned path pattern '{matched}' in URL: {url}")

    # --- Conditionally banned paths (checkout, non-FULL modes) ---
    security_mode = load_security_mode()
    if security_mode != "full":
        matched = path_matches_banned(url_path, CHECKOUT_BANNED_PATHS)
        if matched:
            deny(
                f"BLOCKED: Checkout path '{matched}' is not allowed in "
                f"{security_mode.upper()} mode. URL: {url}"
            )

    # --- All checks passed ---
    allow()


if __name__ == "__main__":
    main()
