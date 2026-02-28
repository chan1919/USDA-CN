# -*- coding: utf-8 -*-
"""
USDA-CN 主客户端模块
==================

提供统一的API客户端入口，支持多个USDA数据源。
"""

import os
from typing import Optional, Dict, Any, List, Union
import pandas as pd
from dotenv import load_dotenv

from usda_cn.api.quickstats import QuickStatsAPI
from usda_cn.api.psd import PSDAPI
from usda_cn.utils.helpers import validate_api_key, setup_logger
from usda_cn.utils.constants import (
    COMMODITY_NAMES_CN,
    STATISTIC_CATEGORIES_CN,
    AGGREGATION_LEVELS_CN,
)


class NASSClient:
    """
    NASS Quick Stats API 客户端

    美国国家农业统计局(NASS) Quick Stats 数据库的Python接口。
    提供美国农业生产、价格、库存等官方统计数据。

    参数:
        api_key: USDA API密钥。如未提供，将从环境变量 USDA_API_KEY 读取。
        base_url: API基础URL，默认为官方地址。
        timeout: 请求超时时间(秒)，默认30秒。
        retries: 失败重试次数，默认3次。

    属性:
        api_key: 当前使用的API密钥
        quickstats: QuickStats API实例
        psd: PSD API实例

    示例:
        >>> # 使用环境变量中的API密钥
        >>> client = NASSClient()
        >>>
        >>> # 或直接传入API密钥
        >>> client = NASSClient(api_key="YOUR_API_KEY")
        >>>
        >>> # 获取大豆产量数据
        >>> df = client.get_soybean_production(year=2024)
        >>> print(df.head())
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://quickstats.nass.usda.gov/api",
        timeout: int = 30,
        retries: int = 3,
    ):
        # 加载环境变量
        load_dotenv()

        # 获取API密钥
        self.api_key = api_key or os.getenv("USDA_API_KEY")
        if not self.api_key:
            raise ValueError(
                "未找到API密钥。请设置环境变量 USDA_API_KEY 或在初始化时传入 api_key 参数。\n"
                "申请API密钥: https://quickstats.nass.usda.gov/api"
            )

        # 验证API密钥格式
        validate_api_key(self.api_key)

        # 初始化API实例
        self._base_url = base_url
        self._timeout = timeout
        self._retries = retries
        self._logger = setup_logger("usda_cn")

        # 创建API客户端
        self.quickstats = QuickStatsAPI(
            api_key=self.api_key,
            base_url=base_url,
            timeout=timeout,
            retries=retries,
        )

        # PSD API (全球供需数据)
        self.psd = PSDAPI(api_key=self.api_key)

        self._logger.info("USDA-CN客户端初始化成功")

    def get_data(
        self,
        commodity: str,
        statistic_category: Optional[str] = None,
        year: Optional[Union[int, List[int]]] = None,
        state: Optional[str] = None,
        agg_level: str = "NATIONAL",
        format: str = "dataframe",
        **kwargs,
    ) -> Union[pd.DataFrame, Dict, str]:
        """
        通用数据查询接口

        从Quick Stats数据库获取指定商品的统计数据。

        参数:
            commodity: 商品名称(中文或英文均可)
                - 中文: "大豆", "玉米", "小麦", "棉花" 等
                - 英文: "SOYBEANS", "CORN", "WHEAT", "COTTON" 等
            statistic_category: 统计类别
                - 中文: "产量", "种植面积", "收获面积", "单产", "价格" 等
                - 英文: "PRODUCTION", "AREA PLANTED", "AREA HARVESTED", "YIELD", "PRICE RECEIVED"
            year: 年份，可以是单年、年份列表或范围
                - 单年: 2024
                - 多年: [2020, 2021, 2022, 2023, 2024]
                - 范围(使用ge/le): {"ge": 2020, "le": 2024}
            state: 州代码或名称(如 "IA" 或 "IOWA")
            agg_level: 地理聚合级别
                - "NATIONAL": 全国级别
                - "STATE": 州级别
                - "COUNTY": 县级别
            format: 返回格式
                - "dataframe": Pandas DataFrame (默认)
                - "dict": 字典
                - "csv": CSV字符串
            **kwargs: 其他查询参数

        返回:
            根据format参数返回相应格式的数据

        示例:
            >>> # 获取2024年全国大豆产量
            >>> df = client.get_data("大豆", "产量", year=2024)
            >>>
            >>> # 获取2020-2024年玉米种植面积
            >>> df = client.get_data("玉米", "种植面积", year={"ge": 2020, "le": 2024})
            >>>
            >>> # 获取爱荷华州大豆数据
            >>> df = client.get_data("大豆", year=2024, state="IA", agg_level="STATE")
        """
        # 转换中文参数为英文
        commodity_en = COMMODITY_NAMES_CN.get(commodity, commodity.upper() if isinstance(commodity, str) else commodity)
        
        statistic_en = None
        if statistic_category:
            statistic_en = STATISTIC_CATEGORIES_CN.get(statistic_category, statistic_category)

        params = {
            "commodity_desc": commodity_en,
            "agg_level_desc": AGGREGATION_LEVELS_CN.get(agg_level, agg_level),
        }

        if statistic_en:
            params["statisticcat_desc"] = statistic_en
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

        # 获取数据
        data = self.quickstats.query(**params)

        # 转换格式
        if format == "dataframe":
            return self._to_dataframe(data)
        elif format == "dict":
            return data
        elif format == "csv":
            df = self._to_dataframe(data)
            return df.to_csv(index=False)
        else:
            return data

    def get_soybean_production(
        self,
        year: Optional[Union[int, List[int], Dict]] = None,
        state: Optional[str] = None,
        agg_level: str = "NATIONAL",
    ) -> pd.DataFrame:
        """
        获取大豆产量数据

        参数:
            year: 年份，默认为最近5年
            state: 州代码(如 "IA", "IL")
            agg_level: 地理聚合级别

        返回:
            包含大豆产量数据的DataFrame

        示例:
            >>> df = client.get_soybean_production(year=2024)
            >>> print(df[["year", "Value", "unit_desc"]])
        """
        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self.get_data(
            commodity="大豆",
            statistic_category="产量",
            year=year,
            state=state,
            agg_level=agg_level,
            unit_desc="BU",
        )

    def get_soybean_area_planted(
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
            包含大豆种植面积数据的DataFrame
        """
        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self.get_data(
            commodity="大豆",
            statistic_category="种植面积",
            year=year,
            state=state,
            agg_level=agg_level,
        )

    def get_soybean_yield(
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
            包含大豆单产数据的DataFrame (单位: 蒲式耳/英亩)
        """
        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self.get_data(
            commodity="大豆",
            statistic_category="单产",
            year=year,
            state=state,
            agg_level=agg_level,
        )

    def get_soybean_price(
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
            包含大豆价格数据的DataFrame (单位: 美元/蒲式耳)
        """
        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self.get_data(
            commodity="大豆",
            statistic_category="价格",
            year=year,
            state=state,
            agg_level=agg_level,
        )

    def get_soybean_stocks(
        self,
        year: Optional[Union[int, List[int], Dict]] = None,
        reference_period: str = "YEAR",
    ) -> pd.DataFrame:
        """
        获取大豆库存数据

        参数:
            year: 年份
            reference_period: 参考期间 ("YEAR", "DEC 1", "MAR 1", "JUN 1", "SEP 1")

        返回:
            包含大豆库存数据的DataFrame
        """
        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self.get_data(
            commodity="大豆",
            statistic_category="库存",
            year=year,
            reference_period_desc=reference_period,
        )

    def get_corn_production(
        self,
        year: Optional[Union[int, List[int], Dict]] = None,
        state: Optional[str] = None,
        agg_level: str = "NATIONAL",
    ) -> pd.DataFrame:
        """获取玉米产量数据"""
        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self.get_data(
            commodity="玉米",
            statistic_category="产量",
            year=year,
            state=state,
            agg_level=agg_level,
        )

    def get_wheat_production(
        self,
        year: Optional[Union[int, List[int], Dict]] = None,
        state: Optional[str] = None,
        agg_level: str = "NATIONAL",
    ) -> pd.DataFrame:
        """获取小麦产量数据"""
        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self.get_data(
            commodity="小麦",
            statistic_category="产量",
            year=year,
            state=state,
            agg_level=agg_level,
        )

    def get_cotton_production(
        self,
        year: Optional[Union[int, List[int], Dict]] = None,
        state: Optional[str] = None,
        agg_level: str = "NATIONAL",
    ) -> pd.DataFrame:
        """获取棉花产量数据"""
        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self.get_data(
            commodity="棉花",
            statistic_category="产量",
            year=year,
            state=state,
            agg_level=agg_level,
        )

    def list_commodities(self) -> pd.DataFrame:
        """
        获取所有可用商品列表

        返回:
            包含所有商品名称的DataFrame
        """
        data = self.quickstats.get_param_values("commodity_desc")
        return pd.DataFrame(
            {
                "commodity_en": data,
                "commodity_cn": [COMMODITY_NAMES_CN.get(c, c) for c in data],
            }
        )

    def list_states(self) -> pd.DataFrame:
        """
        获取所有可用州列表

        返回:
            包含所有州代码和名称的DataFrame
        """
        data = self.quickstats.get_param_values("state_alpha")
        return pd.DataFrame({"state_alpha": data})

    def list_statistic_categories(self) -> pd.DataFrame:
        """
        获取所有统计类别

        返回:
            包含所有统计类别的DataFrame
        """
        data = self.quickstats.get_param_values("statisticcat_desc")
        return pd.DataFrame(
            {
                "statistic_en": data,
                "statistic_cn": [STATISTIC_CATEGORIES_CN.get(s, s) for s in data],
            }
        )

    def get_record_count(self, **params) -> int:
        """
        获取查询结果记录数量

        在执行查询前，可先使用此方法预估返回记录数，
        避免超过50000条记录限制。

        参数:
            **params: 查询参数

        返回:
            记录数量
        """
        return self.quickstats.get_count(**params)

    def _to_dataframe(self, data: List[Dict]) -> pd.DataFrame:
        """将API返回数据转换为DataFrame"""
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)

        # 转换数值列
        if "Value" in df.columns:
            # 移除逗号和空格，转换为数值
            df["Value"] = df["Value"].astype(str).str.replace(",", "").str.strip()
            df["Value_numeric"] = pd.to_numeric(df["Value"], errors="coerce")

        # 转换年份为整数
        if "year" in df.columns:
            df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")

        return df

    def __repr__(self) -> str:
        return f"NASSClient(api_key='***{self.api_key[-6:]}')"
