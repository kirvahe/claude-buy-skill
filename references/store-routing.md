# Store Routing

## Country Presets

Load preset based on `country` in config.yml. Custom stores from config `stores:` array are merged with preset.

### ES — Spain (v1, fully built)

| Store | Domain | Search URL | Category | Notes |
|-------|--------|-----------|----------|-------|
| Amazon.es | amazon.es | `https://www.amazon.es/s?k={query}` | general | Prime member pricing, filter stars >= 3.5 |
| Decantalo | decantalo.com | `https://www.decantalo.com/es/en/search?q={query}` | wine | Wine specialist, Parker scores shown |
| Zara | zara.com | `https://www.zara.com/es/en/search?searchTerm={query}` | clothing | Size selection required before add-to-cart |
| El Corte Ingles | elcorteingles.es | `https://www.elcorteingles.es/search/?s={query}` | general | Department store, wide range |
| Temu | temu.com | `https://www.temu.com/search_result.html?search_key={query}` | clothing, general | Budget option, long delivery |
| MediaMarkt | mediamarkt.es | `https://www.mediamarkt.es/es/search.html?query={query}` | electronics | Tech specialist |
| Uniqlo | uniqlo.com | `https://www.uniqlo.com/es/es/search?q={query}` | clothing | Basics, quality fabrics |
| Leroy Merlin | leroymerlin.es | `https://www.leroymerlin.es/buscador?query={query}` | home, tools | DIY and home improvement |
| IKEA | ikea.com | `https://www.ikea.com/es/es/search/?q={query}` | furniture, home | May prompt for zip code |

To add a new country, copy the ES section above as a template. See README for contributing guidelines.

## Category to Store Mapping

Determined per country preset. For ES:

| Category | Stores | Detection keywords |
|----------|--------|--------------------|
| Electronics/tech | Amazon.es, MediaMarkt, El Corte Ingles | gadget, laptop, phone, TV, headphones, cable, charger, battery, robot, vacuum |
| Wine | Decantalo, Amazon.es | wine, vino, bottle, vintage, grape, parker, rioja, tempranillo |
| Furniture/home | IKEA, Leroy Merlin, Amazon.es | furniture, shelf, lamp, decoration, curtain, tool, drill, paint |
| Clothing | Zara, Uniqlo, El Corte Ingles, Temu | shirt, jacket, pants, dress, shoes, clothing, coat, t-shirt |
| General/other | Amazon.es, El Corte Ingles | everything not matching above |

If ambiguous category → search broader store set. Claude decides.

## Playwright Interaction Patterns

Use `browser_snapshot` (accessibility tree) over hardcoded CSS selectors — more resilient to UI changes.

### General flow per store

1. `browser_navigate` to search URL (with query substituted)
2. `browser_snapshot` to read search results
3. Extract: product name, price, rating, delivery info, product URL
4. For detailed info: `browser_click` on product → `browser_snapshot` product page
5. For add-to-cart: find "Add to cart" / "Anadir a la cesta" button via snapshot → `browser_click`

### Store-specific quirks

**Amazon.es**
- Filter by Prime delivery: append `&rh=p_76%3AA0322001` to search URL
- Filter by stars >= 3.5: look for star rating in results, skip lower
- Subscribe & Save: check product page for "Suscribete y ahorra" option
- Seller info: extract seller name + rating from "Vendido por" section

**Zara**
- Size selection REQUIRED before add-to-cart
- If user hasn't specified size → ask, or check taste-profile.md for saved sizes
- Product images are important for taste-driven selection

**IKEA**
- May prompt for zip code on first visit — use city from config to determine
- Product availability varies by location
- Some items are pickup-only

**Temu**
- Delivery times are long (7-15 days typically)
- Always note delivery estimate in comparison table
- Good for "not urgent" purchases

**El Corte Ingles**
- Wide range but prices often higher than Amazon
- Good for same-day pickup (Click & Collect)
- Quality delta logic applies — may be worth paying more for immediate pickup
