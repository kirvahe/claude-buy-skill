# /buy — Shopping Research & Cart Assistant

Search, compare, and buy products across online stores from [Claude Code](https://claude.ai/code). Handles product name, photo, or description. Compares prices with historical data. Adds to cart via browser automation. Never touches checkout without explicit confirmation.

## Features

- Three entry modes: product name, photo (Google Lens), or natural language description
- Price analysis with CamelCamelCamel and Idealo, per-unit pricing, Subscribe & Save detection
- Expert research via Wirecutter, Serious Eats, Reddit synthesis, Parker scores for wine
- Smart store routing by product category
- Recurring purchase detection with Telegram reminders
- Three security modes: RESEARCH (links only), CART (add to cart), FULL (checkout with guards)
- Country presets: Spain fully built, extensible for other countries
- Config-driven, no personal data in skill code

## Requirements

- [Claude Code](https://claude.ai/code) CLI or desktop app
- **Playwright MCP** (required) — browser automation
- **Firecrawl MCP** (recommended) — web scraping fallback
- **Exa MCP** (recommended) — semantic search for expert research
- **Telegram MCP** (optional) — recurring reminders, FULL mode confirmation

> Gmail import was removed to reduce security surface. To import purchase history, add entries to purchase-history.md manually.

## Install

```bash
git clone https://github.com/kirvahe/claude-buy-skill.git ~/.claude/skills/buy
```

## Setup

Run `/buy` for the first time and follow the onboarding prompts (security mode, location, stores, preferences). Config is saved to `config.yml` (gitignored, stays local).

### Security Hooks (recommended)

Install deterministic security hooks that enforce URL whitelist, config immutability, and audit log protection at the Claude Code level — immune to prompt injection:

```bash
bash ~/.claude/skills/buy/hooks/install-hooks.sh
```

Then add the displayed JSON to your `~/.claude/settings.json`. See `hooks/install-hooks.sh` for details.

## Usage

```
/buy Roborock Q7 Max+              # exact product -> find best price
/buy best robot vacuum under 300   # category -> expert research + comparison
/buy [drag photo here]             # photo -> Google Lens -> find product
/buy nice jacket for spring        # description -> clarifying questions -> options
/buy same dishwasher tablets       # repeat -> check history, suggest recurring
```

## Security Modes

Three modes control what Playwright is allowed to do. Set during onboarding, enforced by `references/security-rules.md`.

- **RESEARCH** — search and scrape only, returns links
- **CART** — can add items to cart, no checkout
- **FULL** — can complete checkout with guards (Telegram confirmation, per-transaction limit)

Account settings, password pages, and payment method management are always banned. See `references/security-rules.md` for the full policy.

## Contributing

**Add a country preset:** copy the ES section in `references/store-routing.md` as a template, add stores with search URLs, category mapping, and Playwright interaction patterns.

**Improve existing stores:** store search URLs and Playwright patterns break when stores update UI. The skill uses `browser_snapshot` (accessibility tree) for resilience, but contributions to keep patterns current are welcome.

## License

MIT
