# -*- coding: utf-8 -*-
"""
FAS PSD API 接口模块
===================

美国农业部外国农业服务局(FAS)生产、供应和分销(PSD)数据库API。
提供全球农产品供需数据，包括大豆、玉米、小麦等主要农产品。
"""

from typing import Optional, Dict, Any, List, Union
import pandas as pd
import requests

from usda_cn.utils.helpers import setup_logger
from usda_cn.utils.constants import PSD_COMMODITIES, COUNTRY_NAMES_CN


logger = setup_logger("usda_cn.psd")


class PSDAPI:
    """
    FAS PSD API 客户端

    PSD数据库包含全球农产品的生产、供应和分销数据，
    数据按国家和商品分类，适合分析全球农产品市场。

    数据来源: https://apps.fas.usda.gov/psdonline/

    参数:
        api_key: API密钥(部分端点可能不需要)

    示例:
        >>> api = PSDAPI()
        >>> # 获取全球大豆数据
        >>> df = api.get_commodity_data("Soybeans")
    """

    BASE_URL = "https://apps.fas.usda.gov/PSDOnlineDataServices/api"

    # PSD支持的商品代码
    COMMODITY_CODES = {
        "Soybeans": "0430000",
        "Soybean Meal": "0831500",
        "Soybean Oil": "4232000",
        "Corn": "0440000",
        "Wheat": "0410000",
        "Rice, Milled": "0422110",
        "Cotton": "3232110",
        "Beef and Veal": "1122110",
        "Pork": "1131110",
        "Poultry Meat": "1061110",
    }

    # 数据类型代码
    DATA_TYPES = {
        "Production": 20,
        "Total Supply": 30,
        "Total Use": 80,
        "Exports": 84,
        "Imports": 81,
        "Ending Stocks": 90,
        "Total Domestic Consumption": 83,
        "Feed and Residual": 82,
    }

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "USDA-CN/0.1.0",
                "Accept": "application/json",
            }
        )
        if api_key:
            self.session.headers["Authorization"] = f"Bearer {api_key}"

    def get_commodity_data(
        self,
        commodity: str,
        year: Optional[int] = None,
        country: Optional[str] = None,
        format: str = "dataframe",
    ) -> Union[pd.DataFrame, List[Dict]]:
        """
        获取商品供需数据

        参数:
            commodity: 商品名称 (英文)
                - "Soybeans": 大豆
                - "Corn": 玉米
                - "Wheat": 小麦
                - "Cotton": 棉花
            year: 市场年度
            country: 国家代码或名称
            format: 返回格式 ("dataframe" 或 "dict")

        返回:
            商品供需数据

        示例:
            >>> api = PSDAPI()
            >>> df = api.get_commodity_data("Soybeans", year=2024)
        """
        commodity_code = self.COMMODITY_CODES.get(commodity)
        if not commodity_code:
            raise ValueError(
                f"不支持的商品: {commodity}。支持的商品: {list(self.COMMODITY_CODES.keys())}"
            )

        url = f"{self.BASE_URL}/CommodityData/GetCommodityDataByCode"
        params = {"commodityCode": commodity_code}

        if year:
            params["marketYear"] = year
        if country:
            params["countryCode"] = country

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"PSD API请求失败: {e}")
            return pd.DataFrame() if format == "dataframe" else []

        if format == "dataframe":
            return self._to_dataframe(data)
        return data

    def get_all_countries(self) -> pd.DataFrame:
        """
        获取所有国家列表

        返回:
            包含国家代码和名称的DataFrame
        """
        url = f"{self.BASE_URL}/CountryData/GetCountries"

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            return pd.DataFrame(data)
        except requests.exceptions.RequestException as e:
            logger.error(f"获取国家列表失败: {e}")
            return pd.DataFrame()

    def get_all_commodities(self) -> pd.DataFrame:
        """
        获取所有商品列表

        返回:
            包含商品代码和名称的DataFrame
        """
        url = f"{self.BASE_URL}/CommodityData/GetCommodities"

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            return pd.DataFrame(data)
        except requests.exceptions.RequestException as e:
            logger.error(f"获取商品列表失败: {e}")
            return pd.DataFrame()

    def get_global_soybean_supply(
        self,
        year: Optional[int] = None,
    ) -> pd.DataFrame:
        """
        获取全球大豆供需平衡表

        参数:
            year: 市场年度

        返回:
            全球大豆供需数据DataFrame
        """
        return self.get_commodity_data("Soybeans", year=year)

    def get_global_corn_supply(
        self,
        year: Optional[int] = None,
    ) -> pd.DataFrame:
        """获取全球玉米供需数据"""
        return self.get_commodity_data("Corn", year=year)

    def get_global_wheat_supply(
        self,
        year: Optional[int] = None,
    ) -> pd.DataFrame:
        """获取全球小麦供需数据"""
        return self.get_commodity_data("Wheat", year=year)

    def _to_dataframe(self, data: List[Dict]) -> pd.DataFrame:
        """转换为DataFrame"""
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)

        # 添加中文名称
        if "Country_Name" in df.columns:
            df["国家名称"] = df["Country_Name"].map(lambda x: COUNTRY_NAMES_CN.get(x, x))

        return df

    def close(self):
        """关闭会话"""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
