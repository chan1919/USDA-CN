# -*- coding: utf-8 -*-
"""
乳制品数据模块
=============

包含所有乳制品的数据获取接口：
- 牛奶: 产量、价格
- 奶制品: 奶酪、黄油、酸奶等
"""

from typing import Optional, Union, Dict
import pandas as pd

from usda_cn.data.base import BaseDataFetcher
from usda_cn.utils.helpers import setup_logger


logger = setup_logger("usda_cn.dairy")


class DairyData(BaseDataFetcher):
    """
    乳制品数据获取器

    提供所有乳制品的数据访问接口。

    示例:
        >>> dairy = DairyData()
        >>> df = dairy.get_milk_production(year=2024)
        >>> df = dairy.get_cheese_production(year=2024)
    """

    SECTOR = "ANIMALS & PRODUCTS"
    GROUP = "DAIRY"

    # 乳制品类型
    DAIRY_TYPES = {
        "MILK": {"cn": "牛奶", "unit": "LB"},
        "CHEESE": {"cn": "奶酪", "unit": "LB"},
        "BUTTER": {"cn": "黄油", "unit": "LB"},
        "CREAM": {"cn": "奶油", "unit": "LB"},
        "ICE CREAM": {"cn": "冰淇淋", "unit": "GAL"},
        "YOGURT": {"cn": "酸奶", "unit": "LB"},
        "BUTTERMILK": {"cn": "酪乳", "unit": "LB"},
    }

    def __init__(self, client=None, api_key=None):
        super().__init__(client=client, api_key=api_key)

    def get_milk_production(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
        agg_level: str = "NATIONAL",
    ) -> pd.DataFrame:
        """
        获取牛奶产量数据

        参数:
            year: 年份
            state: 州代码
            agg_level: 地理聚合级别

        返回:
            产量数据DataFrame (单位: 磅)
        """
        self.COMMODITY = "MILK"
        self.COMMODITY_CN = "牛奶"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self.get_production(year=year, state=state, agg_level=agg_level, unit_desc="LB")

    def get_milk_price(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        获取牛奶价格数据

        参数:
            year: 年份
            state: 州代码

        返回:
            价格数据DataFrame (单位: 美元/英担)
        """
        self.COMMODITY = "MILK"
        self.COMMODITY_CN = "牛奶"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self.get_price(year=year, state=state)

    def get_milk_fat(self, year=None, state=None) -> pd.DataFrame:
        """获取牛奶脂肪含量数据"""
        self.COMMODITY = "MILK"
        self.COMMODITY_CN = "牛奶脂肪"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="MILKFAT",
            year=year,
            state=state,
        )

    def get_cheese_production(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取奶酪产量数据"""
        self.COMMODITY = "CHEESE"
        self.COMMODITY_CN = "奶酪"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self.get_production(year=year, state=state, unit_desc="LB")

    def get_butter_production(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取黄油产量数据"""
        self.COMMODITY = "BUTTER"
        self.COMMODITY_CN = "黄油"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self.get_production(year=year, state=state, unit_desc="LB")

    def get_cream_production(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取奶油产量数据"""
        self.COMMODITY = "CREAM"
        self.COMMODITY_CN = "奶油"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self.get_production(year=year, state=state, unit_desc="LB")

    def get_ice_cream_production(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取冰淇淋产量数据"""
        self.COMMODITY = "ICE CREAM"
        self.COMMODITY_CN = "冰淇淋"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self.get_production(year=year, state=state)

    def get_dairy_product(
        self,
        product: str,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        获取指定乳制品数据

        参数:
            product: 产品名称 (英文或中文)
            year: 年份
            state: 州代码
        """
        product_en = self._translate_product(product)
        self.COMMODITY = product_en

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self.get_production(year=year, state=state)

    def get_summary(
        self,
        year: int = 2024,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取乳制品数据汇总"""
        results = []

        data_methods = [
            ("牛奶产量", self.get_milk_production, {}),
            ("牛奶价格", self.get_milk_price, {}),
            ("奶酪产量", self.get_cheese_production, {}),
            ("黄油产量", self.get_butter_production, {}),
        ]

        for metric_name, func, kwargs in data_methods:
            try:
                df = func(year=year, state=state, **kwargs)
                if not df.empty:
                    row = df.iloc[0]
                    results.append(
                        {
                            "指标": metric_name,
                            "年份": year,
                            "数值": row.get("Value", ""),
                            "单位": row.get("unit_desc", ""),
                        }
                    )
            except Exception as e:
                logger.debug(f"获取{metric_name}数据失败: {e}")

        return pd.DataFrame(results)

    def list_products(self) -> pd.DataFrame:
        """列出所有支持的乳制品"""
        return pd.DataFrame(
            [
                {"英文": en, "中文": info["cn"], "单位": info["unit"]}
                for en, info in self.DAIRY_TYPES.items()
            ]
        )

    def _translate_product(self, product: str) -> str:
        """转换产品名称"""
        product_upper = product.upper()

        if product_upper in self.DAIRY_TYPES:
            return product_upper

        for en, info in self.DAIRY_TYPES.items():
            if info["cn"] == product:
                return en

        return product_upper
