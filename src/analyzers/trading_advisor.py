"""
交易建议生成模块
根据技术分析生成具体的做单建议
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from loguru import logger


class TradeDirection(Enum):
    """交易方向"""
    LONG = "做多"
    SHORT = "做空"
    NEUTRAL = "观望"


class StopLossType(Enum):
    """止损类型"""
    AGGRESSIVE = "激进止损"
    STANDARD = "标准止损"
    STRUCTURE = "结构止损"


@dataclass
class TradingAdvice:
    """交易建议数据结构"""
    direction: TradeDirection          # 当前偏向
    bias_reason: str                   # 偏向理由
    
    main_plan: str                     # 主方案
    alternative_plan: str              # 备选方案
    
    entry_price: float                 # 建议入场价
    entry_range: Tuple[float, float]   # 入场区间
    
    stop_loss_aggressive: float        # 激进止损
    stop_loss_standard: float          # 标准止损
    stop_loss_structure: float         # 结构止损
    
    take_profit_1: float               # 第一目标
    take_profit_2: float               # 第二目标
    take_profit_3: Optional[float]     # 第三目标
    
    stop_loss_zone: Tuple[float, float]  # 扫损区
    invalidation_condition: str        # 作废条件
    
    position_suggestion: str           # 仓位建议
    risk_reward_ratio: float           # 盈亏比
    
    confidence_score: int              # 置信度 (0-100)
    time_frame: str                    # 时间周期


class TradingAdvisor:
    """交易建议生成器"""
    
    def __init__(self):
        self.logger = logger.bind(name=self.__class__.__name__)
    
    def generate_advice(
        self,
        df: pd.DataFrame,
        technical_data: Dict[str, Any],
        support_levels: List[float],
        resistance_levels: List[float],
        current_price: float,
        timeframe: str = "1d"
    ) -> TradingAdvice:
        """
        生成交易建议
        
        Args:
            df: K线数据
            technical_data: 技术指标数据
            support_levels: 支撑位列表
            resistance_levels: 阻力位列表
            current_price: 当前价格
            timeframe: 时间周期
            
        Returns:
            TradingAdvice 对象
        """
        try:
            # 分析趋势方向
            direction, bias_reason = self._analyze_direction(
                df, technical_data, current_price
            )
            
            # 生成交易方案
            main_plan, alternative_plan = self._generate_plans(
                direction, current_price, support_levels, resistance_levels
            )
            
            # 计算入场区间
            entry_price, entry_range = self._calculate_entry(
                direction, current_price, support_levels, resistance_levels
            )
            
            # 计算止损位
            sl_aggressive, sl_standard, sl_structure = self._calculate_stop_loss(
                direction, current_price, df, support_levels, resistance_levels
            )
            
            # 计算目标位
            tp1, tp2, tp3 = self._calculate_take_profit(
                direction, current_price, support_levels, resistance_levels
            )
            
            # 计算扫损区
            stop_loss_zone = self._calculate_stop_loss_zone(
                direction, current_price, sl_standard, support_levels, resistance_levels
            )
            
            # 生成作废条件
            invalidation = self._generate_invalidation_condition(
                direction, technical_data, current_price
            )
            
            # 仓位建议
            position_suggestion = self._generate_position_suggestion(
                direction, technical_data
            )
            
            # 计算盈亏比
            risk = abs(entry_price - sl_standard)
            reward = abs(tp1 - entry_price)
            rr_ratio = reward / risk if risk > 0 else 0
            
            # 计算置信度
            confidence = self._calculate_confidence(
                direction, technical_data, df
            )
            
            return TradingAdvice(
                direction=direction,
                bias_reason=bias_reason,
                main_plan=main_plan,
                alternative_plan=alternative_plan,
                entry_price=entry_price,
                entry_range=entry_range,
                stop_loss_aggressive=sl_aggressive,
                stop_loss_standard=sl_standard,
                stop_loss_structure=sl_structure,
                take_profit_1=tp1,
                take_profit_2=tp2,
                take_profit_3=tp3,
                stop_loss_zone=stop_loss_zone,
                invalidation_condition=invalidation,
                position_suggestion=position_suggestion,
                risk_reward_ratio=rr_ratio,
                confidence_score=confidence,
                time_frame=timeframe
            )
            
        except Exception as e:
            self.logger.error(f"生成交易建议失败: {e}")
            return self._generate_default_advice(current_price, timeframe)
    
    def _analyze_direction(
        self,
        df: pd.DataFrame,
        technical_data: Dict[str, Any],
        current_price: float
    ) -> Tuple[TradeDirection, str]:
        """分析交易方向"""
        
        signals = []
        
        # 1. 趋势分析
        trend = technical_data.get('trend', 'neutral')
        if trend == 'bullish':
            signals.append(('趋势', 1))
        elif trend == 'bearish':
            signals.append(('趋势', -1))
        else:
            signals.append(('趋势', 0))
        
        # 2. MACD信号
        macd_signal = technical_data.get('macd_signal', 'neutral')
        if macd_signal in ['golden_cross', 'bullish']:
            signals.append(('MACD', 1))
        elif macd_signal in ['death_cross', 'bearish']:
            signals.append(('MACD', -1))
        else:
            signals.append(('MACD', 0))
        
        # 3. RSI信号
        rsi_signal = technical_data.get('rsi_signal', 'normal')
        if rsi_signal == 'oversold':
            signals.append(('RSI', 1))
        elif rsi_signal == 'overbought':
            signals.append(('RSI', -1))
        else:
            signals.append(('RSI', 0))
        
        # 4. MA排列
        ma_alignment = technical_data.get('ma_alignment', False)
        if ma_alignment:
            signals.append(('MA排列', 1))
        else:
            signals.append(('MA排列', -1))
        
        # 5. 布林带位置
        bb_position = technical_data.get('bb_position', 'middle')
        if bb_position == 'below_lower':
            signals.append(('布林带', 1))
        elif bb_position == 'above_upper':
            signals.append(('布林带', -1))
        else:
            signals.append(('布林带', 0))
        
        # 计算总分
        total_score = sum(score for _, score in signals)
        
        # 确定方向
        if total_score >= 2:
            direction = TradeDirection.LONG
            reasons = [name for name, score in signals if score > 0]
            bias_reason = f"多头信号占优: {', '.join(reasons)}"
        elif total_score <= -2:
            direction = TradeDirection.SHORT
            reasons = [name for name, score in signals if score < 0]
            bias_reason = f"空头信号占优: {', '.join(reasons)}"
        else:
            direction = TradeDirection.NEUTRAL
            bias_reason = "多空信号均衡，建议观望"
        
        return direction, bias_reason
    
    def _generate_plans(
        self,
        direction: TradeDirection,
        current_price: float,
        supports: List[float],
        resistances: List[float]
    ) -> Tuple[str, str]:
        """生成主方案和备选方案"""
        
        if direction == TradeDirection.LONG:
            main_plan = f"等待回调至支撑位附近做多"
            if supports:
                main_plan += f"，参考支撑: ${supports[0]:.2f}"
            
            alternative_plan = f"突破近期高点追多"
            if resistances:
                alternative_plan += f"，突破: ${resistances[0]:.2f}"
                
        elif direction == TradeDirection.SHORT:
            main_plan = f"等待反弹至阻力位附近做空"
            if resistances:
                main_plan += f"，参考阻力: ${resistances[0]:.2f}"
            
            alternative_plan = f"跌破近期低点追空"
            if supports:
                alternative_plan += f"，跌破: ${supports[0]:.2f}"
        else:
            main_plan = "观望，等待方向明确"
            alternative_plan = "突破关键位后再考虑入场"
        
        return main_plan, alternative_plan
    
    def _calculate_entry(
        self,
        direction: TradeDirection,
        current_price: float,
        supports: List[float],
        resistances: List[float]
    ) -> Tuple[float, Tuple[float, float]]:
        """计算入场价格和区间"""
        
        if direction == TradeDirection.LONG:
            if supports:
                entry = supports[0]
                entry_low = supports[0] * 0.995
                entry_high = supports[0] * 1.005
            else:
                entry = current_price * 0.99
                entry_low = current_price * 0.985
                entry_high = current_price * 0.995
                
        elif direction == TradeDirection.SHORT:
            if resistances:
                entry = resistances[0]
                entry_low = resistances[0] * 0.995
                entry_high = resistances[0] * 1.005
            else:
                entry = current_price * 1.01
                entry_low = current_price * 1.005
                entry_high = current_price * 1.015
        else:
            entry = current_price
            entry_low = current_price * 0.995
            entry_high = current_price * 1.005
        
        return entry, (entry_low, entry_high)
    
    def _calculate_stop_loss(
        self,
        direction: TradeDirection,
        current_price: float,
        df: pd.DataFrame,
        supports: List[float],
        resistances: List[float]
    ) -> Tuple[float, float, float]:
        """计算三种止损位"""
        
        # 计算ATR
        atr = self._calculate_atr(df, 14)
        
        if direction == TradeDirection.LONG:
            # 激进止损: 前低下方1倍ATR
            sl_aggressive = current_price - atr * 1.5
            # 标准止损: 前低下方2倍ATR
            sl_standard = current_price - atr * 2.5
            # 结构止损: 关键支撑位下方
            if len(supports) >= 2:
                sl_structure = supports[1] * 0.99
            elif supports:
                sl_structure = supports[0] * 0.99
            else:
                sl_structure = current_price * 0.95
                
        elif direction == TradeDirection.SHORT:
            # 激进止损: 前高上方1倍ATR
            sl_aggressive = current_price + atr * 1.5
            # 标准止损: 前高上方2倍ATR
            sl_standard = current_price + atr * 2.5
            # 结构止损: 关键阻力位上方
            if len(resistances) >= 2:
                sl_structure = resistances[1] * 1.01
            elif resistances:
                sl_structure = resistances[0] * 1.01
            else:
                sl_structure = current_price * 1.05
        else:
            sl_aggressive = sl_standard = sl_structure = current_price
        
        return sl_aggressive, sl_standard, sl_structure
    
    def _calculate_take_profit(
        self,
        direction: TradeDirection,
        current_price: float,
        supports: List[float],
        resistances: List[float]
    ) -> Tuple[float, float, Optional[float]]:
        """计算目标位"""
        
        if direction == TradeDirection.LONG:
            if resistances:
                tp1 = resistances[0]
                tp2 = resistances[1] if len(resistances) > 1 else current_price * 1.03
                tp3 = resistances[2] if len(resistances) > 2 else current_price * 1.05
            else:
                tp1 = current_price * 1.02
                tp2 = current_price * 1.04
                tp3 = current_price * 1.06
                
        elif direction == TradeDirection.SHORT:
            if supports:
                tp1 = supports[0]
                tp2 = supports[1] if len(supports) > 1 else current_price * 0.97
                tp3 = supports[2] if len(supports) > 2 else current_price * 0.95
            else:
                tp1 = current_price * 0.98
                tp2 = current_price * 0.96
                tp3 = current_price * 0.94
        else:
            tp1 = tp2 = current_price
            tp3 = None
        
        return tp1, tp2, tp3
    
    def _calculate_stop_loss_zone(
        self,
        direction: TradeDirection,
        current_price: float,
        sl_standard: float,
        supports: List[float],
        resistances: List[float]
    ) -> Tuple[float, float]:
        """计算扫损区"""
        
        if direction == TradeDirection.LONG:
            zone_low = sl_standard * 0.995
            zone_high = sl_standard * 1.005
        elif direction == TradeDirection.SHORT:
            zone_low = sl_standard * 0.995
            zone_high = sl_standard * 1.005
        else:
            zone_low = current_price * 0.99
            zone_high = current_price * 1.01
        
        return zone_low, zone_high
    
    def _generate_invalidation_condition(
        self,
        direction: TradeDirection,
        technical_data: Dict[str, Any],
        current_price: float
    ) -> str:
        """生成作废条件"""
        
        conditions = []
        
        if direction == TradeDirection.LONG:
            conditions.append("价格跌破结构止损位")
            conditions.append("MACD出现死叉信号")
            conditions.append("RSI进入超卖区间(<30)")
            conditions.append("出现重大利空消息")
            
        elif direction == TradeDirection.SHORT:
            conditions.append("价格突破结构止损位")
            conditions.append("MACD出现金叉信号")
            conditions.append("RSI进入超买区间(>70)")
            conditions.append("出现重大利好消息")
        else:
            conditions.append("方向明确后重新评估")
        
        return "; ".join(conditions)
    
    def _generate_position_suggestion(
        self,
        direction: TradeDirection,
        technical_data: Dict[str, Any]
    ) -> str:
        """生成仓位建议"""
        
        if direction == TradeDirection.NEUTRAL:
            return "空仓观望"
        
        # 根据信号强度调整仓位
        trend = technical_data.get('trend', 'neutral')
        macd_signal = technical_data.get('macd_signal', 'neutral')
        rsi_signal = technical_data.get('rsi_signal', 'normal')
        
        strength = 0
        if trend == 'bullish':
            strength += 1
        if macd_signal in ['golden_cross', 'bullish']:
            strength += 1
        if rsi_signal == 'oversold':
            strength += 1
        
        if strength >= 3:
            return "标准仓位 (5-10%)"
        elif strength >= 2:
            return "轻仓试探 (3-5%)"
        else:
            return "极小仓位 (1-3%)"
    
    def _calculate_confidence(
        self,
        direction: TradeDirection,
        technical_data: Dict[str, Any],
        df: pd.DataFrame
    ) -> int:
        """计算置信度 (0-100)"""
        
        if direction == TradeDirection.NEUTRAL:
            return 30
        
        score = 50  # 基础分
        
        # 趋势一致性
        trend = technical_data.get('trend', 'neutral')
        if trend != 'neutral':
            score += 15
        
        # MACD信号
        macd_signal = technical_data.get('macd_signal', 'neutral')
        if macd_signal in ['golden_cross', 'death_cross']:
            score += 15
        elif macd_signal in ['bullish', 'bearish']:
            score += 10
        
        # RSI位置
        rsi_signal = technical_data.get('rsi_signal', 'normal')
        if rsi_signal in ['oversold', 'overbought']:
            score += 10
        
        # MA排列
        if technical_data.get('ma_alignment', False):
            score += 10
        
        # 数据量
        if len(df) >= 100:
            score += 10
        
        return min(95, max(20, score))
    
    def _calculate_atr(self, df: pd.DataFrame, period: int = 14) -> float:
        """计算ATR"""
        try:
            high = df['high']
            low = df['low']
            close = df['close']
            
            tr1 = high - low
            tr2 = (high - close.shift()).abs()
            tr3 = (low - close.shift()).abs()
            
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr = tr.rolling(window=period).mean().iloc[-1]
            
            return atr if not pd.isna(atr) else (high - low).mean()
        except:
            return (df['high'] - df['low']).mean()
    
    def _generate_default_advice(
        self,
        current_price: float,
        timeframe: str
    ) -> TradingAdvice:
        """生成默认建议"""
        return TradingAdvice(
            direction=TradeDirection.NEUTRAL,
            bias_reason="数据不足，无法判断",
            main_plan="观望",
            alternative_plan="等待信号明确",
            entry_price=current_price,
            entry_range=(current_price * 0.99, current_price * 1.01),
            stop_loss_aggressive=current_price * 0.95,
            stop_loss_standard=current_price * 0.93,
            stop_loss_structure=current_price * 0.90,
            take_profit_1=current_price * 1.02,
            take_profit_2=current_price * 1.04,
            take_profit_3=current_price * 1.06,
            stop_loss_zone=(current_price * 0.92, current_price * 0.95),
            invalidation_condition="数据不足",
            position_suggestion="空仓观望",
            risk_reward_ratio=1.0,
            confidence_score=20,
            time_frame=timeframe
        )
    
    def to_dict(self, advice: TradingAdvice) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'direction': advice.direction.value,
            'bias_reason': advice.bias_reason,
            'main_plan': advice.main_plan,
            'alternative_plan': advice.alternative_plan,
            'entry_price': round(advice.entry_price, 2),
            'entry_range': (round(advice.entry_range[0], 2), round(advice.entry_range[1], 2)),
            'stop_loss': {
                'aggressive': round(advice.stop_loss_aggressive, 2),
                'standard': round(advice.stop_loss_standard, 2),
                'structure': round(advice.stop_loss_structure, 2)
            },
            'take_profit': {
                'tp1': round(advice.take_profit_1, 2),
                'tp2': round(advice.take_profit_2, 2),
                'tp3': round(advice.take_profit_3, 2) if advice.take_profit_3 else None
            },
            'stop_loss_zone': (round(advice.stop_loss_zone[0], 2), round(advice.stop_loss_zone[1], 2)),
            'invalidation_condition': advice.invalidation_condition,
            'position_suggestion': advice.position_suggestion,
            'risk_reward_ratio': round(advice.risk_reward_ratio, 2),
            'confidence_score': advice.confidence_score,
            'time_frame': advice.time_frame
        }
