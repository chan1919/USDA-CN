# -*- coding: utf-8 -*-
"""
USDA-CN 常量定义
===============

包含商品名称映射、统计类别映射等常量。
"""

# API操作符
API_OPERATORS = ["LE", "LT", "GT", "GE", "LIKE", "NOT_LIKE", "NE"]

# 最大记录数限制
MAX_RECORDS = 50000

# 商品中英文名称映射
COMMODITY_NAMES_CN = {
    # 中文 -> 英文
    "大豆": "SOYBEANS",
    "玉米": "CORN",
    "小麦": "WHEAT",
    "棉花": "COTTON",
    "水稻": "RICE",
    "大麦": "BARLEY",
    "燕麦": "OATS",
    "高粱": "SORGHUM",
    "油菜籽": "RAPESEED",
    "花生": "PEANUTS",
    "向日葵": "SUNFLOWER",
    "甘蔗": "SUGARCANE",
    "甜菜": "SUGARBEETS",
    "干草": "HAY",
    "马铃薯": "POTATOES",
    "番茄": "TOMATOES",
    "洋葱": "ONIONS",
    "苹果": "APPLES",
    "橙子": "ORANGES",
    "葡萄": "GRAPES",
    "草莓": "STRAWBERRIES",
    "杏仁": "ALMONDS",
    "核桃": "WALNUTS",
    "牛": "CATTLE",
    "猪": "HOGS",
    "鸡": "CHICKENS",
    "火鸡": "TURKEYS",
    "鸡蛋": "EGGS",
    "牛奶": "MILK",
    "蜂蜜": "HONEY",
    "羊毛": "WOOL",
    # 英文 -> 中文 (反向映射)
    "SOYBEANS": "大豆",
    "CORN": "玉米",
    "WHEAT": "小麦",
    "COTTON": "棉花",
    "RICE": "水稻",
    "BARLEY": "大麦",
    "OATS": "燕麦",
    "SORGHUM": "高粱",
    "RAPESEED": "油菜籽",
    "PEANUTS": "花生",
    "SUNFLOWER": "向日葵",
    "SUGARCANE": "甘蔗",
    "SUGARBEETS": "甜菜",
    "HAY": "干草",
    "POTATOES": "马铃薯",
    "TOMATOES": "番茄",
    "ONIONS": "洋葱",
    "APPLES": "苹果",
    "ORANGES": "橙子",
    "GRAPES": "葡萄",
    "STRAWBERRIES": "草莓",
    "ALMONDS": "杏仁",
    "WALNUTS": "核桃",
    "CATTLE": "牛",
    "HOGS": "猪",
    "CHICKENS": "鸡",
    "TURKEYS": "火鸡",
    "EGGS": "鸡蛋",
    "MILK": "牛奶",
    "HONEY": "蜂蜜",
    "WOOL": "羊毛",
}

# 统计类别中英文映射
STATISTIC_CATEGORIES_CN = {
    # 中文 -> 英文
    "产量": "PRODUCTION",
    "种植面积": "AREA PLANTED",
    "收获面积": "AREA HARVESTED",
    "单产": "YIELD",
    "价格": "PRICE RECEIVED",
    "库存": "STOCKS",
    "销售": "SALES",
    "收入": "GROSS INCOME",
    "净收入": "NET INCOME",
    "产值": "VALUE",
    "出口": "EXPORTS",
    "进口": "IMPORTS",
    "压榨": "CRUSHED",
    "养殖数量": "INVENTORY",
    "屠宰": "SLAUGHTERED",
    "产能": "CAPACITY",
    # 英文 -> 中文
    "PRODUCTION": "产量",
    "AREA PLANTED": "种植面积",
    "AREA HARVESTED": "收获面积",
    "YIELD": "单产",
    "PRICE RECEIVED": "价格",
    "STOCKS": "库存",
    "SALES": "销售",
    "GROSS INCOME": "收入",
    "NET INCOME": "净收入",
    "VALUE": "产值",
    "EXPORTS": "出口",
    "IMPORTS": "进口",
    "CRUSHED": "压榨",
    "INVENTORY": "养殖数量",
    "SLAUGHTERED": "屠宰",
    "CAPACITY": "产能",
}

