# USDA-CN 数据模块文档

## 模块概览

USDA-CN 提供以下数据模块，覆盖USDA全部数据类别：

| 模块 | 类名 | 覆盖商品 |
|------|------|----------|
| [大田作物](field_crops.md) | `FieldCropsData` | 玉米、大豆、小麦、棉花、水稻等 |
| [水果坚果](fruit_nuts.md) | `FruitNutsData` | 苹果、橙子、杏仁、核桃、草莓等 |
| [蔬菜](vegetables.md) | `VegetablesData` | 番茄、马铃薯、生菜、胡萝卜等 |
| [畜牧](livestock.md) | `LivestockData` | 牛、猪、羊、山羊等 |
| [家禽](poultry.md) | `PoultryData` | 鸡、火鸡、鸭、鸡蛋等 |
| [乳制品](dairy.md) | `DairyData` | 牛奶、奶酪、黄油、冰淇淋等 |
| [农业经济](economics.md) | `EconomicsData` | 收入、支出、资产、土地价值等 |

## 基础使用

所有模块都继承自 `BaseDataFetcher` 基类，提供统一的使用接口：

```python
from usda_cn import FieldCropsData

# 创建实例
crops = FieldCropsData()

# 获取数据
data = crops.get_production(year=2024)

# 或使用专用方法
corn = crops.get_corn(year=2024)
```

## 通用方法

每个模块都提供以下通用方法：

| 方法 | 说明 |
|------|------|
| `get_production()` | 获取产量数据 |
| `get_area_planted()` | 获取种植面积 |
| `get_yield()` | 获取单产数据 |
| `get_price()` | 获取价格数据 |
| `get_summary()` | 获取数据汇总 |
| `get_top_states()` | 获取主产州排名 |
| `get_historical_trend()` | 获取历史趋势 |

## 快速示例

### 大田作物

```python
from usda_cn import FieldCropsData

crops = FieldCropsData()

# 玉米
corn = crops.get_corn(year=2024)
print(f"玉米产量: {corn['Value'].iloc[0]} 蒲式耳")

# 大豆
soybeans = crops.get_soybeans(year=2024)
print(f"大豆产量: {soybeans['Value'].iloc[0]} 蒲式耳")
```

### 畜牧

```python
from usda_cn import LivestockData

livestock = LivestockData()

# 牛存栏
cattle = livestock.get_cattle_inventory(year=2024)
print(f"牛存栏: {cattle['Value'].iloc[0]} 头")

# 猪存栏
hogs = livestock.get_hog_inventory(year=2024)
print(f"猪存栏: {hogs['Value'].iloc[0]} 头")
```

### 家禽

```python
from usda_cn import PoultryData

poultry = PoultryData()

# 鸡蛋产量
eggs = poultry.get_egg_production(year=2024)
print(f"鸡蛋产量: {eggs['Value'].iloc[0]}")
```

## 详细文档

- [大田作物模块](field_crops.md)
- [水果坚果模块](fruit_nuts.md)
- [蔬菜模块](vegetables.md)
- [畜牧模块](livestock.md)
- [家禽模块](poultry.md)
- [乳制品模块](dairy.md)
- [农业经济模块](economics.md)