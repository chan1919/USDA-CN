# -*- coding: utf-8 -*-
"""
数据可视化示例
=============

展示如何使用 USDA-CN 获取数据并绘制图表。
"""

import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams["font.sans-serif"] = ["SimHei", "Arial Unicode MS"]
matplotlib.rcParams["axes.unicode_minus"] = False

from usda_cn import SoybeanData, CornData, WheatData

# 获取数据
soy = SoybeanData()
corn = CornData()
wheat = WheatData()

# 获取历史数据 (2015-2024)
years = {"ge": 2015, "le": 2024}

soy_production = soy.get_production(year=years)
corn_production = corn.get_production(year=years)
wheat_production = wheat.get_production(year=years)

# 创建图表
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. 产量趋势对比
ax1 = axes[0, 0]
if not soy_production.empty:
    soy_prod = soy_production.sort_values("year")
    ax1.plot(soy_prod["year"], soy_prod["Value_numeric"] / 1e9, "g-o", label="大豆", linewidth=2)
if not corn_production.empty:
    corn_prod = corn_production.sort_values("year")
    ax1.plot(corn_prod["year"], corn_prod["Value_numeric"] / 1e9, "b-s", label="玉米", linewidth=2)
if not wheat_production.empty:
    wheat_prod = wheat_production.sort_values("year")
    ax1.plot(wheat_prod["year"], wheat_prod["Value_numeric"] / 1e9, "y-^", label="小麦", linewidth=2)

ax1.set_title("美国主要农作物产量趋势 (2015-2024)", fontsize=14)
ax1.set_xlabel("年份")
ax1.set_ylabel("产量 (十亿蒲式耳)")
ax1.legend()
ax1.grid(True, alpha=0.3)

# 2. 大豆主产州排名
ax2 = axes[0, 1]
top_states = soy.get_top_states(year=2024, metric="production", top_n=10)
if not top_states.empty:
    colors = plt.cm.Greens(range(50, 250, 20))
    ax2.barh(top_states["州名"], top_states["Value_numeric"] / 1e6, color=colors)
    ax2.set_title("2024年美国大豆主产州排名", fontsize=14)
    ax2.set_xlabel("产量 (百万蒲式耳)")
    ax2.invert_yaxis()

# 3. 大豆单产趋势
ax3 = axes[1, 0]
soy_yield = soy.get_yield(year=years)
if not soy_yield.empty:
    yield_data = soy_yield.sort_values("year")
    ax3.plot(yield_data["year"], yield_data["Value_numeric"], "g-o", linewidth=2, markersize=8)
    ax3.fill_between(yield_data["year"], yield_data["Value_numeric"], alpha=0.3, color="green")
    ax3.set_title("美国大豆单产趋势 (2015-2024)", fontsize=14)
    ax3.set_xlabel("年份")
    ax3.set_ylabel("单产 (蒲式耳/英亩)")
    ax3.grid(True, alpha=0.3)

# 4. 大豆种植面积
ax4 = axes[1, 1]
soy_area = soy.get_area_planted(year=years)
if not soy_area.empty:
    area_data = soy_area.sort_values("year")
    ax4.bar(
        area_data["year"],
        area_data["Value_numeric"] / 1e6,
        color="forestgreen",
        edgecolor="darkgreen",
    )
    ax4.set_title("美国大豆种植面积 (2015-2024)", fontsize=14)
    ax4.set_xlabel("年份")
    ax4.set_ylabel("面积 (百万英亩)")
    ax4.set_xticks(area_data["year"])

plt.tight_layout()
plt.savefig("usda_cn_visualization.png", dpi=150, bbox_inches="tight")
print("图表已保存为 usda_cn_visualization.png")

# 显示图表
# plt.show()
