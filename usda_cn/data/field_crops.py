# -*- coding: utf-8 -*-
"""
大田作物数据模块
==============

包含所有大田作物的数据获取接口：
- 谷物: 玉米、小麦、大麦、燕麦、高粱、水稻
- 油料: 大豆、油菜籽、向日葵、花生
- 纤维: 棉花
- 饲料: 干草
"""

from typing import Optional, Union, List, Dict
import pandas as pd

from usda_cn.data.base import BaseDataFetcher
from usda_cn.utils.helpers import setup_logger


logger = setup_logger("usda_cn.field_crops")


class FieldCropsData(BaseDataFetcher):
    """
    大田作物数据获取器

    提供所有大田作物的统一数据访问接口。

    示例:
        >>> crops = FieldCropsData()
        >>> df = crops.get_commodity_data("CORN", year=2024)
    """

    SECTOR = "CROPS"
    GROUP = "FIELD CROPS"

    # 主要大田作物列表
    MAJOR_CROPS = {
        # 谷物
        "CORN": {"cn": "玉米", "unit": "BU"},
        "WHEAT": {"cn": "小麦", "unit": "BU"},
        "BARLEY": {"cn": "大麦", "unit": "BU"},
        "OATS": {"cn": "燕麦", "unit": "BU"},
        "SORGHUM": {"cn": "高粱", "unit": "BU"},
        "RICE": {"cn": "水稻", "unit": "CWT"},
        # 油料
        "SOYBEANS": {"cn": "大豆", "unit": "BU"},
        "CANOLA": {"cn": "油菜籽", "unit": "LB"},
        "SUNFLOWER": {"cn": "向日葵", "unit": "LB"},
        "PEANUTS": {"cn": "花生", "unit": "LB"},
        # 纤维
        "COTTON": {"cn": "棉花", "unit": "480 LB BALES"},
        # 饲料
        "HAY": {"cn": "干草", "unit": "TONS"},
    }

    def __init__(self, client=None, api_key=None):
        super().__init__(client=client, api_key=api_key)

    def get_commodity_data(
        self,
        commodity: str,
        statistic: str = "PRODUCTION",
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
        agg_level: str = "NATIONAL",
    ) -> pd.DataFrame:
        """
        获取指定作物的数据

        参数:
            commodity: 作物名称 (英文或中文)
            statistic: 统计类别
            year: 年份
            state: 州代码
            agg_level: 地理聚合级别

        返回:
            数据DataFrame

        示例:
            >>> crops = FieldCropsData()
            >>> df = crops.get_commodity_data("CORN", "PRODUCTION", year=2024)
            >>> df = crops.get_commodity_data("大豆", year=2024)  # 支持中文
        """
        # 转换中文到英文
        commodity_en = self._translate_commodity(commodity)

        self.COMMODITY = commodity_en
        return self._query(
            statisticcat_desc=statistic,
            year=year,
            state=state,
            agg_level=agg_level,
        )

    def get_corn(self, year=None, state=None, agg_level="NATIONAL") -> pd.DataFrame:
        """获取玉米数据"""
        self.COMMODITY = "CORN"
        self.COMMODITY_CN = "玉米"
        return self.get_production(year=year, state=state, agg_level=agg_level)

    def get_wheat(self, year=None, state=None, agg_level="NATIONAL") -> pd.DataFrame:
        """获取小麦数据"""
        self.COMMODITY = "WHEAT"
        self.COMMODITY_CN = "小麦"
        return self.get_production(year=year, state=state, agg_level=agg_level)

    def get_soybeans(self, year=None, state=None, agg_level="NATIONAL") -> pd.DataFrame:
        """获取大豆数据"""
        self.COMMODITY = "SOYBEANS"
        self.COMMODITY_CN = "大豆"
        return self.get_production(year=year, state=state, agg_level=agg_level)

    def get_cotton(self, year=None, state=None, agg_level="NATIONAL") -> pd.DataFrame:
        """获取棉花数据"""
        self.COMMODITY = "COTTON"
        self.COMMODITY_CN = "棉花"
        return self.get_production(year=year, state=state, agg_level=agg_level)

    def get_rice(self, year=None, state=None, agg_level="NATIONAL") -> pd.DataFrame:
        """获取水稻数据"""
        self.COMMODITY = "RICE"
        self.COMMODITY_CN = "水稻"
        return self.get_production(year=year, state=state, agg_level=agg_level)

    def get_barley(self, year=None, state=None, agg_level="NATIONAL") -> pd.DataFrame:
        """获取大麦数据"""
        self.COMMODITY = "BARLEY"
        self.COMMODITY_CN = "大麦"
        return self.get_production(year=year, state=state, agg_level=agg_level)

    def get_sorghum(self, year=None, state=None, agg_level="NATIONAL") -> pd.DataFrame:
        """获取高粱数据"""
        self.COMMODITY = "SORGHUM"
        self.COMMODITY_CN = "高粱"
        return self.get_production(year=year, state=state, agg_level=agg_level)

    def get_oats(self, year=None, state=None, agg_level="NATIONAL") -> pd.DataFrame:
        """获取燕麦数据"""
        self.COMMODITY = "OATS"
        self.COMMODITY_CN = "燕麦"
        return self.get_production(year=year, state=state, agg_level=agg_level)

    def get_hay(self, year=None, state=None, agg_level="NATIONAL") -> pd.DataFrame:
        """获取干草数据"""
        self.COMMODITY = "HAY"
        self.COMMODITY_CN = "干草"
        return self.get_production(year=year, state=state, agg_level=agg_level)

    def get_peanuts(self, year=None, state=None, agg_level="NATIONAL") -> pd.DataFrame:
        """获取花生数据"""
        self.COMMODITY = "PEANUTS"
        self.COMMODITY_CN = "花生"
        return self.get_production(year=year, state=state, agg_level=agg_level)

    def get_sunflower(self, year=None, state=None, agg_level="NATIONAL") -> pd.DataFrame:
        """获取向日葵数据"""
        self.COMMODITY = "SUNFLOWER"
        self.COMMODITY_CN = "向日葵"
        return self.get_production(year=year, state=state, agg_level=agg_level)

    def get_canola(self, year=None, state=None, agg_level="NATIONAL") -> pd.DataFrame:
        """获取油菜籽数据"""
        self.COMMODITY = "CANOLA"
        self.COMMODITY_CN = "油菜籽"
        return self.get_production(year=year, state=state, agg_level=agg_level)

    def list_crops(self) -> pd.DataFrame:
        """列出所有支持的大田作物"""
        return pd.DataFrame(
            [
                {"英文": en, "中文": info["cn"], "默认单位": info["unit"]}
                for en, info in self.MAJOR_CROPS.items()
            ]
        )

    def compare_crops(
        self,
        crops: List[str],
        year: int = 2024,
        metric: str = "production",
    ) -> pd.DataFrame:
        """
        比较多个作物的数据

        参数:
            crops: 作物列表
            year: 年份
            metric: 指标类型

        返回:
            比较数据DataFrame
        """
        results = []

        for crop in crops:
            crop_en = self._translate_commodity(crop)
            self.COMMODITY = crop_en

            try:
                if metric == "production":
                    df = self.get_production(year=year)
                elif metric == "area":
                    df = self.get_area_planted(year=year)
                elif metric == "yield":
                    df = self.get_yield(year=year)
                else:
                    continue

                if not df.empty:
                    row = df.iloc[0]
                    results.append(
                        {
                            "作物": self.MAJOR_CROPS.get(crop_en, {}).get("cn", crop_en),
                            "英文": crop_en,
                            "数值": row.get("Value", ""),
                            "单位": row.get("unit_desc", ""),
                        }
                    )
            except Exception as e:
                logger.debug(f"获取{crop}数据失败: {e}")

        return pd.DataFrame(results)

    def _translate_commodity(self, commodity: str) -> str:
        """转换商品名称（中文->英文）"""
        commodity_upper = commodity.upper()

        # 如果是英文，直接返回
        if commodity_upper in self.MAJOR_CROPS:
            return commodity_upper

        # 中文转英文
        for en, info in self.MAJOR_CROPS.items():
            if info["cn"] == commodity or info["cn"] == commodity_upper:
                return en

        # 尝试直接匹配
        return commodity_upper
