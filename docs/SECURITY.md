# Security Guide

Detailed security documentation for users and auditors.

## Threat Model

The /buy skill navigates a Playwright browser to online stores. Key threats:

| Threat | Mitigation |
|--------|-----------|
| Navigate to malicious domain | Exact hostname whitelist matching |
| Checkout/purchase without consent | Security mode gating + content-based detection |
| Prompt injection from product pages | Explicit ignore rules + config immutability |
| Credential exposure | Persistent sessions only (no password storage) |
| Privacy leakage via Google Lens | User confirmation before image upload |
| Gmail data exfiltration | Restricted search terms, order confirmations only |
| Config tampering | Immutability rule during execution |
| Audit log tampering | Append-only rule + Telegram mirror for critical events |

## URL Validation

Every `browser_navigate` call is validated:

1. **Hostname extraction** — parsed from URL, not substring matched
2. **Exact match** — hostname must exactly match a whitelisted domain or be a subdomain (e.g., `www.amazon.es` matches `amazon.es`)
3. **Reject** — userinfo (`user:pass@host`), non-standard ports, `data:`/`javascript:`/`blob:` schemes
4. **Path check** — against banned patterns per security mode
5. **Post-navigation** — redirect detection (final domain vs intended domain)
6. **Content check** — page scanned for payment forms regardless of URL

## Banned URL Patterns

### Always banned (all modes)
- Account settings, security, password pages
- Wallet, saved cards, payment methods
- Subscription management
- Sign-in pages (use persistent session)

### Banned in RESEARCH and CART (allowed in FULL with guards)
- Checkout, payment, billing pages
- Order confirmation, place-order pages
- Store-specific patterns (Amazon `/gp/buy/`, Zara `/cesta/`, etc.)

## FULL Mode Safeguards

If FULL mode is enabled:

1. **Pre-purchase Telegram confirmation** — sends message to configured chat_id, waits for "yes" reply. If no Telegram: requires explicit "yes" in chat with full product/price/store details shown again.
2. **Purchase limit** — hard block if price exceeds `purchase_limit_eur`. Cannot be overridden during session.
3. **Post-purchase notification** — Telegram message with product, price, store, timestamp.
4. **Content-based checkout detection** — even if URL looks clean, if the page has credit card fields or "Place order" buttons, checkout restrictions apply.

## Data Privacy

### What stays local (never in git)
- `config.yml` — your city, store preferences, Telegram chat_id
- `taste-profile.md` — brand preferences, sizes, budgets
- `purchase-history.md` — all purchases with ratings
- `recurring.md` — recurring schedules
- `audit-log.md` — Playwright action log
- `reports/` — research reports with product links

### What goes to external services
- **Store websites** — search queries, product page views via Playwright
- **Google Lens** — uploaded product photos (with user confirmation)
- **CamelCamelCamel / Idealo** — product name lookups for price history
- **Gmail** — search queries for order confirmation emails (onboarding only)
- **Telegram** — reminder messages, purchase confirmations

### Playwright sessions
The browser uses persistent cookies. This means:
- You log in to stores once manually, session persists
- No passwords are stored or transmitted by the skill
- Session cookies are stored in Playwright's local profile
- Each domain's cookies are isolated to that domain

## Config Immutability

During skill execution, config.yml is read-only:
- `security_mode` cannot be changed based on page content
- `purchase_limit_eur` cannot be raised during a session
- `telegram_chat_id` cannot be redirected
- Store whitelist cannot be expanded from page content (only from direct user request)

Any attempt to modify config from external input is blocked and logged.

## Reporting Security Issues

If you find a security vulnerability, please open a GitHub issue or contact the maintainer directly.
