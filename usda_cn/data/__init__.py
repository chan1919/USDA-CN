# -*- coding: utf-8 -*-
"""
USDA-CN 数据子包
===============

提供所有USDA数据类别的专用数据获取模块。

模块列表:
- FieldCropsData: 大田作物 (玉米、大豆、小麦、棉花等)
- FruitNutsData: 水果和坚果 (苹果、橙子、杏仁、核桃等)
- VegetablesData: 蔬菜 (番茄、马铃薯、生菜等)
- LivestockData: 畜牧 (牛、猪、羊等)
- PoultryData: 家禽 (鸡、火鸡、鸡蛋等)
- DairyData: 乳制品 (牛奶、奶酪、黄油等)
- SoybeanData: 大豆专用模块
- CornData: 玉米专用模块
- WheatData: 小麦专用模块
"""

from usda_cn.data.base import BaseDataFetcher
from usda_cn.data.field_crops import FieldCropsData
from usda_cn.data.fruit_nuts import FruitNutsData
from usda_cn.data.vegetables import VegetablesData
from usda_cn.data.livestock import LivestockData
from usda_cn.data.poultry import PoultryData
from usda_cn.data.dairy import DairyData
from usda_cn.data.soybean import SoybeanData
from usda_cn.data.corn import CornData
from usda_cn.data.wheat import WheatData

__all__ = [
    # 基类
    "BaseDataFetcher",
    # 综合模块
    "FieldCropsData",
    "FruitNutsData",
    "VegetablesData",
    "LivestockData",
    "PoultryData",
    "DairyData",
    # 专用模块
    "SoybeanData",
    "CornData",
    "WheatData",
]
