# Workflow: Search by Photo

## Step 1: Analyze the Photo

1. Read the image file from the path provided by user. Validate file extension (.jpg, .jpeg, .png, .webp, .heic, .gif). If not a supported image format → skip Google Lens, use Claude's visual description as search query.
2. Describe the product in detail:
   - Brand (if visible)
   - Model name/number (if visible)
   - Category (electronics, clothing, furniture, wine, etc.)
   - Visual features: color, material, style, size estimate
   - Any text/labels on the product
3. Determine product category for store routing

## Step 2: Google Lens Search

1. "This image will be uploaded to Google Lens. The ENTIRE image will be processed — including background content (documents, screens, people, home details), not just the product. EXIF metadata may also contain location data. Google may store it per their privacy policy. Alternative: I can describe the product from the photo and search by text (no upload needed). Proceed with upload, or use text search instead?"
2. `browser_navigate` to `https://lens.google.com/` (validate URL per security-rules.md)
3. `browser_file_upload` — upload the image file
4. `browser_wait_for` results to load. Wait up to 15 seconds for results. If timeout → retry once, then fall back to Claude's visual description as search query.
5. `browser_snapshot` to read matching product results
6. Extract from results:
   - Matching product names and brands
   - Store links where product is available
   - Prices shown in results
7. `browser_take_screenshot` of results for reference

## Step 3: Filter and Cross-Reference

From Google Lens results:

1. **Filter by store whitelist** — keep only matches from whitelisted stores
2. **If whitelisted store matches found** → proceed to Step 4 with those products
3. **If NO whitelisted store matches** → use product name/brand from Lens results as search query → proceed to [search-by-name.md](search-by-name.md) workflow

## Step 4: Confirm Product Identity

Present findings to user:

"I see this is a **{brand} {model}** — {description}.
Google Lens found it on: {list of stores with prices}.
Is this the right product?"

Wait for user confirmation before proceeding.

If user says "no" or corrects → refine search with their input.

## Step 5: Proceed to Price Comparison

Once product identity confirmed:

1. Follow search-by-name.md from **Ask Urgency** through **Save Report & Update History**:
   - Ask urgency
   - Search all relevant stores (not just those from Lens)
   - Full price analysis with CCC/Idealo
   - Build comparison table
   - User confirms → execute action per security mode
   - Save report

## Edge Cases

**Photo is unclear or low quality:**
- Describe what you can see
- Ask user for more context: "I can see it's a {general category} but can't identify the exact product. Can you tell me the brand or model?"

**Product not found via Google Lens:**
- Use Claude's description as search query
- Proceed to [search-by-name.md](search-by-name.md) with the description

**Multiple products in photo:**
- Ask user which product they want: "I see several items in this photo: {list}. Which one are you looking for?"

## Google Lens Failure Fallback

If Google Lens upload or result extraction fails at ANY step:
1. Skip Google Lens entirely
2. Use Claude's visual analysis of the photo to identify product name, brand, category
3. Proceed to [search-by-name.md](search-by-name.md) using that description as query
