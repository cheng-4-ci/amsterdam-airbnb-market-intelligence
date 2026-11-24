
from pathlib import Path
from datetime import datetime
import sqlite3

import pandas as pd

# =====================================
# 1. Project paths
# =====================================

ROOT = Path(__file__).resolve().parent.parent

RAW = ROOT / "data" / "raw"
SQL = ROOT / "sql"
OUTPUTS = ROOT / "outputs"

TEST_DIR = ROOT / "repro_test"
TEST_DIR.mkdir(exist_ok=True)

# Create a new test database on every run.
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
TEST_DB = TEST_DIR / f"rebuilt_{timestamp}.db"

SUMMARY_CSV = RAW / "listings.csv"
DETAILED_CSV = RAW / "listings.csv.gz"

VIEW_SQL = SQL / "00_create_views.sql"

EVIDENCE_FILES = {
    "E01": (
        "01_neighbourhood_pricing.sql",
        "01_neighbourhood_pricing.csv",
    ),
    "E02": (
        "02_like_for_like_pricing.sql",
        "02_like_for_like_pricing.csv",
    ),
    "E03": (
        "03_price_quality_sensitivity.sql",
        "03_price_quality_sensitivity.csv",
    ),
    "E04": (
        "04_host_supply_structure.sql",
        "04_host_supply_structure.csv",
    ),
}

# =====================================
# 2. Check required files
# =====================================

required_files = [
    SUMMARY_CSV,
    DETAILED_CSV,
    VIEW_SQL,
]

for sql_name, csv_name in EVIDENCE_FILES.values():
    required_files.extend([
        SQL / sql_name,
        OUTPUTS / csv_name,
    ])

missing = [
    str(path)
    for path in required_files
    if not path.is_file()
]

if missing:
    raise FileNotFoundError(
        "Missing required files:\n" + "\n".join(missing)
    )

print("Step 1: Required files found.")

# =====================================
# 3. Import original datasets
# =====================================

summary = pd.read_csv(
    SUMMARY_CSV,
    low_memory=False
)

detailed = pd.read_csv(
    DETAILED_CSV,
    compression="gzip",
    low_memory=False
)

for name, df in [
    ("Summary", summary),
    ("Detailed", detailed),
]:
    if len(df) != 10612:
        raise ValueError(
            f"{name}: unexpected row count {len(df)}"
        )

    if df["id"].isna().any():
        raise ValueError(f"{name}: missing IDs")

    if df["id"].duplicated().any():
        raise ValueError(f"{name}: duplicate IDs")

if set(summary["id"]) != set(detailed["id"]):
    raise ValueError("Listing IDs do not match")

print("Step 2: Original datasets validated.")

# =====================================
# 4. Build an independent database
# =====================================

results = {}

with sqlite3.connect(TEST_DB) as conn:

    summary.to_sql(
        "listings_raw",
        conn,
        if_exists="fail",
        index=False,
    )

    detailed.to_sql(
        "amsterdam_listings_detailed",
        conn,
        if_exists="fail",
        index=False,
    )

    print("Step 3: Fresh database created.")

    # Create the three saved SQL views.
    view_script = VIEW_SQL.read_text(
        encoding="utf-8-sig"
    )

    conn.executescript(view_script)

    expected_views = {
        "listings_clean",
        "listing_attributes_clean",
        "listing_amenities_clean",
    }

    existing_views = {
        row[0]
        for row in conn.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type = 'view'"
        )
    }

    if not expected_views.issubset(existing_views):
        raise RuntimeError(
            "Missing views: "
            + str(expected_views - existing_views)
        )

    print("Step 4: Three views created.")

    # =================================
    # 5. Re-run the original SQL files
    # =================================

    for evidence, (sql_name, csv_name) in (
        EVIDENCE_FILES.items()
    ):
        query = (SQL / sql_name).read_text(
            encoding="utf-8-sig"
        )

        print(f"\nRunning {evidence}...")

        actual = pd.read_sql_query(query, conn)

        expected = pd.read_csv(
            OUTPUTS / csv_name,
            encoding="utf-8-sig",
        )

        # Ignore the order of rows, but NOT columns.
        if list(actual.columns) != list(expected.columns):
            print(f"{evidence}: COLUMN MISMATCH")
            print("SQL columns:", actual.columns.tolist())
            print("CSV columns:", expected.columns.tolist())
            results[evidence] = False
            continue

        if actual.shape != expected.shape:
            print(f"{evidence}: SHAPE MISMATCH")
            print("New shape:", actual.shape)
            print("Saved shape:", expected.shape)
            results[evidence] = False
            continue

        # Normalize numerical values to two decimals.
        for column in actual.columns:
            actual_num = pd.to_numeric(
                actual[column], errors="coerce"
            )
            expected_num = pd.to_numeric(
                expected[column], errors="coerce"
            )

            if (
                actual_num.notna().sum() ==
                actual[column].notna().sum()
                and expected_num.notna().sum() ==
                expected[column].notna().sum()
            ):
                actual[column] = actual_num.round(2)
                expected[column] = expected_num.round(2)

        # Sort both tables consistently.
        columns = actual.columns.tolist()

        actual = (
            actual.sort_values(
                by=columns,
                key=lambda s: s.astype(str),
            )
            .reset_index(drop=True)
        )

        expected = (
            expected.sort_values(
                by=columns,
                key=lambda s: s.astype(str),
            )
            .reset_index(drop=True)
        )

        try:
            pd.testing.assert_frame_equal(
                actual,
                expected,
                check_dtype=False,
                check_exact=False,
                atol=0.01,
                rtol=0,
            )

            print(
                f"{evidence}: PASS "
                f"({len(actual)} rows)"
            )
            results[evidence] = True

        except AssertionError as error:
            print(f"{evidence}: DATA MISMATCH")
            print(str(error)[:1500])
            results[evidence] = False

# =====================================
# 6. Final report
# =====================================

print("\n==============================")
print("REPRODUCIBILITY TEST SUMMARY")
print("==============================")

for evidence, passed in results.items():
    print(
        f"{evidence}: "
        f"{'PASS' if passed else 'FAIL'}"
    )

print("\nTest database:", TEST_DB)

if len(results) == 4 and all(results.values()):
    print("\nALL FOUR EVIDENCE TESTS PASSED")
else:
    print("\nSOME TESTS REQUIRE INVESTIGATION")
