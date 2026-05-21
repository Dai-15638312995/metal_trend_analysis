"""
Twelve Data 数据获取模块
提供高质量的金融数据，包括 XAU/USD 现货黄金
官网: https://twelvedata.com/
免费API: https://twelvedata.com/pricing
"""
from __future__ import annotations

import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import pandas as pd
import requests
from loguru import logger

from ..utils.exceptions import DataFetchError, NetworkError, ValidationError
from ..utils.common import with_retry, validate_config


class TwelveDataClient:
    """Twelve Data API 客户端

    支持的数据:
    - XAU/USD (现货黄金)
    - XAG/USD (现货白银)
    - 股票、外汇、加密货币等

    免费版限制: 每月 800 次请求
    """

    BASE_URL = "https://api.twelvedata.com"  # 注意: 端点不在 /v1/ 下

    # Twelve Data 的贵金属符号
    SYMBOL_MAP = {
        "xauusd": "XAU/USD",   # 现货黄金现货
        "xagusd": "XAG/USD",   # 现货白银现货
        "gold": "XAU/USD",
        "silver": "XAG/USD",
    }

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)

        api_key = config.get("api_key", "")
        if not api_key:
            raise ValidationError("Twelve Data API key is required")

        self.api_key = api_key
        self.timeout = config.get("timeout", 20)
        self.max_requests_per_minute = config.get("max_requests_per_minute", 4)  # 保守限制

        self._request_count = 0
        self._last_request_time = time.time()
        self._cache = {}  # 简单缓存
        self._cache_duration = 60  # 缓存60秒

        self.logger.info("Twelve Data client initialized")

    def _rate_limit(self):
        """简单的速率限制"""
        self._request_count += 1
        if self._request_count >= self.max_requests_per_minute:
            elapsed = time.time() - self._last_request_time
            if elapsed < 60:
                sleep_time = 60 - elapsed
                self.logger.debug(f"Rate limit reached, sleeping for {sleep_time:.1f}s")
                time.sleep(sleep_time)
            self._request_count = 0
            self._last_request_time = time.time()

    def _request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """发送 API 请求"""
        params = params or {}
        params["apikey"] = self.api_key

        url = f"{self.BASE_URL}/{endpoint}"

        try:
            self._rate_limit()
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            if data.get("status") == "error":
                raise DataFetchError(f"Twelve Data API error: {data.get('message', 'Unknown error')}")

            return data

        except requests.exceptions.Timeout:
            raise NetworkError(f"Request timeout for {endpoint}")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Request failed for {endpoint}: {e}")
        except Exception as e:
            raise DataFetchError(f"Unexpected error for {endpoint}: {e}")

    @with_retry(max_attempts=3, exceptions=(NetworkError, DataFetchError))
    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时报价

        Args:
            symbol: 交易品种代码 (如 "xauusd")

        Returns:
            包含实时价格数据的字典
        """
        if not symbol:
            raise ValidationError("Symbol cannot be empty")

        td_symbol = self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

        try:
            # 使用 /price 端点获取实时价格
            data = self._request("price", {"symbol": td_symbol})

            price = float(data.get("price", 0))

            # 获取 K 线数据获取更多信息
            kline = self.get_kline(symbol, interval="1day", output_size=2)
            if not kline.empty:
                latest = kline.iloc[-1]
                prev = kline.iloc[-2] if len(kline) > 1 else latest
                change = float(latest['close']) - float(prev['close'])
                change_pct = (change / float(prev['close']) * 100) if float(prev['close']) else 0

                quote_data = {
                    "symbol": symbol,
                    "price": float(latest['close']),
                    "change": change,
                    "change_percent": change_pct,
                    "high": float(latest['high']),
                    "low": float(latest['low']),
                    "open": float(latest['open']),
                    "volume": float(latest.get('volume', 0) or 0),
                    "timestamp": str(kline.index[-1]),
                }
            else:
                quote_data = {
                    "symbol": symbol,
                    "price": price,
                    "change": 0,
                    "change_percent": 0,
                    "high": price,
                    "low": price,
                    "open": price,
                    "volume": 0,
                    "timestamp": None,
                }

            self.logger.info(f"Quote retrieved for {symbol}: ${quote_data['price']:.2f}")
            return quote_data

        except Exception as e:
            self.logger.error(f"Failed to get quote for {symbol}: {e}")
            raise

    def get_kline(
        self,
        symbol: str,
        interval: str = "1day",
        output_size: int = 200
    ) -> pd.DataFrame:
        """获取 K 线数据

        Args:
            symbol: 交易品种代码
            interval: 时间周期
                - "1min", "5min", "15min", "30min", "45min"
                - "1hour", "2hour", "4hour", "6hour", "8hour", "12hour"
                - "1day", "1week", "1month"
            output_size: 数据条数 (最大 5000)

        Returns:
            K 线数据 DataFrame
        """
        if not symbol:
            raise ValidationError("Symbol cannot be empty")

        td_symbol = self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())

        # 映射时间周期 (使用 Twelve Data 支持的格式)
        interval_map = {
            "5m": "5min",
            "15m": "15min",
            "30m": "30min",
            "45m": "45min",
            "1h": "1h",      # 1hour → 1h
            "2h": "2h",
            "4h": "4h",      # 4hour → 4h
            "6h": "6h",
            "8h": "8h",
            "12h": "12h",
            "1d": "1day",
            "1w": "1week",
            "1month": "1month",
        }
        td_interval = interval_map.get(interval, interval)

        try:
            params = {
                "symbol": td_symbol,
                "interval": td_interval,
                "outputsize": min(output_size, 5000),
                "format": "JSON",
                "date_format": "RFC3339",
            }

            data = self._request("time_series", params)

            if "values" not in data:
                raise DataFetchError(f"No data returned for {symbol}")

            # 转换为 DataFrame
            df = pd.DataFrame(data["values"])

            # 转换日期
            df["datetime"] = pd.to_datetime(df["datetime"])
            df.set_index("datetime", inplace=True)
            df = df.sort_index()

            # 转换数据类型
            for col in ["open", "high", "low", "close", "volume"]:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce")

            # 重命名列
            df.columns = [c.lower() for c in df.columns]

            self.logger.info(f"Retrieved {len(df)} records for {symbol} ({td_interval})")
            return df

        except Exception as e:
            self.logger.error(f"Failed to get kline for {symbol}: {e}")
            raise

    def get_multi_timeframe_data(
        self,
        symbol: str,
        timeframes: List[str] = None
    ) -> Dict[str, pd.DataFrame]:
        """获取多时间周期数据

        Args:
            symbol: 交易品种代码
            timeframes: 时间周期列表，如 ["5min", "1hour", "1day"]

        Returns:
            各时间周期的 DataFrame 字典
        """
        if timeframes is None:
            timeframes = ["1day"]

        result = {}

        for tf in timeframes:
            try:
                df = self.get_kline(symbol, interval=tf)
                result[tf] = df
            except Exception as e:
                self.logger.warning(f"Failed to get {tf} data for {symbol}: {e}")
                continue

        return result

    def get_forex_quote(self, symbol: str) -> Dict[str, Any]:
        """获取外汇/贵金属实时报价（专用接口）

        Args:
            symbol: 如 "XAU/USD"

        Returns:
            实时报价数据
        """
        if not symbol:
            raise ValidationError("Symbol cannot be empty")

        # 确保符号格式正确
        if "/" not in symbol:
            td_symbol = self.SYMBOL_MAP.get(symbol.lower(), symbol.upper())
        else:
            td_symbol = symbol.upper()

        try:
            params = {"symbol": td_symbol}
            data = self._request("fx_quote", params)

            quote = data.get("ask", {})
            bid = data.get("bid", {})

            mid_price = (float(quote.get("price", 0)) + float(bid.get("price", 0))) / 2

            quote_data = {
                "symbol": symbol.lower().replace("/", ""),
                "price": mid_price,
                "ask": float(quote.get("price", 0)),
                "bid": float(bid.get("price", 0)),
                "high": float(data.get("high", 0)),
                "low": float(data.get("low", 0)),
                "change": 0,
                "change_percent": 0,
                "timestamp": data.get("timestamp"),
            }

            self.logger.info(f"Forex quote for {symbol}: ${quote_data['price']:.2f}")
            return quote_data

        except Exception as e:
            self.logger.error(f"Failed to get forex quote for {symbol}: {e}")
            # 降级到普通 quote
            return self.get_quote(symbol)
