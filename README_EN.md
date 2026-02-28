# USDA-CN 🌾

<div align="center">

**USDA Data API for Chinese Users**

A Python library for fetching US agricultural data with Chinese interface

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

[简体中文](README.md) | English

</div>

---

## Overview

USDA-CN is a Python library designed for Chinese users to easily access US Department of Agriculture (USDA) agricultural statistics. With a simple Chinese interface, you can retrieve official data on production, prices, and stocks for major agricultural commodities like soybeans, corn, and wheat.

## Installation

```bash
pip install usda-cn
```

## Quick Start

```python
from usda_cn import NASSClient, SoybeanData

# Initialize client
client = NASSClient(api_key="YOUR_API_KEY")

# Get soybean production data
df = client.get_soybean_production(year=2024)
print(df)

# Or use the dedicated SoybeanData module
soy = SoybeanData()
production = soy.get_production(year=2024)
print(f"2024 Soybean Production: {production['Value'].iloc[0]} bushels")
```

## Features

- 🇨🇳 Chinese interface with commodity names in Chinese
- 🚀 Simple API - one line of code to get data
- 📊 Pandas integration - returns DataFrame
- 🔒 Secure API key management via environment variables
- 📦 Multiple data sources - NASS Quick Stats, FAS PSD

## Data Sources

- **NASS Quick Stats**: US agricultural production, prices, stocks
- **FAS PSD**: Global supply and demand data

## License

MIT License

## Disclaimer

This tool is for research and educational purposes only. Data is sourced from USDA official API.