
WITH ranked AS (
    SELECT
        id,
        neighbourhood,
        price_numeric,

        ROW_NUMBER() OVER (
            PARTITION BY neighbourhood
            ORDER BY price_numeric, id
        ) AS rn,

        COUNT(*) OVER (
            PARTITION BY neighbourhood
        ) AS n

    FROM listings_clean

    WHERE room_type = 'Entire home/apt'
      AND price_numeric IS NOT NULL
      AND neighbourhood IN (
          'Centrum-West',
          'Centrum-Oost',
          'De Baarsjes - Oud-West'
      )
),

pricing AS (
    SELECT
        neighbourhood,
        COUNT(*) AS priced_listings,
        ROUND(AVG(price_numeric), 2) AS avg_price,

        ROUND(
            AVG(
                CASE
                    WHEN rn IN (
                        CAST((n + 1) / 2 AS INTEGER),
                        CAST((n + 2) / 2 AS INTEGER)
                    )
                    THEN price_numeric
                END
            ),
            2
        ) AS median_price

    FROM ranked
    GROUP BY neighbourhood
),

coverage AS (
    SELECT
        neighbourhood,
        COUNT(*) AS total_listings,

        ROUND(
            100.0 * SUM(
                CASE
                    WHEN price_numeric IS NULL THEN 1
                    ELSE 0
                END
            ) / COUNT(*),
            2
        ) AS missing_price_rate

    FROM listings_clean

    WHERE room_type = 'Entire home/apt'
      AND neighbourhood IN (
          'Centrum-West',
          'Centrum-Oost',
          'De Baarsjes - Oud-West'
      )

    GROUP BY neighbourhood
)

SELECT
    p.neighbourhood,
    c.total_listings,
    p.priced_listings,
    c.missing_price_rate,
    p.avg_price,
    p.median_price

FROM pricing AS p

INNER JOIN coverage AS c
    ON p.neighbourhood = c.neighbourhood

ORDER BY p.avg_price DESC;
