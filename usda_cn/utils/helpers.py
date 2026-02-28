# -*- coding: utf-8 -*-
"""
USDA-CN 工具函数模块
===================

提供日志配置、参数验证等辅助功能。
"""

import os
import re
import logging
from typing import Optional
from datetime import datetime


def setup_logger(
    name: str = "usda_cn",
    level: Optional[str] = None,
) -> logging.Logger:
    """
    配置并返回日志记录器

    参数:
        name: 日志记录器名称
        level: 日志级别 (DEBUG/INFO/WARNING/ERROR)

    返回:
        配置好的日志记录器
    """
    log_level = level or os.getenv("USDA_LOG_LEVEL", "INFO")

    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    return logger


def validate_api_key(api_key: str) -> bool:
    """
    验证API密钥格式

    参数:
        api_key: API密钥字符串

    返回:
        是否有效

    异常:
        ValueError: 当密钥格式无效时
    """
    if not api_key:
        raise ValueError("API密钥不能为空")

    # 检查长度
    if len(api_key) < 10:
        raise ValueError("API密钥长度无效")

    # 检查格式 (UUID格式或自定义格式)
    uuid_pattern = r"^[A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12}$"
    if not re.match(uuid_pattern, api_key, re.IGNORECASE):
        # 不是UUID格式，检查是否是有效的字母数字组合
        if not re.match(r"^[A-Za-z0-9\-_]+$", api_key):
            raise ValueError("API密钥包含无效字符")

    return True


def format_number(value: str) -> float:
    """
    将字符串格式的数字转换为浮点数

    参数:
        value: 字符串格式的数字 (如 "1,234,567")

    返回:
        浮点数值
    """
    if not value:
        return 0.0

    # 移除逗号和空格
    cleaned = str(value).replace(",", "").strip()

    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def parse_date(date_str: str) -> Optional[datetime]:
    """
    解析日期字符串

    参数:
        date_str: 日期字符串

    返回:
        datetime对象或None
    """
    formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%m/%d/%Y",
        "%Y-%m-%d %H:%M:%S",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    return None


def clean_dataframe(df):
    """
    清理DataFrame，处理缺失值和格式

    参数:
        df: Pandas DataFrame

    返回:
        清理后的DataFrame
    """
    import pandas as pd

    if df.empty:
        return df

    # 替换空字符串为None
    df = df.replace("", None)

    # 移除全空的行
    df = df.dropna(how="all")

    return df


def retry_with_backoff(func, max_retries: int = 3, base_delay: float = 1.0):
    """
    带指数退避的重试装饰器

    参数:
        func: 要执行的函数
        max_retries: 最大重试次数
        base_delay: 基础延迟时间(秒)

    返回:
        函数结果
    """
    import time

    def wrapper(*args, **kwargs):
        last_error = None

        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                if attempt < max_retries - 1:
                    delay = base_delay * (2**attempt)
                    time.sleep(delay)

        raise last_error

    return wrapper


def convert_to_chinese(text: str, mapping: dict) -> str:
    """
    将英文文本转换为中文

    参数:
        text: 英文文本
        mapping: 映射字典

    返回:
        中文文本
    """
    return mapping.get(text, text)


def build_query_url(base_url: str, params: dict) -> str:
    """
    构建查询URL

    参数:
        base_url: 基础URL
        params: 查询参数

    返回:
        完整URL
    """
    from urllib.parse import urlencode

    # 过滤空值
    filtered = {k: v for k, v in params.items() if v is not None}

    return f"{base_url}?{urlencode(filtered)}"
