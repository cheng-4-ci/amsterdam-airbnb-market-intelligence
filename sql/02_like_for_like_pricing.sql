
WITH ranked AS (
    SELECT
        a.id,
        a.neighbourhood,
        a.price_numeric,
        b.accommodates,
        b.bedrooms_numeric,

        ROW_NUMBER() OVER (
            PARTITION BY
                a.neighbourhood,
                b.accommodates,
                b.bedrooms_numeric
            ORDER BY
                a.price_numeric,
                a.id
        ) AS rn,

        COUNT(*) OVER (
            PARTITION BY
                a.neighbourhood,
                b.accommodates,
                b.bedrooms_numeric
        ) AS n

    FROM listings_clean AS a

    INNER JOIN listing_attributes_clean AS b
        ON a.id = b.id

    WHERE a.room_type = 'Entire home/apt'
      AND a.price_numeric IS NOT NULL

      AND (
          (b.accommodates = 2 AND b.bedrooms_numeric = 1)
          OR
          (b.accommodates = 4 AND b.bedrooms_numeric = 2)
      )

      AND a.neighbourhood IN (
          'Centrum-West',
          'Centrum-Oost',
          'De Baarsjes - Oud-West'
      )
)

SELECT
    neighbourhood,
    accommodates,
    bedrooms_numeric,
    COUNT(*) AS listing_count,
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

GROUP BY
    neighbourhood,
    accommodates,
    bedrooms_numeric

ORDER BY
    accommodates,
    median_price DESC;
