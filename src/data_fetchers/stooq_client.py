"""
Yahoo Finance data client (free, no API key required)
Replaces Stooq which now requires an API key.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd
import yfinance as yf
from loguru import logger

from ..utils.exceptions import DataFetchError, NetworkError, ValidationError
from ..utils.common import with_retry, validate_config


# Yahoo Finance ticker mapping
# 使用外汇现货代码获取现货黄金/白银价格
TICKER_MAP = {
    "xauusd": "XAUUSD=X",   # 现货黄金现货 (Gold Spot)
    "xagusd": "XAGUSD=X",   # 现货白银现货 (Silver Spot)
}


class StooqClient:
    """Yahoo Finance 数据客户端（免费、无需 API Key）

    保持类名为 StooqClient 以兼容现有调用代码。
    实际使用 Yahoo Finance (yfinance) 作为数据源。
    """

    def __init__(self, config: Dict[str, Any]):
        self.logger = logger.bind(name=self.__class__.__name__)

        validate_config(config, [], "StooqClient config")

        self.base_url = config.get("base_url", "https://stooq.com/q/d/l/")
        self.timeout = config.get("timeout", 20)
        self.retry = config.get("retry", 3)
        self.retry_delay = config.get("retry_delay", 2)
        self.default_kline_count = config.get("default_kline_count", 200)

        self.logger.info("Yahoo Finance client initialized (replacing Stooq)")

    def _get_yf_ticker(self, stooq_symbol: str) -> str:
        """Convert stooq symbol to Yahoo Finance ticker."""
        return TICKER_MAP.get(stooq_symbol.lower(), stooq_symbol.upper())

    def _fetch_data(self, yf_ticker: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
        """Fetch historical data from Yahoo Finance."""
        try:
            ticker = yf.Ticker(yf_ticker)
            df = ticker.history(period=period, interval=interval, auto_adjust=True)

            if df.empty:
                raise DataFetchError(f"No data from Yahoo Finance for ticker: {yf_ticker}")

            # Normalize column names to match expected format
            df = df.rename(columns={
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume",
            })

            # Keep only needed columns
            available_cols = [c for c in ["open", "high", "low", "close", "volume"] if c in df.columns]
            df = df[available_cols].copy()

            # Ensure index is named 'timestamp'
            df.index.name = "timestamp"

            self.logger.debug(f"Fetched {len(df)} records for {yf_ticker}")
            return df

        except Exception as e:
            if isinstance(e, DataFetchError):
                raise
            raise DataFetchError(f"Yahoo Finance fetch failed for {yf_ticker}: {e}")

    def _normalize_timeframe(self, timeframe: str) -> str:
        if not timeframe or not isinstance(timeframe, str):
            self.logger.warning(f"Invalid timeframe: {timeframe}, defaulting to '1d'")
            return "1d"

        normalized = timeframe.lower().strip()
        if normalized in {"1d", "d", "day"}:
            return "1d"
        if normalized in {"1w", "1wk", "week"}:
            return "1wk"
        if normalized in {"1m", "1mo", "month"}:
            return "1mo"

        self.logger.warning(f"Unknown timeframe: {timeframe}, defaulting to '1d'")
        return "1d"

    def _get_period_for_count(self, count: int, interval: str = "1d") -> str:
        """Convert record count to yfinance period string."""
        if interval == "1wk":
            # Weekly: each record = 1 week
            weeks = count
            if weeks <= 4:
                return "1mo"
            elif weeks <= 26:
                return "6mo"
            elif weeks <= 52:
                return "1y"
            else:
                return "2y"
        elif interval == "1mo":
            # Monthly: each record = 1 month
            months = count
            if months <= 12:
                return "1y"
            elif months <= 24:
                return "2y"
            else:
                return "5y"
        else:
            # Daily: each record = 1 trading day (~252/year)
            days = count
            if days <= 7:
                return "5d"
            elif days <= 30:
                return "1mo"
            elif days <= 90:
                return "3mo"
            elif days <= 180:
                return "6mo"
            elif days <= 365:
                return "1y"
            else:
                return "2y"

    @with_retry(max_attempts=3, exceptions=(NetworkError, DataFetchError))
    def _request_csv(self, symbol: str) -> pd.DataFrame:
        """Fetch daily data (kept for API compatibility)."""
        if not symbol or not isinstance(symbol, str):
            raise ValidationError(f"Invalid symbol: {symbol}")

        yf_ticker = self._get_yf_ticker(symbol)
        period = self._get_period_for_count(self.default_kline_count, "1d")

        try:
            df = self._fetch_data(yf_ticker, period=period, interval="1d")
        except Exception as e:
            raise NetworkError(f"Failed to fetch data for {symbol}: {e}")

        if df.empty:
            raise DataFetchError(f"No data available for symbol: {symbol}")

        self.logger.debug(f"Successfully fetched {len(df)} records for {symbol}")
        return df

    def _resample(self, df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
        if timeframe == "1wk":
            rule = "W-FRI"
        elif timeframe == "1mo":
            rule = "ME"
        else:
            return df

        try:
            resampled = pd.DataFrame()
            resampled["open"] = df["open"].resample(rule).first()
            resampled["high"] = df["high"].resample(rule).max()
            resampled["low"] = df["low"].resample(rule).min()
            resampled["close"] = df["close"].resample(rule).last()
            resampled["volume"] = df["volume"].resample(rule).sum() if "volume" in df.columns else 0
            resampled.dropna(inplace=True)

            self.logger.debug(f"Resampled data to {timeframe}: {len(resampled)} records")
            return resampled

        except Exception as e:
            self.logger.error(f"Error resampling data to {timeframe}: {e}")
            return df

    def get_quote(self, symbol: str, region: str | None = None) -> Dict[str, Any]:
        if not symbol:
            raise ValidationError("Symbol cannot be empty")

        try:
            yf_ticker = self._get_yf_ticker(symbol)
            df = self._fetch_data(yf_ticker, period="5d", interval="1d")

            if df.empty:
                raise DataFetchError(f"No data available for symbol: {symbol}")

            latest = df.iloc[-1]
            prev = df.iloc[-2] if len(df) > 1 else latest

            change = latest["close"] - prev["close"]
            change_percent = (change / prev["close"] * 100) if prev["close"] else 0

            quote_data = {
                "symbol": symbol,
                "price": float(latest["close"]),
                "change": float(change),
                "change_percent": float(change_percent),
                "high": float(latest["high"]),
                "low": float(latest["low"]),
                "open": float(latest["open"]),
                "volume": float(latest.get("volume", 0)),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"Quote data retrieved for {symbol}: ${quote_data['price']:.2f}")
            return quote_data

        except (DataFetchError, ValidationError):
            raise
        except Exception as e:
            raise DataFetchError(f"Unexpected error getting quote for {symbol}: {e}")

    def get_kline(
        self,
        symbol: str,
        timeframe: str = "1d",
        count: Optional[int] = None,
        region: str | None = None,
    ) -> pd.DataFrame:
        if not symbol:
            raise ValidationError("Symbol cannot be empty")

        if count is None:
            count = self.default_kline_count
        elif count <= 0:
            raise ValidationError(f"Count must be positive, got: {count}")

        try:
            yf_ticker = self._get_yf_ticker(symbol)
            normalized_tf = self._normalize_timeframe(timeframe)

            # Map timeframe to yfinance interval
            interval_map = {"1d": "1d", "1wk": "1wk", "1mo": "1mo"}
            yf_interval = interval_map.get(normalized_tf, "1d")

            period = self._get_period_for_count(count, normalized_tf)
            df = self._fetch_data(yf_ticker, period=period, interval=yf_interval)

            if len(df) > count:
                df = df.tail(count)

            self.logger.info(f"K-line data retrieved for {symbol}: {len(df)} records ({normalized_tf})")
            return df

        except (DataFetchError, ValidationError):
            raise
        except Exception as e:
            raise DataFetchError(f"Unexpected error getting K-line data for {symbol}: {e}")

    def get_multi_timeframe_data(
        self,
        symbol: str,
        timeframes: list = None,
        region: str | None = None,
    ) -> Dict[str, pd.DataFrame]:
        """
        获取多时间周期的K线数据

        Args:
            symbol: 交易品种代码
            timeframes: 时间周期列表，如 ['5m', '15m', '30m', '1h', '4h', '1d']
            region: 地区代码

        Returns:
            各时间周期的DataFrame字典
        """
        if timeframes is None:
            timeframes = ['1d']

        result = {}
        yf_ticker = self._get_yf_ticker(symbol)

        # Yahoo Finance 支持的interval和对应period
        timeframe_config = {
            '1m': {'interval': '1m', 'period': '7d', 'count': 1000},
            '5m': {'interval': '5m', 'period': '1mo', 'count': 1000},
            '15m': {'interval': '15m', 'period': '1mo', 'count': 1000},
            '30m': {'interval': '30m', 'period': '1mo', 'count': 1000},
            '1h': {'interval': '1h', 'period': '3mo', 'count': 500},
            '4h': {'interval': '1h', 'period': '6mo', 'count': 500},  # yfinance没有4h，用1h聚合
            '1d': {'interval': '1d', 'period': '1y', 'count': 200},
            '1w': {'interval': '1wk', 'period': '2y', 'count': 100},
        }

        for tf in timeframes:
            try:
                config = timeframe_config.get(tf, timeframe_config['1d'])

                # 对于4h，需要从1h数据聚合
                if tf == '4h':
                    df_1h = self._fetch_data(yf_ticker, period=config['period'], interval='1h')
                    if not df_1h.empty:
                        df = self._resample_to_4h(df_1h)
                    else:
                        df = df_1h
                else:
                    df = self._fetch_data(yf_ticker, period=config['period'], interval=config['interval'])

                if not df.empty:
                    # 限制数据量
                    if len(df) > config['count']:
                        df = df.tail(config['count'])
                    result[tf] = df
                    self.logger.info(f"Fetched {tf} data: {len(df)} records")
                else:
                    self.logger.warning(f"No data for {tf}")

            except Exception as e:
                self.logger.error(f"Failed to fetch {tf} data: {e}")
                continue

        return result

    def _resample_to_4h(self, df_1h: pd.DataFrame) -> pd.DataFrame:
        """将1小时数据聚合为4小时数据"""
        try:
            df_4h = pd.DataFrame()
            df_4h['open'] = df_1h['open'].resample('4H').first()
            df_4h['high'] = df_1h['high'].resample('4H').max()
            df_4h['low'] = df_1h['low'].resample('4H').min()
            df_4h['close'] = df_1h['close'].resample('4H').last()
            df_4h['volume'] = df_1h['volume'].resample('4H').sum() if 'volume' in df_1h.columns else 0
            df_4h.dropna(inplace=True)
            return df_4h
        except Exception as e:
            self.logger.error(f"Error resampling to 4h: {e}")
            return df_1h

    def save_raw_data(self, df: pd.DataFrame, symbol: str, timeframe: str) -> Optional[Path]:
        try:
            if df.empty:
                self.logger.warning(f"No data to save for {symbol}")
                return None

            output_dir = Path("data/raw")
            output_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{symbol}_{timeframe}_{timestamp}.csv"
            filepath = output_dir / filename

            df.to_csv(filepath)
            self.logger.info(f"Raw data saved: {filepath}")
            return filepath

        except Exception as e:
            self.logger.error(f"Error saving raw data for {symbol}: {e}")
            return None
