# Workflow: Search by Description (Deep Research)

## Step 1: Determine Selection Scenario

**Spec-driven** — user provides specs, budget, or measurable criteria:
- "best robot vacuum under 300 EUR"
- "laptop with 16GB RAM for coding"
→ Proceed to Step 2A

**Taste-driven** — subjective, no clear specs:
- "nice jacket for spring"
- "something cool for the living room"
→ Proceed to Step 2B

## Step 2A: Spec-Driven Research

### 2A.1: Expert Research

Read [review-sources.md](../references/review-sources.md) for source list per category.

**ALWAYS check** (for any "find best" / "recommend" query):
1. **Wirecutter (NYT)**: `mcp__exa__web_search_exa` with `site:nytimes.com/wirecutter best {product category}`
2. **Reddit**: `mcp__exa__web_search_exa` with `site:reddit.com {product category} recommendation best {current year}`
3. **Serious Eats** (kitchen/food items): `site:seriouseats.com best {product}`

**For wine**: follow critic whitelist and search patterns in [review-sources.md](../references/review-sources.md). NO bloggers, NO influencers.

For found articles: use `mcp__firecrawl__firecrawl_scrape` or `mcp__exa__web_search_exa` to extract recommended models, pros/cons, price points.

### 2A.2: Synthesize Research

From expert sources, identify **top 3 candidates**:
- Products recommended across multiple sources get priority
- Reddit community consensus (most upvoted recommendations)
- Match against taste-profile.md: respect brand blacklist, budget preferences
- Exclude brands in user's blacklist

### 2A.3: Find on Stores + Price Analysis

For each of the 3 candidates → follow search-by-name.md from **Ask Urgency** through **Save Report & Update History**:
- Ask urgency
- Search stores
- Price analysis with CCC/Idealo
- Build comparison table
- User confirms → execute action per security mode
- Save report + update purchase-history (if CART/FULL mode)

Note: the report saved by search-by-name.md delegation is the primary report. Do NOT save a second report from Step 3 below when using the spec-driven (2A) path.

### 2A.4: Build Enhanced Comparison Table

| # | Product | Expert Source | Score | Store | Price | Delivery | Total | Rating | Verdict |
|---|---------|-------------|-------|-------|-------|----------|-------|--------|---------|

Recommend #1 with reasoning: which experts endorse it, why this model, why this store.

## Step 2B: Taste-Driven Research

### 2B.1: Clarifying Questions

Ask in ONE message (not one by one):
- What's the occasion / use case?
- Any brand preferences? (check taste-profile.md first — if brands known, suggest them)
- Budget range?
- Specific features, colors, styles?
- Sizes? (check taste-profile.md for saved sizes)
- When do you need this? (tomorrow / this week / not urgent)

Skip questions already answered in user's request or taste-profile.

### 2B.2: Search Stores

After clarifying → search relevant stores from category mapping.

For each store:
1. Navigate to store search page (Playwright)
2. Search with refined query
3. `browser_snapshot` to extract product list
4. Extract per product: name, brief description, price, product URL

### 2B.3: Present Options

Present as **numbered text list with links** (NOT screenshots by default):

```
1. {Product name} — {price} EUR — {store}
   {Brief description: color, material, key feature}
   {product URL}

2. {Product name} — {price} EUR — {store}
   ...
```

Then: "Pick a number, or say 'screenshot N' to see it closer."

**Screenshots on request only**: use `mcp__playwright__browser_take_screenshot` of the product page.

### 2B.4: User Picks → Complete Flow

User picks a number → follow search-by-name.md from **Ask Urgency** through **Save Report & Update History**:
- Price analysis (always run, even for single chosen product)
- Comparison (if user wants to see alternatives)
- Confirm → cart/purchase per security mode
- Save report + update purchase-history (if CART/FULL mode)

## Step 3: Save Report (taste-driven 2B path only)

Save to `{data_dir}/reports/{query-slug}-YYYY-MM-DD.md` only if this workflow used the taste-driven (2B) path. If the spec-driven (2A) path was used, the report was already saved by the search-by-name.md delegation in Step 2A.3. `query-slug`: lowercase, dashes, max 50 chars, only `[a-z0-9-]` characters. If file exists, append `-2`, `-3`, etc. Include: original query, all research sources consulted, comparison table, final choice, links.
