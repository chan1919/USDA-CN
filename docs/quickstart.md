# 快速开始

5分钟上手USDA-CN，获取您的第一份USDA数据。

## 目录

- [第一个程序](#第一个程序)
- [获取不同类型数据](#获取不同类型数据)
- [保存数据](#保存数据)
- [下一步](#下一步)

---

## 第一个程序

### 创建项目文件夹

```bash
mkdir my_usda_project
cd my_usda_project
```

### 创建配置文件

创建 `.env` 文件：
```
USDA_API_KEY=您的API密钥
```

### 创建Python文件

创建 `main.py`：

```python
from usda_cn import NASSClient

# 1. 创建客户端连接
client = NASSClient()

# 2. 获取2024年美国大豆产量
data = client.get_soybean_production(year=2024)

# 3. 显示结果
print("=" * 40)
print("2024年美国大豆产量报告")
print("=" * 40)
print(f"产量: {data['Value'].iloc[0]} 蒲式耳")
print(f"单位: {data['unit_desc'].iloc[0]}")
print("=" * 40)
```

### 运行程序

```bash
python main.py
```

**输出示例**：
```
========================================
2024年美国大豆产量报告
========================================
产量: 4,374,228,000 蒲式耳
单位: BU
========================================
```

🎉 **恭喜！您已经成功获取了USDA数据！**

---

## 获取不同类型数据

### 大豆完整数据

```python
from usda_cn import NASSClient

client = NASSClient()

# 产量
production = client.get_soybean_production(year=2024)
print(f"产量: {production['Value'].iloc[0]} 蒲式耳")

# 种植面积
area = client.get_soybean_area_planted(year=2024)
print(f"种植面积: {area['Value'].iloc[0]} 英亩")

# 单产
yield_data = client.get_soybean_yield(year=2024)
print(f"单产: {yield_data['Value'].iloc[0]} 蒲式耳/英亩")

# 价格
price = client.get_soybean_price(year=2024)
print(f"价格: ${price['Value'].iloc[0]}/蒲式耳")

# 库存
stocks = client.get_soybean_stocks(year=2024)
print(f"库存: {stocks['Value'].iloc[0]} 蒲式耳")
```

### 玉米数据

```python
from usda_cn import NASSClient

client = NASSClient()

# 玉米产量
corn = client.get_corn_production(year=2024)
print(f"玉米产量: {corn['Value'].iloc[0]} 蒲式耳")
```

### 小麦数据

```python
from usda_cn import NASSClient

client = NASSClient()

# 小麦产量
wheat = client.get_wheat_production(year=2024)
print(f"小麦产量: {wheat['Value'].iloc[0]} 蒲式耳")
```

### 使用数据模块

```python
from usda_cn import FieldCropsData, LivestockData, PoultryData

# 大田作物模块
crops = FieldCropsData()
print("玉米:", crops.get_corn(year=2024)['Value'].iloc[0])
print("大豆:", crops.get_soybeans(year=2024)['Value'].iloc[0])
print("小麦:", crops.get_wheat(year=2024)['Value'].iloc[0])

# 畜牧模块
livestock = LivestockData()
print("牛存栏:", livestock.get_cattle_inventory(year=2024)['Value'].iloc[0])
print("猪存栏:", livestock.get_hog_inventory(year=2024)['Value'].iloc[0])

# 家禽模块
poultry = PoultryData()
print("鸡蛋:", poultry.get_egg_production(year=2024)['Value'].iloc[0])
```

---

## 保存数据

### 保存为CSV

```python
from usda_cn import NASSClient

client = NASSClient()

# 获取数据
data = client.get_soybean_production(year={"ge": 2020, "le": 2024})

# 保存为CSV
data.to_csv("大豆产量.csv", index=False, encoding='utf-8-sig')
print("已保存到 大豆产量.csv")
```

### 保存为Excel

```python
from usda_cn import NASSClient
import pandas as pd

client = NASSClient()

# 获取数据
data = client.get_soybean_production(year={"ge": 2020, "le": 2024})

# 保存为Excel
data.to_excel("大豆产量.xlsx", index=False)
print("已保存到 大豆产量.xlsx")
```

---

## 下一步

- [API参考文档](api_reference.md) - 了解所有可用接口
- [数据模块文档](modules/README.md) - 各数据类型详细说明
- [常见问题](faq.md) - 解决遇到的问题