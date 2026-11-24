
from pathlib import Path
import pandas as pd

# 找到项目根目录
project_dir = Path(__file__).resolve().parent.parent

# 第一份 SQL 导出的 CSV
csv_path = (
    project_dir
    / "outputs"
    / "01_neighbourhood_pricing.csv"
)

# 读取数据
df = pd.read_csv(csv_path)

# 检查行数、列数
print("Data shape:", df.shape)

# 检查字段名称
print("\nColumns:")
print(df.columns.tolist())

# 显示完整数据
print("\nData:")
print(df.to_string(index=False))

# 检查缺失值
print("\nMissing values:")
print(df.isna().sum())
