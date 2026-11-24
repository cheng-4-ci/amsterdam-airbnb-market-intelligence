
WITH entire_homes AS (
    SELECT
        id,
        price_numeric
    FROM listings_clean
    WHERE room_type = 'Entire home/apt'
),

priced AS (
    SELECT
        id,
        price_numeric
    FROM entire_homes
    WHERE price_numeric IS NOT NULL
),

ranked AS (
    SELECT
        id,
        price_numeric,
        ROW_NUMBER() OVER (
            ORDER BY price_numeric, id
        ) AS rn,
        COUNT(*) OVER () AS n
    FROM priced
),

quantiles AS (
    SELECT
        ROUND(
            AVG(
                CASE
                    WHEN rn IN (
                        CAST((n + 1) / 2 AS INTEGER),
                        CAST((n + 2) / 2 AS INTEGER)
                    )
                    THEN price_numeric
                END
            ), 2
        ) AS median_price,

        MAX(
            CASE
                WHEN rn = CAST((n + 3) / 4 AS INTEGER)
                THEN price_numeric
            END
        ) AS p25,

        MAX(
            CASE
                WHEN rn = CAST((3 * n + 3) / 4 AS INTEGER)
                THEN price_numeric
            END
        ) AS p75

    FROM ranked
),

thresholds AS (
    SELECT
        median_price,
        p25,
        p75,
        p75 - p25 AS iqr,
        p75 + 1.5 * (p75 - p25) AS upper_fence
    FROM quantiles
)

SELECT
    (SELECT COUNT(*) FROM entire_homes)
        AS total_entire_homes,

    (SELECT COUNT(*) FROM priced)
        AS priced_listings,

    (SELECT COUNT(*) FROM entire_homes)
      - (SELECT COUNT(*) FROM priced)
        AS missing_prices,

    ROUND(
        100.0 *
        (
            (SELECT COUNT(*) FROM entire_homes)
            - (SELECT COUNT(*) FROM priced)
        )
        / (SELECT COUNT(*) FROM entire_homes),
        2
    ) AS missing_rate,

    t.median_price,
    t.p25,
    t.p75,
    t.iqr,
    t.upper_fence,

    SUM(
        CASE
            WHEN p.price_numeric > t.upper_fence
            THEN 1 ELSE 0
        END
    ) AS high_price_count,

    ROUND(AVG(p.price_numeric), 2)
        AS full_mean,

    ROUND(
        AVG(
            CASE
                WHEN p.price_numeric <= t.upper_fence
                THEN p.price_numeric
            END
        ), 2
    ) AS mean_without_high_prices

FROM priced AS p
CROSS JOIN thresholds AS t;
