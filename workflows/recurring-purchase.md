# Workflow: Recurring Purchases

## Required Reading

1. [security-rules.md](../references/security-rules.md)
2. `{data_dir}/purchase-history.md`
3. `{data_dir}/recurring.md`
4. `{data_dir}/taste-profile.md`
5. config.yml — for `telegram_chat_id` and `security_mode`

## Detection (passive — runs after any purchase)

After any add-to-cart or purchase via other workflows:

1. Check purchase-history.md for same product (match by name or product URL)
2. If found (2nd+ purchase) → ask user:
   "You bought **{product}** before ({date}, {price} EUR). Set up recurring?"
3. If Amazon product → also check Subscribe & Save availability

## Setup Flow

### Step 1: Confirm Product

Show user:
- Product name
- Last purchase: date + price
- Current price
- Price change since last purchase

### Step 2: Choose Frequency

Ask: "How often do you need this?"
- Weekly
- Every 2 weeks
- Monthly
- Every 2 months
- Custom interval (N days)

If purchase-history has 3+ orders of this product → calculate average interval and suggest:
"Based on your history, you reorder every ~{N} days. Use that?"

### Step 3: Amazon Subscribe & Save Check

If product is on Amazon:

1. Navigate to product page (Playwright)
2. Check for "Suscribete y ahorra" / "Subscribe & Save" option
3. If available → show discount:
   "Subscribe & Save saves {X}%. Set up on Amazon directly, or use my reminder system?"
   - **"Amazon"** → guide user to S&S setup on product page (but NEVER enter payment — user does that)
   - **"Reminder"** → proceed to Step 4

If not Amazon or S&S not available → proceed to Step 4.

### Step 4: Save to Recurring

Append to `{data_dir}/recurring.md`:

```markdown
### {Product Name}
- **Store:** {store}
- **Link:** {product URL}
- **Frequency:** every {N} days
- **Last purchase:** {YYYY-MM-DD}
- **Next reminder:** {YYYY-MM-DD}
- **Price at setup:** {X} EUR
- **Current price:** {X} EUR
- **Subscribe & Save:** {yes — X% / no / not available}
- **Status:** active
```

### Step 5: Calculate Next Reminder Date

Calculate `next_reminder` = last_purchase + frequency. Save to recurring.md.

**How reminders work**: reminders are checked at the start of each `/buy` invocation (see Session Start Check below). Claude Code is session-based — there is no background scheduler. If Telegram is configured, a notification is sent during the session check.

**Future**: for autonomous scheduled reminders, use Claude Code `/schedule` to create a recurring trigger that runs `/buy check-recurring` daily.

## Session Start Check (primary reminder mechanism)

At the beginning of each `/buy` invocation (after setup):

1. Read `{data_dir}/recurring.md` (if exists)
2. Check for items where `next_reminder` <= today AND `status` = active
3. If found:
   a. Quick price check via Firecrawl for each due item
   b. Update `current_price` in recurring.md
   c. Present to user in chat: "You have {N} recurring items due:"

**Normal price** (within 20% of setup price):
"- **{product}**: {X} EUR (was {Y} EUR at setup)"

**Price spike** (> 20% increase):
"- **{product}**: {X} EUR (was {Y} EUR — +{Z}% increase!)"

4. If Telegram configured → also send notification via `mcp__plugin_telegram_telegram__reply`
5. Ask user: "Reorder any? (say product name, 'all', or 'skip')"

### Handle Response

| Response | Action |
|----------|--------|
| Product name or "all" | Execute add-to-cart via [search-by-name.md](search-by-name.md) (repeat mode). Update recurring.md: last_purchase, next_reminder. |
| "skip" / "no" / "later" | Skip this cycle. Update next_reminder = today + frequency. |
| "postpone {product}" | Set next_reminder = today + 7 days for that product. |
| "cancel {product}" | Set status = "cancelled" in recurring.md. |

## Consumption Pattern Learning

When saving a recurring entry AND purchase-history has 3+ orders of this product:

1. Calculate actual average interval between purchases
2. Compare with user-set frequency
3. If difference > 20%:
   - Faster → suggest: "You reorder every ~{actual} days, but reminder is set for {set}. Shorten?"
   - Slower → suggest: "You reorder every ~{actual} days, but reminder is set for {set}. Extend?"
4. Update frequency only if user confirms

## Managing Recurring Items

User can say:
- "show my recurring" → list all active items with dates and prices
- "pause {product}" → set status to "paused"
- "resume {product}" → set status to "active", recalculate next_reminder
- "cancel {product}" → set status to "cancelled"
- "change frequency {product} to {N} days" → update frequency + next_reminder

## Success Criteria

- [ ] Recurring product correctly identified
- [ ] Frequency confirmed (or suggested from history)
- [ ] Subscribe & Save checked for Amazon products
- [ ] Entry saved to recurring.md
- [ ] Session Start Check implemented (primary mechanism)
- [ ] Telegram notification sent if configured
