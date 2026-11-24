-- Amsterdam Airbnb: view definitions
-- Run after importing the two raw tables.

-- View: listings_clean
CREATE VIEW listings_clean AS
SELECT
    *,
    CASE
        WHEN price IS NULL
             OR TRIM(price) = ''
        THEN NULL
        ELSE CAST(price AS REAL)
    END AS price_numeric
FROM listings_raw;

-- View: listing_attributes_clean
CREATE VIEW listing_attributes_clean AS
SELECT
    d.*,

    CASE
        WHEN d.bedrooms IS NULL
             OR TRIM(CAST(d.bedrooms AS TEXT)) = ''
        THEN NULL

        ELSE CAST(d.bedrooms AS REAL)
    END AS bedrooms_numeric

FROM amsterdam_listings_detailed AS d;

-- View: listing_amenities_clean
CREATE VIEW listing_amenities_clean AS
SELECT
    d.id,

    CASE
        WHEN json_valid(d.amenities) = 1
             AND EXISTS (
                 SELECT 1
                 FROM json_each(d.amenities) AS a
                 WHERE a.value = 'Air conditioning'
             )
        THEN 1
        ELSE 0
    END AS has_air_conditioning

FROM amsterdam_listings_detailed AS d;

