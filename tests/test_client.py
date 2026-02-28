# -*- coding: utf-8 -*-
"""
USDA-CN 测试模块
"""

import pytest
import pandas as pd
from unittest.mock import Mock, patch, MagicMock

from usda_cn.client import NASSClient
from usda_cn.api.quickstats import QuickStatsAPI
from usda_cn.data.soybean import SoybeanData


class TestNASSClient:
    """NASSClient 测试类"""

    @patch.dict("os.environ", {"USDA_API_KEY": "TEST-API-KEY-12345678"})
    def test_init_with_env_var(self):
        """测试使用环境变量初始化"""
        client = NASSClient()
        assert client.api_key == "TEST-API-KEY-12345678"

    def test_init_with_api_key(self):
        """测试使用API密钥初始化"""
        client = NASSClient(api_key="TEST-API-KEY-12345678")
        assert client.api_key == "TEST-API-KEY-12345678"

    def test_init_without_api_key(self):
        """测试没有API密钥时抛出异常"""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="未找到API密钥"):
                NASSClient()

    @patch("usda_cn.client.QuickStatsAPI")
    def test_list_commodities(self, mock_quickstats):
        """测试获取商品列表"""
        mock_instance = MagicMock()
        mock_instance.get_param_values.return_value = ["SOYBEANS", "CORN", "WHEAT"]
        mock_quickstats.return_value = mock_instance

        client = NASSClient(api_key="TEST-API-KEY-12345678")
        result = client.list_commodities()

        assert isinstance(result, pd.DataFrame)
        assert "commodity_en" in result.columns

    @patch("usda_cn.client.QuickStatsAPI")
    def test_list_states(self, mock_quickstats):
        """测试获取州列表"""
        mock_instance = MagicMock()
        mock_instance.get_param_values.return_value = ["IA", "IL", "MN"]
        mock_quickstats.return_value = mock_instance

        client = NASSClient(api_key="TEST-API-KEY-12345678")
        result = client.list_states()

        assert isinstance(result, pd.DataFrame)
        assert "state_alpha" in result.columns


class TestQuickStatsAPI:
    """QuickStatsAPI 测试类"""

    def test_init(self):
        """测试初始化"""
        api = QuickStatsAPI(api_key="TEST-API-KEY-12345678")
        assert api.api_key == "TEST-API-KEY-12345678"
        assert api.base_url == "https://quickstats.nass.usda.gov/api"

    def test_validate_params(self):
        """测试参数验证"""
        api = QuickStatsAPI(api_key="TEST-API-KEY-12345678")

        # 有效参数
        api._validate_params({"commodity_desc": "SOYBEANS", "year": 2024})

        # 无效参数会打印警告但不会抛出异常
        api._validate_params({"invalid_param": "value"})

    def test_query_params_list(self):
        """测试查询参数列表"""
        api = QuickStatsAPI(api_key="TEST-API-KEY-12345678")

        # 检查关键参数存在
        assert "commodity_desc" in api.QUERY_PARAMS
        assert "year" in api.QUERY_PARAMS
        assert "state_alpha" in api.QUERY_PARAMS
        assert "statisticcat_desc" in api.QUERY_PARAMS


class TestSoybeanData:
    """SoybeanData 测试类"""

    @patch("usda_cn.data.soybean.NASSClient")
    def test_init(self, mock_client):
        """测试初始化"""
        soy = SoybeanData(api_key="TEST-API-KEY-12345678")
        assert soy.COMMODITY == "SOYBEANS"
        assert soy.COMMODITY_CN == "大豆"

    def test_process_data(self):
        """测试数据处理"""
        soy = SoybeanData.__new__(SoybeanData)
        soy.client = MagicMock()

        # 测试空数据
        result = soy._process_data([])
        assert isinstance(result, pd.DataFrame)
        assert result.empty

        # 测试有效数据
        data = [{"year": "2024", "Value": "4,374,228,000", "unit_desc": "BU", "state_alpha": "US"}]
        result = soy._process_data(data)

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert "Value_numeric" in result.columns
        assert result["Value_numeric"].iloc[0] == 4374228000.0


class TestConstants:
    """常量测试类"""

    def test_commodity_names_cn(self):
        """测试商品名称映射"""
        from usda_cn.utils.constants import COMMODITY_NAMES_CN

        # 测试中文到英文
        assert COMMODITY_NAMES_CN["大豆"] == "SOYBEANS"
        assert COMMODITY_NAMES_CN["玉米"] == "CORN"
        assert COMMODITY_NAMES_CN["小麦"] == "WHEAT"

        # 测试英文到中文
        assert COMMODITY_NAMES_CN["SOYBEANS"] == "大豆"
        assert COMMODITY_NAMES_CN["CORN"] == "玉米"

    def test_statistic_categories_cn(self):
        """测试统计类别映射"""
        from usda_cn.utils.constants import STATISTIC_CATEGORIES_CN

        assert STATISTIC_CATEGORIES_CN["产量"] == "PRODUCTION"
        assert STATISTIC_CATEGORIES_CN["种植面积"] == "AREA PLANTED"
        assert STATISTIC_CATEGORIES_CN["单产"] == "YIELD"

    def test_state_names_cn(self):
        """测试州名映射"""
        from usda_cn.utils.constants import STATE_NAMES_CN

        assert STATE_NAMES_CN["IA"] == "爱荷华"
        assert STATE_NAMES_CN["IL"] == "伊利诺伊"


class TestHelpers:
    """辅助函数测试类"""

    def test_validate_api_key_valid(self):
        """测试有效API密钥"""
        from usda_cn.utils.helpers import validate_api_key

        # UUID格式
        assert validate_api_key("4AB84799-0BD2-3EBA-AC70-03E51B016275")

        # 自定义格式
        assert validate_api_key("nrxTfWN1nBDidXNeIIeXaEkxOg7lZLaErhksb35G")

    def test_validate_api_key_invalid(self):
        """测试无效API密钥"""
        from usda_cn.utils.helpers import validate_api_key

        # 空密钥
        with pytest.raises(ValueError):
            validate_api_key("")

        # 太短的密钥
        with pytest.raises(ValueError):
            validate_api_key("abc")

    def test_format_number(self):
        """测试数字格式化"""
        from usda_cn.utils.helpers import format_number

        assert format_number("1,234,567") == 1234567.0
        assert format_number("1,000,000.5") == 1000000.5
        assert format_number("") == 0.0
        assert format_number("N/A") == 0.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
