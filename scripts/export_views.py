
from pathlib import Path
import sqlite3

project_dir = Path(__file__).resolve().parent.parent

db_path = project_dir / "amsterdam_airbnb.db"
output_path = project_dir / "sql" / "00_create_views.sql"

view_names = [
    "listings_clean",
    "listing_attributes_clean",
    "listing_amenities_clean",
]

if not db_path.is_file():
    raise FileNotFoundError(f"Database not found: {db_path}")

# 只读连接，不修改现有数据库
with sqlite3.connect(db_path) as conn:
    rows = conn.execute(
        """
        SELECT name, sql
        FROM sqlite_master
        WHERE type = 'view'
        """
    ).fetchall()

view_definitions = dict(rows)

missing = [
    name for name in view_names
    if name not in view_definitions
]

if missing:
    raise ValueError(f"Missing views: {missing}")

output_path.parent.mkdir(parents=True, exist_ok=True)

with output_path.open("w", encoding="utf-8") as f:
    f.write("-- Amsterdam Airbnb: view definitions\n")
    f.write("-- Run after importing the two raw tables.\n\n")

    for name in view_names:
        definition = view_definitions[name].strip().rstrip(";")
        f.write(f"-- View: {name}\n")
        f.write(definition + ";\n\n")

print("Exported", len(view_names), "views")
print("Saved to:", output_path)
