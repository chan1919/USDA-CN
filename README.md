# USDA-CN 🌾

<div align="center">

**美国农业部(USDA)数据接口中文版**

为中国产业用户提供的农业数据获取工具 - 覆盖USDA全部数据类别

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/pypi-0.2.0-orange.svg)](https://pypi.org/project/usda-cn/)

[English](README_EN.md) | 简体中文

</div>

---

## 📖 简介

USDA-CN 是一个专为中文用户设计的 Python 库，用于获取美国农业部(USDA)的农业统计数据。**覆盖USDA全部数据类别**，通过简洁的中文接口，您可以轻松获取农产品产量、价格、库存、畜牧存栏等官方数据。

### 主要特性

- 🇨🇳 **全中文接口** - 支持中文商品名称和统计类别
- 🚀 **简单易用** - 一行代码获取数据，无需学习复杂API
- 📊 **Pandas集成** - 返回标准DataFrame，便于数据分析
- 📦 **全面覆盖** - 覆盖USDA全部467种商品数据
- 🔒 **安全配置** - API密钥通过环境变量管理

### 数据覆盖

| 类别 | 模块 | 包含商品 |
|------|------|----------|
| **大田作物** | `FieldCropsData` | 玉米、大豆、小麦、棉花、水稻等 |
| **水果坚果** | `FruitNutsData` | 苹果、橙子、杏仁、核桃、草莓等 |
| **蔬菜** | `VegetablesData` | 番茄、马铃薯、生菜、胡萝卜等 |
| **畜牧** | `LivestockData` | 牛、猪、羊、山羊等 |
| **家禽** | `PoultryData` | 鸡、火鸡、鸭、鸡蛋等 |
| **乳制品** | `DairyData` | 牛奶、奶酪、黄油等 |
| **农业经济** | `EconomicsData` | 农场收入、支出、资产、土地价值等 |

## 🔧 安装

```bash
pip install usda-cn
```

## ⚙️ 配置

### 1. 申请API密钥

访问 [USDA Quick Stats API](https://quickstats.nass.usda.gov/api) 申请免费的API密钥。

### 2. 配置环境变量

创建 `.env` 文件：

```bash
USDA_API_KEY=YOUR_API_KEY_HERE
```

## 🚀 快速开始

### 基础用法

```python
from usda_cn import NASSClient

# 初始化客户端
client = NASSClient()

# 获取2024年全国大豆产量
df = client.get_soybean_production(year=2024)
print(df[["year", "Value", "unit_desc"]])
```

### 使用专用数据模块

```python
from usda_cn import FieldCropsData, LivestockData, PoultryData

# 大田作物
crops = FieldCropsData()
corn = crops.get_corn(year=2024)
wheat = crops.get_wheat(year=2024)
soybeans = crops.get_soybeans(year=2024)

# 畜牧
livestock = LivestockData()
cattle = livestock.get_cattle_inventory(year=2024)
hogs = livestock.get_hog_inventory(year=2024)

# 家禽
poultry = PoultryData()
chickens = poultry.get_chicken_inventory(year=2024)
eggs = poultry.get_egg_production(year=2024)
```

## 📚 API 参考

### 数据模块

| 模块 | 说明 | 主要方法 |
|------|------|----------|
| `FieldCropsData` | 大田作物 | `get_corn()`, `get_wheat()`, `get_soybeans()` |
| `FruitNutsData` | 水果坚果 | `get_apple_production()`, `get_orange_production()` |
| `VegetablesData` | 蔬菜 | `get_tomato_production()`, `get_potato_production()` |
| `LivestockData` | 畜牧 | `get_cattle_inventory()`, `get_hog_inventory()` |
| `PoultryData` | 家禽 | `get_chicken_inventory()`, `get_egg_production()` |
| `DairyData` | 乳制品 | `get_milk_production()`, `get_cheese_production()` |
| `EconomicsData` | 农业经济 | `get_cash_receipts()`, `get_net_income()` |

## 📄 许可证

MIT License

---

<div align="center">

**如果这个项目对您有帮助，请给一个 ⭐️ Star！**

Made with ❤️ for Chinese agricultural industry

</div>
