# -*- coding: utf-8 -*-
"""
NASS Quick Stats API 接口模块
============================

提供对美国国家农业统计局Quick Stats数据库的完整API访问。
"""

import time
from typing import Optional, Dict, Any, List, Union
from functools import wraps
import requests

from usda_cn.utils.helpers import setup_logger
from usda_cn.utils.constants import API_OPERATORS, MAX_RECORDS


logger = setup_logger("usda_cn.quickstats")


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """
    失败重试装饰器

    参数:
        max_retries: 最大重试次数
        delay: 重试间隔(秒)
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        logger.warning(f"请求失败，第{attempt + 1}次重试: {e}")
                        time.sleep(delay * (attempt + 1))
                    else:
                        logger.error(f"请求失败，已达最大重试次数: {e}")
            raise last_exception

        return wrapper

    return decorator


class QuickStatsAPI:
    """
    NASS Quick Stats API 客户端

    Quick Stats是美国农业部国家农业统计局的官方统计数据库，
    包含数百万条农业生产、价格、库存等数据记录。

    API文档: https://quickstats.nass.usda.gov/api

    参数:
        api_key: USDA API密钥
        base_url: API基础URL
        timeout: 请求超时时间(秒)
        retries: 失败重试次数

    示例:
        >>> api = QuickStatsAPI(api_key="YOUR_KEY")
        >>> data = api.query(commodity_desc="SOYBEANS", year=2024)
    """

    ENDPOINTS = {
        "query": "/api_GET",
        "param_values": "/get_param_values",
        "count": "/get_counts",
    }

    # 支持的输出格式
    FORMATS = ["JSON", "CSV", "XML"]

    # 支持的查询参数
    QUERY_PARAMS = [
        # What维度 - 商品相关
        "source_desc",  # 数据来源 (SURVEY/CENSUS)
        "sector_desc",  # 部门 (CROPS/ANIMALS & PRODUCTS/ECONOMICS等)
        "group_desc",  # 商品组 (FIELD CROPS/FRUIT & TREE NUTS等)
        "commodity_desc",  # 商品名称 (SOYBEANS/CORN/WHEAT等)
        "class_desc",  # 类别
        "prodn_practice_desc",  # 生产实践
        "util_practice_desc",  # 利用实践
        "statisticcat_desc",  # 统计类别 (PRODUCTION/AREA PLANTED/YIELD等)
        "unit_desc",  # 单位
        "short_desc",  # 简短描述
        "domain_desc",  # 域
        "domaincat_desc",  # 域类别
        # Where维度 - 地理相关
        "agg_level_desc",  # 聚合级别 (NATIONAL/STATE/COUNTY等)
        "state_ansi",  # 州ANSI代码
        "state_fips_code",  # 州FIPS代码
        "state_alpha",  # 州字母代码
        "state_name",  # 州名称
        "asd_code",  # 农业统计区代码
        "asd_desc",  # 农业统计区名称
        "county_ansi",  # 县ANSI代码
        "county_code",  # 县代码
        "county_name",  # 县名称
        "region_desc",  # 区域
        "zip_5",  # 邮政编码
        "watershed_code",  # 流域代码
        "watershed_desc",  # 流域名称
        "congr_district_code",  # 国会选区代码
        "country_code",  # 国家代码
        "country_name",  # 国家名称
        "location_desc",  # 位置描述
        # When维度 - 时间相关
        "year",  # 年份
        "freq_desc",  # 频率 (ANNUAL/MONTHLY/WEEKLY等)
        "begin_code",  # 开始代码
        "end_code",  # 结束代码
        "reference_period_desc",  # 参考期间
        "week_ending",  # 周结束日期
        "load_time",  # 加载时间
    ]

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://quickstats.nass.usda.gov/api",
        timeout: int = 30,
        retries: int = 3,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = retries
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "USDA-CN/0.1.0 (Python)",
                "Accept": "application/json",
            }
        )

    @retry_on_failure(max_retries=3)
    def _request(
        self,
        endpoint: str,
        params: Dict[str, Any],
        format: str = "JSON",
    ) -> Union[List[Dict], str]:
        """
        发送API请求

        参数:
            endpoint: 端点名称
            params: 请求参数
            format: 输出格式 (JSON/CSV/XML)

        返回:
            API响应数据
        """
        url = f"{self.base_url}{self.ENDPOINTS.get(endpoint, endpoint)}"

        # 添加API密钥和格式
        params = {k: v for k, v in params.items() if v is not None}
        params["key"] = self.api_key
        params["format"] = format.upper()

        logger.debug(f"请求: {url}, 参数: {list(params.keys())}")

        response = self.session.get(url, params=params, timeout=self.timeout)

        if response.status_code == 401:
            raise PermissionError("API密钥无效或已过期，请检查您的USDA_API_KEY")
        elif response.status_code == 400:
            error_data = (
                response.json()
                if "json" in response.headers.get("content-type", "")
                else {}
            )
            error_msg = (
                error_data.get("error", ["未知错误"])[0] if error_data else response.text
            )
            raise ValueError(f"请求参数错误: {error_msg}")
        elif response.status_code != 200:
            raise requests.exceptions.HTTPError(f"HTTP错误: {response.status_code}")

        # 解析响应
        if format.upper() == "JSON":
            data = response.json()
            return data.get("data", data)
        else:
            return response.text

    def query(
        self,
        format: str = "JSON",
        **params,
    ) -> List[Dict[str, Any]]:
        """
        执行数据查询

        这是最通用的查询方法，支持所有Quick Stats参数。

        参数:
            format: 输出格式 (JSON/CSV/XML)
            **params: 查询参数，支持以下操作符后缀:
                - __LE: <= (小于等于)
                - __LT: < (小于)
                - __GT: > (大于)
                - __GE: >= (大于等于)
                - __LIKE: 模糊匹配
                - __NOT_LIKE: 排除匹配
                - __NE: 不等于

        返回:
            查询结果列表，每个元素是一条记录字典

        示例:
            >>> # 查询2024年大豆产量
            >>> data = api.query(commodity_desc="SOYBEANS", year=2024)
            >>>
            >>> # 查询2020年以来的玉米数据
            >>> data = api.query(commodity_desc="CORN", year__GE=2020)
            >>>
            >>> # 按州查询
            >>> data = api.query(commodity_desc="SOYBEANS", state_alpha="IA", agg_level_desc="STATE")
        """
        # 验证参数
        self._validate_params(params)

        # 检查记录数量
        count = self.get_count(**params)
        if count > MAX_RECORDS:
            logger.warning(f"查询将返回{count}条记录，超过最大限制{MAX_RECORDS}。" "建议添加更多筛选条件或分批查询。")

        return self._request("query", params, format)

    def get_param_values(self, param: str) -> List[str]:
        """
        获取参数的所有可能值

        参数:
            param: 参数名称

        返回:
            该参数的所有可能值列表

        示例:
            >>> commodities = api.get_param_values("commodity_desc")
            >>> print(commodities[:5])  # ['AG LAND', 'AG SERVICES', ...]
            >>>
            >>> states = api.get_param_values("state_alpha")
            >>> print(states[:5])  # ['AL', 'AR', 'AZ', ...]
        """
        if param not in self.QUERY_PARAMS:
            raise ValueError(f"未知参数: {param}。可用参数: {self.QUERY_PARAMS}")

        result = self._request("param_values", {"param": param})
        return result.get(param, result) if isinstance(result, dict) else result

    def get_count(self, **params) -> int:
        """
        获取查询结果的记录数量

        在执行实际查询前，建议先调用此方法预估数据量。

        参数:
            **params: 查询参数

        返回:
            记录数量

        示例:
            >>> count = api.get_count(commodity_desc="SOYBEANS", year=2024)
            >>> print(f"将返回{count}条记录")
        """
        result = self._request("count", params)
        if isinstance(result, dict):
            return int(result.get("count", 0))
        return 0

    def _validate_params(self, params: Dict[str, Any]) -> None:
        """验证查询参数"""
        for key in params.keys():
            # 移除操作符后缀
            base_key = key
            for op in API_OPERATORS:
                if key.endswith(f"__{op}"):
                    base_key = key[: -len(f"__{op}")]
                    break

            if base_key not in self.QUERY_PARAMS:
                logger.warning(f"参数 '{key}' 可能不是有效的Quick Stats参数")

    def get_commodities(self) -> List[str]:
        """获取所有商品列表"""
        return self.get_param_values("commodity_desc")

    def get_states(self) -> List[str]:
        """获取所有州代码列表"""
        return self.get_param_values("state_alpha")

    def get_statistic_categories(self) -> List[str]:
        """获取所有统计类别列表"""
        return self.get_param_values("statisticcat_desc")

    def get_units(self) -> List[str]:
        """获取所有单位列表"""
        return self.get_param_values("unit_desc")

    def get_years(self, commodity: str = None) -> List[int]:
        """
        获取数据可用的年份

        参数:
            commodity: 可选，指定商品筛选

        返回:
            年份列表
        """
        params = {"param": "year"}
        if commodity:
            params["commodity_desc"] = commodity

        years = self.get_param_values("year")
        return sorted([int(y) for y in years if y.isdigit()], reverse=True)

    def get_aggregation_levels(self) -> List[str]:
        """获取所有地理聚合级别"""
        return self.get_param_values("agg_level_desc")

    def close(self):
        """关闭会话"""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
