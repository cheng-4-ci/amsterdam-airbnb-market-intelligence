
-- Amsterdam Airbnb
-- Restore missing detailed-data cleaning views
-- Source: amsterdam_listings_detailed

-- ====================================
-- 1. Listing attributes cleaning
-- ====================================

CREATE VIEW IF NOT EXISTS listing_attributes_clean AS
SELECT
    d.*,

    CASE
        WHEN d.bedrooms IS NULL
             OR TRIM(CAST(d.bedrooms AS TEXT)) = ''
        THEN NULL

        ELSE CAST(d.bedrooms AS REAL)
    END AS bedrooms_numeric

FROM amsterdam_listings_detailed AS d;


-- ====================================
-- 2. Air conditioning amenity flag
-- ====================================

CREATE VIEW IF NOT EXISTS listing_amenities_clean AS
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
