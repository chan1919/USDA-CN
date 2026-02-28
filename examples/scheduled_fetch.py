# -*- coding: utf-8 -*-
"""
定时数据拉取示例
===============

展示如何设置定时任务定期获取USDA数据。
"""

import os
import pandas as pd
from datetime import datetime
from usda_cn import SoybeanData, CornData, WheatData


def fetch_and_save_data():
    """
    获取并保存数据到本地
    """
    # 创建数据目录
    data_dir = "data/raw"
    os.makedirs(data_dir, exist_ok=True)

    # 当前日期
    today = datetime.now().strftime("%Y%m%d")

    # 初始化数据获取器
    soy = SoybeanData()
    corn = CornData()
    wheat = WheatData()

    # 获取当前年份
    current_year = datetime.now().year

    # 获取数据
    print(f"开始获取数据... ({datetime.now()})")

    results = {}

    # 大豆数据
    try:
        soy_production = soy.get_production(year=current_year)
        soy_area = soy.get_area_planted(year=current_year)
        soy_yield = soy.get_yield(year=current_year)
        soy_price = soy.get_price(year=current_year)

        # 合并数据
        soy_summary = pd.DataFrame(
            [
                {
                    "指标": "产量",
                    "数值": soy_production["Value"].iloc[0] if not soy_production.empty else "N/A",
                    "单位": "BU",
                },
                {
                    "指标": "种植面积",
                    "数值": soy_area["Value"].iloc[0] if not soy_area.empty else "N/A",
                    "单位": "ACRES",
                },
                {
                    "指标": "单产",
                    "数值": soy_yield["Value"].iloc[0] if not soy_yield.empty else "N/A",
                    "单位": "BU/ACRE",
                },
                {
                    "指标": "价格",
                    "数值": soy_price["Value"].iloc[0] if not soy_price.empty else "N/A",
                    "单位": "$/BU",
                },
            ]
        )
        results["大豆"] = soy_summary
        print("✓ 大豆数据获取成功")
    except Exception as e:
        print(f"✗ 大豆数据获取失败: {e}")

    # 玉米数据
    try:
        corn_production = corn.get_production(year=current_year)
        corn_area = corn.get_area_planted(year=current_year)
        corn_yield = corn.get_yield(year=current_year)

        corn_summary = pd.DataFrame(
            [
                {
                    "指标": "产量",
                    "数值": corn_production["Value"].iloc[0] if not corn_production.empty else "N/A",
                    "单位": "BU",
                },
                {
                    "指标": "种植面积",
                    "数值": corn_area["Value"].iloc[0] if not corn_area.empty else "N/A",
                    "单位": "ACRES",
                },
                {
                    "指标": "单产",
                    "数值": corn_yield["Value"].iloc[0] if not corn_yield.empty else "N/A",
                    "单位": "BU/ACRE",
                },
            ]
        )
        results["玉米"] = corn_summary
        print("✓ 玉米数据获取成功")
    except Exception as e:
        print(f"✗ 玉米数据获取失败: {e}")

    # 小麦数据
    try:
        wheat_production = wheat.get_production(year=current_year)
        wheat_area = wheat.get_area_planted(year=current_year)
        wheat_yield = wheat.get_yield(year=current_year)

        wheat_summary = pd.DataFrame(
            [
                {
                    "指标": "产量",
                    "数值": wheat_production["Value"].iloc[0]
                    if not wheat_production.empty
                    else "N/A",
                    "单位": "BU",
                },
                {
                    "指标": "种植面积",
                    "数值": wheat_area["Value"].iloc[0] if not wheat_area.empty else "N/A",
                    "单位": "ACRES",
                },
                {
                    "指标": "单产",
                    "数值": wheat_yield["Value"].iloc[0] if not wheat_yield.empty else "N/A",
                    "单位": "BU/ACRE",
                },
            ]
        )
        results["小麦"] = wheat_summary
        print("✓ 小麦数据获取成功")
    except Exception as e:
        print(f"✗ 小麦数据获取失败: {e}")

    # 保存数据
    for commodity, df in results.items():
        filename = f"{data_dir}/{commodity}_{today}.csv"
        df.to_csv(filename, index=False, encoding="utf-8-sig")
        print(f"  已保存: {filename}")

    print(f"\n数据获取完成! ({datetime.now()})")

    return results


def check_for_updates():
    """
    检查是否有新数据更新
    """
    # 这里可以添加逻辑来比较新旧数据
    # 如果有变化，发送通知等
    pass


if __name__ == "__main__":
    fetch_and_save_data()


# ============================================================
# Windows 任务计划程序配置
# ============================================================
#
# 1. 创建批处理文件 (fetch_usda_data.bat):
#    @echo off
#    cd C:\path\to\usda-cn
#    call venv\Scripts\activate
#    python examples\scheduled_fetch.py
#
# 2. 在任务计划程序中创建任务:
#    - 触发器: 每周一早上 8:00
#    - 操作: 启动程序 -> fetch_usda_data.bat
#
# ============================================================
# Linux/Mac cron 配置
# ============================================================
#
# 每周一早上8点运行
# 0 8 * * 1 cd /path/to/usda-cn && /path/to/python examples/scheduled_fetch.py >> logs/fetch.log 2>&1
#
# ============================================================
