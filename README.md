# USDA-CN 🌾

<div align="center">

**美国农业部(USDA)数据接口中文版**

**专为中文用户设计 | 简单易用 | 无需编程基础**

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

</div>

---

## 📖 这是什么？

USDA-CN 是一个**免费的Python工具库**，帮助您轻松获取美国农业部(USDA)的官方农业数据。

**适合谁使用？**
- 🌾 农产品贸易商 - 获取产量、价格数据
- 📊 金融分析师 - 分析农产品市场趋势
- 🏢 企业决策者 - 了解农产品供应情况
- 🎓 研究人员 - 获取可靠的农业统计数据
- 📰 媒体工作者 - 获取权威数据来源

**不需要高级编程技能！** 只要会复制粘贴代码就能用。

---

## 🚀 快速开始（5分钟上手）

### 第一步：安装Python

如果您还没有安装Python：

1. 访问 [Python官网](https://www.python.org/downloads/)
2. 下载 Python 3.8 或更高版本
3. 安装时勾选 **"Add Python to PATH"**

### 第二步：安装USDA-CN

打开命令提示符（Windows按 `Win+R`，输入 `cmd`），然后输入：

```bash
pip install usda-cn
```

### 第三步：申请免费API密钥

1. 访问 https://quickstats.nass.usda.gov/api
2. 填写邮箱地址（不需要其他信息）
3. 几秒钟后会收到邮件，里面有您的API密钥

**API密钥示例**：`4AB84799-0BD2-3EBA-AC70-03E51B016275`

### 第四步：创建配置文件

在您的项目文件夹中创建一个名为 `.env` 的文件，内容如下：

```
USDA_API_KEY=这里填您的API密钥
```

### 第五步：运行第一个程序

创建一个文件 `test.py`，复制以下代码：

```python
from usda_cn import NASSClient

# 连接USDA数据库
client = NASSClient()

# 获取2024年美国大豆产量
data = client.get_soybean_production(year=2024)

# 打印结果
print("2024年美国大豆产量：")
print(data)
```

运行：`python test.py`

**恭喜！您已经成功获取了USDA数据！** 🎉

---

## 📚 详细使用教程

### 1. 获取大豆数据

```python
from usda_cn import NASSClient

client = NASSClient()

# 获取大豆产量
production = client.get_soybean_production(year=2024)
print("产量：", production['Value'].iloc[0], "蒲式耳")

# 获取大豆种植面积
area = client.get_soybean_area_planted(year=2024)
print("种植面积：", area['Value'].iloc[0], "英亩")

# 获取大豆单产
yield_data = client.get_soybean_yield(year=2024)
print("单产：", yield_data['Value'].iloc[0], "蒲式耳/英亩")

# 获取大豆价格
price = client.get_soybean_price(year=2024)
print("价格：$", price['Value'].iloc[0], "/蒲式耳")
```

### 2. 获取历史数据

```python
from usda_cn import NASSClient

client = NASSClient()

# 获取2020-2024年的大豆产量（5年数据）
data = client.get_soybean_production(year={"ge": 2020, "le": 2024})

# 按年份排序显示
for index, row in data.iterrows():
    print(f"{row['year']}年: {row['Value']} 蒲式耳")
```

### 3. 获取各州数据

```python
from usda_cn import NASSClient

client = NASSClient()

# 获取爱荷华州(IA)的大豆产量
data = client.get_soybean_production(year=2024, state="IA")
print("爱荷华州大豆产量：", data['Value'].iloc[0])

# 主要大豆生产州代码：
# IA = 爱荷华州（第一大产区）
# IL = 伊利诺伊州
# MN = 明尼苏达州
# NE = 内布拉斯加州
# IN = 印第安纳州
```

### 4. 保存数据到Excel

```python
from usda_cn import NASSClient

client = NASSClient()

# 获取数据
data = client.get_soybean_production(year={"ge": 2020, "le": 2024})

# 保存为CSV文件（可用Excel打开）
data.to_csv("大豆产量.csv", index=False, encoding='utf-8-sig')
print("数据已保存到 大豆产量.csv")
```

---

## 🌽 所有可用数据类型

### 大田作物 (FieldCropsData)

包括：玉米、大豆、小麦、棉花、水稻、大麦、燕麦、高粱、花生、向日葵等

```python
from usda_cn import FieldCropsData

crops = FieldCropsData()

# 玉米
corn = crops.get_corn(year=2024)

# 小麦
wheat = crops.get_wheat(year=2024)

# 大豆
soybeans = crops.get_soybeans(year=2024)

# 棉花
cotton = crops.get_cotton(year=2024)

# 水稻
rice = crops.get_rice(year=2024)
```

### 畜牧产品 (LivestockData)

包括：牛、猪、羊、山羊等

```python
from usda_cn import LivestockData

livestock = LivestockData()

# 牛存栏量
cattle = livestock.get_cattle_inventory(year=2024)
print("牛存栏：", cattle['Value'].iloc[0], "头")

# 猪存栏量
hogs = livestock.get_hog_inventory(year=2024)
print("猪存栏：", hogs['Value'].iloc[0], "头")

# 绵羊存栏量
sheep = livestock.get_sheep_inventory(year=2024)
print("绵羊存栏：", sheep['Value'].iloc[0], "头")
```

### 家禽产品 (PoultryData)

包括：鸡、火鸡、鸡蛋等

```python
from usda_cn import PoultryData

poultry = PoultryData()

# 鸡存栏量
chickens = poultry.get_chicken_inventory(year=2024)

# 鸡蛋产量
eggs = poultry.get_egg_production(year=2024)

# 火鸡存栏量
turkeys = poultry.get_turkey_inventory(year=2024)
```

### 乳制品 (DairyData)

包括：牛奶、奶酪、黄油等

```python
from usda_cn import DairyData

dairy = DairyData()

# 牛奶产量
milk = dairy.get_milk_production(year=2024)

# 奶酪产量
cheese = dairy.get_cheese_production(year=2024)

# 黄油产量
butter = dairy.get_butter_production(year=2024)
```

### 农业经济 (EconomicsData)

包括：农场收入、支出、土地价值等

```python
from usda_cn import EconomicsData

econ = EconomicsData()

# 农业现金收入
receipts = econ.get_cash_receipts(year=2024)

# 农场净收入
income = econ.get_net_income(year=2024)

# 农地价值
land = econ.get_land_value(year=2024)
```

---

## 📊 数据说明

### 数据来源

所有数据来自美国农业部国家农业统计局(NASS)的官方数据库，是**最权威**的美国农业数据来源。

### 数据更新频率

| 数据类型 | 更新频率 |
|----------|----------|
| 作物产量 | 年度 |
| 种植面积 | 年度 |
| 畜牧存栏 | 季度/年度 |
| 价格数据 | 月度/年度 |
| 库存数据 | 季度 |

### 常用单位说明

| 单位 | 中文含义 |
|------|----------|
| BU | 蒲式耳（约35.24升） |
| ACRE | 英亩（约6.07亩） |
| LB | 磅（约0.45公斤） |
| CWT | 英担（100磅） |
| HEAD | 头（牲畜计数） |

---

## ❓ 常见问题

### Q1: 提示 "未找到API密钥" 怎么办？

**答**：请确保：
1. 已经申请了API密钥
2. 在项目文件夹中创建了 `.env` 文件
3. `.env` 文件内容格式正确：`USDA_API_KEY=您的密钥`

### Q2: 返回的数据为空怎么办？

**答**：可能是查询条件太严格。尝试：
- 不指定年份（获取最近数据）
- 检查州代码是否正确
- 尝试不同的统计类别

### Q3: 数据更新频率是多少？

**答**：
- 作物产量数据：每年10月更新最终数据
- 畜牧存栏数据：每季度更新
- 价格数据：每月更新

### Q4: 如何获取多个州的数据？

**答**：
```python
from usda_cn import FieldCropsData

crops = FieldCropsData()

# 获取所有州的数据
data = crops.get_corn(year=2024, agg_level="STATE")

# 查看数据
print(data[['state_alpha', 'Value']])
```

### Q5: 如何处理错误？

**答**：
```python
from usda_cn import NASSClient

client = NASSClient()

try:
    data = client.get_soybean_production(year=2024)
    if data.empty:
        print("没有找到数据")
    else:
        print("获取成功：", data['Value'].iloc[0])
except Exception as e:
    print("出错了：", e)
```

---

## 📦 完整示例代码

### 示例1：生成大豆年度报告

```python
from usda_cn import NASSClient

client = NASSClient()

print("=" * 50)
print("美国大豆年度报告（2020-2024）")
print("=" * 50)

# 获取数据
production = client.get_soybean_production(year={"ge": 2020, "le": 2024})
area = client.get_soybean_area_planted(year={"ge": 2020, "le": 2024})
yield_data = client.get_soybean_yield(year={"ge": 2020, "le": 2024})
price = client.get_soybean_price(year={"ge": 2020, "le": 2024})

# 打印报告
for year in range(2020, 2025):
    print(f"\n{year}年：")
    print(f"  种植面积：{area[area['year']==year]['Value'].iloc[0] if len(area[area['year']==year]) > 0 else 'N/A'} 英亩")
    print(f"  产量：{production[production['year']==year]['Value'].iloc[0] if len(production[production['year']==year]) > 0 else 'N/A'} 蒲式耳")
```

### 示例2：对比主要作物产量

```python
from usda_cn import FieldCropsData

crops = FieldCropsData()

print("2024年美国主要作物产量对比：")
print("-" * 40)

# 玉米
corn = crops.get_corn(year=2024)
print(f"玉米：{corn['Value'].iloc[0]} 蒲式耳")

# 大豆
soybeans = crops.get_soybeans(year=2024)
print(f"大豆：{soybeans['Value'].iloc[0]} 蒲式耳")

# 小麦
wheat = crops.get_wheat(year=2024)
print(f"小麦：{wheat['Value'].iloc[0]} 蒲式耳")
```

---

## 🆘 获取帮助

- **GitHub**: https://github.com/chan1919/USDA-CN
- **问题反馈**: 在GitHub上提交Issue

---

## 📄 许可证

本项目采用 MIT 许可证，可免费使用。

---

## ⚠️ 免责声明

本工具仅供研究和学习使用，数据来源于USDA官方API。使用本工具获取的数据仅供参考，不构成任何投资建议。

---

<div align="center">

**如果这个项目对您有帮助，请给一个 ⭐️ Star！**

Made with ❤️ for Chinese agricultural industry

</div>