# 地理聚合级别映射 (中文 -> 英文)
AGGREGATION_LEVELS_CN = {
    "全国": "NATIONAL",
    "州": "STATE",
    "县": "COUNTY",
    "农业统计区": "AGRICULTURAL DISTRICT",
    "地区": "REGION",
    "流域": "WATERSHED",
    "邮政编码": "ZIP CODE",
}

# 地理聚合级别映射 (英文 -> 中文)
AGGREGATION_LEVELS_EN = {
    "NATIONAL": "全国",
    "STATE": "州",
    "COUNTY": "县",
    "AGRICULTURAL DISTRICT": "农业统计区",
    "REGION": "地区",
    "WATERSHED": "流域",
    "ZIP CODE": "邮政编码",
}

# 美国州名映射
STATE_NAMES_CN = {
    "AL": "阿拉巴马",
    "AK": "阿拉斯加",
    "AZ": "亚利桑那",
    "AR": "阿肯色",
    "CA": "加利福尼亚",
    "CO": "科罗拉多",
    "CT": "康涅狄格",
    "DE": "特拉华",
    "FL": "佛罗里达",
    "GA": "佐治亚",
    "HI": "夏威夷",
    "ID": "爱达荷",
    "IL": "伊利诺伊",
    "IN": "印第安纳",
    "IA": "爱荷华",
    "KS": "堪萨斯",
    "KY": "肯塔基",
    "LA": "路易斯安那",
    "ME": "缅因",
    "MD": "马里兰",
    "MA": "马萨诸塞",
    "MI": "密歇根",
    "MN": "明尼苏达",
    "MS": "密西西比",
    "MO": "密苏里",
    "MT": "蒙大拿",
    "NE": "内布拉斯加",
    "NV": "内华达",
    "NH": "新罕布什尔",
    "NJ": "新泽西",
    "NM": "新墨西哥",
    "NY": "纽约",
    "NC": "北卡罗来纳",
    "ND": "北达科他",
    "OH": "俄亥俄",
    "OK": "俄克拉荷马",
    "OR": "俄勒冈",
    "PA": "宾夕法尼亚",
    "RI": "罗德岛",
    "SC": "南卡罗来纳",
    "SD": "南达科他",
    "TN": "田纳西",
    "TX": "得克萨斯",
    "UT": "犹他",
    "VT": "佛蒙特",
    "VA": "弗吉尼亚",
    "WA": "华盛顿",
    "WV": "西弗吉尼亚",
    "WI": "威斯康星",
    "WY": "怀俄明",
}

# 主要大豆生产州
MAJOR_SOYBEAN_STATES = ["IA", "IL", "MN", "NE", "IN", "MO", "OH", "SD", "AR", "KS"]

# 主要玉米生产州
MAJOR_CORN_STATES = ["IA", "IL", "NE", "MN", "IN", "SD", "KS", "OH", "MO", "WI"]

# 主要小麦生产州
MAJOR_WHEAT_STATES = ["KS", "ND", "OK", "MT", "WA", "TX", "CO", "NE", "SD", "MN"]

# 国家名称中英文映射
COUNTRY_NAMES_CN = {
    "United States": "美国",
    "China": "中国",
    "Brazil": "巴西",
    "Argentina": "阿根廷",
    "India": "印度",
    "Russia": "俄罗斯",
    "Ukraine": "乌克兰",
    "Canada": "加拿大",
    "Australia": "澳大利亚",
    "Mexico": "墨西哥",
    "Indonesia": "印度尼西亚",
    "Thailand": "泰国",
    "Vietnam": "越南",
    "Japan": "日本",
    "South Korea": "韩国",
    "European Union": "欧盟",
    "Egypt": "埃及",
    "Turkey": "土耳其",
    "Iran": "伊朗",
    "Pakistan": "巴基斯坦",
}

# PSD商品代码
PSD_COMMODITIES = {
    "Soybeans": "0430000",
    "Soybean Meal": "0831500",
    "Soybean Oil": "4232000",
    "Corn": "0440000",
    "Wheat": "0410000",
    "Rice, Milled": "0422110",
    "Cotton": "3232110",
}

# 单位中英文映射
UNIT_NAMES_CN = {
    "BU": "蒲式耳",
    "BU / ACRE": "蒲式耳/英亩",
    "ACRES": "英亩",
    "$": "美元",
    "$ / BU": "美元/蒲式耳",
    "LB": "磅",
    "TONS": "吨",
    "CWT": "英担",
    "HEAD": "头",
    "DOZEN": "打",
    "PCT": "百分比",
}
