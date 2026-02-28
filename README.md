# USDA-CN 🌾

<div align="center">

**美国农业部(USDA)数据接口中文版**

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

</div>

---

## 简介

USDA-CN 是专为中文用户设计的 Python 库，用于获取美国农业部(USDA)的官方农业数据。覆盖USDA全部467种商品数据，提供简洁的中文接口。

**特点**：
- 🇨🇳 全中文接口
- 📦 覆盖USDA全部数据类别
- 🚀 简单易用，无需编程基础
- 📊 Pandas DataFrame输出

## 快速开始

### 安装

```bash
pip install usda-cn
```

### 配置

创建 `.env` 文件：
```
USDA_API_KEY=您的API密钥
```

[申请免费API密钥](https://quickstats.nass.usda.gov/api)

### 使用

```python
from usda_cn import NASSClient

client = NASSClient()

# 获取2024年大豆产量
data = client.get_soybean_production(year=2024)
print(f"产量: {data['Value'].iloc[0]} 蒲式耳")
```

## 📚 完整文档

详细文档请查看：[https://github.com/chan1919/USDA-CN/tree/main/docs](docs/)

| 文档 | 说明 |
|------|------|
| [安装指南](docs/installation.md) | 环境配置、安装步骤 |
| [快速开始](docs/quickstart.md) | 5分钟上手教程 |
| [API参考](docs/api_reference.md) | 所有接口详细说明 |
| [数据模块](docs/modules/README.md) | 各数据模块使用方法 |
| [常见问题](docs/faq.md) | 常见问题解答 |

## 数据覆盖

| 类别 | 模块 | 商品示例 |
|------|------|----------|
| 大田作物 | `FieldCropsData` | 玉米、大豆、小麦、棉花 |
| 水果坚果 | `FruitNutsData` | 苹果、橙子、杏仁、核桃 |
| 蔬菜 | `VegetablesData` | 番茄、马铃薯、生菜 |
| 畜牧 | `LivestockData` | 牛、猪、羊 |
| 家禽 | `PoultryData` | 鸡、火鸡、鸡蛋 |
| 乳制品 | `DairyData` | 牛奶、奶酪、黄油 |
| 农业经济 | `EconomicsData` | 收入、支出、资产 |

## 示例代码

### 获取多种作物数据

```python
from usda_cn import FieldCropsData

crops = FieldCropsData()

corn = crops.get_corn(year=2024)
wheat = crops.get_wheat(year=2024)
soybeans = crops.get_soybeans(year=2024)
```

### 获取畜牧数据

```python
from usda_cn import LivestockData

livestock = LivestockData()

cattle = livestock.get_cattle_inventory(year=2024)
hogs = livestock.get_hog_inventory(year=2024)
```

### 保存数据到CSV

```python
data = client.get_soybean_production(year={"ge": 2020, "le": 2024})
data.to_csv("大豆产量.csv", index=False, encoding='utf-8-sig')
```

## 安装

```bash
pip install usda-cn
```

详细安装步骤请查看 [安装指南](docs/installation.md)

## 许可证

MIT License

## 免责声明

本工具仅供研究和学习使用，数据来源于USDA官方API。不构成任何投资建议。

---

<div align="center">

**如果这个项目对您有帮助，请给一个 ⭐️ Star！**

Made with ❤️ for Chinese agricultural industry

</div>
