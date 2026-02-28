# -*- coding: utf-8 -*-
"""
USDA-CN: 美国农业部数据接口中文版
===============================

为中国产业用户提供的USDA数据接口库，支持：
- NASS Quick Stats API (农业统计数据)
- FAS PSD API (全球供需数据)
- WASDE报告解析

示例用法:
    >>> from usda_cn import NASSClient
    >>> client = NASSClient()
    >>> data = client.get_soybean_production(year=2024)
"""

__version__ = "0.1.0"
__author__ = "USDA-CN Team"
__email__ = "usda-cn@example.com"

from usda_cn.client import NASSClient
from usda_cn.api.quickstats import QuickStatsAPI
from usda_cn.api.psd import PSDAPI
from usda_cn.data.soybean import SoybeanData
from usda_cn.data.corn import CornData
from usda_cn.data.wheat import WheatData

__all__ = [
    "NASSClient",
    "QuickStatsAPI",
    "PSDAPI",
    "SoybeanData",
    "CornData",
    "WheatData",
]
