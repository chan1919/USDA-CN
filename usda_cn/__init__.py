# -*- coding: utf-8 -*-
"""
USDA-CN: 美国农业部数据接口中文版
===============================

为中国产业用户提供的USDA数据接口库，支持：
- NASS Quick Stats API (农业统计数据)
- FAS PSD API (全球供需数据)
- 所有USDA数据类别的全面覆盖

数据模块:
- FieldCropsData: 大田作物 (玉米、大豆、小麦、棉花等)
- FruitNutsData: 水果坚果 (苹果、橙子、杏仁等)
- VegetablesData: 蔬菜 (番茄、马铃薯等)
- LivestockData: 畜牧 (牛、猪、羊)
- PoultryData: 家禽 (鸡、火鸡、鸡蛋)
- DairyData: 乳制品 (牛奶、奶酪、黄油)
- EconomicsData: 农业经济 (收入、支出、资产)

示例用法:
    >>> from usda_cn import NASSClient
    >>> client = NASSClient()
    >>> df = client.get_soybean_production(year=2024)
    
    >>> # 使用专用数据模块
    >>> from usda_cn import FieldCropsData, LivestockData
    >>> crops = FieldCropsData()
    >>> df = crops.get_corn(year=2024)
    >>> livestock = LivestockData()
    >>> df = livestock.get_cattle_inventory(year=2024)
"""

__version__ = "0.2.0"
__author__ = "USDA-CN Team"
__email__ = "usda-cn@example.com"

# 核心客户端
from usda_cn.client import NASSClient
from usda_cn.api.quickstats import QuickStatsAPI
from usda_cn.api.psd import PSDAPI

# 综合数据模块
from usda_cn.data.field_crops import FieldCropsData
from usda_cn.data.fruit_nuts import FruitNutsData
from usda_cn.data.vegetables import VegetablesData
from usda_cn.data.livestock import LivestockData
from usda_cn.data.poultry import PoultryData
from usda_cn.data.dairy import DairyData
from usda_cn.data.economics import EconomicsData

# 专用数据模块
from usda_cn.data.soybean import SoybeanData
from usda_cn.data.corn import CornData
from usda_cn.data.wheat import WheatData

__all__ = [
    # 核心客户端
    "NASSClient",
    "QuickStatsAPI",
    "PSDAPI",
    # 综合数据模块
    "FieldCropsData",
    "FruitNutsData",
    "VegetablesData",
    "LivestockData",
    "PoultryData",
    "DairyData",
    "EconomicsData",
    # 专用数据模块
    "SoybeanData",
    "CornData",
    "WheatData",
]
