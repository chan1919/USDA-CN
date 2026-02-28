# -*- coding: utf-8 -*-
"""
水果和坚果数据模块
=================

包含所有水果和坚果的数据获取接口：
- 落叶水果: 苹果、桃、梨、樱桃、葡萄
- 柑橘类: 橙子、柠檬、葡萄柚
- 浆果: 草莓、蓝莓、树莓
- 坚果: 杏仁、核桃、碧根果
"""

from typing import Optional, Union, Dict, List
import pandas as pd

from usda_cn.data.base import BaseDataFetcher
from usda_cn.utils.helpers import setup_logger


logger = setup_logger("usda_cn.fruit_nuts")


class FruitNutsData(BaseDataFetcher):
    """
    水果和坚果数据获取器

    提供所有水果和坚果的数据访问接口。

    示例:
        >>> fruit = FruitNutsData()
        >>> df = fruit.get_apple_production(year=2024)
        >>> df = fruit.get_almond_production(year=2024)
    """

    SECTOR = "CROPS"
    GROUP = "FRUIT & TREE NUTS"

    # 水果类型
    FRUIT_TYPES = {
        # 落叶水果
        "APPLES": {"cn": "苹果", "unit": "LB"},
        "PEACHES": {"cn": "桃", "unit": "LB"},
        "PEARS": {"cn": "梨", "unit": "LB"},
        "CHERRIES": {"cn": "樱桃", "unit": "LB"},
        "GRAPES": {"cn": "葡萄", "unit": "LB"},
        "APRICOTS": {"cn": "杏", "unit": "LB"},
        "NECTARINES": {"cn": "油桃", "unit": "LB"},
        "PLUMS": {"cn": "李子", "unit": "LB"},
        "PRUNES": {"cn": "西梅", "unit": "LB"},
        # 柑橘类
        "ORANGES": {"cn": "橙子", "unit": "BOX"},
        "LEMONS": {"cn": "柠檬", "unit": "BOX"},
        "GRAPEFRUIT": {"cn": "葡萄柚", "unit": "BOX"},
        "TANGERINES": {"cn": "橘子", "unit": "BOX"},
        "CITRUS": {"cn": "柑橘", "unit": "BOX"},
        # 浆果
        "STRAWBERRIES": {"cn": "草莓", "unit": "LB"},
        "BLUEBERRIES": {"cn": "蓝莓", "unit": "LB"},
        "RASPBERRIES": {"cn": "树莓", "unit": "LB"},
        "BLACKBERRIES": {"cn": "黑莓", "unit": "LB"},
        "CRANBERRIES": {"cn": "蔓越莓", "unit": "LB"},
        # 热带水果
        "BANANAS": {"cn": "香蕉", "unit": "LB"},
        "PINEAPPLES": {"cn": "菠萝", "unit": "LB"},
        "AVOCADOS": {"cn": "牛油果", "unit": "LB"},
        # 坚果
        "ALMONDS": {"cn": "杏仁", "unit": "LB"},
        "WALNUTS": {"cn": "核桃", "unit": "LB"},
        "PECANS": {"cn": "碧根果", "unit": "LB"},
        "PISTACHIOS": {"cn": "开心果", "unit": "LB"},
        "HAZELNUTS": {"cn": "榛子", "unit": "LB"},
        "MACADAMIA": {"cn": "夏威夷果", "unit": "LB"},
    }

    def __init__(self, client=None, api_key=None):
        super().__init__(client=client, api_key=api_key)

    def get_apple_production(self, year=None, state=None) -> pd.DataFrame:
        """获取苹果产量数据"""
        self.COMMODITY = "APPLES"
        self.COMMODITY_CN = "苹果"
        return self.get_production(year=year, state=state)

    def get_peach_production(self, year=None, state=None) -> pd.DataFrame:
        """获取桃产量数据"""
        self.COMMODITY = "PEACHES"
        self.COMMODITY_CN = "桃"
        return self.get_production(year=year, state=state)

    def get_cherry_production(self, year=None, state=None) -> pd.DataFrame:
        """获取樱桃产量数据"""
        self.COMMODITY = "CHERRIES"
        self.COMMODITY_CN = "樱桃"
        return self.get_production(year=year, state=state)

    def get_grape_production(self, year=None, state=None) -> pd.DataFrame:
        """获取葡萄产量数据"""
        self.COMMODITY = "GRAPES"
        self.COMMODITY_CN = "葡萄"
        return self.get_production(year=year, state=state)

    def get_orange_production(self, year=None, state=None) -> pd.DataFrame:
        """获取橙子产量数据"""
        self.COMMODITY = "ORANGES"
        self.COMMODITY_CN = "橙子"
        return self.get_production(year=year, state=state)

    def get_lemon_production(self, year=None, state=None) -> pd.DataFrame:
        """获取柠檬产量数据"""
        self.COMMODITY = "LEMONS"
        self.COMMODITY_CN = "柠檬"
        return self.get_production(year=year, state=state)

    def get_grapefruit_production(self, year=None, state=None) -> pd.DataFrame:
        """获取葡萄柚产量数据"""
        self.COMMODITY = "GRAPEFRUIT"
        self.COMMODITY_CN = "葡萄柚"
        return self.get_production(year=year, state=state)

    def get_strawberry_production(self, year=None, state=None) -> pd.DataFrame:
        """获取草莓产量数据"""
        self.COMMODITY = "STRAWBERRIES"
        self.COMMODITY_CN = "草莓"
        return self.get_production(year=year, state=state)

    def get_blueberry_production(self, year=None, state=None) -> pd.DataFrame:
        """获取蓝莓产量数据"""
        self.COMMODITY = "BLUEBERRIES"
        self.COMMODITY_CN = "蓝莓"
        return self.get_production(year=year, state=state)

    def get_cranberry_production(self, year=None, state=None) -> pd.DataFrame:
        """获取蔓越莓产量数据"""
        self.COMMODITY = "CRANBERRIES"
        self.COMMODITY_CN = "蔓越莓"
        return self.get_production(year=year, state=state)

    def get_avocado_production(self, year=None, state=None) -> pd.DataFrame:
        """获取牛油果产量数据"""
        self.COMMODITY = "AVOCADOS"
        self.COMMODITY_CN = "牛油果"
        return self.get_production(year=year, state=state)

    def get_almond_production(self, year=None, state=None) -> pd.DataFrame:
        """获取杏仁产量数据"""
        self.COMMODITY = "ALMONDS"
        self.COMMODITY_CN = "杏仁"
        return self.get_production(year=year, state=state)

    def get_walnut_production(self, year=None, state=None) -> pd.DataFrame:
        """获取核桃产量数据"""
        self.COMMODITY = "WALNUTS"
        self.COMMODITY_CN = "核桃"
        return self.get_production(year=year, state=state)

    def get_pecan_production(self, year=None, state=None) -> pd.DataFrame:
        """获取碧根果产量数据"""
        self.COMMODITY = "PECANS"
        self.COMMODITY_CN = "碧根果"
        return self.get_production(year=year, state=state)

    def get_pistachio_production(self, year=None, state=None) -> pd.DataFrame:
        """获取开心果产量数据"""
        self.COMMODITY = "PISTACHIOS"
        self.COMMODITY_CN = "开心果"
        return self.get_production(year=year, state=state)

    def get_bearing_area(
        self,
        commodity: str,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        获取果树结果面积数据

        参数:
            commodity: 水果/坚果名称
            year: 年份
            state: 州代码
        """
        commodity_en = self._translate_commodity(commodity)
        self.COMMODITY = commodity_en

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="AREA BEARING",
            year=year,
            state=state,
            unit_desc="ACRES",
        )

    def get_non_bearing_area(
        self,
        commodity: str,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取果树未结果面积数据"""
        commodity_en = self._translate_commodity(commodity)
        self.COMMODITY = commodity_en

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="AREA NON-BEARING",
            year=year,
            state=state,
            unit_desc="ACRES",
        )

    def get_utilization(
        self,
        commodity: str,
        util_practice: str = "FRESH MARKET",
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        获取水果利用方式数据

        参数:
            commodity: 水果名称
            util_practice: 利用方式 (FRESH MARKET, PROCESSING)
            year: 年份
            state: 州代码
        """
        commodity_en = self._translate_commodity(commodity)
        self.COMMODITY = commodity_en

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="PRODUCTION",
            year=year,
            state=state,
            util_practice_desc=util_practice,
        )

    def get_price(
        self,
        commodity: str,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取水果/坚果价格数据"""
        commodity_en = self._translate_commodity(commodity)
        self.COMMODITY = commodity_en

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return super().get_price(year=year, state=state)

    def compare_fruits(
        self,
        fruits: List[str],
        year: int = 2024,
        metric: str = "production",
    ) -> pd.DataFrame:
        """比较多种水果的数据"""
        results = []

        for fruit in fruits:
            fruit_en = self._translate_commodity(fruit)
            self.COMMODITY = fruit_en

            try:
                if metric == "production":
                    df = self.get_production(year=year)
                elif metric == "area":
                    df = self.get_bearing_area(fruit, year=year)
                else:
                    continue

                if not df.empty:
                    row = df.iloc[0]
                    results.append(
                        {
                            "水果/坚果": self.FRUIT_TYPES.get(fruit_en, {}).get("cn", fruit_en),
                            "英文": fruit_en,
                            "数值": row.get("Value", ""),
                            "单位": row.get("unit_desc", ""),
                        }
                    )
            except Exception as e:
                logger.debug(f"获取{fruit}数据失败: {e}")

        return pd.DataFrame(results)

    def list_fruits(self) -> pd.DataFrame:
        """列出所有支持的水果和坚果"""
        return pd.DataFrame(
            [
                {"英文": en, "中文": info["cn"], "默认单位": info["unit"]}
                for en, info in self.FRUIT_TYPES.items()
            ]
        )

    def _translate_commodity(self, commodity: str) -> str:
        """转换商品名称"""
        commodity_upper = commodity.upper()

        if commodity_upper in self.FRUIT_TYPES:
            return commodity_upper

        for en, info in self.FRUIT_TYPES.items():
            if info["cn"] == commodity:
                return en

        return commodity_upper
