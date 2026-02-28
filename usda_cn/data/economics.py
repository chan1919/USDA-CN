# -*- coding: utf-8 -*-
"""
农业经济数据模块
==============

包含农业经济相关的数据获取接口：
- 价格数据: 农产品价格、价格指数
- 收入数据: 农场收入、净收入
- 支出数据: 生产成本、经营费用
- 资产数据: 农场资产、土地价值
"""

from typing import Optional, Union, Dict, List
import pandas as pd

from usda_cn.data.base import BaseDataFetcher
from usda_cn.utils.helpers import setup_logger


logger = setup_logger("usda_cn.economics")


class EconomicsData(BaseDataFetcher):
    """
    农业经济数据获取器

    提供农业经济相关的数据访问接口。

    示例:
        >>> econ = EconomicsData()
        >>> df = econ.get_farm_income(year=2024)
        >>> df = econ.get_land_value(year=2024)
    """

    SECTOR = "ECONOMICS"

    # 经济指标类型
    ECONOMICS_TYPES = {
        # 收入相关
        "CASH RECEIPTS": {"cn": "现金收入", "unit": "$"},
        "GROSS INCOME": {"cn": "总收入", "unit": "$"},
        "NET INCOME": {"cn": "净收入", "unit": "$"},
        "GOVERNMENT PAYMENTS": {"cn": "政府补贴", "unit": "$"},
        # 支出相关
        "EXPENSES": {"cn": "生产支出", "unit": "$"},
        "PRODUCTION EXPENSES": {"cn": "生产成本", "unit": "$"},
        "FEED EXPENSES": {"cn": "饲料支出", "unit": "$"},
        "FERTILIZER EXPENSES": {"cn": "肥料支出", "unit": "$"},
        "CHEMICAL EXPENSES": {"cn": "农药支出", "unit": "$"},
        "FUEL EXPENSES": {"cn": "燃料支出", "unit": "$"},
        "LABOR EXPENSES": {"cn": "人工支出", "unit": "$"},
        # 资产相关
        "ASSETS": {"cn": "资产", "unit": "$"},
        "REAL ESTATE": {"cn": "房地产", "unit": "$"},
        "MACHINERY": {"cn": "机械设备", "unit": "$"},
        "DEBT": {"cn": "负债", "unit": "$"},
        # 价格指数
        "PRICE RECEIVED": {"cn": "价格指数", "unit": "INDEX"},
        "PRICE PAID": {"cn": "支出价格指数", "unit": "INDEX"},
    }

    # 收入组
    INCOME_GROUPS = {
        "CROPS": {"cn": "作物收入", "unit": "$"},
        "LIVESTOCK": {"cn": "畜牧收入", "unit": "$"},
        "DAIRY": {"cn": "乳制品收入", "unit": "$"},
    }

    def __init__(self, client=None, api_key=None):
        super().__init__(client=client, api_key=api_key)

    def get_cash_receipts(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
        agg_level: str = "NATIONAL",
    ) -> pd.DataFrame:
        """
        获取农业现金收入数据

        参数:
            year: 年份
            state: 州代码
            agg_level: 地理聚合级别

        返回:
            现金收入数据DataFrame
        """
        self.COMMODITY = "CASH RECEIPT TOTALS"
        self.COMMODITY_CN = "农业现金收入"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="RECEIPTS",
            year=year,
            state=state,
            agg_level=agg_level,
            unit_desc="$",
        )

    def get_crop_receipts(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取作物收入数据"""
        self.COMMODITY = "CASH RECEIPT TOTALS"
        self.COMMODITY_CN = "作物收入"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="RECEIPTS",
            year=year,
            state=state,
            group_desc="CROP TOTALS",
            unit_desc="$",
        )

    def get_livestock_receipts(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取畜牧收入数据"""
        self.COMMODITY = "CASH RECEIPT TOTALS"
        self.COMMODITY_CN = "畜牧收入"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="RECEIPTS",
            year=year,
            state=state,
            group_desc="ANIMAL TOTALS",
            unit_desc="$",
        )

    def get_gross_income(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取农场总收入数据"""
        self.COMMODITY = "INCOME"
        self.COMMODITY_CN = "农场总收入"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="GROSS INCOME",
            year=year,
            state=state,
            unit_desc="$",
        )

    def get_net_income(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取农场净收入数据"""
        self.COMMODITY = "INCOME, NET CASH FARM"
        self.COMMODITY_CN = "农场净收入"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="NET INCOME",
            year=year,
            state=state,
            unit_desc="$",
        )

    def get_government_payments(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取政府补贴数据"""
        self.COMMODITY = "GOVERNMENT PAYMENTS"
        self.COMMODITY_CN = "政府补贴"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="PAYMENTS",
            year=year,
            state=state,
            unit_desc="$",
        )

    def get_production_expenses(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取生产支出数据"""
        self.COMMODITY = "EXPENSES"
        self.COMMODITY_CN = "生产支出"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="EXPENSE",
            year=year,
            state=state,
            unit_desc="$",
        )

    def get_feed_expenses(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取饲料支出数据"""
        self.COMMODITY = "FEED"
        self.COMMODITY_CN = "饲料支出"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="EXPENSE",
            year=year,
            state=state,
            unit_desc="$",
        )

    def get_fertilizer_expenses(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取肥料支出数据"""
        self.COMMODITY = "FERTILIZER"
        self.COMMODITY_CN = "肥料支出"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="EXPENSE",
            year=year,
            state=state,
            unit_desc="$",
        )

    def get_chemical_expenses(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取农药支出数据"""
        self.COMMODITY = "CHEMICAL TOTALS"
        self.COMMODITY_CN = "农药支出"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="EXPENSE",
            year=year,
            state=state,
            unit_desc="$",
        )

    def get_farm_assets(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取农场资产数据"""
        self.COMMODITY = "ASSETS"
        self.COMMODITY_CN = "农场资产"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="ASSET VALUE",
            year=year,
            state=state,
            unit_desc="$",
        )

    def get_land_value(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        获取农地价值数据

        参数:
            year: 年份
            state: 州代码

        返回:
            农地价值DataFrame (单位: 美元/英亩)
        """
        self.COMMODITY = "AG LAND"
        self.COMMODITY_CN = "农地价值"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="ASSET VALUE",
            year=year,
            state=state,
            unit_desc="$ / ACRE",
        )

    def get_farm_debt(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取农场负债数据"""
        self.COMMODITY = "DEBT"
        self.COMMODITY_CN = "农场负债"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="DEBT",
            year=year,
            state=state,
            unit_desc="$",
        )

    def get_price_index_received(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取农产品价格指数"""
        self.COMMODITY = "PRICE RECEIVED"
        self.COMMODITY_CN = "农产品价格指数"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="PRICE REACTION",
            year=year,
            state=state,
        )

    def get_farm_count(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取农场数量数据"""
        self.COMMODITY = "FARMS & LAND & ASSETS"
        self.COMMODITY_CN = "农场数量"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="OPERATIONS",
            year=year,
            state=state,
            unit_desc="OPERATIONS",
        )

    def get_farm_size(
        self,
        year: Optional[Union[int, Dict]] = None,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取农场平均规模数据"""
        self.COMMODITY = "AG LAND"
        self.COMMODITY_CN = "农场规模"

        if year is None:
            year = {"ge": 2020, "le": 2024}

        return self._query(
            statisticcat_desc="AREA OPERATED, AVG",
            year=year,
            state=state,
            unit_desc="ACRES",
        )

    def get_summary(
        self,
        year: int = 2024,
        state: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取农业经济数据汇总"""
        results = []

        data_methods = [
            ("农业现金收入", self.get_cash_receipts, {}),
            ("作物收入", self.get_crop_receipts, {}),
            ("畜牧收入", self.get_livestock_receipts, {}),
            ("农场净收入", self.get_net_income, {}),
            ("政府补贴", self.get_government_payments, {}),
            ("生产支出", self.get_production_expenses, {}),
            ("农场数量", self.get_farm_count, {}),
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

    def compare_states(
        self,
        states: List[str],
        year: int = 2024,
        metric: str = "cash_receipts",
    ) -> pd.DataFrame:
        """
        比较多个州的经济数据

        参数:
            states: 州代码列表
            year: 年份
            metric: 指标类型
        """
        metric_methods = {
            "cash_receipts": self.get_cash_receipts,
            "net_income": self.get_net_income,
            "farm_count": self.get_farm_count,
            "land_value": self.get_land_value,
        }

        if metric not in metric_methods:
            raise ValueError(f"不支持的指标: {metric}")

        results = []
        for state in states:
            try:
                df = metric_methods[metric](year=year, state=state)
                if not df.empty:
                    row = df.iloc[0]
                    results.append(
                        {
                            "州": state,
                            "数值": row.get("Value", ""),
                            "单位": row.get("unit_desc", ""),
                        }
                    )
            except Exception as e:
                logger.debug(f"获取{state}数据失败: {e}")

        return pd.DataFrame(results)

    def list_indicators(self) -> pd.DataFrame:
        """列出所有支持的经济指标"""
        return pd.DataFrame(
            [
                {"英文": en, "中文": info["cn"], "单位": info["unit"]}
                for en, info in self.ECONOMICS_TYPES.items()
            ]
        )
