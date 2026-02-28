# 大田作物模块 (FieldCropsData)

## 概述

大田作物模块提供所有主要大田作物的数据获取接口。

## 覆盖商品

### 谷物类
- 玉米 (CORN)
- 小麦 (WHEAT)
- 大麦 (BARLEY)
- 燕麦 (OATS)
- 高粱 (SORGHUM)
- 水稻 (RICE)

### 油料类
- 大豆 (SOYBEANS)
- 油菜籽 (CANOLA)
- 向日葵 (SUNFLOWER)
- 花生 (PEANUTS)

### 纤维类
- 棉花 (COTTON)

### 饲料类
- 干草 (HAY)

## 快速开始

```python
from usda_cn import FieldCropsData

crops = FieldCropsData()

# 获取玉米产量
corn = crops.get_corn(year=2024)
print(f"玉米产量: {corn['Value'].iloc[0]} 蒲式耳")

# 获取大豆产量
soybeans = crops.get_soybeans(year=2024)
print(f"大豆产量: {soybeans['Value'].iloc[0]} 蒲式耳")
```

## 专用方法

### 玉米相关

```python
# 玉米产量
corn = crops.get_corn(year=2024)

# 玉米种植面积
corn_area = crops.get_corn_area_planted(year=2024)

# 玉米单产
corn_yield = crops.get_corn_yield(year=2024)

# 玉米价格
corn_price = crops.get_corn_price(year=2024)
```

### 小麦相关

```python
# 小麦产量
wheat = crops.get_wheat(year=2024)

# 小麦种植面积
wheat_area = crops.get_wheat_area_planted(year=2024)

# 小麦单产
wheat_yield = crops.get_wheat_yield(year=2024)
```

### 大豆相关

```python
# 大豆产量
soybeans = crops.get_soybeans(year=2024)

# 大豆种植面积
soybeans_area = crops.get_soybeans_area_planted(year=2024)

# 大豆单产
soybeans_yield = crops.get_soybeans_yield(year=2024)

# 大豆价格
soybeans_price = crops.get_soybeans_price(year=2024)
```

### 其他作物

```python
# 棉花
cotton = crops.get_cotton(year=2024)

# 水稻
rice = crops.get_rice(year=2024)

# 大麦
barley = crops.get_barley(year=2024)

# 高粱
sorghum = crops.get_sorghum(year=2024)

# 燕麦
oats = crops.get_oats(year=2024)

# 干草
hay = crops.get_hay(year=2024)

# 花生
peanuts = crops.get_peanuts(year=2024)

# 向日葵
sunflower = crops.get_sunflower(year=2024)

# 油菜籽
canola = crops.get_canola(year=2024)
```

## 通用方法

### get_commodity_data()

获取指定作物的数据。

```python
# 获取玉米产量
data = crops.get_commodity_data("CORN", statistic="PRODUCTION", year=2024)

# 支持中文
data = crops.get_commodity_data("玉米", year=2024)
```

### compare_crops()

比较多种作物的数据。

```python
# 比较玉米、小麦、大豆的产量
comparison = crops.compare_crops(
    crops=["CORN", "WHEAT", "SOYBEANS"],
    year=2024,
    metric="production"
)
print(comparison)
```

### list_crops()

列出所有支持的大田作物。

```python
print(crops.list_crops())
```

输出：
```
     英文   中文      默认单位
0    CORN   玉米         BU
1    WHEAT  小麦         BU
2   SOYBEANS 大豆         BU
...
```

## 按州获取数据

```python
from usda_cn import FieldCropsData

crops = FieldCropsData()

# 获取爱荷华州玉米产量
ia_corn = crops.get_corn(year=2024, state="IA")
print(f"爱荷华州玉米产量: {ia_corn['Value'].iloc[0]} 蒲式耳")

# 获取伊利诺伊州大豆产量
il_soybeans = crops.get_soybeans(year=2024, state="IL")
print(f"伊利诺伊州大豆产量: {il_soybeans['Value'].iloc[0]} 蒲式耳")
```

## 历史趋势

```python
# 获取2010-2024年玉米产量趋势
trend = crops.get_historical_trend(
    start_year=2010,
    end_year=2024,
    metric="production"
)

# 绘制趋势图（需要matplotlib）
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.plot(trend['year'], trend['Value_numeric'])
plt.title("美国玉米产量趋势 (2010-2024)")
plt.xlabel("年份")
plt.ylabel("产量 (蒲式耳)")
plt.grid(True)
plt.show()
```

## 主产州排名

```python
# 获取玉米主产州前10名
top_states = crops.get_top_states(
    year=2024,
    metric="production",
    top_n=10
)
print(top_states)
```

输出示例：
```
  state_alpha   州名  year        Value unit_desc
0          IA  爱荷华  2024  2,500,000,000      BU
1          IL 伊利诺伊  2024  2,200,000,000      BU
2          NE 内布拉斯加 2024  1,800,000,000      BU
...
```

## 数据汇总

```python
# 获取2024年数据汇总
summary = crops.get_summary(year=2024)
print(summary)
```

输出示例：
```
     指标     年份           数值        单位
  种植面积  2024    90,909,000     ACRES
    单产  2024         179.3  BU / ACRE
    产量  2024  14,891,756,000        BU
```

## 完整示例

```python
from usda_cn import FieldCropsData
import pandas as pd

# 创建实例
crops = FieldCropsData()

print("=" * 60)
print("2024年美国主要作物产量报告")
print("=" * 60)

# 获取各作物产量
corn = crops.get_corn(year=2024)
wheat = crops.get_wheat(year=2024)
soybeans = crops.get_soybeans(year=2024)
cotton = crops.get_cotton(year=2024)
rice = crops.get_rice(year=2024)

# 打印报告
print(f"\n玉米产量:  {corn['Value'].iloc[0]:>20} 蒲式耳")
print(f"小麦产量:  {wheat['Value'].iloc[0]:>20} 蒲式耳")
print(f"大豆产量:  {soybeans['Value'].iloc[0]:>20} 蒲式耳")
print(f"棉花产量:  {cotton['Value'].iloc[0]:>20} 包")
print(f"水稻产量:  {rice['Value'].iloc[0]:>20} 英担")

print("\n" + "=" * 60)

# 保存到CSV
all_data = []
for crop_name, method in [
    ("玉米", crops.get_corn),
    ("小麦", crops.get_wheat),
    ("大豆", crops.get_soybeans),
]:
    data = method(year=2024)
    if not data.empty:
        all_data.append({
            "作物": crop_name,
            "产量": data['Value'].iloc[0],
            "单位": data['unit_desc'].iloc[0]
        })

df = pd.DataFrame(all_data)
df.to_csv("2024年作物产量.csv", index=False, encoding='utf-8-sig')
print("数据已保存到 2024年作物产量.csv")
```