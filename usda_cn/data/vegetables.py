# -*- coding: utf-8 -*-
"""
蔬菜数据模块
===========

包含所有蔬菜的数据获取接口：
- 根茎类: 马铃薯、胡萝卜、洋葱
- 叶菜类: 生菜、菠菜、卷心菜
- 茄果类: 番茄、辣椒、茄子
- 瓜类: 黄瓜、南瓜、甜瓜
- 豆类: 四季豆、豌豆
"""

from typing import Optional, Union, Dict, List
import pandas as pd

from usda_cn.data.base import BaseDataFetcher
from usda_cn.utils.helpers import setup_logger


logger = setup_logger("usda_cn.vegetables")


class VegetablesData(BaseDataFetcher):
    """
    蔬菜数据获取器

    提供所有蔬菜的数据访问接口。

    示例:
        >>> veg = VegetablesData()
        >>> df = veg.get_tomato_production(year=2024)
        >>> df = veg.get_potato_production(year=2024)
    """

    SECTOR = "CROPS"
    GROUP = "VEGETABLES"

    # 蔬菜类型
    VEGETABLE_TYPES = {
        # 根茎类
        "POTATOES": {"cn": "马铃薯", "unit": "CWT"},
        "CARROTS": {"cn": "胡萝卜", "unit": "CWT"},
        "ONIONS": {"cn": "洋葱", "unit": "CWT"},
        "SWEET POTATOES": {"cn": "红薯", "unit": "CWT"},
        # 叶菜类
        "LETTUCE": {"cn": "生菜", "unit": "CWT"},
        "SPINACH": {"cn": "菠菜", "unit": "CWT"},
        "CABBAGE": {"cn": "卷心菜", "unit": "CWT"},
        "BROCCOLI": {"cn": "西兰花", "unit": "CWT"},
        "CAULIFLOWER": {"cn": "花椰菜", "unit": "CWT"},
        "CELERY": {"cn": "芹菜", "unit": "CWT"},
        "KALE": {"cn": "羽衣甘蓝", "unit": "CWT"},
        # 茄果类
        "TOMATOES": {"cn": "番茄", "unit": "CWT"},
        "PEPPERS": {"cn": "辣椒", "unit": "CWT"},
        "EGGPLANT": {"cn": "茄子", "unit": "CWT"},
        # 瓜类
        "CUCUMBERS": {"cn": "黄瓜", "unit": "CWT"},
        "SQUASH": {"cn": "南瓜", "unit": "CWT"},
        "MELONS": {"cn": "甜瓜", "unit": "CWT"},
        "WATERMELONS": {"cn": "西瓜", "unit": "CWT"},
        "PUMPKINS": {"cn": "南瓜", "unit": "CWT"},
        # 豆类
        "SNAP BEANS": {"cn": "四季豆", "unit": "CWT"},
        "GREEN PEAS": {"cn": "青豆", "unit": "CWT"},
        "SWEET CORN": {"cn": "甜玉米", "unit": "CWT"},
        # 其他
        "ASPARAGUS": {"cn": "芦笋", "unit": "CWT"},
        "GARLIC": {"cn": "大蒜", "unit": "CWT"},
        "MUSHROOMS": {"cn": "蘑菇", "unit": "LB"},
        "ARTICHOKES": {"cn": "朝鲜蓟", "unit": "CWT"},
    }

    def __init__(self, client=None, api_key=None):
        super().__init__(client=client, api_key=api_key)

    def get_potato_production(self, year=None, state=None) -> pd.DataFrame:
        """获取马铃薯产量数据"""
        self.COMMODITY = "POTATOES"
        self.COMMODITY_CN = "马铃薯"
        return self.get_production(year=year, state=state)

    def get_carrot_production(self, year=None, state=None) -> pd.DataFrame:
        """获取胡萝卜产量数据"""
        self.COMMODITY = "CARROTS"
        self.COMMODITY_CN = "胡萝卜"
        return self.get_production(year=year, state=state)

    def get_onion_production(self, year=None, state=None) -> pd.DataFrame:
        """获取洋葱产量数据"""
        self.COMMODITY = "ONIONS"
        self.COMMODITY_CN = "洋葱"
        return self.get_production(year=year, state=state)

    def get_lettuce_production(self, year=None, state=None) -> pd.DataFrame:
        """获取生菜产量数据"""
        self.COMMODITY = "LETTUCE"
        self.COMMODITY_CN = "生菜"
        return self.get_production(year=year, state=state)

    def get_cabbage_production(self, year=None, state=None) -> pd.DataFrame:
        """获取卷心菜产量数据"""
        self.COMMODITY = "CABBAGE"
        self.COMMODITY_CN = "卷心菜"
        return self.get_production(year=year, state=state)

    def get_broccoli_production(self, year=None, state=None) -> pd.DataFrame:
        """获取西兰花产量数据"""
        self.COMMODITY = "BROCCOLI"
        self.COMMODITY_CN = "西兰花"
        return self.get_production(year=year, state=state)

    def get_tomato_production(self, year=None, state=None) -> pd.DataFrame:
        """获取番茄产量数据"""
        self.COMMODITY = "TOMATOES"
        self.COMMODITY_CN = "番茄"
        return self.get_production(year=year, state=state)

    def get_pepper_production(self, year=None, state=None) -> pd.DataFrame:
        """获取辣椒产量数据"""
        self.COMMODITY = "PEPPERS"
        self.COMMODITY_CN = "辣椒"
        return self.get_production(year=year, state=state)

    def get_cucumber_production(self, year=None, state=None) -> pd.DataFrame:
        """获取黄瓜产量数据"""
        self.COMMODITY = "CUCUMBERS"
        self.COMMODITY_CN = "黄瓜"
        return self.get_production(year=year, state=state)

    def get_melon_production(self, year=None, state=None) -> pd.DataFrame:
        """获取甜瓜产量数据"""
        self.COMMODITY = "MELONS"
        self.COMMODITY_CN = "甜瓜"
        return self.get_production(year=year, state=state)

    def get_watermelon_production(self, year=None, state=None) -> pd.DataFrame:
        """获取西瓜产量数据"""
        self.COMMODITY = "WATERMELONS"
        self.COMMODITY_CN = "西瓜"
        return self.get_production(year=year, state=state)

    def get_bean_production(self, year=None, state=None) -> pd.DataFrame:
        """获取四季豆产量数据"""
        self.COMMODITY = "SNAP BEANS"
        self.COMMODITY_CN = "四季豆"
        return self.get_production(year=year, state=state)

    def get_pea_production(self, year=None, state=None) -> pd.DataFrame:
        """获取青豆产量数据"""
        self.COMMODITY = "GREEN PEAS"
        self.COMMODITY_CN = "青豆"
        return self.get_production(year=year, state=state)

    def get_sweet_corn_production(self, year=None, state=None) -> pd.DataFrame:
        """获取甜玉米产量数据"""
        self.COMMODITY = "SWEET CORN"
        self.COMMODITY_CN = "甜玉米"
        return self.get_production(year=year, state=state)

    def get_asparagus_production(self, year=None, state=None) -> pd.DataFrame:
        """获取芦笋产量数据"""
        self.COMMODITY = "ASPARAGUS"
        self.COMMODITY_CN = "芦笋"
        return self.get_production(year=year, state=state)

    def get_garlic_production(self, year=None, state=None) -> pd.DataFrame:
        """获取大蒜产量数据"""
        self.COMMODITY = "GARLIC"
        self.COMMODITY_CN = "大蒜"
        return self.get_production(year=year, state=state)

    def get_mushroom_production(self, year=None, state=None) -> pd.DataFrame:
        """获取蘑菇产量数据"""
        self.COMMODITY = "MUSHROOMS"
        self.COMMODITY_CN = "蘑菇"
        return self.get_production(year=year, state=state)

    def get_vegetable_data(
        self,
        vegetable: str,
        statistic: str = "PRODUCTION",
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        获取指定蔬菜数据

        参数:
            vegetable: 蔬菜名称 (英文或中文)
            statistic: 统计类别
            year: 年份
            state: 州代码
        """
        veg_en = self._translate_commodity(vegetable)
        self.COMMODITY = veg_en

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc=statistic,
            year=year,
            state=state,
        )

    def get_fresh_market(
        self,
        vegetable: str,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取鲜菜市场数据"""
        veg_en = self._translate_commodity(vegetable)
        self.COMMODITY = veg_en

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="PRODUCTION",
            year=year,
            state=state,
            util_practice_desc="FRESH MARKET",
        )

    def get_processing(
        self,
        vegetable: str,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取加工用蔬菜数据"""
        veg_en = self._translate_commodity(vegetable)
        self.COMMODITY = veg_en

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="PRODUCTION",
            year=year,
            state=state,
            util_practice_desc="PROCESSING",
        )

    def compare_vegetables(
        self,
        vegetables: List[str],
        year: int = 2024,
        metric: str = "production",
    ) -> pd.DataFrame:
        """比较多种蔬菜的数据"""
        results = []

        for veg in vegetables:
            veg_en = self._translate_commodity(veg)
            self.COMMODITY = veg_en

            try:
                if metric == "production":
                    df = self.get_production(year=year)
                elif metric == "area":
                    df = self.get_area_harvested(year=year)
                else:
                    continue

                if not df.empty:
                    row = df.iloc[0]
                    results.append(
                        {
                            "蔬菜": self.VEGETABLE_TYPES.get(veg_en, {}).get("cn", veg_en),
                            "英文": veg_en,
                            "数值": row.get("Value", ""),
                            "单位": row.get("unit_desc", ""),
                        }
                    )
            except Exception as e:
                logger.debug(f"获取{veg}数据失败: {e}")

        return pd.DataFrame(results)

    def list_vegetables(self) -> pd.DataFrame:
        """列出所有支持的蔬菜"""
        return pd.DataFrame(
            [
                {"英文": en, "中文": info["cn"], "默认单位": info["unit"]}
                for en, info in self.VEGETABLE_TYPES.items()
            ]
        )

    def _translate_commodity(self, commodity: str) -> str:
        """转换商品名称"""
        commodity_upper = commodity.upper()

        if commodity_upper in self.VEGETABLE_TYPES:
            return commodity_upper

        for en, info in self.VEGETABLE_TYPES.items():
            if info["cn"] == commodity:
                return en

        return commodity_upper
