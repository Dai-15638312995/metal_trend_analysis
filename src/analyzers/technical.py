"""
Technical Indicator Calculation Module
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from loguru import logger

from ..utils.exceptions import AnalysisError, ValidationError
from ..utils.common import validate_config, safe_execute


class TechnicalAnalyzer:
    """Technical Analyzer"""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Technical Analyzer

        Args:
            config: 技术指标配置

        Raises:
            ValidationError: 配置无效时抛出
        """
        self.logger = logger.bind(name=self.__class__.__name__)

        # 验证配置
        validate_config(config, [], "Technical analyzer config")

        # 指标参数配置，带默认值和验证
        self.ma_config = self._validate_ma_config(config.get('ma', {}))
        self.macd_config = self._validate_macd_config(config.get('macd', {}))
        self.rsi_config = self._validate_rsi_config(config.get('rsi', {}))
        self.bollinger_config = self._validate_bollinger_config(config.get('bollinger', {}))
        self.sr_config = self._validate_sr_config(config.get('support_resistance', {}))

        self.logger.info("Technical analyzer initialized with validated parameters")

    def _validate_ma_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """验证移动平均线配置"""
        periods = config.get('periods', [5, 10, 20, 60])
        if not isinstance(periods, list) or not periods:
            periods = [5, 10, 20, 60]

        # 验证周期值
        validated_periods = []
        for period in periods:
            try:
                period = int(period)
                if period > 0:
                    validated_periods.append(period)
            except (ValueError, TypeError):
                continue

        if not validated_periods:
            validated_periods = [5, 10, 20, 60]

        return {'periods': sorted(validated_periods)}

    def _validate_macd_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """验证MACD配置"""
        return {
            'fast': max(1, int(config.get('fast', 12))),
            'slow': max(1, int(config.get('slow', 26))),
            'signal': max(1, int(config.get('signal', 9)))
        }

    def _validate_rsi_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """验证RSI配置"""
        return {
            'period': max(1, int(config.get('period', 14))),
            'overbought': max(50, min(100, int(config.get('overbought', 70)))),
            'oversold': max(0, min(50, int(config.get('oversold', 30))))
        }

    def _validate_bollinger_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """验证布林带配置"""
        return {
            'period': max(1, int(config.get('period', 20))),
            'std_dev': max(0.1, float(config.get('std_dev', 2.0)))
        }

    def _validate_sr_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """验证支撑阻力配置"""
        return {
            'lookback': max(10, int(config.get('lookback', 100))),
            'swing_points': max(1, int(config.get('swing_points', 3))),
            'proximity': max(0.001, float(config.get('proximity', 0.01)))
        }

    def calculate_all_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        计算所有技术指标

        Args:
            df: K 线数据 DataFrame

        Returns:
            包含所有指标的 DataFrame

        Raises:
            ValidationError: 数据无效时抛出
            AnalysisError: 计算失败时抛出
        """
        try:
            # 验证输入数据
            self._validate_kline_data(df)

            result_df = df.copy()

            # 计算移动平均线
            ma_data = safe_execute(
                lambda: self.calculate_ma(result_df),
                default_value={},
                logger_name="calculate_ma"
            )

            for period, ma_values in ma_data.items():
                if ma_values is not None:
                    result_df[f'MA{period}'] = ma_values

            # 计算 MACD
            macd_data = safe_execute(
                lambda: self.calculate_macd(result_df),
                default_value={},
                logger_name="calculate_macd"
            )

            if macd_data:
                result_df['MACD_DIF'] = macd_data.get('dif')
                result_df['MACD_DEA'] = macd_data.get('dea')
                result_df['MACD_HIST'] = macd_data.get('hist')

            # 计算 RSI
            rsi_values = safe_execute(
                lambda: self.calculate_rsi(result_df),
                default_value=None,
                logger_name="calculate_rsi"
            )

            if rsi_values is not None:
                result_df['RSI'] = rsi_values

            # 计算布林带
            bb_data = safe_execute(
                lambda: self.calculate_bollinger(result_df),
                default_value={},
                logger_name="calculate_bollinger"
            )

            if bb_data:
                result_df['BB_UPPER'] = bb_data.get('upper')
                result_df['BB_MIDDLE'] = bb_data.get('middle')
                result_df['BB_LOWER'] = bb_data.get('lower')

            # 计算成交量移动平均
            if 'volume' in result_df.columns:
                volume_ma = safe_execute(
                    lambda: result_df['volume'].rolling(window=20).mean(),
                    default_value=None,
                    logger_name="calculate_volume_ma"
                )
                if volume_ma is not None:
                    result_df['VOLUME_MA'] = volume_ma

            self.logger.info(f"Calculated indicators for {len(result_df)} data points")
            return result_df

        except ValidationError:
            raise
        except Exception as e:
            raise AnalysisError(f"Failed to calculate technical indicators: {e}")

    def _validate_kline_data(self, df: pd.DataFrame) -> None:
        """
        验证K线数据

        Args:
            df: K线数据DataFrame

        Raises:
            ValidationError: 数据无效时抛出
        """
        if df is None or df.empty:
            raise ValidationError("K-line data cannot be empty")

        required_columns = ['open', 'high', 'low', 'close']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValidationError(f"Missing required columns: {missing_columns}")

        # 检查数据类型和有效性
        for col in required_columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                raise ValidationError(f"Column '{col}' must be numeric")

            if df[col].isna().all():
                raise ValidationError(f"Column '{col}' contains only NaN values")

        # 检查OHLC关系
        if len(df) > 0:
            invalid_ohlc = (
                (df['high'] < df['low']) |
                (df['high'] < df['open']) |
                (df['high'] < df['close']) |
                (df['low'] > df['open']) |
                (df['low'] > df['close'])
            ).any()

            if invalid_ohlc:
                self.logger.warning("Some OHLC relationships are invalid")

    def calculate_ma(self, df: pd.DataFrame) -> Dict[int, pd.Series]:
        """
        计算移动平均线

        Args:
            df: K 线数据 DataFrame

        Returns:
            移动平均线字典 {period: Series}

        Raises:
            AnalysisError: 计算失败时抛出
        """
        try:
            ma_dict = {}

            for period in self.ma_config.get('periods', [5, 10, 20, 60]):
                if len(df) >= period:
                    ma_dict[period] = df['close'].rolling(window=period, min_periods=1).mean()
                else:
                    self.logger.warning(f"Insufficient data for MA({period}), need {period} points, got {len(df)}")
                    ma_dict[period] = pd.Series(index=df.index, dtype=float)

            return ma_dict

        except Exception as e:
            raise AnalysisError(f"Failed to calculate moving averages: {e}")

    def calculate_macd(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        """
        计算 MACD 指标

        Args:
            df: K 线数据 DataFrame

        Returns:
            MACD 数据字典

        Raises:
            AnalysisError: 计算失败时抛出
        """
        try:
            fast = self.macd_config.get('fast', 12)
            slow = self.macd_config.get('slow', 26)
            signal = self.macd_config.get('signal', 9)

            # 确保fast < slow
            if fast >= slow:
                self.logger.warning(f"MACD fast period ({fast}) should be less than slow period ({slow})")
                fast, slow = min(fast, slow), max(fast, slow)

            if len(df) < slow:
                self.logger.warning(f"Insufficient data for MACD, need {slow} points, got {len(df)}")
                return {
                    'dif': pd.Series(index=df.index, dtype=float),
                    'dea': pd.Series(index=df.index, dtype=float),
                    'hist': pd.Series(index=df.index, dtype=float)
                }

            # 计算EMA
            ema_fast = df['close'].ewm(span=fast, min_periods=1).mean()
            ema_slow = df['close'].ewm(span=slow, min_periods=1).mean()

            # 计算DIF
            dif = ema_fast - ema_slow

            # 计算DEA (DIF的EMA)
            dea = dif.ewm(span=signal, min_periods=1).mean()

            # 计算HIST (柱状图)
            hist = 2 * (dif - dea)

            return {
                'dif': dif,
                'dea': dea,
                'hist': hist
            }

        except Exception as e:
            raise AnalysisError(f"Failed to calculate MACD: {e}")

    def calculate_rsi(self, df: pd.DataFrame) -> pd.Series:
        """
        计算 RSI 指标

        Args:
            df: K 线数据 DataFrame

        Returns:
            RSI 数值序列

        Raises:
            AnalysisError: 计算失败时抛出
        """
        try:
            period = self.rsi_config.get('period', 14)

            if len(df) < period:
                self.logger.warning(f"Insufficient data for RSI, need {period} points, got {len(df)}")
                return pd.Series(index=df.index, dtype=float)

            # 计算价格变化
            close_diff = df['close'].diff()

            # 分离上涨和下跌
            gains = close_diff.where(close_diff > 0, 0.0)
            losses = (-close_diff).where(close_diff < 0, 0.0)

            # 计算平均涨跌幅
            avg_gains = gains.rolling(window=period, min_periods=1).mean()
            avg_losses = losses.rolling(window=period, min_periods=1).mean()

            # 避免除零
            rs = avg_gains / (avg_losses + 1e-10)
            rsi = 100 - (100 / (1 + rs))

            return rsi

        except Exception as e:
            raise AnalysisError(f"Failed to calculate RSI: {e}")

    def calculate_bollinger(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        """
        计算布林带指标

        Args:
            df: K 线数据 DataFrame

        Returns:
            布林带数据字典

        Raises:
            AnalysisError: 计算失败时抛出
        """
        try:
            period = self.bollinger_config.get('period', 20)
            std_dev = self.bollinger_config.get('std_dev', 2)

            if len(df) < period:
                self.logger.warning(f"Insufficient data for Bollinger Bands, need {period} points, got {len(df)}")
                empty_series = pd.Series(index=df.index, dtype=float)
                return {
                    'upper': empty_series,
                    'middle': empty_series,
                    'lower': empty_series
                }

            # 中轨 (移动平均)
            middle = df['close'].rolling(window=period, min_periods=1).mean()

            # 标准差
            std = df['close'].rolling(window=period, min_periods=1).std()

            # 上下轨
            upper = middle + (std * std_dev)
            lower = middle - (std * std_dev)

            return {
                'upper': upper,
                'middle': middle,
                'lower': lower
            }

        except Exception as e:
            raise AnalysisError(f"Failed to calculate Bollinger Bands: {e}")

    def get_trend_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        获取趋势分析

        Args:
            df: 包含技术指标的 DataFrame

        Returns:
            趋势分析结果

        Raises:
            AnalysisError: 分析失败时抛出
        """
        try:
            if df.empty:
                raise ValidationError("DataFrame cannot be empty for trend analysis")

            latest = df.iloc[-1]
            trend_signals = []

            # MA趋势分析
            ma_trend = self._analyze_ma_trend(df)
            if ma_trend:
                trend_signals.append(ma_trend)

            # MACD信号
            macd_signal = self._analyze_macd_signal(latest)
            if macd_signal:
                trend_signals.append(macd_signal)

            # RSI信号
            rsi_signal = self._analyze_rsi_signal(latest)

            # 综合趋势判断
            bullish_signals = trend_signals.count('bullish')
            bearish_signals = trend_signals.count('bearish')

            if bullish_signals > bearish_signals:
                overall_trend = 'bullish'
            elif bearish_signals > bullish_signals:
                overall_trend = 'bearish'
            else:
                overall_trend = 'neutral'

            return {
                'trend': overall_trend,
                'ma_trend': ma_trend,
                'macd_signal': macd_signal,
                'rsi': latest.get('RSI'),
                'rsi_signal': rsi_signal,
                'signals_count': {
                    'bullish': bullish_signals,
                    'bearish': bearish_signals,
                    'neutral': len(trend_signals) - bullish_signals - bearish_signals
                }
            }

        except Exception as e:
            self.logger.error(f"Failed to analyze trend: {e}")
            return {
                'trend': 'neutral',
                'error': str(e)
            }

    def _analyze_ma_trend(self, df: pd.DataFrame) -> Optional[str]:
        """分析移动平均线趋势"""
        try:
            if len(df) < 2:
                return None

            latest = df.iloc[-1]
            prev = df.iloc[-2]

            # 检查可用的MA
            ma_columns = [col for col in df.columns if col.startswith('MA')]
            if len(ma_columns) < 2:
                return None

            # 短期MA > 长期MA 且 价格 > 短期MA
            ma_short = f"MA{min(self.ma_config['periods'])}"
            ma_long = f"MA{max(self.ma_config['periods'])}"

            if ma_short not in df.columns or ma_long not in df.columns:
                return None

            current_short = latest[ma_short]
            current_long = latest[ma_long]
            prev_short = prev[ma_short]
            prev_long = prev[ma_long]

            if pd.isna(current_short) or pd.isna(current_long):
                return None

            # 金叉/死叉判断
            if current_short > current_long and prev_short <= prev_long:
                return 'bullish'  # 金叉
            elif current_short < current_long and prev_short >= prev_long:
                return 'bearish'  # 死叉
            elif current_short > current_long:
                return 'bullish'
            elif current_short < current_long:
                return 'bearish'
            else:
                return 'neutral'

        except Exception as e:
            self.logger.warning(f"MA trend analysis failed: {e}")
            return None

    def _analyze_macd_signal(self, latest_data: pd.Series) -> Optional[str]:
        """分析MACD信号"""
        try:
            dif = latest_data.get('MACD_DIF')
            dea = latest_data.get('MACD_DEA')
            hist = latest_data.get('MACD_HIST')

            if pd.isna(dif) or pd.isna(dea) or pd.isna(hist):
                return None

            if dif > dea and hist > 0:
                return 'bullish'
            elif dif < dea and hist < 0:
                return 'bearish'
            else:
                return 'neutral'

        except Exception as e:
            self.logger.warning(f"MACD signal analysis failed: {e}")
            return None

    def _analyze_rsi_signal(self, latest_data: pd.Series) -> Optional[str]:
        """分析RSI信号"""
        try:
            rsi = latest_data.get('RSI')
            if pd.isna(rsi):
                return None

            overbought = self.rsi_config.get('overbought', 70)
            oversold = self.rsi_config.get('oversold', 30)

            if rsi > overbought:
                return 'bearish'  # 超买
            elif rsi < oversold:
                return 'bullish'  # 超卖
            else:
                return 'neutral'

        except Exception as e:
            self.logger.warning(f"RSI signal analysis failed: {e}")
            return None

    def identify_support_resistance(self, df: pd.DataFrame) -> Tuple[List[float], List[float]]:
        """
        识别支撑阻力位

        Args:
            df: K线数据DataFrame

        Returns:
            支撑位和阻力位列表的元组

        Raises:
            AnalysisError: 识别失败时抛出
        """
        try:
            if df.empty or len(df) < self.sr_config['lookback']:
                self.logger.warning(f"Insufficient data for S/R analysis, need {self.sr_config['lookback']} points")
                return [], []

            lookback = min(self.sr_config['lookback'], len(df))
            recent_data = df.tail(lookback).copy()

            # 寻找局部高点和低点
            highs, lows = self._find_swing_points(recent_data)

            # 聚类相近的点位
            support_levels = self._cluster_levels(lows, recent_data['low'].median())
            resistance_levels = self._cluster_levels(highs, recent_data['high'].median())

            # 按重要性排序
            support_levels = sorted(support_levels, reverse=True)[:5]
            resistance_levels = sorted(resistance_levels)[:5]

            self.logger.debug(f"Identified {len(support_levels)} support and {len(resistance_levels)} resistance levels")
            return support_levels, resistance_levels

        except Exception as e:
            self.logger.error(f"Failed to identify support/resistance: {e}")
            return [], []

    def _find_swing_points(self, df: pd.DataFrame) -> Tuple[List[float], List[float]]:
        """寻找摆动高点和低点"""
        swing_points = self.sr_config.get('swing_points', 3)
        highs = []
        lows = []

        for i in range(swing_points, len(df) - swing_points):
            # 检查是否为局部高点
            if all(df['high'].iloc[i] >= df['high'].iloc[i-j] for j in range(1, swing_points + 1)) and \
               all(df['high'].iloc[i] >= df['high'].iloc[i+j] for j in range(1, swing_points + 1)):
                highs.append(float(df['high'].iloc[i]))

            # 检查是否为局部低点
            if all(df['low'].iloc[i] <= df['low'].iloc[i-j] for j in range(1, swing_points + 1)) and \
               all(df['low'].iloc[i] <= df['low'].iloc[i+j] for j in range(1, swing_points + 1)):
                lows.append(float(df['low'].iloc[i]))

        return highs, lows

    def _cluster_levels(self, levels: List[float], reference_price: float) -> List[float]:
        """聚类相近的价格水平"""
        if not levels:
            return []

        proximity = self.sr_config.get('proximity', 0.01)
        clustered = []

        for level in sorted(levels):
            # 检查是否与已有聚类相近
            merged = False
            for i, cluster in enumerate(clustered):
                if abs(level - cluster) / reference_price <= proximity:
                    # 合并到现有聚类（取平均值）
                    clustered[i] = (cluster + level) / 2
                    merged = True
                    break

            if not merged:
                clustered.append(level)

        return clustered

        # 计算 EMA
        ema_fast = df['close'].ewm(span=fast, adjust=False).mean()
        ema_slow = df['close'].ewm(span=slow, adjust=False).mean()

        # 计算 DIF
        dif = ema_fast - ema_slow

        # 计算 DEA (信号线)
        dea = dif.ewm(span=signal, adjust=False).mean()

        # 计算柱状图
        hist = (dif - dea) * 2

        return {
            'dif': dif,
            'dea': dea,
            'hist': hist
        }

    def calculate_rsi(self, df: pd.DataFrame) -> pd.Series:
        """
        计算 RSI 指标

        Args:
            df: K 线数据 DataFrame

        Returns:
            RSI 值 Series
        """
        period = self.rsi_config.get('period', 14)

        # 计算价格变化
        delta = df['close'].diff()

        # 分离涨跌
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        # 计算 RSI
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def calculate_bollinger(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        """
        计算布林带

        Args:
            df: K 线数据 DataFrame

        Returns:
            布林带数据字典
        """
        period = self.bollinger_config.get('period', 20)
        std_dev = self.bollinger_config.get('std_dev', 2)

        # 中轨（移动平均）
        middle = df['close'].rolling(window=period).mean()

        # 标准差
        std = df['close'].rolling(window=period).std()

        # 上轨和下轨
        upper = middle + (std * std_dev)
        lower = middle - (std * std_dev)

        return {
            'upper': upper,
            'middle': middle,
            'lower': lower
        }

    def calculate_atr(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """
        计算平均真实波幅 (ATR)

        Args:
            df: K 线数据 DataFrame
            period: 计算周期

        Returns:
            ATR 值 Series
        """
        high = df['high']
        low = df['low']
        close = df['close']

        # 计算真实波幅
        tr1 = high - low
        tr2 = (high - close.shift()).abs()
        tr3 = (low - close.shift()).abs()

        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

        # 计算 ATR
        atr = tr.rolling(window=period).mean()

        return atr

    def identify_support_resistance(self, df: pd.DataFrame) -> Tuple[List[float], List[float]]:
        """
        识别支撑位和阻力位

        Args:
            df: K 线数据 DataFrame

        Returns:
            (支撑位列表, 阻力位列表)
        """
        lookback = self.sr_config.get('lookback', 100)
        swing_points = self.sr_config.get('swing_points', 3)
        proximity = self.sr_config.get('proximity', 0.01)

        # 获取最近的数据
        recent_df = df.tail(lookback)

        # 寻找局部高点和低点
        highs = []
        lows = []

        for i in range(swing_points, len(recent_df) - swing_points):
            # 局部高点
            is_high = all(
                recent_df.iloc[i]['high'] >= recent_df.iloc[j]['high']
                for j in range(i - swing_points, i + swing_points + 1)
                if j != i
            )

            # 局部低点
            is_low = all(
                recent_df.iloc[i]['low'] <= recent_df.iloc[j]['low']
                for j in range(i - swing_points, i + swing_points + 1)
                if j != i
            )

            if is_high:
                highs.append(recent_df.iloc[i]['high'])
            if is_low:
                lows.append(recent_df.iloc[i]['low'])

        # 合并相近的价格点
        def merge_levels(levels: List[float], proximity: float) -> List[float]:
            if not levels:
                return []

            levels.sort(reverse=True)
            merged = [levels[0]]

            for level in levels[1:]:
                # 检查是否与已存在的点位相近
                is_close = any(
                    abs(level - existing) / existing < proximity
                    for existing in merged
                )

                if not is_close:
                    merged.append(level)

            return merged

        support_levels = merge_levels(lows, proximity)
        resistance_levels = merge_levels(highs, proximity)

        return support_levels, resistance_levels

    def get_trend_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        获取趋势分析结果

        Args:
            df: 包含技术指标的 DataFrame

        Returns:
            趋势分析字典
        """
        if len(df) < 20:
            return {'error': '数据不足'}

        # 获取最新数据
        latest = df.iloc[-1]
        prev = df.iloc[-2]

        # MA 趋势分析
        ma_periods = self.ma_config.get('periods', [5, 10, 20, 60])
        ma_trend = {}
        ma_alignment = True  # 是否多头排列

        for period in ma_periods:
            ma_key = f'MA{period}'
            if ma_key in df.columns:
                ma_trend[ma_key] = latest[ma_key]
                # 检查多头排列：短期 > 长期
                if period < ma_periods[-1]:
                    next_ma_key = f'MA{ma_periods[ma_periods.index(period) + 1]}'
                    if next_ma_key in df.columns:
                        if latest[ma_key] < latest[next_ma_key]:
                            ma_alignment = False

        # MACD 信号
        macd_signal = 'neutral'
        if 'MACD_DIF' in df.columns and 'MACD_DEA' in df.columns:
            if latest['MACD_DIF'] > latest['MACD_DEA'] and prev['MACD_DIF'] <= prev['MACD_DEA']:
                macd_signal = 'golden_cross'  # 金叉
            elif latest['MACD_DIF'] < latest['MACD_DEA'] and prev['MACD_DIF'] >= prev['MACD_DEA']:
                macd_signal = 'death_cross'  # 死叉
            elif latest['MACD_DIF'] > latest['MACD_DEA']:
                macd_signal = 'bullish'  # 多头
            else:
                macd_signal = 'bearish'  # 空头

        # RSI 信号
        rsi_signal = 'neutral'
        if 'RSI' in df.columns:
            rsi_value = latest['RSI']
            overbought = self.rsi_config.get('overbought', 70)
            oversold = self.rsi_config.get('oversold', 30)

            if rsi_value > overbought:
                rsi_signal = 'overbought'
            elif rsi_value < oversold:
                rsi_signal = 'oversold'
            else:
                rsi_signal = 'normal'

        # 布林带位置
        bb_position = 'middle'
        if all(col in df.columns for col in ['BB_UPPER', 'BB_MIDDLE', 'BB_LOWER']):
            if latest['close'] > latest['BB_UPPER']:
                bb_position = 'above_upper'
            elif latest['close'] < latest['BB_LOWER']:
                bb_position = 'below_lower'

        # 综合趋势判断
        trend = 'neutral'
        if ma_alignment and macd_signal in ['golden_cross', 'bullish']:
            trend = 'bullish'
        elif not ma_alignment and macd_signal in ['death_cross', 'bearish']:
            trend = 'bearish'

        return {
            'ma_trend': ma_trend,
            'ma_alignment': ma_alignment,
            'macd_signal': macd_signal,
            'rsi_signal': rsi_signal,
            'bb_position': bb_position,
            'trend': trend
        }

    def save_indicators(self, df: pd.DataFrame, symbol: str, timeframe: str):
        """
        保存指标数据到文件

        Args:
            df: 包含指标的 DataFrame
            symbol: 交易品种代码
            timeframe: 时间周期
        """
        output_dir = Path('data/processed')
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{symbol}_{timeframe}_indicators_{timestamp}.csv"
        filepath = output_dir / filename

        df.to_csv(filepath)
        return filepath
