# -*- coding: utf-8 -*-
"""
USDA-CN 常量定义
===============

包含商品名称映射、统计类别映射等常量。
覆盖USDA所有数据类别。
"""

# API操作符
API_OPERATORS = ["LE", "LT", "GT", "GE", "LIKE", "NOT_LIKE", "NE"]

# 最大记录数限制
MAX_RECORDS = 50000

# ============================================================
# 部门 (Sectors)
# ============================================================
SECTORS = {
    "CROPS": "农作物",
    "ANIMALS & PRODUCTS": "动物及产品",
    "ECONOMICS": "经济",
    "DEMOGRAPHICS": "人口统计",
    "ENVIRONMENTAL": "环境",
}

# ============================================================
# 商品组 (Groups)
# ============================================================
GROUPS = {
    "FIELD CROPS": "大田作物",
    "FRUIT & TREE NUTS": "水果和坚果",
    "HORTICULTURE": "园艺",
    "VEGETABLES": "蔬菜",
    "LIVESTOCK": "牲畜",
    "POULTRY": "家禽",
    "DAIRY": "乳制品",
    "AQUACULTURE": "水产养殖",
    "FARMS & LAND & ASSETS": "农场和土地资产",
    "INCOME": "收入",
    "EXPENSES": "支出",
    "PRICES PAID": "支出价格",
    "ENERGY": "能源",
}

# ============================================================
# 商品名称映射 (中文 <-> 英文)
# ============================================================
COMMODITY_NAMES_CN = {
    # 大田作物
    "CORN": "玉米", "WHEAT": "小麦", "BARLEY": "大麦", "OATS": "燕麦",
    "SORGHUM": "高粱", "RICE": "水稻", "SOYBEANS": "大豆", "CANOLA": "油菜籽",
    "SUNFLOWER": "向日葵", "PEANUTS": "花生", "COTTON": "棉花", "HAY": "干草",
    "SUGARBEETS": "甜菜", "SUGARCANE": "甘蔗",
    # 水果
    "APPLES": "苹果", "PEACHES": "桃", "PEARS": "梨", "CHERRIES": "樱桃",
    "GRAPES": "葡萄", "ORANGES": "橙子", "LEMONS": "柠檬", "GRAPEFRUIT": "葡萄柚",
    "STRAWBERRIES": "草莓", "BLUEBERRIES": "蓝莓", "CRANBERRIES": "蔓越莓",
    "BANANAS": "香蕉", "PINEAPPLES": "菠萝", "AVOCADOS": "牛油果",
    # 坚果
    "ALMONDS": "杏仁", "WALNUTS": "核桃", "PECANS": "碧根果", "PISTACHIOS": "开心果",
    # 蔬菜
    "POTATOES": "马铃薯", "CARROTS": "胡萝卜", "ONIONS": "洋葱", "LETTUCE": "生菜",
    "CABBAGE": "卷心菜", "BROCCOLI": "西兰花", "TOMATOES": "番茄", "PEPPERS": "辣椒",
    "CUCUMBERS": "黄瓜", "MELONS": "甜瓜", "WATERMELONS": "西瓜",
    "SNAP BEANS": "四季豆", "GREEN PEAS": "青豆", "SWEET CORN": "甜玉米",
    "ASPARAGUS": "芦笋", "GARLIC": "大蒜", "MUSHROOMS": "蘑菇",
    # 畜牧
    "CATTLE": "牛", "HOGS": "猪", "SHEEP": "绵羊", "GOATS": "山羊", "BISON": "野牛",
    # 家禽
    "CHICKENS": "鸡", "TURKEYS": "火鸡", "DUCKS": "鸭", "EGGS": "鸡蛋",
    # 乳制品
    "MILK": "牛奶", "CHEESE": "奶酪", "BUTTER": "黄油", "CREAM": "奶油",
    "ICE CREAM": "冰淇淋", "YOGURT": "酸奶",
    # 其他
    "HONEY": "蜂蜜", "WOOL": "羊毛",
    # 经济
    "AG LAND": "农地", "ASSETS": "资产", "DEBT": "负债",
    "INCOME": "收入", "EXPENSES": "支出", "CASH RECEIPTS": "现金收入",
}

# 创建反向映射 (中文 -> 英文)
_CN_TO_EN = {v: k for k, v in COMMODITY_NAMES_CN.items()}
COMMODITY_NAMES_CN.update(_CN_TO_EN)

