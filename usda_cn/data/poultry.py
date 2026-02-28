# -*- coding: utf-8 -*-
"""
家禽产品数据模块
==============

包含所有家禽产品的数据获取接口：
- 鸡: 肉鸡、蛋鸡
- 火鸡
- 鸭
- 鸡蛋
"""

from typing import Optional, Union, Dict
import pandas as pd

from usda_cn.data.base import BaseDataFetcher
from usda_cn.utils.helpers import setup_logger


logger = setup_logger("usda_cn.poultry")


class PoultryData(BaseDataFetcher):
    """
    家禽产品数据获取器

    提供所有家禽产品的数据访问接口。

    示例:
        >>> poultry = PoultryData()
        >>> df = poultry.get_chicken_inventory(year=2024)
        >>> df = poultry.get_egg_production(year=2024)
    """

    SECTOR = "ANIMALS & PRODUCTS"
    GROUP = "POULTRY"

    # 家禽类型
    POULTRY_TYPES = {
        "CHICKENS": {"cn": "鸡", "unit": "HEAD"},
        "CHICKENS, BROILERS": {"cn": "肉鸡", "unit": "HEAD"},
        "CHICKENS, LAYERS": {"cn": "蛋鸡", "unit": "HEAD"},
        "CHICKENS, HENS": {"cn": "母鸡", "unit": "HEAD"},
        "TURKEYS": {"cn": "火鸡", "unit": "HEAD"},
        "DUCKS": {"cn": "鸭", "unit": "HEAD"},
        "EGGS": {"cn": "鸡蛋", "unit": "EGGS"},
    }

    def __init__(self, client=None, api_key=None):
        super().__init__(client=client, api_key=api_key)

    def get_chicken_inventory(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
        agg_level: str = "NATIONAL",
    ) -> pd.DataFrame:
        """
        获取鸡存栏数据

        参数:
            year: 年份
            state: 州代码
            agg_level: 地理聚合级别

        返回:
            存栏数据DataFrame (单位: 只)
        """
        self.COMMODITY = "CHICKENS"
        self.COMMODITY_CN = "鸡"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self.get_inventory(year=year, state=state, agg_level=agg_level, unit_desc="HEAD")

    def get_broiler_inventory(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取肉鸡存栏数据"""
        self.COMMODITY = "CHICKENS"
        self.COMMODITY_CN = "肉鸡"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="INVENTORY",
            year=year,
            state=state,
            class_desc="BROILERS",
            unit_desc="HEAD",
        )

    def get_layer_inventory(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取蛋鸡存栏数据"""
        self.COMMODITY = "CHICKENS"
        self.COMMODITY_CN = "蛋鸡"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="INVENTORY",
            year=year,
            state=state,
            class_desc="LAYERS",
            unit_desc="HEAD",
        )

    def get_hen_inventory(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取母鸡存栏数据"""
        self.COMMODITY = "CHICKENS"
        self.COMMODITY_CN = "母鸡"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="INVENTORY",
            year=year,
            state=state,
            class_desc="HENS",
            unit_desc="HEAD",
        )

    def get_turkey_inventory(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取火鸡存栏数据"""
        self.COMMODITY = "TURKEYS"
        self.COMMODITY_CN = "火鸡"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self.get_inventory(year=year, state=state, unit_desc="HEAD")

    def get_duck_inventory(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取鸭存栏数据"""
        self.COMMODITY = "DUCKS"
        self.COMMODITY_CN = "鸭"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self.get_inventory(year=year, state=state, unit_desc="HEAD")

    def get_egg_production(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
        agg_level: str = "NATIONAL",
    ) -> pd.DataFrame:
        """
        获取鸡蛋产量数据

        参数:
            year: 年份
            state: 州代码
            agg_level: 地理聚合级别

        返回:
            产量数据DataFrame (单位: 打或个)
        """
        self.COMMODITY = "EGGS"
        self.COMMODITY_CN = "鸡蛋"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self.get_production(year=year, state=state, agg_level=agg_level)

    def get_egg_inventory(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取鸡蛋库存数据"""
        self.COMMODITY = "EGGS"
        self.COMMODITY_CN = "鸡蛋"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self.get_stocks(year=year)

    def get_eggs_hatched(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取孵化蛋数据"""
        self.COMMODITY = "EGGS"
        self.COMMODITY_CN = "孵化蛋"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="HATCHED",
            year=year,
            state=state,
        )

    def get_eggs_set(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取入孵蛋数据"""
        self.COMMODITY = "EGGS"
        self.COMMODITY_CN = "入孵蛋"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="EGGS SET",
            year=year,
            state=state,
        )

    def get_chicks_placed(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取雏鸡投放数据"""
        self.COMMODITY = "CHICKENS"
        self.COMMODITY_CN = "雏鸡"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="PLACEMENTS",
            year=year,
            state=state,
            unit_desc="HEAD",
        )

    def get_rate_of_lay(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取产蛋率数据"""
        self.COMMODITY = "CHICKENS"
        self.COMMODITY_CN = "产蛋率"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="RATE OF LAY",
            year=year,
            state=state,
            class_desc="LAYERS",
        )

    def get_slaughter(
        self,
        poultry_type: str = "CHICKENS",
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        获取家禽屠宰数据

        参数:
            poultry_type: 家禽类型 (CHICKENS, TURKEYS, DUCKS)
            year: 年份
            state: 州代码
        """
        self.COMMODITY = poultry_type.upper()

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="SLAUGHTERED",
            year=year,
            state=state,
            unit_desc="HEAD",
        )

    def get_price(
        self,
        poultry_type: str = "CHICKENS",
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取家禽价格数据"""
        self.COMMODITY = poultry_type.upper()

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="PRICE RECEIVED",
            year=year,
            state=state,
        )

    def get_summary(
        self,
        year: int = 2024,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取家禽数据汇总"""
        results = []

        data_methods = [
            ("鸡存栏", self.get_chicken_inventory, {}),
            ("肉鸡存栏", self.get_broiler_inventory, {}),
            ("蛋鸡存栏", self.get_layer_inventory, {}),
            ("火鸡存栏", self.get_turkey_inventory, {}),
            ("鸡蛋产量", self.get_egg_production, {}),
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

    def list_poultry(self) -> pd.DataFrame:
        """列出所有支持的家禽产品"""
        return pd.DataFrame(
            [
                {"英文": en, "中文": info["cn"], "单位": info["unit"]}
                for en, info in self.POULTRY_TYPES.items()
            ]
        )
