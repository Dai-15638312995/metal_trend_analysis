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
            technical_data: 技术指标数据（备用）
            support_levels: 支撑位列表（备用）
            resistance_levels: 阻力位列表（备用）
            current_price: 当前价格
            timeframe: 时间周期
            multi_timeframe_data: 多时间周期K线数据字典

        Returns:
            交易建议字典
        """
        try:
            self.logger.info("=" * 80)
            self.logger.info("【generate_advice 入参】")
            self.logger.info("=" * 80)
            self.logger.info(f"current_price: {current_price}")
            self.logger.info(f"timeframe: {timeframe}")
            self.logger.info(f"kline_data shape: {kline_data.shape if kline_data is not None else None}")
            self.logger.info(f"multi_timeframe_data keys: {list(multi_timeframe_data.keys()) if multi_timeframe_data else None}")
            self.logger.info("=" * 80)

            # 如果有 LLM 分析器，使用 AI 生成建议
            if self.llm_analyzer:
                result = self._generate_advice_with_llm(
                    kline_data, current_price, timeframe, multi_timeframe_data
                )
                self.logger.info("=" * 80)
                self.logger.info("【generate_advice 出参】")
                self.logger.info("=" * 80)
                self.logger.info(f"result: {result}")
                self.logger.info("=" * 80)
                return result
            else:
                result = self._generate_no_llm_advice(current_price, timeframe)
                return result

        except Exception as e:
            self.logger.error(f"生成交易建议失败: {e}")
            return self._generate_error_advice(current_price, timeframe, str(e))

    def _generate_advice_with_llm(
        self,
        kline_data: pd.DataFrame,
        current_price: float,
        timeframe: str,
        multi_timeframe_data: Dict[str, pd.DataFrame] = None
    ) -> Dict[str, Any]:
        """使用 LLM AI 生成交易建议 - 直接传递原始K线数据"""
        try:
            self.logger.info("=" * 60)
            self.logger.info("【交易建议生成开始】")
            self.logger.info(f"当前价格: ${current_price:.2f}")
            self.logger.info("=" * 60)

            # 构建提示词 - 直接传递原始K线数据
            self.logger.info("【步骤1】构建 AI 提示词（原始K线数据）...")
            prompt = self._build_prompt_with_raw_data(
                kline_data, current_price, timeframe, multi_timeframe_data
            )

            # 打印完整提示词
            self.logger.info("-" * 60)
            self.logger.info("【发送给 AI 的提示词】:")
            self.logger.info("-" * 60)
            # 限制日志长度
            prompt_lines = prompt.split('\n')
            for i, line in enumerate(prompt_lines[:100]):
                self.logger.info(f"  {line}")
            if len(prompt_lines) > 100:
                self.logger.info(f"  ... ({len(prompt_lines) - 100} more lines)")
            self.logger.info("-" * 60)

            # 调用 LLM
            self.logger.info("【步骤2】调用通义千问 AI...")
            response = self.llm_analyzer.client.chat.completions.create(
                model=self.llm_analyzer.model,
                messages=[
                    {
                        "role": "system",
                        "content": """你是一位专业的量化交易分析师，精通技术分析和Python pandas数据分析。

你的任务是：
1. 基于提供的原始K线数据，自行计算技术指标（MA、MACD、RSI、布林带等）
2. 分析多周期趋势一致性
3. 找出关键支撑阻力位
4. 给出具体的交易建议

分析要求：
- 使用pandas计算技术指标
- 大周期（日线/4小时）定方向
- 中周期（1小时）找位置
- 小周期（15/30分钟）精确入场
- 多周期共振时信号最强
- 必须基于实际数据计算，禁止虚构价格