# ============================================================
# 统计类别映射
# ============================================================
STATISTIC_CATEGORIES_CN = {
    "PRODUCTION": "产量", "AREA PLANTED": "种植面积", "AREA HARVESTED": "收获面积",
    "AREA BEARING": "结果面积", "YIELD": "单产", "PRICE RECEIVED": "价格",
    "STOCKS": "库存", "SALES": "销售", "INVENTORY": "存栏",
    "GROSS INCOME": "总收入", "NET INCOME": "净收入", "EXPENSE": "支出",
    "ASSET VALUE": "资产价值", "RECEIPTS": "收入", "OPERATIONS": "经营数量",
    "CRUSHED": "压榨", "SLAUGHTERED": "屠宰量", "CALF CROP": "小牛产量",
    "PIG CROP": "仔猪产量", "EGGS SET": "入孵蛋", "HATCHED": "孵化",
    "PLACEMENTS": "投放", "RATE OF LAY": "产蛋率",
}
_CN_TO_EN_STATS = {v: k for k, v in STATISTIC_CATEGORIES_CN.items()}
STATISTIC_CATEGORIES_CN.update(_CN_TO_EN_STATS)

# ============================================================
# 地理聚合级别映射
# ============================================================
AGGREGATION_LEVELS_CN = {
    "全国": "NATIONAL", "州": "STATE", "县": "COUNTY",
    "农业统计区": "AGRICULTURAL DISTRICT", "地区": "REGION",
}

AGGREGATION_LEVELS_EN = {
    "NATIONAL": "全国", "STATE": "州", "COUNTY": "县",
    "AGRICULTURAL DISTRICT": "农业统计区", "REGION": "地区",
}

# ============================================================
# 美国州名映射
# ============================================================
STATE_NAMES_CN = {
    "AL": "阿拉巴马", "AK": "阿拉斯加", "AZ": "亚利桑那", "AR": "阿肯色",
    "CA": "加利福尼亚", "CO": "科罗拉多", "CT": "康涅狄格", "DE": "特拉华",
    "FL": "佛罗里达", "GA": "佐治亚", "HI": "夏威夷", "ID": "爱达荷",
    "IL": "伊利诺伊", "IN": "印第安纳", "IA": "爱荷华", "KS": "堪萨斯",
    "KY": "肯塔基", "LA": "路易斯安那", "ME": "缅因", "MD": "马里兰",
    "MA": "马萨诸塞", "MI": "密歇根", "MN": "明尼苏达", "MS": "密西西比",
    "MO": "密苏里", "MT": "蒙大拿", "NE": "内布拉斯加", "NV": "内华达",
    "NH": "新罕布什尔", "NJ": "新泽西", "NM": "新墨西哥", "NY": "纽约",
    "NC": "北卡罗来纳", "ND": "北达科他", "OH": "俄亥俄", "OK": "俄克拉荷马",
    "OR": "俄勒冈", "PA": "宾夕法尼亚", "RI": "罗德岛", "SC": "南卡罗来纳",
    "SD": "南达科他", "TN": "田纳西", "TX": "得克萨斯", "UT": "犹他",
    "VT": "佛蒙特", "VA": "弗吉尼亚", "WA": "华盛顿", "WV": "西弗吉尼亚",
    "WI": "威斯康星", "WY": "怀俄明",
}

# 主要生产州
MAJOR_SOYBEAN_STATES = ["IA", "IL", "MN", "NE", "IN", "MO", "OH", "SD", "AR", "KS"]
MAJOR_CORN_STATES = ["IA", "IL", "NE", "MN", "IN", "SD", "KS", "OH", "MO", "WI"]
MAJOR_WHEAT_STATES = ["KS", "ND", "OK", "MT", "WA", "TX", "CO", "NE", "SD", "MN"]
MAJOR_CATTLE_STATES = ["TX", "NE", "KS", "OK", "CA", "MO", "IA", "SD", "MT", "CO"]
MAJOR_HOG_STATES = ["IA", "MN", "NC", "IL", "IN", "NE", "MO", "OH", "SD", "KS"]

# ============================================================
# 国家名称映射
# ============================================================
COUNTRY_NAMES_CN = {
    "United States": "美国", "China": "中国", "Brazil": "巴西",
    "Argentina": "阿根廷", "India": "印度", "Russia": "俄罗斯",
    "Ukraine": "乌克兰", "Canada": "加拿大", "Australia": "澳大利亚",
    "Mexico": "墨西哥", "Indonesia": "印度尼西亚", "Thailand": "泰国",
    "Vietnam": "越南", "Japan": "日本", "South Korea": "韩国",
    "European Union": "欧盟",
}

# ============================================================
# 单位映射
# ============================================================
UNIT_NAMES_CN = {
    "BU": "蒲式耳", "BU / ACRE": "蒲式耳/英亩", "ACRES": "英亩",
    "$": "美元", "$ / BU": "美元/蒲式耳", "LB": "磅", "TONS": "吨",
    "CWT": "英担", "HEAD": "头", "DOZEN": "打", "EGGS": "个",
    "GAL": "加仑", "BOX": "箱", "PCT": "百分比",
}

# PSD商品代码
PSD_COMMODITIES = {
    "Soybeans": "0430000", "Soybean Meal": "0831500", "Soybean Oil": "4232000",
    "Corn": "0440000", "Wheat": "0410000", "Rice, Milled": "0422110",
    "Cotton": "3232110",
}
