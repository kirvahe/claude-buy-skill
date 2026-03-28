# Price Analysis

## Total Cost Rule

**Always compare total cost, never base price alone.**

```
total_cost = product_price + delivery_fee
```

If delivery is free (e.g. Prime) → delivery_fee = 0.

## Historical Price Lookup

### Amazon products → CamelCamelCamel

1. Navigate to `https://camelcamelcamel.com/search?sq={product_name_or_ASIN}` via Playwright
2. `browser_snapshot` to find matching product
3. Click through to product page
4. Extract from page: current price, lowest price, highest price, average price
5. Rate limit: wait 3-5 seconds between CCC requests

If CamelCamelCamel unavailable → set `historical = null`, note "price history unavailable".

### Other store products → Idealo.es

1. Navigate to `https://www.idealo.es/` via Playwright
2. Search for product name
3. `browser_snapshot` to extract: price range across stores, price trend
4. Rate limit: wait 3-5 seconds between Idealo requests

If Idealo unavailable → set `historical = null`.

## Price Verdict Logic

```
If historical data unavailable:
  verdict = "no history"

Else if current_price <= historical_minimum * 1.05:
  verdict = "historical minimum!"

Else if current_price <= historical_average:
  verdict = "good price"

Else if current_price <= historical_average * 1.15:
  overpay = current_price - historical_average
  verdict = "slightly above average (+{overpay} EUR)"

Else:
  savings = current_price - historical_average
  verdict = "wait — usually {savings} EUR cheaper"
```

## Per-Unit Pricing

When a product has multiple size or quantity variants:

1. Extract all variants: size/quantity + price
2. Calculate price per unit (EUR/unit, EUR/kg, EUR/L, etc.)
3. Note best value variant
4. Include in comparison table if relevant

Only compare products with the same unit type (e.g., mL vs mL, not mL vs wipes).

Example: dish soap 500ml at 3.50 EUR = 7.00 EUR/L vs 1L at 5.99 EUR = 5.99 EUR/L → recommend 1L.

## Subscribe & Save (Amazon only)

1. On Amazon product page, check for "Suscribete y ahorra" / "Subscribe & Save" option
2. If available: extract discount percentage (typically 5-15%)
3. Calculate effective price: `product_price * (1 - discount / 100)`
4. Note in comparison: "Subscribe & Save: {effective_price} EUR ({discount}% off)"
5. If user confirms recurring → suggest setting up S&S directly or via recurring-purchase workflow

## Quality Delta

When comparing same product across different sellers or stores:

```
quality_delta = min(max(5, cheapest_total_cost * 0.10), 50)
```

A more expensive option is ACCEPTABLE if:
- Price difference <= quality_delta
- AND at least one of:
  - Better seller rating (Amazon marketplace)
  - Prime delivery vs non-Prime
  - Faster delivery (1 day vs 5 days)
  - More reliable store (known vs unknown seller)

Example: Product is 45 EUR on unknown seller, 49 EUR on Amazon Prime seller (4.8 stars).
Delta = max(5, 45 * 0.10) = max(5, 4.5) = 5 EUR. Difference = 4 EUR < 5 EUR → recommend Amazon seller.

## Amazon Seller Filtering

1. Products with rating < 3.5 stars → **EXCLUDE** from results entirely
2. When multiple sellers offer same product:
   - Prefer sellers with higher rating
   - Prefer "Sold by Amazon" or "Fulfilled by Amazon"
   - Apply quality delta for price differences between sellers
3. Note seller name and rating in comparison table for Amazon results

## Rate Limiting

- 2-5 seconds between requests to same domain
- If rate limited (HTTP 429) → wait 30 seconds, retry once, then skip
- CamelCamelCamel and Idealo: 3-5 second minimum between requests
