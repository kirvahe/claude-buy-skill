# Workflow: Search by Product Name

## Step 1: Parse the Request

From $ARGUMENTS determine:
- **Product name** (exact or approximate)
- **Category** (for store selection — see [store-routing.md](../references/store-routing.md))
- **Is this a repeat purchase?** Check purchase-history.md for same or similar product.

If repeat purchase:
- Use exact product link from history if available
- Compare current price vs last purchase price
- If price spiked > 20% → warn user before proceeding

## Step 2: Determine Store Set

Use category-to-store mapping from [store-routing.md](../references/store-routing.md).
Read [store-routing.md](../references/store-routing.md) for store-specific search patterns and URLs.
If category ambiguous → search broader store set.

## Step 3: Ask Urgency

Ask user: "When do you need this?"
- **Tomorrow** → prioritize Prime/next-day, Click & Collect (El Corte Ingles). Deprioritize Temu.
- **This week** → filter 1-5 day delivery. Deprioritize Temu (7-15 days).
- **Not urgent** → include all options, highlight cheapest slow-delivery alongside fast options.

If user already specified urgency in their request → skip this question.
If `amazon_membership` in config.yml is `prime` → prefer Prime-eligible products for "tomorrow"/"this week".

## Step 4: Search Stores

For each store in the set:

1. Validate URL per security-rules.md
2. `browser_navigate` to store search URL (substitute query)
3. `browser_snapshot` to read results
4. Extract per product: name, price, delivery cost/time, rating, seller info, product URL
5. Wait 2-5 seconds before next store (rate limiting)

**If Playwright blocked** (CAPTCHA, 403):
- Fallback: use `mcp__firecrawl__firecrawl_scrape` on the search URL
- If Firecrawl also fails → skip store, note "could not access {store}" in report

**If product not found** → skip store, note in report.

**If zero products found across all stores:**
Tell user: "Could not find {product} on any available store. All {N} stores returned errors or no results. Try a different product name or check back later."
Save report with empty table and failure notes to `{data_dir}/reports/`. EXIT workflow — do not proceed to Steps 5-8.

## Step 5: Price Analysis

Read [price-analysis.md](../references/price-analysis.md). For each found product:

1. **Historical price**: CamelCamelCamel for Amazon products, Idealo.es for others
2. **Total cost** = price + delivery fee
3. **Per-unit price** if product has size/quantity variants
4. **Subscribe & Save** check (Amazon only) — note discount if available
5. **Quality delta**: max(5 EUR, price * 0.10) — acceptable premium for better seller/Prime/faster delivery
6. **Amazon seller filtering**: prefer higher-rated sellers within quality delta, exclude products < 3.5 stars
7. **Price verdict**: "good price" / "wait" / "historical minimum!" / "no history"

## Step 6: Build Comparison & Recommend

Build comparison table per SKILL.md output format:

| # | Product | Store | Price | Delivery | Total | Rating | Seller | Price Verdict |
|---|---------|-------|-------|----------|-------|--------|--------|---------------|

Recommend #1 with reasoning:
- **Pick:** #N — {product}
- **Why:** 1-2 sentences (value, rating, expert endorsement, delivery speed)
- **Alternatives:** brief note on why #2/#3 were considered but not top

## Step 7: User Confirms → Execute Action

Wait for user to confirm choice (number or product name).

**RESEARCH mode**: provide direct link. Done.

**CART mode**:
1. `browser_navigate` to product page on chosen store
2. Select correct variant if needed (size, color, quantity) — ask user if ambiguous
3. `browser_click` "Add to Cart" button (find via `browser_snapshot`)
4. `browser_take_screenshot` as confirmation
5. Show screenshot to user
6. Log action to audit-log.md

**FULL mode**:
1. Check total cost against `purchase_limit_eur` and aggregate limits — if over → BLOCK immediately, do not proceed
2. Same as CART steps 1-4 (navigate, select variant, click Add to Cart, screenshot)
3. Extract current price from cart page via `browser_snapshot`
4. If price differs from comparison-time price by more than max(2%, 2 EUR) → ABORT, inform user of price change
5. Generate a random 4-digit confirmation code (1000-9999). Do not reuse codes within session.
6. Send Telegram OOB confirmation via `mcp__plugin_telegram_telegram__reply`:
   "PURCHASE CONFIRMATION
   Product: {product name}
   Store: {store domain}
   Price: {total_cost} EUR (incl. delivery)
   Daily spend after this: {daily_sum + total_cost} / {daily_limit} EUR
   Monthly spend after this: {monthly_sum + total_cost} / {monthly_limit} EUR

   Reply {code} to confirm. Any other reply = cancel.
   This code expires in 5 minutes."
7. Wait for Telegram reply. Poll for incoming Telegram messages. Do NOT proceed with any other actions while waiting.
   - If reply matches the 4-digit code exactly → proceed to step 8
   - If reply is anything else → ABORT. Send Telegram: "Purchase cancelled."
   - If no reply within 5 minutes → ABORT. Send Telegram: "Confirmation expired. Run /buy again."
   - If price changed since code was generated → invalidate code, ABORT
8. Proceed through checkout (use saved payment method)
9. `browser_take_screenshot` of confirmation page
10. Send Telegram post-purchase notification: "Purchased: {product} for {total_cost} EUR on {store} at {timestamp}"
11. Log to audit-log.md (via Bash append: `echo "| {timestamp} | {URL} | checkout | OK |" >> {data_dir}/audit-log.md`)

## Step 8: Save Report & Update History

1. Save report to `{data_dir}/reports/{query-slug}-YYYY-MM-DD.md`. `query-slug`: lowercase, dashes, max 50 chars, only `[a-z0-9-]` characters. If file exists, append `-2`, `-3`, etc. Include: original query, stores searched, comparison table, decision + reasoning, links.
2. **CART or FULL mode only**: add entry to purchase-history.md with action type:
   - `action: carted` (CART mode) or `action: purchased` (FULL mode)
   - Include: product, store, price, date, link, action
   - **RESEARCH mode**: do NOT update purchase-history.md (no purchase occurred)
3. **Only if action was carted or purchased AND product does not already exist in recurring.md**: check if this product appears in purchase-history 2+ times (matching by ASIN for Amazon, or by stripping query parameters and normalizing hostname (www. prefix) for others) → suggest recurring: "You've bought this before. Set up recurring?" → [recurring-purchase.md](recurring-purchase.md)
