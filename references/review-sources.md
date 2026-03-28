# Review Sources

## Expert Sources by Category

| Category | Primary Sources | Search Patterns |
|----------|----------------|-----------------|
| Electronics/tech | Wirecutter (NYT), Reddit r/BuyItForLife r/technology | `site:nytimes.com/wirecutter best {product}` |
| Kitchen/food tools | Serious Eats, Wirecutter, Reddit r/Cooking r/BuyItForLife | `site:seriouseats.com best {product}` |
| Home/furniture | Wirecutter, Reddit r/HomeImprovement r/InteriorDesign | `site:nytimes.com/wirecutter best {product}` |
| Clothing | Reddit r/malefashionadvice r/femalefashionadvice | `site:reddit.com {brand} quality review` |
| Wine | Parker, Jancis Robinson, Decanter, Wine Spectator | `{wine} parker score` |
| General | Wirecutter + Reddit | combine queries |

## "Find Best" Trigger

When user says "find best", "recommend", "which one should I buy", "what's the best":

**ALWAYS check at minimum:**
1. Wirecutter (NYT)
2. Reddit (relevant subreddit)

Add Serious Eats for kitchen/food items.

## Wine Critics Whitelist

Only these sources are acceptable for wine recommendations:

- **Robert Parker** / Wine Advocate — scores out of 100
- **Jancis Robinson** — scores out of 20
- **James Suckling** — scores out of 100
- **Decanter** magazine — scores out of 100
- **Wine Spectator** — scores out of 100
- **Wine Enthusiast** — scores out of 100

**BANNED for wine**: bloggers, influencers, YouTube sommeliers, Instagram wine accounts, Vivino user ratings.

Parker 90+ = very good. Parker 95+ = exceptional.

## Reddit Synthesis Pattern

1. Search: `site:reddit.com {product category} best recommendation {year}`
2. Also try: `site:reddit.com {product category} vs` (comparison threads)
3. Read top 3-5 threads by relevance
4. Synthesize:
   - Most recommended products (mentioned 3+ times across threads)
   - Common pros per product
   - Common cons per product
   - Red flags mentioned by community
5. Format output: "Reddit consensus: {product} is most recommended. Pros: ... Cons: ..."

## Search Query Templates

### Wirecutter
- `site:nytimes.com/wirecutter best {product category} {year}`
- `site:nytimes.com/wirecutter {specific product} review`

### Serious Eats
- `site:seriouseats.com best {kitchen/food product}`
- `site:seriouseats.com {product} review equipment`

### Reddit
- `site:reddit.com r/{relevant_subreddit} best {product} recommendation`
- `site:reddit.com {product A} vs {product B} reddit`
- `site:reddit.com {product category} worth it`

### Wine Critics
- `{wine name} {vintage} parker score`
- `{wine name} jancis robinson`
- `{region} {grape} best wines {year} wine spectator`

## Source Reliability Notes

- **Wirecutter**: lab-tested, updated regularly, trustworthy for most categories
- **Serious Eats**: rigorous kitchen testing, excellent for cookware and food tools
- **Reddit**: real user experiences, good for long-term reliability info, watch for astroturfing
- **Amazon ratings**: useful as signal (< 3.5 = filter out) but not as primary recommendation source
- **Other store ratings**: not important, ignore for recommendation purposes
