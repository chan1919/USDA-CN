# -*- coding: utf-8 -*-
"""
玉米数据模块
===========

提供便捷的玉米数据获取接口。
"""

from typing import Optional, Union, List, Dict
import pandas as pd

from usda_cn.client import NASSClient
from usda_cn.utils.helpers import setup_logger
from usda_cn.utils.constants import MAJOR_CORN_STATES, STATE_NAMES_CN


logger = setup_logger("usda_cn.corn")


class CornData:
    """
    玉米数据获取器

    专门用于获取美国玉米相关统计数据。

    参数:
        client: NASSClient实例
        api_key: API密钥

    示例:
        >>> corn = CornData(api_key="YOUR_KEY")
        >>> df = corn.get_production(year=2024)
    """

    COMMODITY = "CORN"
    COMMODITY_CN = "玉米"

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

    def get_production(
        self,
        year: Optional[Union[int, List[int], Dict]] = None,
        state: Optional[str] = None,
        agg_level: str = "NATIONAL",
        unit: str = "BU",
    ) -> pd.DataFrame:
        """
        获取玉米产量数据

        参数:
            year: 年份
            state: 州代码
            agg_level: 地理聚合级别
            unit: 单位 ("BU" 或 "$")

        返回:
            产量DataFrame (单位: 蒲式耳)

        示例:
            >>> corn = CornData()
            >>> df = corn.get_production(year=2024)
            >>> print(f"2024年玉米产量: {df['Value_numeric'].iloc[0]:,} 蒲式耳")
        """
        if year is None:
            year = {"ge": 2020, "le": 2024}

        params = {
            "commodity_desc": self.COMMODITY,
            "statisticcat_desc": "PRODUCTION",
            "unit_desc": unit,
            "agg_level_desc": agg_level,
        }

        if isinstance(year, int):
            params["year"] = year
        elif isinstance(year, list):
            params["year"] = ",".join(map(str, year))
        elif isinstance(year, dict):
            if "ge" in year:
                params["year__GE"] = year["ge"]
            if "le" in year:
                params["year__LE"] = year["le"]

        if state:
            params["state_alpha"] = state.upper() if len(state) == 2 else state

        data = self.client.quickstats.query(**params)
        return self._process_data(data)

    def get_area_planted(
        self,
        year: Optional[Union[int, List[int], Dict]] = None,
        state: Optional[str] = None,
        agg_level: str = "NATIONAL",
    ) -> pd.DataFrame:
        """
        获取玉米种植面积数据

        参数:
            year: 年份
            state: 州代码
            agg_level: 地理聚合级别

        返回:
            种植面积DataFrame (单位: 英亩)
        """
        if year is None:
            year = {"ge": 2020, "le": 2024}

        params = {
            "commodity_desc": self.COMMODITY,
            "statisticcat_desc": "AREA PLANTED",
            "unit_desc": "ACRES",
            "agg_level_desc": agg_level,
        }

        if isinstance(year, int):
            params["year"] = year
        elif isinstance(year, dict):
            if "ge" in year:
                params["year__GE"] = year["ge"]
            if "le" in year:
                params["year__LE"] = year["le"]

        if state:
            params["state_alpha"] = state.upper() if len(state) == 2 else state

        data = self.client.quickstats.query(**params)
        return self._process_data(data)

    def get_yield(
        self,
        year: Optional[Union[int, List[int], Dict]] = None,
        state: Optional[str] = None,
        agg_level: str = "NATIONAL",
    ) -> pd.DataFrame:
        """
        获取玉米单产数据

        参数:
            year: 年份
            state: 州代码
            agg_level: 地理聚合级别

        返回:
            单产DataFrame (单位: 蒲式耳/英亩)
        """
        if year is None:
            year = {"ge": 2020, "le": 2024}

        params = {
            "commodity_desc": self.COMMODITY,
            "statisticcat_desc": "YIELD",
            "unit_desc": "BU / ACRE",
            "agg_level_desc": agg_level,
        }

        if isinstance(year, int):
            params["year"] = year
        elif isinstance(year, dict):
            if "ge" in year:
                params["year__GE"] = year["ge"]
            if "le" in year:
                params["year__LE"] = year["le"]

        if state:
            params["state_alpha"] = state.upper() if len(state) == 2 else state

        data = self.client.quickstats.query(**params)
        return self._process_data(data)

    def get_price(
        self,
        year: Optional[Union[int, List[int], Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        获取玉米价格数据

        参数:
            year: 年份
            state: 州代码

        返回:
            价格DataFrame (单位: 美元/蒲式耳)
        """
        if year is None:
            year = {"ge": 2020, "le": 2024}

        params = {
            "commodity_desc": self.COMMODITY,
            "statisticcat_desc": "PRICE RECEIVED",
            "agg_level_desc": "NATIONAL",
        }

        if isinstance(year, int):
            params["year"] = year
        elif isinstance(year, dict):
            if "ge" in year:
                params["year__GE"] = year["ge"]
            if "le" in year:
                params["year__LE"] = year["le"]

        if state:
            params["state_alpha"] = state.upper()

        data = self.client.quickstats.query(**params)
        return self._process_data(data)

    def get_stocks(
        self,
        year: Optional[Union[int, List[int], Dict]] = None,
        reference_period: str = "YEAR",
    ) -> pd.DataFrame:
        """
        获取玉米库存数据

        参数:
            year: 年份
            reference_period: 库存时点

        返回:
            库存DataFrame (单位: 蒲式耳)
        """
        if year is None:
            year = {"ge": 2020, "le": 2024}

        params = {
            "commodity_desc": self.COMMODITY,
            "statisticcat_desc": "STOCKS",
            "unit_desc": "BU",
            "reference_period_desc": reference_period,
            "agg_level_desc": "NATIONAL",
        }

        if isinstance(year, int):
            params["year"] = year
        elif isinstance(year, dict):
            if "ge" in year:
                params["year__GE"] = year["ge"]
            if "le" in year:
                params["year__LE"] = year["le"]

        data = self.client.quickstats.query(**params)
        return self._process_data(data)

    def get_summary(
        self,
        year: int = 2024,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        获取玉米数据汇总

        参数:
            year: 年份
            state: 州代码

        返回:
            汇总DataFrame
        """
        results = []

        metrics = [
            ("种植面积", self.get_area_planted),
            ("单产", self.get_yield),
            ("产量", self.get_production),
        ]

        for metric_name, func in metrics:
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
                        }
                    )
            except Exception as e:
                logger.warning(f"获取{metric_name}数据失败: {e}")

        return pd.DataFrame(results)

    def get_top_states(
        self,
        year: int = 2024,
        metric: str = "production",
        top_n: int = 10,
    ) -> pd.DataFrame:
        """
        获取玉米主产州排名

        参数:
            year: 年份
            metric: 指标类型
            top_n: 返回前N个州

        返回:
            排名DataFrame
        """
        if metric == "production":
            df = self.get_production(year=year, agg_level="STATE")
        elif metric == "area":
            df = self.get_area_planted(year=year, agg_level="STATE")
        elif metric == "yield":
            df = self.get_yield(year=year, agg_level="STATE")
        else:
            raise ValueError(f"不支持的指标: {metric}")

        if df.empty:
            return df

        df = df.sort_values("Value_numeric", ascending=False).head(top_n)
        df["州名"] = df["state_alpha"].map(STATE_NAMES_CN)

        return df[["state_alpha", "州名", "year", "Value", "unit_desc"]]

    def _process_data(self, data: List[Dict]) -> pd.DataFrame:
        """处理API返回的数据"""
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)

        if "Value" in df.columns:
            df["Value_numeric"] = (
                df["Value"].astype(str).str.replace(",", "").str.strip()
            )
            df["Value_numeric"] = pd.to_numeric(df["Value_numeric"], errors="coerce")

        if "year" in df.columns:
            df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")

        return df

    def __repr__(self) -> str:
        return f"CornData(commodity='{self.COMMODITY_CN}')"
