
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. 定位项目文件夹
project_dir = Path(__file__).resolve().parent.parent

# 2. 读取 SQL 导出的结果
csv_path = project_dir / "outputs" / "01_neighbourhood_pricing.csv"
df = pd.read_csv(csv_path)

# 3. 验证字段和数据
required_columns = [
    "neighbourhood",
    "avg_price",
    "median_price"
]

assert all(col in df.columns for col in required_columns), \
    "CSV 缺少必要字段"

assert len(df) == 3, "预期包含三个区域"

# 4. 准备绘图数据
labels = df["neighbourhood"]
mean_prices = df["avg_price"]
median_prices = df["median_price"]

x = np.arange(len(labels))
bar_width = 0.35

# 5. 创建图表
fig, ax = plt.subplots(figsize=(11, 6))

bars_mean = ax.bar(
    x - bar_width / 2,
    mean_prices,
    bar_width,
    label="Mean",
    color="#336B87"
)

bars_median = ax.bar(
    x + bar_width / 2,
    median_prices,
    bar_width,
    label="Median",
    color="#72A9A0"
)

# 6. 添加标题与标签
ax.set_title(
    "Amsterdam Airbnb: Mean vs Median Listing Prices",
    fontsize=16,
    fontweight="bold",
    pad=18
)

ax.set_ylabel("Listing price (EUR)", fontsize=11)

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=10)

ax.set_ylim(0, max(mean_prices) * 1.2)

ax.legend(frameon=False)

# 7. 在柱子上显示价格
ax.bar_label(
    bars_mean,
    fmt="€%.2f",
    padding=4
)

ax.bar_label(
    bars_median,
    fmt="€%.2f",
    padding=4
)

# 8. 优化布局
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.grid(
    axis="y",
    alpha=0.15
)

ax.set_axisbelow(True)

fig.text(
    0.5, 0.01,
    "Entire home/apt | Priced listings only | "
    "Source: Inside Airbnb, Amsterdam (2026-09-16)",
    ha="center",
    fontsize=9,
    color="dimgray"
)

plt.tight_layout(rect=[0, 0.06, 1, 1])

# 9. 保存图表
output_path = (
    project_dir
    / "visualizations"
    / "01_neighbourhood_mean_median.png"
)

fig.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight"
)

print("Chart saved to:", output_path)

# 10. 显示图表
plt.show()
