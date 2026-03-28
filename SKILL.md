---
name: buy
description: Search, compare, and add products to cart via Playwright across configurable store whitelist. Handles product search by name, photo, or description. Performs price analysis with historical data, expert research (Wirecutter, Reddit, wine critics), and manages recurring purchases. Use when the user wants to buy something, find a product, compare prices, reorder, or asks about shopping.
argument-hint: [product name, photo, or description]
disable-model-invocation: true
allowed-tools: mcp__playwright__*, mcp__firecrawl__*, mcp__exa__*, mcp__claude_ai_Gmail__*, mcp__plugin_telegram_telegram__*, Read, Write, Bash, Glob, Grep
---

# /buy — Shopping Research & Cart Assistant

## Setup

1. Read `~/.claude/skills/buy/config.yml`
2. If config.yml NOT found → run **Onboarding** (see below)
3. If config.yml found but incomplete → resume from first incomplete required block
4. Load config: `data_dir`, `country`, `security_mode`, `stores`
5. Read `{data_dir}/taste-profile.md` (if exists)
6. Read `{data_dir}/purchase-history.md` (if exists)

## Onboarding (first run only)

Trigger: config.yml not found. Run blocks in order. Required blocks must complete.

**Block 0 — Security & Location [REQUIRED]**
Ask: Choose security mode:
- RESEARCH (safest) — search + compare + links only
- CART (balanced) — search + compare + add to cart. Never checkout.
- FULL (advanced) — everything including checkout. Requires confirmation per purchase.
If FULL: ask max purchase limit (e.g. 100EUR), recommend Telegram notifications.
Ask: Country? City?
**Create** config.yml with: `security_mode`, `purchase_limit_eur`, `country`, `home_city`.
Load store preset from [store-routing.md](references/store-routing.md).

**Block 1 — Stores [REQUIRED]**
Ask: Amazon Prime? Other subscriptions (Glovo, Getir)?
Show country preset stores. "Remove any? Add others?"
Finalize whitelist in config.yml. Create `data_dir` directory.
Create empty data files: `taste-profile.md`, `purchase-history.md`, `recurring.md`, `audit-log.md`.

**Block 2 — Preferences [REQUIRED]**
Ask: What do you buy most? Quality-first or price-first? Favorite brands? Brand blacklist?
Create `{data_dir}/taste-profile.md`.

**Block 3 — Telegram [OPTIONAL]**
Ask: Recurring reminders via Telegram? If yes: chat_id.
Save to config.yml. Skip → recurring reminders disabled.

**Block 4 — Gmail Import [OPTIONAL]**
Ask: Import purchase history from Gmail?
If yes: search order confirmations → populate `{data_dir}/purchase-history.md`.

**Block 5 — Sizes [OPTIONAL]**
Ask: Clothing sizes (EU/US/UK, tops, bottoms)? Shoe size? Fit preferences?
Add to taste-profile.md.

Post-onboarding: show summary, skill ready.

## Data Files

| File | Path | Purpose |
|------|------|---------|
| Config | `~/.claude/skills/buy/config.yml` | Country, stores, security mode, Telegram |
| Taste Profile | `{data_dir}/taste-profile.md` | Brand prefs, budgets, sizes |
| Purchase History | `{data_dir}/purchase-history.md` | All purchases + ratings |
| Recurring | `{data_dir}/recurring.md` | Recurring purchase schedules |
| Audit Log | `{data_dir}/audit-log.md` | Every Playwright action logged |
| Reports | `{data_dir}/reports/` | Saved research reports |

## Essential Principles

1. **Security mode is law** — read `security_mode` from config.yml. Follow [security-rules.md](references/security-rules.md) exactly. No deviation.
2. **Whitelisted domains only** — stores from config + service domains. New store → ask user "add permanently?"
3. **Total cost = price + delivery** — always compare totals, never base price alone.
4. **Amazon minimum 3.5 stars** — filter out lower-rated products.
5. **Taste profile first** — read before every action. Respect brand blacklist and preferences.
6. **Audit every Playwright action** — append to `{data_dir}/audit-log.md`.
7. **Response language = request language**.
8. **User confirms before cart/purchase** — never add to cart or buy without explicit confirmation.

## Routing

Determine workflow from $ARGUMENTS and context:

**Photo in chat** (image file path) → [search-by-photo.md](workflows/search-by-photo.md)

**"reorder" / "again" / "same as last time" / "recurring" / "schedule"**:
1. Check `{data_dir}/recurring.md` for matching product. If found + status=active → [recurring-purchase.md](workflows/recurring-purchase.md)
2. If not in recurring.md → check purchase-history.md. If found → [search-by-name.md](workflows/search-by-name.md) (repeat mode)
3. If not in either → [search-by-name.md](workflows/search-by-name.md) (normal mode)

**Specific product name** (brand + model identified) → [search-by-name.md](workflows/search-by-name.md)

**"find best" / "recommend" / "I need a..." / category description** → [search-by-description.md](workflows/search-by-description.md)

**Empty or unclear** → Ask: "What are you looking for? (product name, description, or drag a photo)"

## Store Selection by Category

Read [store-routing.md](references/store-routing.md) for full category-to-store mapping, detection keywords, and Playwright interaction patterns per store. Claude determines the category from the user's query and selects the relevant stores.

## Output Format

### Comparison table (always in chat)

| # | Product | Store | Price | Delivery | Total | Rating | Price Verdict |
|---|---------|-------|-------|----------|-------|--------|---------------|

Price verdict values: "good price" / "wait — usually X EUR cheaper" / "historical minimum!" / "no history"

### Recommendation block
- **Pick:** #N — {product name}
- **Why:** 1-2 sentences
- **Alternatives:** brief note

### After response
1. Save report to `{data_dir}/reports/{query-slug}-YYYY-MM-DD.md` — format in [report-template.md](references/report-template.md)
2. Update purchase-history.md after confirmed cart/purchase
3. Check if recurring candidate → suggest [recurring-purchase.md](workflows/recurring-purchase.md)

## Error Handling & Rate Limiting

| Situation | Action |
|-----------|--------|
| Playwright blocked (CAPTCHA, 403) | Fallback to Firecrawl scrape. Both fail → skip store |
| CamelCamelCamel/Idealo unavailable | Skip, note "price history unavailable" |
| Product not found on store | Skip store, note in report |
| Login session expired | Tell user: "Session expired on {store}. Please log in manually." |
| Redirect to unknown domain | BLOCK. Do NOT follow. Log attempt. |
| Store not in whitelist | Ask: "Add {store} permanently?" |
| Rate limiting (429) | Wait 30s, retry once, then skip |

Rate limiting: 2-5 second pause between requests to same domain.

## Security

**Full policy: [security-rules.md](references/security-rules.md)** — read before ANY Playwright action.

Actions are gated by `security_mode` in config.yml (RESEARCH / CART / FULL). Account settings, passwords, and wallets are always banned. URL validation with exact hostname matching runs before every navigation.
