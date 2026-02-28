# USDA-CN 🌾

<div align="center">

**美国农业部(USDA)数据接口中文版**

为中国产业用户提供的农业数据获取工具

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/pypi-0.1.0-orange.svg)](https://pypi.org/project/usda-cn/)

[English](README_EN.md) | 简体中文

</div>

---

## 📖 简介

USDA-CN 是一个专为中文用户设计的 Python 库，用于获取美国农业部(USDA)的农业统计数据。通过简洁的中文接口，您可以轻松获取大豆、玉米、小麦等主要农产品的产量、价格、库存等官方数据。

### 主要特性

- 🇨🇳 **全中文接口** - 支持中文商品名称和统计类别
- 🚀 **简单易用** - 一行代码获取数据，无需学习复杂API
- 📊 **Pandas集成** - 返回标准DataFrame，便于数据分析
- 🔒 **安全配置** - API密钥通过环境变量管理
- 📦 **完整数据** - 覆盖NASS、PSD等多个数据源

## 🔧 安装

### 通过 pip 安装

```bash
pip install usda-cn
```

### 从源码安装

```bash
git clone https://github.com/usda-cn/usda-cn.git
cd usda-cn
pip install -e .
```

## ⚙️ 配置

### 1. 申请API密钥

访问 [USDA Quick Stats API](https://quickstats.nass.usda.gov/api) 申请免费的API密钥。

### 2. 配置环境变量

创建 `.env` 文件：

```bash
# 复制示例文件
cp .env.example .env

# 编辑 .env 文件，填入您的API密钥
USDA_API_KEY=YOUR_API_KEY_HERE
```

或者在代码中直接传入：

```python
from usda_cn import NASSClient

client = NASSClient(api_key="YOUR_API_KEY")
```

## 🚀 快速开始

### 基础用法

```python
from usda_cn import NASSClient

# 初始化客户端（自动从 .env 读取 API 密钥）
client = NASSClient()

# 获取2024年全国大豆产量
df = client.get_soybean_production(year=2024)
print(df[["year", "Value", "unit_desc"]])

# 输出:
#    year         Value    unit_desc
# 0  2024  4,374,228,000          BU
```

### 使用大豆数据模块

```python
from usda_cn import SoybeanData

# 创建大豆数据获取器
soy = SoybeanData()

# 获取产量数据
production = soy.get_production(year=2024)
print(f"2024年大豆产量: {production['Value'].iloc[0]} 蒲式耳")

# 获取种植面积
area = soy.get_area_planted(year=2024)
print(f"2024年大豆种植面积: {area['Value'].iloc[0]} 英亩")

# 获取单产
yield_df = soy.get_yield(year=2024)
print(f"2024年大豆单产: {yield_df['Value'].iloc[0]} 蒲式耳/英亩")

# 获取价格
price = soy.get_price(year=2024)
print(f"2024年大豆价格: ${price['Value'].iloc[0]}/蒲式耳")

# 获取库存
stocks = soy.get_stocks(year=2024)
print(f"2024年大豆库存: {stocks['Value'].iloc[0]} 蒲式耳")

# 获取数据汇总
summary = soy.get_summary(year=2024)
print(summary)
```

### 按州获取数据

```python
from usda_cn import SoybeanData

soy = SoybeanData()

# 获取爱荷华州(IA)大豆产量
df = soy.get_production(year=2024, state="IA")
print(f"爱荷华州2024年大豆产量: {df['Value'].iloc[0]} 蒲式耳")

# 获取各州产量排名
top_states = soy.get_top_states(year=2024, metric="production", top_n=10)
print(top_states)
```

### 历史数据

```python
from usda_cn import SoybeanData

soy = SoybeanData()

# 获取最近5年数据
df = soy.get_production(year={"ge": 2020, "le": 2024})

# 获取历史趋势
trend = soy.get_historical_trend(start_year=2010, end_year=2024)

# 绘制趋势图
import matplotlib.pyplot as plt
trend.plot(x="year", y="Value_numeric", kind="line")
plt.title("美国大豆产量趋势 (2010-2024)")
plt.xlabel("年份")
plt.ylabel("产量 (蒲式耳)")
plt.show()
```

### 玉米和小麦数据

```python
from usda_cn import CornData, WheatData

# 玉米数据
corn = CornData()
corn_production = corn.get_production(year=2024)
print(f"2024年玉米产量: {corn_production['Value'].iloc[0]} 蒲式耳")

# 小麦数据
wheat = WheatData()
wheat_production = wheat.get_production(year=2024)
print(f"2024年小麦产量: {wheat_production['Value'].iloc[0]} 蒲式耳")
```

### 高级查询

```python
from usda_cn import NASSClient

client = NASSClient()

# 使用中文参数
df = client.get_data(
    commodity="大豆",           # 支持中文
    statistic_category="产量",
    year={"ge": 2020, "le": 2024},
    state="IA",
    agg_level="STATE"
)

# 使用英文参数
df = client.get_data(
    commodity="SOYBEANS",
    statistic_category="PRODUCTION",
    year=2024
)

# 查询所有可用商品
commodities = client.list_commodities()
print(f"可用商品数量: {len(commodities)}")

# 查询所有州
states = client.list_states()
print(f"可用州数量: {len(states)}")
```

## 📚 API 参考

### NASSClient

主要的API客户端类。

```python
from usda_cn import NASSClient

client = NASSClient(api_key="YOUR_KEY")
```

#### 方法

| 方法 | 说明 | 参数 |
|------|------|------|
| `get_data()` | 通用数据查询 | commodity, statistic_category, year, state, agg_level |
| `get_soybean_production()` | 大豆产量 | year, state, agg_level |
| `get_soybean_area_planted()` | 大豆种植面积 | year, state, agg_level |
| `get_soybean_yield()` | 大豆单产 | year, state, agg_level |
| `get_soybean_price()` | 大豆价格 | year, state |
| `get_soybean_stocks()` | 大豆库存 | year, reference_period |
| `get_corn_production()` | 玉米产量 | year, state, agg_level |
| `get_wheat_production()` | 小麦产量 | year, state, agg_level |
| `list_commodities()` | 商品列表 | - |
| `list_states()` | 州列表 | - |
| `list_statistic_categories()` | 统计类别列表 | - |

### SoybeanData

大豆专用数据获取器。

```python
from usda_cn import SoybeanData

soy = SoybeanData()
```

#### 方法

| 方法 | 说明 | 返回单位 |
|------|------|----------|
| `get_production()` | 产量数据 | 蒲式耳 (BU) |
| `get_area_planted()` | 种植面积 | 英亩 (ACRES) |
| `get_area_harvested()` | 收获面积 | 英亩 (ACRES) |
| `get_yield()` | 单产 | 蒲式耳/英亩 |
| `get_price()` | 价格 | 美元/蒲式耳 |
| `get_stocks()` | 库存 | 蒲式耳 (BU) |
| `get_crush()` | 压榨量 | 蒲式耳 (BU) |
| `get_summary()` | 数据汇总 | DataFrame |
| `get_top_states()` | 主产州排名 | DataFrame |
| `get_historical_trend()` | 历史趋势 | DataFrame |

### 参数说明

#### 商品名称 (commodity)

| 中文 | 英文 |
|------|------|
| 大豆 | SOYBEANS |
| 玉米 | CORN |
| 小麦 | WHEAT |
| 棉花 | COTTON |
| 水稻 | RICE |

#### 统计类别 (statistic_category)

| 中文 | 英文 |
|------|------|
| 产量 | PRODUCTION |
| 种植面积 | AREA PLANTED |
| 收获面积 | AREA HARVESTED |
| 单产 | YIELD |
| 价格 | PRICE RECEIVED |
| 库存 | STOCKS |

#### 地理聚合级别 (agg_level)

| 中文 | 英文 |
|------|------|
| 全国 | NATIONAL |
| 州 | STATE |
| 县 | COUNTY |

#### 主要生产州代码

**大豆主产州:**
- IA (爱荷华) - 第一大产区
- IL (伊利诺伊)
- MN (明尼苏达)
- NE (内布拉斯加)
- IN (印第安纳)

## 📊 数据源说明

### NASS Quick Stats

美国国家农业统计局(NASS)的官方统计数据库，包含：

- 作物产量、面积、单产
- 价格数据
- 库存数据
- 畜牧业数据

**数据更新频率:** 年度、季度、月度

### FAS PSD

美国外国农业服务局(FAS)的全球供需数据库，包含：

- 全球产量数据
- 进出口数据
- 期末库存
- 消费数据

**覆盖国家:** 100+ 国家

## 🛠️ 开发

### 运行测试

```bash
pip install -e ".[dev]"
pytest tests/
```

### 代码格式化

```bash
black usda_cn/
isort usda_cn/
```

### 类型检查

```bash
mypy usda_cn/
```

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- 数据来源: [USDA National Agricultural Statistics Service](https://www.nass.usda.gov/)
- API文档: [Quick Stats API](https://quickstats.nass.usda.gov/api)

## ⚠️ 免责声明

本工具仅供研究和学习使用，数据来源于USDA官方API。使用本工具获取的数据仅供参考，不构成任何投资建议。

---

<div align="center">

**如果这个项目对您有帮助，请给一个 ⭐️ Star！**

Made with ❤️ for Chinese agricultural industry

</div>