# -*- coding: utf-8 -*-
"""
畜牧产品数据模块
==============

包含所有畜牧产品的数据获取接口：
- 牛: 肉牛、奶牛
- 猪: 生猪
- 羊: 绵羊、山羊
- 其他: 野牛、羊驼等
"""

from typing import Optional, Union, Dict
import pandas as pd

from usda_cn.data.base import BaseDataFetcher
from usda_cn.utils.helpers import setup_logger


logger = setup_logger("usda_cn.livestock")


class LivestockData(BaseDataFetcher):
    """
    畜牧产品数据获取器

    提供所有畜牧产品的数据访问接口。

    示例:
        >>> livestock = LivestockData()
        >>> df = livestock.get_cattle_inventory(year=2024)
        >>> df = livestock.get_hog_inventory(year=2024)
    """

    SECTOR = "ANIMALS & PRODUCTS"
    GROUP = "LIVESTOCK"

    # 主要畜牧产品
    LIVESTOCK_TYPES = {
        "CATTLE": {"cn": "牛", "unit": "HEAD"},
        "CATTLE, CALVES": {"cn": "小牛", "unit": "HEAD"},
        "CATTLE, COWS": {"cn": "奶牛", "unit": "HEAD"},
        "CATTLE, COWS, BEEF": {"cn": "肉牛", "unit": "HEAD"},
        "CATTLE, COWS, MILK": {"cn": "泌乳牛", "unit": "HEAD"},
        "CATTLE, ON FEED": {"cn": "育肥牛", "unit": "HEAD"},
        "HOGS": {"cn": "猪", "unit": "HEAD"},
        "HOGS, BREEDING": {"cn": "种猪", "unit": "HEAD"},
        "HOGS, MARKET": {"cn": "商品猪", "unit": "HEAD"},
        "SHEEP": {"cn": "绵羊", "unit": "HEAD"},
        "SHEEP, BREEDING": {"cn": "种羊", "unit": "HEAD"},
        "LAMBS": {"cn": "羔羊", "unit": "HEAD"},
        "GOATS": {"cn": "山羊", "unit": "HEAD"},
        "BISON": {"cn": "野牛", "unit": "HEAD"},
    }

    def __init__(self, client=None, api_key=None):
        super().__init__(client=client, api_key=api_key)

    def get_cattle_inventory(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
        agg_level: str = "NATIONAL",
    ) -> pd.DataFrame:
        """
        获取牛存栏数据

        参数:
            year: 年份
            state: 州代码
            agg_level: 地理聚合级别

        返回:
            存栏数据DataFrame (单位: 头)
        """
        self.COMMODITY = "CATTLE"
        self.COMMODITY_CN = "牛"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self.get_inventory(year=year, state=state, agg_level=agg_level, unit_desc="HEAD")

    def get_beef_cows(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取肉牛数据"""
        self.COMMODITY = "CATTLE"
        self.COMMODITY_CN = "肉牛"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="INVENTORY",
            year=year,
            state=state,
            class_desc="COWS, BEEF",
            unit_desc="HEAD",
        )

    def get_milk_cows(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取奶牛数据"""
        self.COMMODITY = "CATTLE"
        self.COMMODITY_CN = "奶牛"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="INVENTORY",
            year=year,
            state=state,
            class_desc="COWS, MILK",
            unit_desc="HEAD",
        )

    def get_cattle_on_feed(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取育肥牛数据"""
        self.COMMODITY = "CATTLE"
        self.COMMODITY_CN = "育肥牛"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="INVENTORY",
            year=year,
            state=state,
            prodn_practice_desc="ON FEED",
            unit_desc="HEAD",
        )

    def get_calf_crop(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        获取小牛产量数据

        参数:
            year: 年份
            state: 州代码

        返回:
            小牛产量DataFrame
        """
        self.COMMODITY = "CATTLE"
        self.COMMODITY_CN = "小牛"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="CALF CROP",
            year=year,
            state=state,
            unit_desc="HEAD",
        )

    def get_hog_inventory(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
        agg_level: str = "NATIONAL",
    ) -> pd.DataFrame:
        """
        获取猪存栏数据

        参数:
            year: 年份
            state: 州代码
            agg_level: 地理聚合级别

        返回:
            存栏数据DataFrame (单位: 头)
        """
        self.COMMODITY = "HOGS"
        self.COMMODITY_CN = "猪"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self.get_inventory(year=year, state=state, agg_level=agg_level, unit_desc="HEAD")

    def get_breeding_hogs(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取种猪数据"""
        self.COMMODITY = "HOGS"
        self.COMMODITY_CN = "种猪"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="INVENTORY",
            year=year,
            state=state,
            class_desc="BREEDING",
            unit_desc="HEAD",
        )

    def get_market_hogs(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取商品猪数据"""
        self.COMMODITY = "HOGS"
        self.COMMODITY_CN = "商品猪"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="INVENTORY",
            year=year,
            state=state,
            class_desc="MARKET",
            unit_desc="HEAD",
        )

    def get_pig_crop(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取仔猪产量数据"""
        self.COMMODITY = "HOGS"
        self.COMMODITY_CN = "仔猪"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="PIG CROP",
            year=year,
            state=state,
            unit_desc="HEAD",
        )

    def get_sheep_inventory(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取绵羊存栏数据"""
        self.COMMODITY = "SHEEP"
        self.COMMODITY_CN = "绵羊"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self.get_inventory(year=year, state=state, unit_desc="HEAD")

    def get_goat_inventory(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取山羊存栏数据"""
        self.COMMODITY = "GOATS"
        self.COMMODITY_CN = "山羊"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self.get_inventory(year=year, state=state, unit_desc="HEAD")

    def get_slaughter(
        self,
        commodity: str = "CATTLE",
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        获取屠宰数据

        参数:
            commodity: 畜禽类型
            year: 年份
            state: 州代码

        返回:
            屠宰数据DataFrame
        """
        self.COMMODITY = commodity.upper()

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="SLAUGHTERED",
            year=year,
            state=state,
            unit_desc="HEAD",
        )

    def get_summary(
        self,
        year: int = 2024,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取畜牧数据汇总"""
        results = []

        data_methods = [
            ("牛存栏", self.get_cattle_inventory, {}),
            ("肉牛", self.get_beef_cows, {}),
            ("奶牛", self.get_milk_cows, {}),
            ("猪存栏", self.get_hog_inventory, {}),
            ("绵羊存栏", self.get_sheep_inventory, {}),
            ("山羊存栏", self.get_goat_inventory, {}),
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
                            "州": state or "全国",
                        }
                    )
            except Exception as e:
                logger.debug(f"获取{metric_name}数据失败: {e}")

        return pd.DataFrame(results)

    def list_livestock(self) -> pd.DataFrame:
        """列出所有支持的畜牧产品"""
        return pd.DataFrame(
            [
                {"英文": en, "中文": info["cn"], "单位": info["unit"]}
                for en, info in self.LIVESTOCK_TYPES.items()
            ]
        )
