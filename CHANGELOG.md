# USDA-CN 更新日志

所有重要的更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [0.1.0] - 2024-02-28

### 新增
- 初始版本发布
- NASS Quick Stats API 完整支持
- FAS PSD API 基础支持
- 大豆(SoybeanData)、玉米(CornData)、小麦(WheatData)专用数据模块
- 中文接口支持
- Pandas DataFrame 输出格式
- 环境变量配置支持
- 完整的错误处理和重试机制

### 功能
- `NASSClient` 主客户端类
  - `get_data()` 通用查询接口
  - `get_soybean_production()` 大豆产量
  - `get_soybean_area_planted()` 大豆种植面积
  - `get_soybean_yield()` 大豆单产
  - `get_soybean_price()` 大豆价格
  - `get_soybean_stocks()` 大豆库存
  - `get_corn_production()` 玉米产量
  - `get_wheat_production()` 小麦产量
  - `list_commodities()` 商品列表
  - `list_states()` 州列表
  - `list_statistic_categories()` 统计类别列表

- `SoybeanData` 大豆数据模块
  - `get_production()` 产量
  - `get_area_planted()` 种植面积
  - `get_area_harvested()` 收获面积
  - `get_yield()` 单产
  - `get_price()` 价格
  - `get_stocks()` 库存
  - `get_crush()` 压榨量
  - `get_summary()` 数据汇总
  - `get_top_states()` 主产州排名
  - `get_historical_trend()` 历史趋势

- `QuickStatsAPI` 底层API
  - `query()` 执行查询
  - `get_param_values()` 获取参数值
  - `get_count()` 获取记录数

### 文档
- 完整的README文档
- API参考文档
- 使用示例