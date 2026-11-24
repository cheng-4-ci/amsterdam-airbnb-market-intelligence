# Amsterdam Airbnb Market Intelligence — Evidence Register

**Data source:** Inside Airbnb  
**Market:** Amsterdam, Netherlands  
**Snapshot date:** 2026-09-16  
**Project perspective:** Short-term rental platform — Market Intelligence  
**Primary focus:** Neighbourhood pricing and like-for-like property comparisons

---

## E01 — Neighbourhood Pricing and Data Coverage

**Research question:** How do listing prices and price-data coverage differ across selected Amsterdam neighbourhoods?

**SQL file:** `sql/01_neighbourhood_pricing.sql`  
**Output file:** `outputs/01_neighbourhood_pricing.csv`

**Analysis sample:**
- Entire home/apt listings
- Centrum-West, Centrum-Oost and De Baarsjes - Oud-West
- All listings included in coverage calculations
- Only listings with non-missing prices included in price statistics

**Expected output:** 3 rows

**Key metrics:**
- Total listings
- Priced listings
- Missing price rate
- Mean listing price
- Median listing price

**Preliminary finding:** Centrum-West has the highest observed mean and median listing prices among the three selected neighbourhoods.

**Limitations:** Missing prices may introduce selection bias. Mean prices are sensitive to high-priced listings. Listing prices do not represent actual transaction prices.

**Figure:** `visualizations/01_neighbourhood_mean_median.png`

**Key findings:**
- Centrum-West has the highest observed mean and
  median listing prices among the three neighbourhoods.
- Mean prices exceed median prices in all three areas.
- Price-data coverage differs substantially across areas,
  so comparisons are limited to priced listings.

**Business relevance:**
Neighbourhood averages alone may be misleading for
competitive pricing benchmarks.

**Validation status:** Validated


---

## E02 — Like-for-like Neighbourhood Pricing

**Research question:** Do neighbourhood price differences persist when comparing listings with the same guest capacity and bedroom count?

**SQL file:** `sql/02_like_for_like_pricing.sql`  
**Output file:** `outputs/02_like_for_like_pricing.csv`

**Analysis sample:**
- Entire home/apt listings with valid prices
- Three selected neighbourhoods
- Configuration A: accommodates 2 guests, 1 bedroom
- Configuration B: accommodates 4 guests, 2 bedrooms

**Expected output:** 6 rows

**Key metrics:**
- Neighbourhood
- Guest capacity
- Bedroom count
- Listing count
- Mean listing price
- Median listing price

**Preliminary finding:** Centrum-West retains higher observed median listing prices in both property configurations.

**Limitations:** Other property characteristics, including floor area, amenities and micro-location, are not fully controlled. This analysis does not identify a causal location premium.

**Figure:** `visualizations/02_like_for_like_pricing.png`

**Key findings:**
- Centrum-West retains the highest median listing price
  in both selected property configurations.
- The median price gap between Centrum-West and
  De Baarsjes - Oud-West is approximately 8.2% for
  2-guest, 1-bedroom listings.
- The corresponding gap is approximately 18.4% for
  4-guest, 2-bedroom listings.

**Business relevance:**
Competitive pricing comparisons should consider
neighbourhood, guest capacity and bedroom count.

**Limitations:**
Other characteristics, including property quality,
amenities and micro-location, remain uncontrolled.

**Validation status:** Validated


---

## E03 — Price Data Quality and Outlier Sensitivity

**Research question:**
How do missing prices and high-price observations
affect the reliability of pricing comparisons?

**Analysis sample:**
- Amsterdam entire home/apt listings
- 8,579 listings in total
- 4,320 listings with observed prices

**Key metrics:**
- Missing-price rate: 49.64%
- IQR upper fence: EUR 765
- Listings above upper fence: 263
- Full-sample mean price: EUR 401.23
- Mean excluding prices above EUR 765: EUR 348.81

**Preliminary finding:**
The observed mean listing price is sensitive to
high-price observations. Missing-price coverage
also limits the representativeness of pricing results.

**Business relevance:**
Pricing benchmarks should report data coverage
and use median prices alongside mean prices.

**Limitations:**
IQR outliers are not necessarily data errors.
The direction of missing-price selection bias
cannot be determined from these statistics alone.

**SQL file:** `sql/03_price_quality_sensitivity.sql`

**Output file:** `outputs/03_price_quality_sensitivity.csv`

**Validation status:** Validated

**Method notes:**
- Analysis restricted to entire home/apt listings.
- Price statistics use listings with observed prices.
- P25 and P75 use the nearest-rank method.
- The IQR upper fence is P75 + 1.5 × IQR.
- High-price observations are retained in the main
  analysis and excluded only for sensitivity testing.




---

## E04 — Host Supply Structure

**Research question:**
How is Amsterdam's short-term rental supply
distributed between single-listing and
multi-listing host accounts?

**Analysis sample:**
- All 10,612 listings
- 9,231 unique host IDs
- Host groups defined by listing counts
  within the Amsterdam dataset

**Key metrics:**
- Single-listing hosts: 8,627 (93.46%)
- Multi-listing hosts: 604 (6.54%)
- Share of listings from single-listing hosts: 81.29%
- Share of listings from multi-listing hosts: 18.71%

**Preliminary finding:**
Most host accounts have one listing, while
multi-listing hosts contribute a disproportionate
share of listed supply.

**Business relevance:**
Host segmentation may help identify different
operating patterns and potential platform needs.

**Limitations:**
A host ID does not necessarily represent a unique
economic operator. Listing share is not equivalent
to booking or revenue market share.


**SQL file:** `sql/04_host_supply_structure.sql`

**Output file:** `outputs/04_host_supply_structure.csv`

**Validation status:** Validated

**Method notes:**
- Host segments are defined by the number of listings
  associated with each host_id in the Amsterdam snapshot.
- Single-listing: one listing per host ID.
- Multi-listing: two or more listings per host ID.
- Host share uses unique host IDs as the denominator.
- Listing share uses all listings with known host IDs.
- Listing share does not represent booking or revenue share.


---

## Validation Checklist

- [ ] SQL files saved successfully
- [ ] CSV files exported with column headers
- [ ] Output row counts verified
- [ ] Numerical results checked against previous analysis
- [ ] Database views and data preparation logic preserved
- [ ] Source and snapshot date documented

---

## Future Evidence

Additional evidence may include:
- Price missingness and outlier sensitivity
- Premium listing characteristics
- Amenities and review ratings
- Host concentration and operating patterns

Only include findings in the final report after verifying their source, analytical sample and limitations.