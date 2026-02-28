# -*- coding: utf-8 -*-
"""
USDA-CN 使用示例
===============

本示例展示如何使用 USDA-CN 库获取美国农业部数据。
"""

# ============================================================
# 示例 1: 基础用法
# ============================================================

from usda_cn import NASSClient

# 方式1: 使用环境变量中的API密钥 (推荐)
# 首先创建 .env 文件并设置 USDA_API_KEY=YOUR_KEY
client = NASSClient()

# 方式2: 直接传入API密钥
# client = NASSClient(api_key="YOUR_API_KEY")

# 获取2024年全国大豆产量
print("=" * 50)
print("示例1: 获取大豆产量数据")
print("=" * 50)

df = client.get_soybean_production(year=2024)
if not df.empty:
    row = df.iloc[0]
    print(f"年份: {row['year']}")
    print(f"产量: {row['Value']} {row['unit_desc']}")


# ============================================================
# 示例 2: 使用 SoybeanData 模块
# ============================================================

from usda_cn import SoybeanData

print("\n" + "=" * 50)
print("示例2: 使用 SoybeanData 模块")
print("=" * 50)

soy = SoybeanData()

# 获取数据汇总
summary = soy.get_summary(year=2024)
print("\n2024年美国大豆数据汇总:")
print(summary.to_string(index=False))


# ============================================================
# 示例 3: 获取各州数据排名
# ============================================================

print("\n" + "=" * 50)
print("示例3: 大豆主产州排名 (2024)")
print("=" * 50)

top_states = soy.get_top_states(year=2024, metric="production", top_n=5)
print(top_states.to_string(index=False))


# ============================================================
# 示例 4: 历史趋势数据
# ============================================================

print("\n" + "=" * 50)
print("示例4: 大豆产量历史趋势 (2020-2024)")
print("=" * 50)

trend = soy.get_historical_trend(start_year=2020, end_year=2024)
for _, row in trend.iterrows():
    print(f"{row['year']}: {row['Value']} {row['unit_desc']}")


# ============================================================
# 示例 5: 获取价格和库存数据
# ============================================================

print("\n" + "=" * 50)
print("示例5: 价格和库存数据")
print("=" * 50)

# 价格数据
price = soy.get_price(year={"ge": 2020, "le": 2024})
print("\n大豆价格趋势:")
for _, row in price.head(5).iterrows():
    print(f"  {row['year']}: ${row['Value']}")

# 库存数据
stocks = soy.get_stocks(year=2024, reference_period="DEC 1")
if not stocks.empty:
    print(f"\n2024年12月1日大豆库存: {stocks['Value'].iloc[0]} 蒲式耳")


# ============================================================
# 示例 6: 玉米和小麦数据
# ============================================================

from usda_cn import CornData, WheatData

print("\n" + "=" * 50)
print("示例6: 玉米和小麦数据")
print("=" * 50)

# 玉米
corn = CornData()
corn_summary = corn.get_summary(year=2024)
print("\n2024年美国玉米数据汇总:")
print(corn_summary.to_string(index=False))

# 小麦
wheat = WheatData()
wheat_summary = wheat.get_summary(year=2024)
print("\n2024年美国小麦数据汇总:")
print(wheat_summary.to_string(index=False))


# ============================================================
# 示例 7: 高级查询
# ============================================================

print("\n" + "=" * 50)
print("示例7: 高级查询")
print("=" * 50)

# 查询所有可用商品
commodities = client.list_commodities()
print(f"\n可用商品数量: {len(commodities)}")
print(f"前10个商品: {commodities['commodity_en'].head(10).tolist()}")

# 查询所有统计类别
categories = client.list_statistic_categories()
print(f"\n可用统计类别数量: {len(categories)}")
print(f"前10个类别: {categories['statistic_cn'].head(10).tolist()}")

# 检查记录数量
count = client.get_record_count(commodity_desc="SOYBEANS", year=2024)
print(f"\n2024年大豆数据记录数: {count}")


print("\n" + "=" * 50)
print("示例完成!")
print("=" * 50)
