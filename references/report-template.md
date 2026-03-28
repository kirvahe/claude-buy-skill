# Report Template

Save to: `{data_dir}/reports/{query-slug}-YYYY-MM-DD.md`

`query-slug`: lowercase, spaces replaced with dashes, max 50 chars. Example: "robot-vacuum-under-300"

## Template

```markdown
# {Product Query} | {YYYY-MM-DD}

## Request
- **Query:** {original user query}
- **Category:** {detected category}
- **Urgency:** {tomorrow / this week / not urgent}
- **Stores searched:** {list of stores}
- **Security mode:** {research / cart / full}

## Research

### Expert Sources Consulted
- {source 1}: {key finding}
- {source 2}: {key finding}

### Reddit Consensus
{synthesized community opinion — if applicable}

### Price History
- CamelCamelCamel: min {X} EUR / avg {Y} EUR / max {Z} EUR
- Idealo: {price range if checked}

## Comparison

| # | Product | Store | Price | Delivery | Total | Rating | Seller | Price Verdict |
|---|---------|-------|-------|----------|-------|--------|--------|---------------|
| 1 | {name} | {store} | {X} EUR | {Y} EUR | {Z} EUR | {N}/5 | {seller} | {verdict} |
| 2 | ... | ... | ... | ... | ... | ... | ... | ... |

## Decision
- **Chosen:** {product name} from {store}
- **Price:** {total} EUR (product {X} + delivery {Y})
- **Why:** {1-2 sentences — value, expert endorsement, delivery}
- **Action:** {added to cart / link provided / purchased}
- **Timestamp:** {ISO timestamp of action}

## Links
- Product: {direct URL}
- CamelCamelCamel: {CCC URL if available}
- Idealo: {Idealo URL if available}
- Expert review: {Wirecutter/other URL if used}
```
