
from pathlib import Path
import pandas as pd

project_dir = Path(__file__).resolve().parent.parent
data_path = project_dir / "data" / "raw" / "listings.csv.gz"

if not data_path.exists():
    raise FileNotFoundError(
        f"Detailed Airbnb data not found: {data_path}"
    )

df = pd.read_csv(
    data_path,
    compression="gzip",
    low_memory=False
)

print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nRequired fields:")
required_fields = [
    "id",
    "host_id",
    "accommodates",
    "bedrooms",
    "amenities",
    "review_scores_rating",
    "minimum_nights"
]

for field in required_fields:
    print(
        f"{field}:",
        "FOUND" if field in df.columns else "MISSING"
    )

print("\nFirst five listing IDs:")
print(df["id"].head().to_list())

print("\nUnique listing IDs:")
print(df["id"].nunique())
