# -*- coding: utf-8 -*-
"""
测试配置
"""

import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def mock_api_key():
    """模拟API密钥"""
    return "TEST-API-KEY-12345678"


@pytest.fixture
def sample_soybean_data():
    """示例大豆数据"""
    return [
        {
            "source_desc": "SURVEY",
            "sector_desc": "CROPS",
            "group_desc": "FIELD CROPS",
            "commodity_desc": "SOYBEANS",
            "statisticcat_desc": "PRODUCTION",
            "unit_desc": "BU",
            "year": "2024",
            "Value": "4,374,228,000",
            "state_alpha": "US",
            "state_name": "US TOTAL",
            "agg_level_desc": "NATIONAL",
            "reference_period_desc": "YEAR",
            "freq_desc": "ANNUAL",
        }
    ]


@pytest.fixture
def sample_area_data():
    """示例面积数据"""
    return [
        {
            "commodity_desc": "SOYBEANS",
            "statisticcat_desc": "AREA PLANTED",
            "unit_desc": "ACRES",
            "year": "2024",
            "Value": "87,260,000",
            "state_alpha": "US",
            "agg_level_desc": "NATIONAL",
        }
    ]
