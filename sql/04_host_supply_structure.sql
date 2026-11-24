
WITH host_counts AS (
    SELECT
        host_id,
        COUNT(*) AS listings_per_host
    FROM amsterdam_listings_detailed
    WHERE host_id IS NOT NULL
    GROUP BY host_id
),

host_segments AS (
    SELECT
        host_id,
        listings_per_host,
        CASE
            WHEN listings_per_host = 1
                THEN 'Single-listing'
            ELSE 'Multi-listing'
        END AS host_segment
    FROM host_counts
),

segment_summary AS (
    SELECT
        host_segment,
        COUNT(*) AS host_count,
        SUM(listings_per_host) AS listing_count
    FROM host_segments
    GROUP BY host_segment
),

totals AS (
    SELECT
        SUM(host_count) AS total_hosts,
        SUM(listing_count) AS total_listings
    FROM segment_summary
)

SELECT
    s.host_segment,
    s.host_count,
    s.listing_count,

    ROUND(
        100.0 * s.host_count / t.total_hosts,
        2
    ) AS host_share_pct,

    ROUND(
        100.0 * s.listing_count / t.total_listings,
        2
    ) AS listing_share_pct,

    ROUND(
        1.0 * s.listing_count / s.host_count,
        2
    ) AS avg_listings_per_host

FROM segment_summary AS s
CROSS JOIN totals AS t

ORDER BY s.host_count DESC;