输出必须包含具体的入场价位、止损、目标位和理由。"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,
                max_tokens=2000
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
            self.logger.info("【步骤3】解析 AI 响应...")
            advice = self._parse_llm_response_v2(llm_response, current_price)

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

    def _build_prompt_with_raw_data(
        self,
        kline_data: pd.DataFrame,
        current_price: float,
        timeframe: str,
        multi_timeframe_data: Dict[str, pd.DataFrame] = None
    ) -> str:
        """构建提示词 - 直接传递原始K线数据"""
        lines = []

        lines.append("## 交易分析任务")
        lines.append("")
        lines.append("请基于以下原始K线数据进行技术分析，并给出交易建议。")
        lines.append("")

        # 当前价格
        lines.append(f"### 当前价格: ${current_price:.2f}")
        lines.append("")

        # 主时间周期K线数据
        lines.append(f"### 主时间周期 ({timeframe}) K线数据")
        lines.append("```csv")
        lines.append(kline_data.tail(30).to_csv())  # 最近30根K线
        lines.append("```")
        lines.append("")

        # 多时间周期K线数据
        if multi_timeframe_data:
            lines.append("### 多时间周期K线数据（用于多周期分析）")
            lines.append("")

            timeframe_names = {
                '5m': '5分钟',
                '15m': '15分钟',
                '30m': '30分钟',
                '1h': '1小时',
                '4h': '4小时',
                '1d': '日线'
            }

            for tf, df in multi_timeframe_data.items():
                if df is not None and not df.empty:
                    tf_name = timeframe_names.get(tf, tf)
                    lines.append(f"#### {tf_name} ({tf}) - 最近10根K线")
                    lines.append("```csv")
                    lines.append(df.tail(10).to_csv())
                    lines.append("```")
                    lines.append("")

        # 分析要求
        lines.append("### 分析要求")
        lines.append("")
        lines.append("请基于以上K线数据：")
        lines.append("1. **计算技术指标**：MA(5,10,20,60)、MACD、RSI(14)、布林带")
        lines.append("2. **判断趋势方向**：日线/4小时定方向，小周期确认")
        lines.append("3. **找出支撑阻力位**：基于近期高低点")
        lines.append("4. **评估多周期一致性**：各周期趋势是否共振")
        lines.append("5. **给出交易建议**：具体入场、止损、目标位")
        lines.append("")

        # 输出格式要求
        lines.append("### 输出格式（纯文本）")
        lines.append("""
方向: 做多/做空/观望
理由: [基于技术指标的详细分析，包括计算出的MA、MACD、RSI值]
入场: [具体入场价位和分析]
止损: [止损价位]
目标1: [第一目标位]
目标2: [第二目标位]
目标3: [第三目标位]
仓位: [轻仓/标准/重仓]
风险: [高/中/低]

### 技术指标计算结果（可选）
- MA5: [值]
- MA10: [值]
- MA20: [值]
- MA60: [值]
- MACD: [金叉/死叉/多头/空头]
- RSI: [值]
- 布林带: [上轨/中轨/下轨]
""")

        return "\n".join(lines)

    def _parse_llm_response_v2(
        self,
        response: str,
        current_price: float
    ) -> Dict[str, Any]:
        """解析 LLM 响应（简化版）"""

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
        bias_reason = self._extract_field(response, "理由", "基于技术分析")
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

        # 提取入场价
        entry_text = self._extract_field(response, "入场", "")
        entry_price = self._extract_price(entry_text)

        # 如果没有提取到入场价，使用当前价
        if not entry_price:
            entry_price = current_price
            self.logger.info(f"  未解析到入场价，使用当前价: ${entry_price:.2f}")
        else:
            self.logger.info(f"  解析入场价: ${entry_price:.2f}")

        self.logger.info("-" * 40)

        # 根据方向生成默认止损和目标
        if direction == "做多":
            if not stop_loss_standard or stop_loss_standard >= entry_price:
                stop_loss_standard = entry_price * 0.995  # 默认0.5%止损
            if not tp1 or tp1 <= entry_price:
                tp1 = entry_price * 1.01  # 默认1%目标1
            if not tp2 or tp2 <= entry_price:
                tp2 = entry_price * 1.02  # 默认2%目标2
            if not tp3 or tp3 <= entry_price:
                tp3 = entry_price * 1.03  # 默认3%目标3
        elif direction == "做空":
            if not stop_loss_standard or stop_loss_standard <= entry_price:
                stop_loss_standard = entry_price * 1.005  # 默认0.5%止损
            if not tp1 or tp1 >= entry_price:
                tp1 = entry_price * 0.99  # 默认1%目标1
            if not tp2 or tp2 >= entry_price:
                tp2 = entry_price * 0.98  # 默认2%目标2
            if not tp3 or tp3 >= entry_price:
                tp3 = entry_price * 0.97  # 默认3%目标3
        else:
            # 观望
            stop_loss_standard = entry_price * 0.995
            tp1 = entry_price * 1.01
            tp2 = entry_price * 1.02
            tp3 = entry_price * 1.03

        # 计算止损距离和盈亏比
        stop_distance = abs(entry_price - stop_loss_standard)
        tp1_distance = abs(tp1 - entry_price)
        risk_reward_ratio = tp1_distance / stop_distance if stop_distance > 0 else 0

        self.logger.info("-" * 40)
        self.logger.info("【最终交易参数】")
        self.logger.info(f"  方向: {direction}")
        self.logger.info(f"  入场价: ${entry_price:.2f}")
        self.logger.info(f"  入场区间: ${entry_price - 5:.2f} - ${entry_price + 5:.2f}")
        self.logger.info(f"  激进止损: ${entry_price - stop_distance * 0.5:.2f} (距离 {stop_distance * 0.5:.2f})")
        self.logger.info(f"  标准止损: ${stop_loss_standard:.2f} (距离 {stop_distance:.2f})")
        self.logger.info(f"  结构止损: ${entry_price - stop_distance * 1.5:.2f} (距离 {stop_distance * 1.5:.2f})")
        self.logger.info(f"  TP1: ${tp1:.2f} (距离 {tp1_distance:.2f})")
        self.logger.info(f"  TP2: ${tp2:.2f} (距离 {abs(tp2 - entry_price):.2f})")
        self.logger.info(f"  TP3: ${tp3:.2f} (距离 {abs(tp3 - entry_price):.2f})")
        self.logger.info(f"  盈亏比: 1:{risk_reward_ratio:.2f}")
        self.logger.info("-" * 40)

        return {
            'direction': direction,
            'bias_reason': bias_reason,
            'main_plan': main_plan,
            'alternative_plan': '观望或反向突破追单',
            'entry_price': round(entry_price, 2),
            'entry_range': [round(entry_price - 5, 2), round(entry_price + 5, 2)],
            'stop_loss': {
                'aggressive': round(entry_price - stop_distance * 0.5, 2) if direction == "做多" else round(entry_price + stop_distance * 0.5, 2),
                'standard': round(stop_loss_standard, 2),
                'structure': round(entry_price - stop_distance * 1.5, 2) if direction == "做多" else round(entry_price + stop_distance * 1.5, 2)
            },
            'take_profit': {
                'tp1': round(tp1, 2),
                'tp2': round(tp2, 2),
                'tp3': round(tp3, 2)
            },
            'stop_loss_zone': [
                round(stop_loss_standard - stop_distance * 0.3, 2),
                round(stop_loss_standard + stop_distance * 0.3, 2)
            ],
            'invalidation_condition': '价格反向突破结构止损位',
            'position_suggestion': position_suggestion if position_suggestion in ['轻仓', '标准', '重仓'] else '标准',
            'risk_reward_ratio': round(risk_reward_ratio, 2),
            'confidence_score': 70
        }

    def _extract_field(self, text: str, field_name: str, default: str = "") -> str:
        """从文本中提取字段值"""
        import re
        patterns = [
            rf'{field_name}[：:]\s*(.+?)(?=\n|$)',
            rf'{field_name}\s*[:：]\s*(.+?)(?=\n|目标|止损|入场|方向|仓位|风险|$)'
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        return default

    def _extract_price(self, text: str) -> Optional[float]:
        """从文本中提取价格"""
        import re
        if not text:
            return None
        # 匹配 $1234.56 或 1234.56
        match = re.search(r'\$?(\d{3,5}\.\d{1,2})', text)
        if match:
            return float(match.group(1))
        return None

    def _generate_no_llm_advice(self, current_price: float, timeframe: str) -> Dict[str, Any]:
        """无 LLM 时的默认建议"""
        return {
            'direction': '观望',
            'bias_reason': 'LLM 分析器未配置，无法生成建议',
            'main_plan': '请配置 LLM API',
            'alternative_plan': '手动分析',
            'entry_price': round(current_price, 2),
            'entry_range': [round(current_price - 5, 2), round(current_price + 5, 2)],
            'stop_loss': {
                'aggressive': round(current_price * 0.99, 2),
                'standard': round(current_price * 0.985, 2),
                'structure': round(current_price * 0.98, 2)
            },
            'take_profit': {
                'tp1': round(current_price * 1.01, 2),
                'tp2': round(current_price * 1.02, 2),
                'tp3': round(current_price * 1.03, 2)
            },
            'stop_loss_zone': [round(current_price * 0.98, 2), round(current_price * 0.995, 2)],
            'invalidation_condition': 'LLM 未配置',
            'position_suggestion': '观望',
            'risk_reward_ratio': 0,
            'confidence_score': 0
        }

    def _generate_error_advice(self, current_price: float, timeframe: str, error_msg: str) -> Dict[str, Any]:
        """错误时的默认建议"""
        return {
            'direction': '观望',
            'bias_reason': f'分析出错: {error_msg}',
            'main_plan': '请检查系统配置',
            'alternative_plan': '稍后重试',
            'entry_price': round(current_price, 2),
            'entry_range': [round(current_price - 5, 2), round(current_price + 5, 2)],
            'stop_loss': {
                'aggressive': round(current_price * 0.99, 2),
                'standard': round(current_price * 0.985, 2),
                'structure': round(current_price * 0.98, 2)
            },
            'take_profit': {
                'tp1': round(current_price * 1.01, 2),
                'tp2': round(current_price * 1.02, 2),
                'tp3': round(current_price * 1.03, 2)
            },'stop_loss_zone': [round(current_price * 0.98, 2), round(current_price * 0.995, 2)],
            'invalidation_condition': f'错误: {error_msg}',
            'position_suggestion': '观望',
            'risk_reward_ratio': 0,
            'confidence_score': 0
        }
