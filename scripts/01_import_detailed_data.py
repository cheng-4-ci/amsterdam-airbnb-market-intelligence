
from pathlib import Path
import sqlite3
import pandas as pd

# 1. 定位项目文件
project_dir = Path(__file__).resolve().parent.parent

csv_path = (
    project_dir / "data" / "raw" / "listings.csv.gz"
)

db_path = project_dir / "amsterdam_airbnb.db"

table_name = "amsterdam_listings_detailed"

# 2. 检查源文件是否存在
if not csv_path.is_file():
    raise FileNotFoundError(
        f"CSV file not found: {csv_path}"
    )

if not db_path.is_file():
    raise FileNotFoundError(
        f"Database not found: {db_path}"
    )

# 3. 读取详细数据
df = pd.read_csv(
    csv_path,
    compression="gzip",
    low_memory=False
)

# 4. 检查数据完整性
required_columns = [
    "id",
    "host_id",
    "accommodates",
    "bedrooms",
    "amenities",
    "review_scores_rating",
    "minimum_nights"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing columns: {missing_columns}"
    )

if len(df) != 10612:
    raise ValueError(
        f"Unexpected row count: {len(df)}"
    )

if df["id"].isna().any():
    raise ValueError("Missing listing IDs detected")

if df["id"].duplicated().any():
    raise ValueError("Duplicate listing IDs detected")

print("Source data validation passed.")
print("Rows:", len(df))
print("Columns:", len(df.columns))

# 5. 将详细数据导入 SQLite
with sqlite3.connect(db_path) as conn:

    existing_tables = {
        row[0]
        for row in conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            """
        )
    }

    # 防止意外覆盖已有详细表
    if table_name in existing_tables:
        raise RuntimeError(
            f"Table already exists: {table_name}. "
            "Import stopped to prevent overwriting."
        )

    # 导入为新表
    df.to_sql(
        table_name,
        conn,
        if_exists="fail",
        index=False
    )

    # 6. 检查导入结果
    row_count = conn.execute(
        f"SELECT COUNT(*) FROM {table_name}"
    ).fetchone()[0]

    unique_ids = conn.execute(
        f"SELECT COUNT(DISTINCT id) FROM {table_name}"
    ).fetchone()[0]

    host_count = conn.execute(
        f"SELECT COUNT(DISTINCT host_id) FROM {table_name}"
    ).fetchone()[0]

    if row_count != len(df):
        raise RuntimeError("Imported row count mismatch")

    if unique_ids != len(df):
        raise RuntimeError("Imported listing IDs mismatch")

print("\nSQLite import completed.")
print("Imported rows:", row_count)
print("Unique listing IDs:", unique_ids)
print("Unique host IDs:", host_count)
print("Database:", db_path)
