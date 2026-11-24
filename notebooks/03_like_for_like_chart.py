
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# 1. 定位项目根目录
project_dir = Path(__file__).resolve().parent.parent

# 2. 读取第二份 SQL 结果
csv_path = (
    project_dir
    / "outputs"
    / "02_like_for_like_pricing.csv"
)

df = pd.read_csv(csv_path)

# 3. 数据检查
required_columns = [
    "neighbourhood",
    "accommodates",
    "bedrooms_numeric",
    "listing_count",
    "avg_price",
    "median_price"
]

assert all(
    col in df.columns for col in required_columns
), "Missing required columns"

assert len(df) == 6, "Expected six groups"

assert not df[required_columns].isna().any().any(), \
    "Missing values detected"

# 检查配置与区域组合是否重复
assert not df.duplicated(
    ["neighbourhood", "accommodates", "bedrooms_numeric"]
).any(), "Duplicate groups detected"

# 4. 定义两个细分市场
configurations = [
    (2, 1, "2 guests · 1 bedroom"),
    (4, 2, "4 guests · 2 bedrooms")
]

areas = [
    "Centrum-West",
    "Centrum-Oost",
    "De Baarsjes - Oud-West"
]

# 5. 创建左右两个面板
fig, axes = plt.subplots(
    1, 2,
    figsize=(13, 5.8),
    sharex=True
)

for ax, (guests, bedrooms, title) in zip(
    axes, configurations
):
    subset = df[
        (df["accommodates"] == guests)
        & (df["bedrooms_numeric"] == bedrooms)
    ].copy()

    subset = (
        subset.set_index("neighbourhood")
        .loc[areas]
        .reset_index()
    )

    # 中位数越高，柱子越长
    bars = ax.barh(
        subset["neighbourhood"],
        subset["median_price"],
        color="#367F79",
        height=0.58
    )

    ax.invert_yaxis()

    ax.set_title(
        title,
        fontsize=13,
        fontweight="bold"
    )

    ax.set_xlim(0, 650)
    ax.set_xlabel("Median listing price (EUR)")

    # 标注价格和样本量
    for bar, (_, row) in zip(
        bars, subset.iterrows()
    ):
        ax.text(
            bar.get_width() + 9,
            bar.get_y() + bar.get_height() / 2,
            f"€{row['median_price']:,.2f}  (n={int(row['listing_count'])})",
            va="center",
            fontsize=9
        )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", alpha=0.15)
    ax.set_axisbelow(True)

# 6. 标题与来源
fig.suptitle(
    "Amsterdam Airbnb: Like-for-like Pricing",
    fontsize=17,
    fontweight="bold"
)

fig.text(
    0.5, 0.03,
    "Entire home/apt · Observed listing prices · "
    "Source: Inside Airbnb (2026-09-16)",
    ha="center",
    fontsize=9,
    color="dimgray"
)

# 7. 保存
output_path = (
    project_dir
    / "visualizations"
    / "02_like_for_like_pricing.png"
)

fig.tight_layout(rect=[0, 0.07, 1, 0.91])

fig.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight"
)

print("Chart saved to:", output_path)

plt.show()
