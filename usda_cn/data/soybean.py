# -*- coding: utf-8 -*-
"""
大豆数据模块
===========

提供便捷的大豆数据获取接口，包括：
- 产量数据
- 种植面积
- 单产数据
- 价格数据
- 库存数据
- 压榨数据
"""

from typing import Optional, Union, List, Dict
import pandas as pd

from usda_cn.client import NASSClient
from usda_cn.utils.helpers import setup_logger
from usda_cn.utils.constants import MAJOR_SOYBEAN_STATES, STATE_NAMES_CN


logger = setup_logger("usda_cn.soybean")


class SoybeanData:
    """
    大豆数据获取器

    专门用于获取美国大豆相关统计数据，提供简洁的中文接口。

    参数:
        client: NASSClient实例，如未提供将自动创建
        api_key: API密钥（仅在未提供client时使用）

    示例:
        >>> # 使用已有客户端
        >>> client = NASSClient(api_key="YOUR_KEY")
        >>> soy = SoybeanData(client=client)
        >>>
        >>> # 或直接传入API密钥
        >>> soy = SoybeanData(api_key="YOUR_KEY")
        >>>
        >>> # 获取产量数据
        >>> df = soy.get_production(year=2024)
        >>> print(df.head())
    """

    COMMODITY = "SOYBEANS"
    COMMODITY_CN = "大豆"

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

        self._cache = {}

    def get_production(
        self,
        year: Optional[Union[int, List[int]]] = None,
        state: Optional[str] = None,
        agg_level: str = "NATIONAL",
        unit: str = "BU",
    ) -> pd.DataFrame:
        """
        获取大豆产量数据

        参数:
            year: 年份
                - 单年: 2024
                - 多年: [2020, 2021, 2022, 2023, 2024]
                - 范围: 使用字典 {"ge": 2020, "le": 2024}
            state: 州代码 (如 "IA", "IL") 或州名
            agg_level: 地理聚合级别
                - "NATIONAL": 全国
                - "STATE": 州
                - "COUNTY": 县
            unit: 单位
                - "BU": 蒲式耳 (默认)
                - "$": 美元 (产值)

        返回:
            产量数据DataFrame

        示例:
            >>> soy = SoybeanData()
            >>>
            >>> # 获取2024年全国产量
            >>> df = soy.get_production(year=2024)
            >>>
            >>> # 获取爱荷华州近5年产量
            >>> df = soy.get_production(year={"ge": 2020, "le": 2024}, state="IA")
            >>>
            >>> # 获取各州2024年产量
            >>> df = soy.get_production(year=2024, agg_level="STATE")
        """
        params = {
            "commodity_desc": self.COMMODITY,
            "statisticcat_desc": "PRODUCTION",
            "unit_desc": unit,
            "agg_level_desc": agg_level,
        }

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

        if state:
            params["state_alpha"] = state.upper() if len(state) == 2 else state

        data = self.client.quickstats.query(**params)
        df = self._process_data(data)

        return df

    def get_area_planted(
        self,
        year: Optional[Union[int, List[int], Dict]] = None,
        state: Optional[str] = None,
        agg_level: str = "NATIONAL",
    ) -> pd.DataFrame:
        """
        获取大豆种植面积数据

        参数:
            year: 年份
            state: 州代码
            agg_level: 地理聚合级别

        返回:
            种植面积DataFrame (单位: 英亩)

        示例:
            >>> soy = SoybeanData()
            >>> df = soy.get_area_planted(year=2024)
            >>> print(f"2024年种植面积: {df['Value_numeric'].iloc[0]:,} 英亩")
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

    def get_area_harvested(
        self,
        year: Optional[Union[int, List[int], Dict]] = None,
        state: Optional[str] = None,
        agg_level: str = "NATIONAL",
    ) -> pd.DataFrame:
        """
        获取大豆收获面积数据

        参数:
            year: 年份
            state: 州代码
            agg_level: 地理聚合级别

        返回:
            收获面积DataFrame (单位: 英亩)
        """
        if year is None:
            year = {"ge": 2020, "le": 2024}

        params = {
            "commodity_desc": self.COMMODITY,
            "statisticcat_desc": "AREA HARVESTED",
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
        获取大豆单产数据

        参数:
            year: 年份
            state: 州代码
            agg_level: 地理聚合级别

        返回:
            单产DataFrame (单位: 蒲式耳/英亩)

        示例:
            >>> soy = SoybeanData()
            >>> df = soy.get_yield(year=2024)
            >>> print(f"2024年单产: {df['Value_numeric'].iloc[0]} 蒲式耳/英亩")
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
        agg_level: str = "NATIONAL",
    ) -> pd.DataFrame:
        """
        获取大豆价格数据

        参数:
            year: 年份
            state: 州代码
            agg_level: 地理聚合级别

        返回:
            价格DataFrame (单位: 美元/蒲式耳)

        示例:
            >>> soy = SoybeanData()
            >>> df = soy.get_price(year=2024)
            >>> print(f"2024年价格: ${df['Value_numeric'].iloc[0]}/蒲式耳")
        """
        if year is None:
            year = {"ge": 2020, "le": 2024}

        params = {
            "commodity_desc": self.COMMODITY,
            "statisticcat_desc": "PRICE RECEIVED",
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

    def get_stocks(
        self,
        year: Optional[Union[int, List[int], Dict]] = None,
        reference_period: str = "YEAR",
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        获取大豆库存数据

        参数:
            year: 年份
            reference_period: 库存时点
                - "YEAR": 年度库存
                - "DEC 1": 12月1日库存
                - "MAR 1": 3月1日库存
                - "JUN 1": 6月1日库存
                - "SEP 1": 9月1日库存
            state: 州代码

        返回:
            库存DataFrame (单位: 蒲式耳)

        示例:
            >>> soy = SoybeanData()
            >>> df = soy.get_stocks(year=2024, reference_period="DEC 1")
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

        if state:
            params["state_alpha"] = state.upper()

        data = self.client.quickstats.query(**params)
        return self._process_data(data)

    def get_crush(
        self,
        year: Optional[Union[int, List[int], Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        获取大豆压榨数据

        参数:
            year: 年份
            state: 州代码

        返回:
            压榨量DataFrame (单位: 蒲式耳)
        """
        if year is None:
            year = {"ge": 2020, "le": 2024}

        params = {
            "commodity_desc": self.COMMODITY,
            "statisticcat_desc": "CRUSHED",
            "unit_desc": "BU",
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
        获取大豆数据汇总

        一次性获取指定年份的所有关键指标：
        - 种植面积
        - 收获面积
        - 单产
        - 产量
        - 价格

        参数:
            year: 年份
            state: 州代码

        返回:
            汇总数据DataFrame

        示例:
            >>> soy = SoybeanData()
            >>> summary = soy.get_summary(year=2024)
            >>> print(summary)
        """
        results = []

        # 获取各项数据
        metrics = [
            ("种植面积", self.get_area_planted),
            ("收获面积", self.get_area_harvested),
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
                            "州": state or "全国",
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
        获取大豆主产州排名

        参数:
            year: 年份
            metric: 指标类型
                - "production": 产量
                - "area": 种植面积
                - "yield": 单产
            top_n: 返回前N个州

        返回:
            排名DataFrame

        示例:
            >>> soy = SoybeanData()
            >>> top_states = soy.get_top_states(year=2024, metric="production")
            >>> print(top_states)
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

        # 排序
        df = df.sort_values("Value_numeric", ascending=False).head(top_n)

        # 添加州名
        df["州名"] = df["state_alpha"].map(STATE_NAMES_CN)

        return df[["state_alpha", "州名", "year", "Value", "unit_desc"]]

    def get_historical_trend(
        self,
        start_year: int = 2010,
        end_year: int = 2024,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        获取大豆历史趋势数据

        参数:
            start_year: 起始年份
            end_year: 结束年份
            state: 州代码

        返回:
            历史趋势DataFrame

        示例:
            >>> soy = SoybeanData()
            >>> trend = soy.get_historical_trend(2010, 2024)
            >>> trend.plot(x="year", y="Value_numeric")
        """
        year_range = {"ge": start_year, "le": end_year}

        # 获取产量数据
        df = self.get_production(year=year_range, state=state)

        # 按年份排序
        df = df.sort_values("year")

        return df

    def _process_data(self, data: List[Dict]) -> pd.DataFrame:
        """处理API返回的数据"""
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)

        # 转换数值
        if "Value" in df.columns:
            df["Value_numeric"] = (
                df["Value"].astype(str).str.replace(",", "").str.strip()
            )
            df["Value_numeric"] = pd.to_numeric(df["Value_numeric"], errors="coerce")

        # 转换年份
        if "year" in df.columns:
            df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")

        return df

    def __repr__(self) -> str:
        return f"SoybeanData(commodity='{self.COMMODITY_CN}')"
