# API参考文档

本文档详细介绍USDA-CN的所有可用接口。

## 目录

- [核心客户端](#核心客户端)
- [数据模块](#数据模块)
- [通用方法](#通用方法)
- [查询参数](#查询参数)
- [返回数据结构](#返回数据结构)

---

## 核心客户端

### NASSClient

主要的API客户端类，用于连接USDA数据库。

```python
from usda_cn import NASSClient

# 使用环境变量中的API密钥
client = NASSClient()

# 或直接传入API密钥
client = NASSClient(api_key="YOUR_API_KEY")
```

#### 初始化参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `api_key` | str | 否 | USDA API密钥，未提供则从环境变量读取 |
| `base_url` | str | 否 | API基础URL，默认为官方地址 |
| `timeout` | int | 否 | 请求超时时间(秒)，默认30 |
| `retries` | int | 否 | 失败重试次数，默认3 |

#### 主要方法

##### get_soybean_production()

获取大豆产量数据。

```python
client.get_soybean_production(
    year=2024,           # 年份
    state="IA",          # 州代码（可选）
    agg_level="NATIONAL" # 地理级别
)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `year` | int/dict/list | 年份，支持单年、范围、列表 |
| `state` | str | 州代码，如 "IA", "IL" |
| `agg_level` | str | 地理聚合级别 |

**年份参数格式**：
```python
# 单年
year=2024

# 年份范围
year={"ge": 2020, "le": 2024}

# 多个年份
year=[2020, 2021, 2022, 2023, 2024]
```

##### get_soybean_area_planted()

获取大豆种植面积数据。

```python
client.get_soybean_area_planted(year=2024, state="IA")
```

##### get_soybean_yield()

获取大豆单产数据。

```python
client.get_soybean_yield(year=2024)
```

##### get_soybean_price()

获取大豆价格数据。

```python
client.get_soybean_price(year=2024)
```

##### get_soybean_stocks()

获取大豆库存数据。

```python
# 年度库存
client.get_soybean_stocks(year=2024)

# 特定时点库存
client.get_soybean_stocks(year=2024, reference_period="DEC 1")
```

**参考期间可选值**：
- `"YEAR"` - 年度
- `"DEC 1"` - 12月1日
- `"MAR 1"` - 3月1日
- `"JUN 1"` - 6月1日
- `"SEP 1"` - 9月1日

##### get_corn_production()

获取玉米产量数据。

```python
client.get_corn_production(year=2024)
```

##### get_wheat_production()

获取小麦产量数据。

```python
client.get_wheat_production(year=2024)
```

##### get_data()

通用数据查询接口，支持所有USDA参数。

```python
client.get_data(
    commodity="大豆",              # 商品名称（中英文均可）
    statistic_category="产量",     # 统计类别
    year=2024,                     # 年份
    state="IA",                    # 州代码
    agg_level="STATE",             # 地理级别
    format="dataframe"             # 返回格式
)
```

##### list_commodities()

获取所有可用商品列表。

```python
commodities = client.list_commodities()
print(f"可用商品数量: {len(commodities)}")
```

##### list_states()

获取所有可用州列表。

```python
states = client.list_states()
```

##### list_statistic_categories()

获取所有统计类别列表。

```python
categories = client.list_statistic_categories()
```

##### get_record_count()

获取查询结果的记录数量（执行前预估）。

```python
count = client.get_record_count(commodity_desc="SOYBEANS", year=2024)
print(f"将返回 {count} 条记录")
```

---

## 数据模块

### FieldCropsData - 大田作物

```python
from usda_cn import FieldCropsData

crops = FieldCropsData()
```

#### 可用方法

| 方法 | 说明 |
|------|------|
| `get_corn()` | 玉米 |
| `get_wheat()` | 小麦 |
| `get_soybeans()` | 大豆 |
| `get_cotton()` | 棉花 |
| `get_rice()` | 水稻 |
| `get_barley()` | 大麦 |
| `get_sorghum()` | 高粱 |
| `get_oats()` | 燕麦 |
| `get_hay()` | 干草 |
| `get_peanuts()` | 花生 |
| `get_sunflower()` | 向日葵 |
| `get_canola()` | 油菜籽 |

#### 示例

```python
crops = FieldCropsData()

# 获取玉米产量
corn = crops.get_corn(year=2024)
print(f"玉米产量: {corn['Value'].iloc[0]} 蒲式耳")

# 比较多种作物
comparison = crops.compare_crops(["CORN", "WHEAT", "SOYBEANS"], year=2024)
print(comparison)

# 列出所有支持的作物
print(crops.list_crops())
```

### LivestockData - 畜牧

```python
from usda_cn import LivestockData

livestock = LivestockData()
```

#### 可用方法

| 方法 | 说明 |
|------|------|
| `get_cattle_inventory()` | 牛存栏 |
| `get_beef_cows()` | 肉牛 |
| `get_milk_cows()` | 奶牛 |
| `get_cattle_on_feed()` | 育肥牛 |
| `get_calf_crop()` | 小牛产量 |
| `get_hog_inventory()` | 猪存栏 |
| `get_breeding_hogs()` | 种猪 |
| `get_market_hogs()` | 商品猪 |
| `get_pig_crop()` | 仔猪产量 |
| `get_sheep_inventory()` | 绵羊存栏 |
| `get_goat_inventory()` | 山羊存栏 |
| `get_slaughter()` | 屠宰数据 |

#### 示例

```python
livestock = LivestockData()

# 牛存栏
cattle = livestock.get_cattle_inventory(year=2024)
print(f"牛存栏: {cattle['Value'].iloc[0]} 头")

# 猪存栏
hogs = livestock.get_hog_inventory(year=2024)
print(f"猪存栏: {hogs['Value'].iloc[0]} 头")

# 获取数据汇总
summary = livestock.get_summary(year=2024)
print(summary)
```

### PoultryData - 家禽

```python
from usda_cn import PoultryData

poultry = PoultryData()
```

#### 可用方法

| 方法 | 说明 |
|------|------|
| `get_chicken_inventory()` | 鸡存栏 |
| `get_broiler_inventory()` | 肉鸡存栏 |
| `get_layer_inventory()` | 蛋鸡存栏 |
| `get_hen_inventory()` | 母鸡存栏 |
| `get_turkey_inventory()` | 火鸡存栏 |
| `get_duck_inventory()` | 鸭存栏 |
| `get_egg_production()` | 鸡蛋产量 |
| `get_eggs_hatched()` | 孵化蛋 |
| `get_eggs_set()` | 入孵蛋 |
| `get_chicks_placed()` | 雏鸡投放 |
| `get_rate_of_lay()` | 产蛋率 |
| `get_slaughter()` | 屠宰数据 |

#### 示例

```python
poultry = PoultryData()

# 鸡蛋产量
eggs = poultry.get_egg_production(year=2024)
print(f"鸡蛋产量: {eggs['Value'].iloc[0]}")

# 肉鸡存栏
broilers = poultry.get_broiler_inventory(year=2024)
print(f"肉鸡存栏: {broilers['Value'].iloc[0]} 只")
```

### DairyData - 乳制品

```python
from usda_cn import DairyData

dairy = DairyData()
```

#### 可用方法

| 方法 | 说明 |
|------|------|
| `get_milk_production()` | 牛奶产量 |
| `get_milk_price()` | 牛奶价格 |
| `get_milk_fat()` | 牛奶脂肪含量 |
| `get_cheese_production()` | 奶酪产量 |
| `get_butter_production()` | 黄油产量 |
| `get_cream_production()` | 奶油产量 |
| `get_ice_cream_production()` | 冰淇淋产量 |
| `get_dairy_product()` | 获取指定乳制品 |

#### 示例

```python
dairy = DairyData()

# 牛奶产量
milk = dairy.get_milk_production(year=2024)
print(f"牛奶产量: {milk['Value'].iloc[0]} 磅")

# 奶酪产量
cheese = dairy.get_cheese_production(year=2024)
print(f"奶酪产量: {cheese['Value'].iloc[0]} 磅")
```

### EconomicsData - 农业经济

```python
from usda_cn import EconomicsData

econ = EconomicsData()
```

#### 可用方法

| 方法 | 说明 |
|------|------|
| `get_cash_receipts()` | 农业现金收入 |
| `get_crop_receipts()` | 作物收入 |
| `get_livestock_receipts()` | 畜牧收入 |
| `get_gross_income()` | 农场总收入 |
| `get_net_income()` | 农场净收入 |
| `get_government_payments()` | 政府补贴 |
| `get_production_expenses()` | 生产支出 |
| `get_feed_expenses()` | 饲料支出 |
| `get_fertilizer_expenses()` | 肥料支出 |
| `get_chemical_expenses()` | 农药支出 |
| `get_farm_assets()` | 农场资产 |
| `get_land_value()` | 农地价值 |
| `get_farm_debt()` | 农场负债 |
| `get_farm_count()` | 农场数量 |
| `get_farm_size()` | 农场规模 |

#### 示例

```python
econ = EconomicsData()

# 农业现金收入
receipts = econ.get_cash_receipts(year=2024)
print(f"农业现金收入: ${receipts['Value'].iloc[0]}")

# 农地价值
land = econ.get_land_value(year=2024)
print(f"农地价值: ${land['Value'].iloc[0]}/英亩")

# 比较各州
comparison = econ.compare_states(["IA", "IL", "MN"], year=2024, metric="cash_receipts")
print(comparison)
```

---

## 通用方法

所有数据模块都继承以下通用方法：

### get_production()

获取产量数据。

```python
crops = FieldCropsData()
production = crops.get_production(year=2024)
```

### get_area_planted()

获取种植面积数据。

```python
area = crops.get_area_planted(year=2024)
```

### get_area_harvested()

获取收获面积数据。

```python
area = crops.get_area_harvested(year=2024)
```

### get_yield()

获取单产数据。

```python
yield_data = crops.get_yield(year=2024)
```

### get_price()

获取价格数据。

```python
price = crops.get_price(year=2024)
```

### get_stocks()

获取库存数据。

```python
stocks = crops.get_stocks(year=2024, reference_period="DEC 1")
```

### get_summary()

获取数据汇总。

```python
summary = crops.get_summary(year=2024)
print(summary)
```

### get_top_states()

获取主产州排名。

```python
top_states = crops.get_top_states(year=2024, metric="production", top_n=10)
print(top_states)
```

### get_historical_trend()

获取历史趋势数据。

```python
trend = crops.get_historical_trend(start_year=2010, end_year=2024)
print(trend)
```

---

## 查询参数

### 商品名称 (commodity)

支持中英文输入：

```python
# 中文
client.get_data("大豆", year=2024)
client.get_data("玉米", year=2024)
client.get_data("小麦", year=2024)

# 英文
client.get_data("SOYBEANS", year=2024)
client.get_data("CORN", year=2024)
client.get_data("WHEAT", year=2024)
```

### 统计类别 (statistic_category)

```python
# 中文
client.get_data("大豆", "产量", year=2024)
client.get_data("大豆", "种植面积", year=2024)
client.get_data("大豆", "单产", year=2024)
client.get_data("大豆", "价格", year=2024)

# 英文
client.get_data("SOYBEANS", "PRODUCTION", year=2024)
client.get_data("SOYBEANS", "AREA PLANTED", year=2024)
```

### 地理聚合级别 (agg_level)

| 中文 | 英文 |
|------|------|
| 全国 | NATIONAL |
| 州 | STATE |
| 县 | COUNTY |

```python
# 全国数据
client.get_soybean_production(year=2024, agg_level="NATIONAL")

# 各州数据
client.get_soybean_production(year=2024, agg_level="STATE")

# 各县数据
client.get_soybean_production(year=2024, agg_level="COUNTY", state="IA")
```

### 年份参数

```python
# 单年
year=2024

# 大于等于
year={"ge": 2020}

# 小于等于
year={"le": 2024}

# 范围
year={"ge": 2020, "le": 2024}

# 多个年份
year=[2020, 2021, 2022, 2023, 2024]
```

### 州代码

常用州代码：

| 代码 | 州名 | 主要产品 |
|------|------|----------|
| IA | 爱荷华州 | 玉米、大豆、猪 |
| IL | 伊利诺伊州 | 玉米、大豆 |
| MN | 明尼苏达州 | 玉米、大豆 |
| NE | 内布拉斯加州 | 玉米、牛 |
| KS | 堪萨斯州 | 小麦、牛 |
| TX | 得克萨斯州 | 棉花、牛 |
| CA | 加利福尼亚州 | 水果、乳制品 |

---

## 返回数据结构

所有方法返回Pandas DataFrame，包含以下常用字段：

| 字段 | 说明 |
|------|------|
| `year` | 年份 |
| `Value` | 数值（字符串格式，可能包含逗号） |
| `Value_numeric` | 数值（数字格式，自动转换） |
| `unit_desc` | 单位 |
| `state_alpha` | 州代码 |
| `state_name` | 州名称 |
| `commodity_desc` | 商品名称 |
| `statisticcat_desc` | 统计类别 |
| `agg_level_desc` | 地理聚合级别 |

### 示例

```python
from usda_cn import NASSClient

client = NASSClient()
data = client.get_soybean_production(year=2024)

# 查看列名
print(data.columns.tolist())

# 访问数值
value = data['Value'].iloc[0]           # "4,374,228,000"
value_num = data['Value_numeric'].iloc[0] # 4374228000.0
unit = data['unit_desc'].iloc[0]        # "BU"
```

---

## 错误处理

```python
from usda_cn import NASSClient

client = NASSClient()

try:
    data = client.get_soybean_production(year=2024)
    if data.empty:
        print("没有找到数据")
    else:
        print(f"获取成功: {data['Value'].iloc[0]}")
except ValueError as e:
    print(f"参数错误: {e}")
except PermissionError as e:
    print(f"API密钥无效: {e}")
except Exception as e:
    print(f"发生错误: {e}")
```