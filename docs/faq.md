# 常见问题解答 (FAQ)

## 安装配置

### Q1: 如何安装USDA-CN？

**答**：打开命令行，输入：
```bash
pip install usda-cn
```

### Q2: 提示"pip不是内部或外部命令"怎么办？

**答**：使用以下命令：
```bash
python -m pip install usda-cn
```

### Q3: 如何申请API密钥？

**答**：
1. 访问 https://quickstats.nass.usda.gov/api
2. 填写邮箱地址
3. 提交后几秒钟会收到邮件，包含API密钥

### Q4: API密钥是免费的吗？

**答**：是的，完全免费。

### Q5: .env文件放在哪里？

**答**：放在您的Python项目文件夹中，与您的.py文件在同一目录。

### Q6: 如何创建.env文件？

**答**：
1. 新建文本文件
2. 重命名为 `.env`（注意前面有点）
3. 内容：`USDA_API_KEY=您的密钥`

### Q7: 提示"未找到API密钥"怎么办？

**答**：
1. 确认.env文件存在且内容正确
2. 或者在代码中直接传入：`NASSClient(api_key="您的密钥")`

## 使用问题

### Q8: 返回的数据为空怎么办？

**答**：
1. 检查年份是否正确
2. 检查州代码是否正确
3. 尝试不指定州（获取全国数据）

### Q9: 如何获取历史数据？

**答**：
```python
# 获取2020-2024年数据
data = client.get_soybean_production(year={"ge": 2020, "le": 2024})
```

### Q10: 如何获取某州的数据？

**答**：
```python
# 获取爱荷华州数据
data = client.get_soybean_production(year=2024, state="IA")
```

### Q11: 常用州代码有哪些？

**答**：
- IA = 爱荷华州
- IL = 伊利诺伊州
- NE = 内布拉斯加州
- MN = 明尼苏达州
- KS = 堪萨斯州

### Q12: 如何保存数据到Excel？

**答**：
```python
data = client.get_soybean_production(year=2024)
data.to_excel("大豆产量.xlsx", index=False)
```

### Q13: 如何保存数据到CSV？

**答**：
```python
data = client.get_soybean_production(year=2024)
data.to_csv("大豆产量.csv", index=False, encoding='utf-8-sig')
```

### Q14: 数据单位是什么？

**答**：
- BU = 蒲式耳（约35.24升）
- ACRE = 英亩（约6.07亩）
- LB = 磅（约0.45公斤）
- HEAD = 头（牲畜计数）

### Q15: 数据多久更新一次？

**答**：
- 作物产量：每年更新
- 畜牧存栏：每季度更新
- 价格数据：每月更新

## 错误处理

### Q16: 提示"连接超时"怎么办？

**答**：
1. 检查网络连接
2. 可能需要使用VPN访问USDA服务器

### Q17: 提示"API密钥无效"怎么办？

**答**：
1. 检查密钥是否正确复制
2. 重新申请新密钥
3. 确认没有多余空格

### Q18: 如何处理错误？

**答**：
```python
try:
    data = client.get_soybean_production(year=2024)
    if data.empty:
        print("没有找到数据")
    else:
        print(f"获取成功: {data['Value'].iloc[0]}")
except Exception as e:
    print(f"发生错误: {e}")
```

### Q19: 数据量太大怎么办？

**答**：
1. 添加更多筛选条件（如指定州）
2. 减少年份范围
3. 使用get_record_count()先检查记录数

### Q20: 如何检查将返回多少条记录？

**答**：
```python
count = client.get_record_count(commodity_desc="SOYBEANS", year=2024)
print(f"将返回 {count} 条记录")
```

## 进阶问题

### Q21: 支持中文参数吗？

**答**：支持！
```python
# 中文
client.get_data("大豆", "产量", year=2024)

# 英文
client.get_data("SOYBEANS", "PRODUCTION", year=2024)
```

### Q22: 如何获取所有可用商品？

**答**：
```python
commodities = client.list_commodities()
print(f"共有 {len(commodities)} 种商品")
```

### Q23: 如何获取所有统计类别？

**答**：
```python
categories = client.list_statistic_categories()
print(categories)
```

### Q24: 可以批量获取多个州的数据吗？

**答**：
```python
from usda_cn import FieldCropsData

crops = FieldCropsData()

# 获取各州数据
states = ["IA", "IL", "MN", "NE"]
for state in states:
    data = crops.get_corn(year=2024, state=state)
    print(f"{state}: {data['Value'].iloc[0]} 蒲式耳")
```

### Q25: 如何绘制数据图表？

**答**：
```python
import matplotlib.pyplot as plt

# 获取数据
data = client.get_soybean_production(year={"ge": 2010, "le": 2024})

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(data['year'], data['Value_numeric'])
plt.title("大豆产量趋势")
plt.xlabel("年份")
plt.ylabel("产量 (蒲式耳)")
plt.grid(True)
plt.show()
```

## 其他问题

### Q26: 这个库是免费的吗？

**答**：是的，完全免费，采用MIT许可证。

### Q27: 可以用于商业用途吗？

**答**：可以，MIT许可证允许商业使用。

### Q28: 数据来源可靠吗？

**答**：数据来自USDA官方NASS数据库，是最权威的美国农业数据来源。

### Q29: 如何报告问题？

**答**：在GitHub提交Issue：https://github.com/chan1919/USDA-CN/issues

### Q30: 如何贡献代码？

**答**：
1. Fork项目
2. 创建分支
3. 提交Pull Request

---

## 仍然遇到问题？

如果以上FAQ没有解决您的问题，请：

1. 查看 [API参考文档](api_reference.md)
2. 查看 [安装指南](installation.md)
3. 在GitHub提交Issue