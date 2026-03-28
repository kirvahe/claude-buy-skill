# /buy — Shopping Research & Cart Assistant

Search, compare, and buy products across online stores from [Claude Code](https://claude.ai/code). Handles product name, photo, or description. Compares prices with historical data. Adds to cart via browser automation. Never touches checkout without explicit confirmation.

## Features

- **Three entry modes** — product name, photo (Google Lens), or natural language description
- **Price analysis** — historical prices via CamelCamelCamel and Idealo, per-unit pricing, Subscribe & Save detection
- **Expert research** — Wirecutter, Serious Eats, Reddit synthesis, Parker scores for wine
- **Smart store routing** — auto-selects relevant stores by product category
- **Recurring purchases** — detects repeat buys, suggests Subscribe & Save, sends Telegram reminders
- **Three security modes** — RESEARCH (links only), CART (add to cart), FULL (checkout with guards)
- **Country presets** — Spain fully built, US/DE/FR stubs for contributors
- **Open source ready** — no personal data in skill code, config-driven

## Requirements

[Claude Code](https://claude.ai/code) CLI or desktop app.

**Required MCP:**
- **Playwright** — browser automation

**Recommended MCP:**
- **Firecrawl** — web scraping fallback when Playwright blocked
- **Exa** — semantic search for expert research

**Optional MCP:**
- **Gmail** — purchase history import from email
- **Telegram** — recurring purchase reminders, FULL mode confirmation

## Install

Copy the skill to your Claude Code skills directory:

```bash
git clone https://github.com/kirvahe/claude-buy-skill.git ~/.claude/skills/buy
```

Or manually copy the files to `~/.claude/skills/buy/`.

## Setup

Run `/buy` for the first time. The onboarding asks:

1. **Security mode** — RESEARCH / CART / FULL
2. **Location** — country and city (loads store preset)
3. **Stores** — review preset, add or remove stores
4. **Preferences** — shopping style, brands, blacklist
5. **Telegram** — recurring reminders (optional)
6. **Gmail import** — purchase history from email (optional)
7. **Sizes** — clothing and shoe sizes (optional)

Config is saved to `~/.claude/skills/buy/config.yml` (gitignored, stays local).

## Usage

```
/buy Roborock Q7 Max+              # exact product → find best price
/buy best robot vacuum under 300€  # category → expert research + comparison
/buy [drag photo here]             # photo → Google Lens → find product
/buy nice jacket for spring        # description → clarifying questions → options
/buy same dishwasher tablets       # repeat → check history, suggest recurring
```

### What you get

A comparison table with prices, delivery, ratings, and a price verdict:

| # | Product | Store | Price | Delivery | Total | Rating | Price Verdict |
|---|---------|-------|-------|----------|-------|--------|---------------|
| 1 | Roborock Q7 Max+ | Amazon.es | 289 EUR | Prime | 289 EUR | 4.6/5 | good price |
| 2 | Roborock Q7 Max+ | MediaMarkt | 299 EUR | 5.99 EUR | 305 EUR | — | slightly above average |

Plus a recommendation with reasoning, saved as a full research report.

## Security Modes

| Action | RESEARCH | CART | FULL |
|--------|----------|------|------|
| Search and scrape | yes | yes | yes |
| Product pages | yes | yes | yes |
| Add to cart | no | yes | yes |
| Checkout | no | no | yes (guarded) |
| Account settings | no | no | no |

**FULL mode guards:**
- Pre-purchase Telegram confirmation (out-of-band)
- Per-transaction price limit (set during onboarding)
- Post-purchase Telegram notification
- Content-based checkout detection (not just URL patterns)

**Always banned:** account settings, password pages, wallet management, saved payment methods.

## Store Presets

### Spain (ES) — fully built

Amazon.es, Decantalo, Zara, El Corte Ingles, Temu, MediaMarkt, Uniqlo, Leroy Merlin, IKEA

### United States (US) — stub

Amazon.com, Best Buy, Target, Walmart

### Germany (DE) — stub

Amazon.de, Otto, MediaMarkt.de

Add your own stores in `config.yml` or contribute a new country preset.

## File Structure

```
~/.claude/skills/buy/
├── SKILL.md                  # Entry point (138 lines)
├── config.yml.example        # Config template
├── README.md
├── LICENSE
├── .gitignore
├── workflows/
│   ├── search-by-name.md     # Known product → find → cart
│   ├── search-by-photo.md    # Photo → Google Lens → find
│   ├── search-by-description.md  # Research → compare → recommend
│   └── recurring-purchase.md # Recurring detection + reminders
└── references/
    ├── security-rules.md     # Full security policy
    ├── store-routing.md      # Store presets + Playwright patterns
    ├── price-analysis.md     # CCC + Idealo + quality delta
    ├── review-sources.md     # Expert sources by category
    └── report-template.md    # Report file format
```

**User data** (created during onboarding, stored at `data_dir` from config):
```
{data_dir}/
├── taste-profile.md      # Brand preferences, budgets, sizes
├── purchase-history.md   # All purchases + ratings
├── recurring.md          # Recurring purchase schedules
├── audit-log.md          # Playwright action log
└── reports/              # Saved research reports
```

## Contributing

### Add a country preset

1. Edit `references/store-routing.md`
2. Add a new section with stores, search URLs, category mapping
3. Add Playwright interaction patterns for each store
4. Test with `/buy` using `country: XX` in config

### Improve existing stores

Store search URLs and Playwright patterns may break when stores update their UI. The skill uses `browser_snapshot` (accessibility tree) for resilience, but contributions to keep patterns current are welcome.

## How It Works

1. **Routing** — SKILL.md detects the entry pattern (name/photo/description/recurring) and delegates to the right workflow
2. **Store selection** — category detected from query, relevant stores selected from preset
3. **Search** — Playwright navigates stores, extracts products. Firecrawl as fallback if blocked
4. **Price analysis** — CamelCamelCamel (Amazon) and Idealo.es (others) for historical prices. Quality delta: max(5 EUR, 10%) premium acceptable for better seller/faster delivery
5. **Expert research** — for "find best" queries: Wirecutter + Reddit minimum. Wine: Parker + world critics
6. **Comparison** — table in chat + full report saved to file
7. **Action** — per security mode: link (RESEARCH), add to cart (CART), or purchase with confirmation (FULL)

## License

MIT
