# -*- coding: utf-8 -*-
"""
USDA-CN 数据获取基类
===================

提供统一的数据获取接口，所有商品数据模块都继承此类。
"""

from typing import Optional, Union, List, Dict, Any, TypeVar, Generic
from abc import ABC, abstractmethod
import pandas as pd

from usda_cn.client import NASSClient
from usda_cn.utils.helpers import setup_logger
from usda_cn.utils.constants import STATE_NAMES_CN


logger = setup_logger("usda_cn.base")
T = TypeVar("T")


class BaseDataFetcher(ABC):
    """
    数据获取器基类

    所有商品数据模块都应继承此类，提供统一的数据获取接口。

    参数:
        client: NASSClient实例
        api_key: API密钥（可选）

    属性:
        COMMODITY: 商品英文名称
        COMMODITY_CN: 商品中文名称
        GROUP: 所属商品组
        SECTOR: 所属部门

    示例:
        >>> class SoybeanData(BaseDataFetcher):
        ...     COMMODITY = "SOYBEANS"
        ...     COMMODITY_CN = "大豆"
        ...     GROUP = "FIELD CROPS"
        ...     SECTOR = "CROPS"
    """

    COMMODITY: str = ""
    COMMODITY_CN: str = ""
    GROUP: str = ""
    SECTOR: str = ""

    # 常用统计类别
    STATS_PRODUCTION = "PRODUCTION"
    STATS_AREA_PLANTED = "AREA PLANTED"
    STATS_AREA_HARVESTED = "AREA HARVESTED"
    STATS_YIELD = "YIELD"
    STATS_PRICE = "PRICE RECEIVED"
    STATS_STOCKS = "STOCKS"
    STATS_SALES = "SALES"
    STATS_INVENTORY = "INVENTORY"
    STATS_VALUE = "VALUE"

    # 常用单位
    UNIT_BU = "BU"
    UNIT_ACRES = "ACRES"
    UNIT_BU_PER_ACRE = "BU / ACRE"
    UNIT_DOLLAR = "$"
    UNIT_DOLLAR_PER_BU = "$ / BU"
    UNIT_LB = "LB"
    UNIT_CWT = "CWT"
    UNIT_TONS = "TONS"
    UNIT_HEAD = "HEAD"

    def __init__(
        self,
        client: Optional[NASSClient] = None,
        api_key: Optional[str] = None,
    ):
        if client:
            self.client = client
        elif api_key:
            self.client = NASSClient(api_key=api_key)
        else:
            self.client = NASSClient()

        self._cache: Dict[str, pd.DataFrame] = {}

    def _query(
        self,
        statisticcat_desc: str,
        year: Optional[Union[int, List[int], Dict]] = None,
        state: Optional[str] = None,
        agg_level: str = "NATIONAL",
        unit_desc: Optional[str] = None,
        reference_period: str = "YEAR",
        **kwargs,
    ) -> pd.DataFrame:
        """
        执行查询的基础方法

        参数:
            statisticcat_desc: 统计类别
            year: 年份
            state: 州代码
            agg_level: 地理聚合级别
            unit_desc: 单位
            reference_period: 参考期间
            **kwargs: 其他参数

        返回:
            查询结果DataFrame
        """
        params: Dict[str, Any] = {
            "commodity_desc": self.COMMODITY,
            "statisticcat_desc": statisticcat_desc,
            "agg_level_desc": agg_level,
        }

        if unit_desc:
            params["unit_desc"] = unit_desc

        if reference_period and reference_period != "YEAR":
            params["reference_period_desc"] = reference_period

        if state:
            params["state_alpha"] = state.upper() if len(state) == 2 else state.upper()

        # 处理年份参数
        if year:
            if isinstance(year, int):
                params["year"] = year
            elif isinstance(year, list):
                params["year"] = ",".join(map(str, year))
            elif isinstance(year, dict):
                if "ge" in year:
                    params["year__GE"] = year["ge"]
                if "le" in year:
                    params["year__LE"] = year["le"]
                if "gt" in year:
                    params["year__GT"] = year["gt"]
                if "lt" in year:
                    params["year__LT"] = year["lt"]

        # 添加其他参数
        params.update(kwargs)

        # 执行查询
        data = self.client.quickstats.query(**params)
        return self._process_data(data)

    def get_production(
        self,
        year: Optional[Union[int, List[int], Dict]] = None,
        state: Optional[str] = None,
        agg_level: str = "NATIONAL",
        **kwargs,
    ) -> pd.DataFrame:
        """
        获取产量数据

        参数:
            year: 年份
            state: 州代码
            agg_level: 地理聚合级别

        返回:
            产量数据DataFrame
        """
        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc=self.STATS_PRODUCTION,
            year=year,
            state=state,
            agg_level=agg_level,
            **kwargs,
        )

    def get_area_planted(
        self,
        year: Optional[Union[int, List[int], Dict]] = None,
        state: Optional[str] = None,
        agg_level: str = "NATIONAL",
        **kwargs,
    ) -> pd.DataFrame:
        """
        获取种植面积数据

        参数:
            year: 年份
            state: 州代码
            agg_level: 地理聚合级别

        返回:
            种植面积DataFrame
        """
        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc=self.STATS_AREA_PLANTED,
            year=year,
            state=state,
            agg_level=agg_level,
            unit_desc=self.UNIT_ACRES,
            **kwargs,
        )

    def get_area_harvested(
        self,
        year: Optional[Union[int, List[int], Dict]] = None,
        state: Optional[str] = None,
        agg_level: str = "NATIONAL",
        **kwargs,
    ) -> pd.DataFrame:
        """
        获取收获面积数据
        """
        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc=self.STATS_AREA_HARVESTED,
            year=year,
            state=state,
            agg_level=agg_level,
            unit_desc=self.UNIT_ACRES,
            **kwargs,
        )

    def get_yield(
        self,
        year: Optional[Union[int, List[int], Dict]] = None,
        state: Optional[str] = None,
        agg_level: str = "NATIONAL",
        **kwargs,
    ) -> pd.DataFrame:
        """
        获取单产数据
        """
        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc=self.STATS_YIELD,
            year=year,
            state=state,
            agg_level=agg_level,
            **kwargs,
        )

    def get_price(
        self,
        year: Optional[Union[int, List[int], Dict]] = None,
        state: Optional[str] = None,
        agg_level: str = "NATIONAL",
        **kwargs,
    ) -> pd.DataFrame:
        """
        获取价格数据
        """
        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc=self.STATS_PRICE,
            year=year,
            state=state,
            agg_level=agg_level,
            **kwargs,
        )

    def get_stocks(
        self,
        year: Optional[Union[int, List[int], Dict]] = None,
        reference_period: str = "YEAR",
        **kwargs,
    ) -> pd.DataFrame:
        """
        获取库存数据

        参数:
            year: 年份
            reference_period: 库存时点 (YEAR, DEC 1, MAR 1, JUN 1, SEP 1)
        """
        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc=self.STATS_STOCKS,
            year=year,
            reference_period=reference_period,
            **kwargs,
        )

    def get_inventory(
        self,
        year: Optional[Union[int, List[int], Dict]] = None,
        state: Optional[str] = None,
        agg_level: str = "NATIONAL",
        **kwargs,
    ) -> pd.DataFrame:
        """
        获取存栏/库存数据（适用于畜牧产品）
        """
        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc=self.STATS_INVENTORY,
            year=year,
            state=state,
            agg_level=agg_level,
            **kwargs,
        )

    def get_sales(
        self,
        year: Optional[Union[int, List[int], Dict]] = None,
        state: Optional[str] = None,
        agg_level: str = "NATIONAL",
        **kwargs,
    ) -> pd.DataFrame:
        """
        获取销售数据
        """
        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc=self.STATS_SALES,
            year=year,
            state=state,
            agg_level=agg_level,
            **kwargs,
        )

    def get_summary(
        self,
        year: int = 2024,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        获取数据汇总

        参数:
            year: 年份
            state: 州代码

        返回:
            汇总数据DataFrame
        """
        results = []

        # 获取各项数据
        methods = [
            ("种植面积", self.get_area_planted),
            ("收获面积", self.get_area_harvested),
            ("单产", self.get_yield),
            ("产量", self.get_production),
            ("价格", self.get_price),
        ]

        for metric_name, func in methods:
            try:
                df = func(year=year, state=state)
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

    def get_top_states(
        self,
        year: int = 2024,
        metric: str = "production",
        top_n: int = 10,
    ) -> pd.DataFrame:
        """
        获取主产州排名

        参数:
            year: 年份
            metric: 指标类型 (production, area, yield)
            top_n: 返回前N个州
        """
        metric_map = {
            "production": self.get_production,
            "area": self.get_area_planted,
            "yield": self.get_yield,
        }

        if metric not in metric_map:
            raise ValueError(f"不支持的指标: {metric}")

        df = metric_map[metric](year=year, agg_level="STATE")

        if df.empty:
            return df

        df = df.sort_values("Value_numeric", ascending=False).head(top_n)
        df["州名"] = df["state_alpha"].map(STATE_NAMES_CN)

        return df[["state_alpha", "州名", "year", "Value", "unit_desc"]]

    def get_historical_trend(
        self,
        start_year: int = 2010,
        end_year: int = 2024,
        state: Optional[str] = None,
        metric: str = "production",
    ) -> pd.DataFrame:
        """
        获取历史趋势数据

        参数:
            start_year: 起始年份
            end_year: 结束年份
            state: 州代码
            metric: 指标类型
        """
        year_range = {"ge": start_year, "le": end_year}

        metric_map = {
            "production": self.get_production,
            "area": self.get_area_planted,
            "yield": self.get_yield,
            "price": self.get_price,
        }

        if metric not in metric_map:
            raise ValueError(f"不支持的指标: {metric}")

        df = metric_map[metric](year=year_range, state=state)
        df = df.sort_values("year")

        return df

    def _process_data(self, data: List[Dict]) -> pd.DataFrame:
        """处理API返回的数据"""
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)

        # 转换数值
        if "Value" in df.columns:
            df["Value_numeric"] = df["Value"].astype(str).str.replace(",", "").str.strip()
            df["Value_numeric"] = pd.to_numeric(df["Value_numeric"], errors="coerce")

        # 转换年份
        if "year" in df.columns:
            df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")

        return df

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(commodity='{self.COMMODITY_CN}')"
