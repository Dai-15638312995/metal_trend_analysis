"""
交易建议生成模块
使用 LLM AI 分析 K 线数据生成做单建议
"""
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from loguru import logger

from ..llm.analyzer import LLMAnalyzer


class TradingAdvisor:
    """交易建议生成器 - 基于 LLM AI 分析"""

    def __init__(self, llm_analyzer: Optional[LLMAnalyzer] = None):
        """
        初始化交易建议生成器

        Args:
            llm_analyzer: LLM 分析器实例（用于调用 AI 生成建议）
        """
        self.logger = logger.bind(name=self.__class__.__name__)
        self.llm_analyzer = llm_analyzer

    def generate_advice(
        self,
        kline_data: pd.DataFrame,
        technical_data: Dict[str, Any],
        support_levels: List[float],
        resistance_levels: List[float],
        current_price: float,
        timeframe: str = "1d",
        multi_timeframe_data: Dict[str, pd.DataFrame] = None
    ) -> Dict[str, Any]:
        """
        生成交易建议（调用 LLM AI 分析）

        Args:
            kline_data: K线数据（主时间周期）
            technical_data: 技术指标数据
            support_levels: 支撑位列表
            resistance_levels: 阻力位列表
            current_price: 当前价格
            timeframe: 时间周期
            multi_timeframe_data: 多时间周期K线数据字典

        Returns:
            交易建议字典
        """
        try:
            # 打印入参
            self.logger.info("=" * 80)
            self.logger.info("【generate_advice 入参】")
            self.logger.info("=" * 80)
            self.logger.info(f"current_price: {current_price}")
            self.logger.info(f"timeframe: {timeframe}")
            self.logger.info(f"kline_data shape: {kline_data.shape if kline_data is not None else None}")
            self.logger.info(f"kline_data columns: {list(kline_data.columns) if kline_data is not None else None}")
            self.logger.info(f"kline_data last 3 rows:\n{kline_data.tail(3) if kline_data is not None else None}")
            self.logger.info(f"technical_data keys: {list(technical_data.keys()) if technical_data else None}")
            self.logger.info(f"technical_data content: {technical_data}")
            self.logger.info(f"support_levels: {support_levels}")
            self.logger.info(f"resistance_levels: {resistance_levels}")
            self.logger.info(f"multi_timeframe_data keys: {list(multi_timeframe_data.keys()) if multi_timeframe_data else None}")
            if multi_timeframe_data:
                for tf, df in multi_timeframe_data.items():
                    self.logger.info(f"  {tf}: shape={df.shape if df is not None else None}")
            self.logger.info("=" * 80)

            # 如果有 LLM 分析器，使用 AI 生成建议
            if self.llm_analyzer:
                result = self._generate_advice_with_llm(
                    kline_data, technical_data, support_levels,
                    resistance_levels, current_price, timeframe,
                    multi_timeframe_data
                )
                # 打印出参
                self.logger.info("=" * 80)
                self.logger.info("【generate_advice 出参】")
                self.logger.info("=" * 80)
                self.logger.info(f"result: {result}")
                self.logger.info("=" * 80)
                return result
            else:
                # 没有 LLM 时返回提示
                result = self._generate_no_llm_advice(current_price, timeframe)
                self.logger.info("=" * 80)
                self.logger.info("【generate_advice 出参 - 无LLM】")
                self.logger.info("=" * 80)
                self.logger.info(f"result: {result}")
                self.logger.info("=" * 80)
                return result

        except Exception as e:
            self.logger.error(f"生成交易建议失败: {e}")
            result = self._generate_error_advice(current_price, timeframe, str(e))
            self.logger.info("=" * 80)
            self.logger.info("【generate_advice 出参 - 错误】")
            self.logger.info("=" * 80)
            self.logger.info(f"result: {result}")
            self.logger.info("=" * 80)
            return result

    def _generate_advice_with_llm(
        self,
        kline_data: pd.DataFrame,
        technical_data: Dict[str, Any],
        support_levels: List[float],
        resistance_levels: List[float],
        current_price: float,
        timeframe: str,
        multi_timeframe_data: Dict[str, pd.DataFrame] = None
    ) -> Dict[str, Any]:
        """使用 LLM AI 生成交易建议"""
        try:
            self.logger.info("=" * 60)
            self.logger.info("【交易建议生成开始】")
            self.logger.info(f"当前价格: ${current_price:.2f}")
            self.logger.info("=" * 60)

            # 先进行多周期技术分析，提取关键信息
            self.logger.info("【步骤1】多周期技术分析...")
            multi_tf_analysis = self._analyze_multi_timeframe(
                multi_timeframe_data, current_price, technical_data
            )

            # 构建提示词（包含多周期分析结果）
            self.logger.info("【步骤2】构建 AI 提示词...")
            prompt = self._build_trading_prompt_v2(
                kline_data, technical_data, support_levels,
                resistance_levels, current_price, timeframe,
                multi_tf_analysis
            )

            # 打印完整提示词
            self.logger.info("-" * 60)
            self.logger.info("【发送给 AI 的提示词】:")
            self.logger.info("-" * 60)
            for line in prompt.split('\n'):
                self.logger.info(f"  {line}")
            self.logger.info("-" * 60)

            # 调用 LLM
            self.logger.info("【步骤3】调用通义千问 AI...")
            response = self.llm_analyzer.client.chat.completions.create(
                model=self.llm_analyzer.model,
                messages=[
                    {
                        "role": "system",
                        "content": """你是一位专业的多周期交易分析师，精通技术分析和趋势判断。

你的任务是：
1. 基于多周期技术分析结果，判断趋势方向
2. 找出最佳入场时机和价位
3. 设置合理的止损和目标位

分析原则：
- 大周期（日线/4小时）定方向
- 中周期（1小时）找位置
- 小周期（15/30分钟）精确入场
- 多周期共振时信号最强
- 周期冲突时观望或轻仓

输出必须基于实际数据，禁止虚构价格。"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,
                max_tokens=1500
            )

            llm_response = response.choices[0].message.content

            # 打印 AI 原始响应
            self.logger.info("-" * 60)
            self.logger.info("【AI 原始响应】:")
            self.logger.info("-" * 60)
            for line in llm_response.split('\n'):
                self.logger.info(f"  {line}")
            self.logger.info("-" * 60)

            if not llm_response:
                return self._generate_error_advice(current_price, timeframe, "LLM 返回为空")

            # 解析 LLM 响应
            self.logger.info("【步骤4】解析 AI 响应...")
            advice = self._parse_llm_response_v2(llm_response, current_price, technical_data)

            self.logger.info("=" * 60)
            self.logger.info("【交易建议生成完成】")
            self.logger.info(f"  方向: {advice.get('direction', '未知')}")
            self.logger.info(f"  入场价: ${advice.get('entry_price', 0):.2f}")
            self.logger.info(f"  标准止损: ${advice['stop_loss']['standard']:.2f}")
            self.logger.info(f"  TP1: ${advice['take_profit']['tp1']:.2f}")
            self.logger.info(f"  盈亏比: 1:{advice.get('risk_reward_ratio', 0):.2f}")
            self.logger.info("=" * 60)

            return advice

        except Exception as e:
            self.logger.error(f"LLM 交易建议生成失败: {e}")
            return self._generate_error_advice(current_price, timeframe, str(e))

    def _analyze_multi_timeframe(
        self,
        multi_timeframe_data: Dict[str, pd.DataFrame],
        current_price: float,
        technical_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        对多周期数据进行预分析，提取关键信息
        重点：使用 technical_data 中的趋势作为主要方向
        """
        result = {
            'trends': {},
            'key_levels': {'supports': [], 'resistances': []},
            'signals': {},
            'alignment': 'neutral',
            'primary_direction': 'neutral'
        }

        # ===== 1. 获取主要趋势方向（来自 technical_data）=====
        if technical_data:
            primary_trend = technical_data.get('trend', 'neutral')
            macd_signal = technical_data.get('macd_signal', 'neutral')
            rsi = technical_data.get('rsi')

            result['primary_direction'] = primary_trend
            result['macd_signal'] = macd_signal
            result['rsi'] = rsi

            self.logger.info("")
            self.logger.info("【技术指标趋势（主要方向）】")
            self.logger.info(f"  日线趋势: {primary_trend} (MACD: {macd_signal})")
            if rsi:
                self.logger.info(f"  RSI: {rsi:.1f}")
            self.logger.info("")

        if not multi_timeframe_data:
            self.logger.warning("没有多周期数据，跳过分析")
            return result

        self.logger.info("【多周期趋势分析（辅助参考）】")
        self.logger.info("-" * 40)

        tf_order = ['1d', '4h', '1h', '30m', '15m', '5m']
        tf_names = {
            '1d': '日线',
            '4h': '4小时',
            '1h': '1小时',
            '30m': '30分钟',
            '15m': '15分钟',
            '5m': '5分钟'
        }

        bullish_count = 0
        bearish_count = 0
        neutral_count = 0

        for tf in tf_order:
            if tf not in multi_timeframe_data or multi_timeframe_data[tf].empty:
                self.logger.info(f"  {tf_names[tf]}: 无数据")
                continue

            df = multi_timeframe_data[tf]

            # 计算该周期的趋势
            trend = self._calculate_trend_simple(df)
            result['trends'][tf_names[tf]] = trend

            trend_icon = {'bullish': '🔴 看涨', 'bearish': '🟢 看跌', 'neutral': '⚪ 中性'}.get(trend, trend)
            self.logger.info(f"  {tf_names[tf]}: {trend_icon} (数据: {len(df)}条)")

            if trend == 'bullish':
                bullish_count += 1
            elif trend == 'bearish':
                bearish_count += 1
            else:
                neutral_count += 1

            # 计算关键价位（只取日线和4小时的）
            if tf in ['1d', '4h']:
                supports, resistances = self._find_key_levels(df, current_price)
                result['key_levels']['supports'].extend(supports)
                result['key_levels']['resistances'].extend(resistances)
                if supports:
                    self.logger.info(f"    支撑位: {', '.join([f'${s:.2f}' for s in supports])}")
                if resistances:
                    self.logger.info(f"    阻力位: {', '.join([f'${r:.2f}' for r in resistances])}")

        # 判断多周期一致性
        total = bullish_count + bearish_count + neutral_count
        if total > 0:
            if bullish_count >= total * 0.6:
                result['alignment'] = 'strong_bullish'
            elif bearish_count >= total * 0.6:
                result['alignment'] = 'strong_bearish'
            elif bullish_count > bearish_count:
                result['alignment'] = 'bullish'
            elif bearish_count > bullish_count:
                result['alignment'] = 'bearish'
            else:
                result['alignment'] = 'neutral'

        alignment_text = {
            'strong_bullish': '强多头共振 ✅✅',
            'strong_bearish': '强空头共振 ✅✅',
            'bullish': '多头占优 ✅',
            'bearish': '空头占优 ✅',
            'neutral': '周期冲突/震荡 ⚠️'
        }.get(result['alignment'], result['alignment'])

        self.logger.info("-" * 40)
        self.logger.info(f"【多周期一致性】: {alignment_text}")
        self.logger.info(f"  看涨周期: {bullish_count}, 看跌周期: {bearish_count}, 中性周期: {neutral_count}")
        self.logger.info("")

        # 去重并排序关键价位
        result['key_levels']['supports'] = sorted(list(set(result['key_levels']['supports'])), reverse=True)[:5]
        result['key_levels']['resistances'] = sorted(list(set(result['key_levels']['resistances'])))[:5]

        return result

    def _calculate_trend_simple(self, df: pd.DataFrame) -> str:
        """简单趋势判断"""
        if len(df) < 10:
            return 'neutral'

        # 使用均线判断
        df = df.copy()
        df['ma5'] = df['close'].rolling(5).mean()
        df['ma10'] = df['close'].rolling(10).mean()
        df['ma20'] = df['close'].rolling(20).mean()

        last = df.iloc[-1]

        if last['close'] > last['ma5'] > last['ma10'] > last['ma20']:
            return 'bullish'
        elif last['close'] < last['ma5'] < last['ma10'] < last['ma20']:
            return 'bearish'
        else:
            return 'neutral'

    def _find_key_levels(self, df: pd.DataFrame, current_price: float) -> Tuple[List[float], List[float]]:
        """找出关键支撑阻力位"""
        supports = []
        resistances = []

        if len(df) < 20:
            return supports, resistances

        # 找近期高低点
        recent = df.tail(20)

        # 支撑位：近期低点
        lows = recent['low'].nsmallest(3).tolist()
        for low in lows:
            if low < current_price * 1.02:  # 在当前价附近或下方
                supports.append(round(low, 2))

        # 阻力位：近期高点
        highs = recent['high'].nlargest(3).tolist()
        for high in highs:
            if high > current_price * 0.98:  # 在当前价附近或上方
                resistances.append(round(high, 2))

        return supports, resistances

    def _build_trading_prompt_v2(
        self,
        kline_data: pd.DataFrame,
        technical_data: Dict[str, Any],
        support_levels: List[float],
        resistance_levels: List[float],
        current_price: float,
        timeframe: str,
        multi_tf_analysis: Dict[str, Any]
    ) -> str:
        """构建交易建议提示词 - 基于技术指标确定方向"""
        lines = []

        lines.append("## 多周期交易分析")
        lines.append("")

        # ====== 1. 主要方向（来自技术指标，必须遵循）======
        lines.append("### ⚠️ 【主要方向 - 必须遵循】")
        primary_trend = multi_tf_analysis.get('primary_direction', technical_data.get('trend', 'neutral'))
        primary_trend_text = {"bullish": "🔴 看涨", "bearish": "🟢 看跌", "neutral": "⚪ 中性"}.get(primary_trend, primary_trend)
        lines.append(f"**日线趋势**: {primary_trend_text}")

        macd_signal = multi_tf_analysis.get('macd_signal', technical_data.get('macd_signal', 'neutral'))
        macd_text = {
            "golden_cross": "金叉",
            "death_cross": "死叉",
            "bullish": "多头",
            "bearish": "空头",
            "neutral": "中性"
        }.get(macd_signal, macd_signal)
        lines.append(f"**MACD信号**: {macd_text}")

        rsi = multi_tf_analysis.get('rsi', technical_data.get('rsi'))
        if rsi:
            rsi_text = "超买 ⚠️" if rsi > 70 else "超卖 ⚠️" if rsi < 30 else "正常"
            lines.append(f"**RSI**: {rsi:.1f} ({rsi_text})")

        # 确定主要方向
        main_direction = "neutral"
        if primary_trend == "bullish" or macd_signal in ["golden_cross", "bullish"]:
            main_direction = "做多"
        elif primary_trend == "bearish" or macd_signal in ["death_cross", "bearish"]:
            main_direction = "做空"

        lines.append("")
        lines.append(f"**【必须遵循的主要方向】**: {main_direction}")
        lines.append("※ 所有交易建议必须与上述技术指标方向一致")
        lines.append("")

        # ====== 2. 当前价格和位置 ======
        lines.append("### 📊 当前行情")
        lines.append(f"- 当前价格: ${current_price:.2f}")
        lines.append("")

        # ====== 3. 多周期趋势辅助参考 ======
        lines.append("### 📈 多周期趋势（辅助参考）")
        trends = multi_tf_analysis.get('trends', {})
        trend_icons = {'bullish': '🔴', 'bearish': '🟢', 'neutral': '⚪'}

        for tf_name in ['日线', '4小时', '1小时', '30分钟', '15分钟', '5分钟']:
            if tf_name in trends:
                trend = trends[tf_name]
                lines.append(f"  {tf_name}: {trend_icons.get(trend, '⚪')} {trend}")

        alignment = multi_tf_analysis.get('alignment', 'neutral')
        alignment_text = {
            'strong_bullish': '强多头共振 ✅✅',
            'strong_bearish': '强空头共振 ✅✅',
            'bullish': '多头占优 ✅',
            'bearish': '空头占优 ✅',
            'neutral': '周期不一致 ⚠️'
        }.get(alignment, alignment)
        lines.append(f"**多周期一致性**: {alignment_text}")
        lines.append("")

        # ====== 4. 关键价位 ======
        lines.append("### 🎯 关键价位")
        key_levels = multi_tf_analysis.get('key_levels', {})
        supports = key_levels.get('supports', [])
        resistances = key_levels.get('resistances', [])

        if supports:
            lines.append(f"**支撑位**: {', '.join([f'${s:.2f}' for s in supports])}")
        if resistances:
            lines.append(f"**阻力位**: {', '.join([f'${r:.2f}' for r in resistances])}")

        # 添加支撑阻力分析
        below_supports = [s for s in supports if s < current_price]
        above_supports = [s for s in supports if s >= current_price]
        above_resistances = [r for r in resistances if r > current_price]
        below_resistances = [r for r in resistances if r <= current_price]

        if main_direction == "做多" and below_supports:
            nearest_support = max(below_supports)
            lines.append(f"**最近下方支撑**: ${nearest_support:.2f} (回调目标)")
            lines.append(f"**入场建议**: 等价格回调到 ${nearest_support:.2f} 附近入场做多")
        elif main_direction == "做空" and above_resistances:
            nearest_resistance = min(above_resistances)
            lines.append(f"**最近上方阻力**: ${nearest_resistance:.2f} (反弹目标)")
            lines.append(f"**入场建议**: 等价格反弹到 ${nearest_resistance:.2f} 附近入场做空")

        lines.append("")

        # ====== 5. 交易建议要求 ======
        lines.append("### 📋 交易建议要求")
        lines.append("")
        lines.append("**【必须遵守的规则】**:")
        lines.append("1. **方向必须与技术指标一致** - MACD死叉时不能做多，MACD金叉时不能做空")
        lines.append("2. **止损距离 10-30 美元**")
        lines.append("3. **盈亏比 ≥ 1:2**")
        lines.append("4. **做多时**: 入场价 > 止损价 < 当前价")
        lines.append("5. **做空时**: 入场价 < 止损价 > 当前价")
        lines.append("")
        lines.append("**【入场价位分析要求】**:")
        lines.append("- 必须分析当前价格在支撑/阻力位中的位置")
        lines.append("- 做多时：给出回调支撑位作为入场参考")
        lines.append("- 做空时：给出反弹阻力位作为入场参考")
        lines.append("- 如果当前价已在支撑/阻力位附近，给出具体入场价")
        lines.append("")
        lines.append("输出格式（纯文本）:")
        lines.append("""
方向: 做多/做空/观望（必须与技术指标方向一致）
理由: [分析当前价格位置和技术指标信号]
入场: [具体入场价位和分析，如：回调至$4560支撑位入场做多]
止损: [止损价位]
目标1: [第一目标位]
目标2: [第二目标位]
目标3: [第三目标位]
仓位: [轻仓/标准/重仓]
风险: [高/中/低]
""")

        return "\n".join(lines)

    def _parse_llm_response_v2(
        self,
        response: str,
        current_price: float,
        technical_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """解析 LLM 响应（简化版，带方向验证）"""

        self.logger.info("")
        self.logger.info("【解析 AI 响应】")
        self.logger.info("-" * 40)

        # 提取方向
        direction = "观望"
        if "做空" in response or "看跌" in response or "卖出" in response:
            direction = "做空"
        elif "做多" in response or "看涨" in response or "买入" in response:
            direction = "做多"

        self.logger.info(f"  提取方向: {direction}")

        # 提取文本字段
        bias_reason = self._extract_field(response, "理由", "基于多周期技术分析")
        main_plan = self._extract_field(response, "入场", "等待信号确认")
        position_suggestion = self._extract_field(response, "仓位", "观望")

        self.logger.info(f"  提取理由: {bias_reason[:50]}...")

        # 提取止损价格
        stop_loss_text = self._extract_field(response, "止损", "")
        stop_loss_standard = self._extract_price(stop_loss_text)
        self.logger.info(f"  AI 止损文本: {stop_loss_text}")
        self.logger.info(f"  解析止损价格: ${stop_loss_standard if stop_loss_standard else 'None'}")

        # 提取目标位价格
        tp1 = self._extract_price(self._extract_field(response, "目标1", ""))
        tp2 = self._extract_price(self._extract_field(response, "目标2", ""))
        tp3 = self._extract_price(self._extract_field(response, "目标3", ""))
        self.logger.info(f"  解析 TP1: ${tp1 if tp1 else 'None'}")
        self.logger.info(f"  解析 TP2: ${tp2 if tp2 else 'None'}")
        self.logger.info(f"  解析 TP3: ${tp3 if tp3 else 'None'}")

        # 提取入场价格
        entry_price = self._extract_price(self._extract_field(response, "入场", ""))
        if not entry_price or abs(entry_price - current_price) > current_price * 0.05:
            entry_price = current_price
            self.logger.info(f"  入场价不合理，使用当前价: ${entry_price:.2f}")
        else:
            self.logger.info(f"  解析入场价: ${entry_price:.2f}")

        self.logger.info("-" * 40)
        self.logger.info("【方向验证】")

        # ====== 方向验证：确保止损和目标位方向正确 ======
        if direction == "做多":
            # 做多：止损必须在入场价下方，目标位必须在入场价上方
            if stop_loss_standard and stop_loss_standard >= entry_price:
                # AI 给反了，忽略 AI 的止损，用默认值
                self.logger.warning(f"  ❌ 做多止损 ${stop_loss_standard:.2f} >= 入场价 ${entry_price:.2f}，方向错误！")
                self.logger.warning(f"  → 使用默认止损: ${entry_price - 20:.2f}")
                stop_loss_standard = None
            else:
                self.logger.info(f"  ✅ 做多止损验证通过")

            if tp1 and tp1 <= entry_price:
                self.logger.warning(f"  ❌ 做多目标1 ${tp1:.2f} <= 入场价 ${entry_price:.2f}，方向错误！")
                self.logger.warning(f"  → 使用默认目标: ${entry_price + 40:.2f}")
                tp1 = None
            else:
                self.logger.info(f"  ✅ 做多目标位验证通过")

            # 默认值：做多止损在下方 15-20 美元
            if not stop_loss_standard:
                stop_loss_standard = entry_price - 20
            if not tp1:
                tp1 = entry_price + 40
            if not tp2:
                tp2 = entry_price + 60
            if not tp3:
                tp3 = entry_price + 80

        elif direction == "做空":
            # 做空：止损必须在入场价上方，目标位必须在入场价下方
            if stop_loss_standard and stop_loss_standard <= entry_price:
                # AI 给反了，忽略 AI 的止损，用默认值
                self.logger.warning(f"  ❌ 做空止损 ${stop_loss_standard:.2f} <= 入场价 ${entry_price:.2f}，方向错误！")
                self.logger.warning(f"  → 使用默认止损: ${entry_price + 20:.2f}")
                stop_loss_standard = None
            else:
                self.logger.info(f"  ✅ 做空止损验证通过")

            if tp1 and tp1 >= entry_price:
                self.logger.warning(f"  ❌ 做空目标1 ${tp1:.2f} >= 入场价 ${entry_price:.2f}，方向错误！")
                self.logger.warning(f"  → 使用默认目标: ${entry_price - 40:.2f}")
                tp1 = None
            else:
                self.logger.info(f"  ✅ 做空目标位验证通过")

            # 默认值：做空止损在上方 15-20 美元
            if not stop_loss_standard:
                stop_loss_standard = entry_price + 20
            if not tp1:
                tp1 = entry_price - 40
            if not tp2:
                tp2 = entry_price - 60
            if not tp3:
                tp3 = entry_price - 80

        else:
            # 观望
            stop_loss_standard = stop_loss_standard or current_price - 20
            tp1 = tp1 or current_price + 40
            tp2 = tp2 or current_price + 60
            tp3 = tp3 or current_price + 80
            self.logger.info(f"  观望模式，使用默认参数")

        self.logger.info("-" * 40)
        self.logger.info("【止损距离检查】")

        # ====== 止损距离合理性检查 ======
        stop_distance = abs(stop_loss_standard - entry_price)
        self.logger.info(f"  止损距离: {stop_distance:.2f} 美元")

        if stop_distance > 50:
            self.logger.warning(f"  ❌ 止损距离 {stop_distance:.2f} 过大（>50），缩紧到 20 美元")
            if direction == "做多":
                stop_loss_standard = entry_price - 20
            elif direction == "做空":
                stop_loss_standard = entry_price + 20
        elif stop_distance < 5:
            self.logger.warning(f"  ❌ 止损距离 {stop_distance:.2f} 过小（<5），放宽到 10 美元")
            if direction == "做多":
                stop_loss_standard = entry_price - 10
            elif direction == "做空":
                stop_loss_standard = entry_price + 10
        else:
            self.logger.info(f"  ✅ 止损距离合理（10-50美元范围内）")

        # 计算三种止损
        if direction == "做多":
            stop_loss_aggressive = entry_price - 10
            stop_loss_structure = entry_price - 30
        elif direction == "做空":
            stop_loss_aggressive = entry_price + 10
            stop_loss_structure = entry_price + 30
        else:
            stop_loss_aggressive = entry_price - 10
            stop_loss_structure = entry_price - 30

        # 入场区间
        entry_range = [round(entry_price - 5, 2), round(entry_price + 5, 2)]

        # 扫损区
        if direction == "做多":
            stop_loss_zone = [round(stop_loss_structure - 5, 2), round(stop_loss_standard + 3, 2)]
        elif direction == "做空":
            stop_loss_zone = [round(stop_loss_standard - 3, 2), round(stop_loss_structure + 5, 2)]
        else:
            stop_loss_zone = [round(stop_loss_standard - 5, 2), round(stop_loss_standard + 5, 2)]

        # 盈亏比
        risk = abs(entry_price - stop_loss_standard)
        reward = abs(tp1 - entry_price)
        rr_ratio = reward / risk if risk > 0 else 1.0

        self.logger.info("-" * 40)
        self.logger.info("【最终交易参数】")
        self.logger.info(f"  方向: {direction}")
        self.logger.info(f"  入场价: ${entry_price:.2f}")
        self.logger.info(f"  入场区间: ${entry_range[0]:.2f} - ${entry_range[1]:.2f}")
        self.logger.info(f"  激进止损: ${stop_loss_aggressive:.2f} (距离 {abs(entry_price - stop_loss_aggressive):.2f})")
        self.logger.info(f"  标准止损: ${stop_loss_standard:.2f} (距离 {abs(entry_price - stop_loss_standard):.2f})")
        self.logger.info(f"  结构止损: ${stop_loss_structure:.2f} (距离 {abs(entry_price - stop_loss_structure):.2f})")
        self.logger.info(f"  TP1: ${tp1:.2f} (距离 {abs(tp1 - entry_price):.2f})")
        self.logger.info(f"  TP2: ${tp2:.2f} (距离 {abs(tp2 - entry_price):.2f})")
        self.logger.info(f"  TP3: ${tp3:.2f} (距离 {abs(tp3 - entry_price):.2f})")
        self.logger.info(f"  盈亏比: 1:{rr_ratio:.2f}")
        self.logger.info("-" * 40)
        self.logger.info("")

        return {
            "direction": direction,
            "bias_reason": bias_reason[:100],
            "main_plan": main_plan[:200],
            "alternative_plan": "观望或反向突破追单",
            "entry_price": round(entry_price, 2),
            "entry_range": entry_range,
            "stop_loss": {
                "aggressive": round(stop_loss_aggressive, 2),
                "standard": round(stop_loss_standard, 2),
                "structure": round(stop_loss_structure, 2)
            },
            "take_profit": {
                "tp1": round(tp1, 2),
                "tp2": round(tp2, 2),
                "tp3": round(tp3, 2)
            },
            "stop_loss_zone": stop_loss_zone,
            "invalidation_condition": "价格反向突破结构止损位",
            "position_suggestion": position_suggestion,
            "risk_reward_ratio": round(rr_ratio, 2),
            "confidence_score": 70 if direction != "观望" else 30
        }

    def _extract_field(self, text: str, field_name: str, default: str = "") -> str:
        """从文本中提取字段"""
        lines = text.split('\n')
        for line in lines:
            if field_name in line and ':' in line:
                return line.split(':', 1)[1].strip()
            if field_name in line and '：' in line:
                return line.split('：', 1)[1].strip()
        return default

    def _extract_price(self, text: str) -> Optional[float]:
        """从文本中提取价格"""
        import re
        matches = re.findall(r'\$?(\d+\.?\d*)', text)
        if matches:
            try:
                return float(matches[0])
            except:
                pass
        return None

    def _generate_no_llm_advice(
        self,
        current_price: float,
        timeframe: str
    ) -> Dict[str, Any]:
        """没有 LLM 时返回提示"""
        return {
            "direction": "观望",
            "bias_reason": "LLM 未配置，无法生成详细建议",
            "main_plan": "请配置 LLM API 以获取交易建议",
            "alternative_plan": "等待 LLM 可用",
            "entry_price": current_price,
            "entry_range": [current_price * 0.995, current_price * 1.005],
            "stop_loss": {
                "aggressive": current_price * 0.98,
                "standard": current_price * 0.97,
                "structure": current_price * 0.95
            },
            "take_profit": {
                "tp1": current_price * 1.02,
                "tp2": current_price * 1.04,
                "tp3": current_price * 1.06
            },
            "stop_loss_zone": [current_price * 0.94, current_price * 0.96],
            "invalidation_condition": "请配置 LLM API",
            "position_suggestion": "观望",
            "risk_reward_ratio": 1.0,
            "confidence_score": 20
        }

    def _generate_error_advice(
        self,
        current_price: float,
        timeframe: str,
        error_msg: str
    ) -> Dict[str, Any]:
        """生成错误状态下的建议"""
        return {
            "direction": "观望",
            "bias_reason": f"生成失败: {error_msg[:30]}",
            "main_plan": "交易建议生成失败，请检查系统配置",
            "alternative_plan": "参考技术分析自行判断",
            "entry_price": current_price,
            "entry_range": [current_price * 0.995, current_price * 1.005],
            "stop_loss": {
                "aggressive": current_price * 0.98,
                "standard": current_price * 0.97,
                "structure": current_price * 0.95
            },
            "take_profit": {
                "tp1": current_price * 1.02,
                "tp2": current_price * 1.04,
                "tp3": current_price * 1.06
            },
            "stop_loss_zone": [current_price * 0.94, current_price * 0.96],
            "invalidation_condition": "系统错误",
            "position_suggestion": "观望",
            "risk_reward_ratio": 1.0,
            "confidence_score": 10
        }

    def to_dict(self, advice: Dict[str, Any]) -> Dict[str, Any]:
        """转换为标准格式（兼容现有代码）"""
        return advice
