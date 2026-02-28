# -*- coding: utf-8 -*-
"""
USDA-CN - 美国农业部数据接口中文版
"""

from setuptools import setup, find_packages

setup(
    name="usda-cn",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "pandas>=1.5.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "viz": [
            "matplotlib>=3.7.0",
            "seaborn>=0.12.0",
        ],
    },
    python_requires=">=3.8",
    include_package_data=True,
    zip_safe=False,
)
