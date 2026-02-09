"""
Telegram 通知推送模块

功能：
1. 使用 Telegram Bot API 发送消息
2. 支持 Markdown 格式
3. 支持长消息自动分批发送
4. 针对贵金属行情优化的消息格式
"""

import os
import time
import requests
from typing import Dict, Any, List
from loguru import logger


class TelegramNotifier:
    """Telegram 通知推送器"""

    # Telegram 消息长度限制
    MAX_MESSAGE_LENGTH = 4096
    MAX_CHUNK_LENGTH = 4000  # 分批发送时的块大小（预留一些空间）

    # 免责声明
    DISCLAIMER = "⚠️ AI生成，仅供参考，不构成投资建议"

    def __init__(self, bot_token: str = None, chat_id: str = None, timeout: int = 30):
        """
        初始化 Telegram 推送器

        Args:
            bot_token: Telegram Bot Token，不传则从环境变量读取
            chat_id: Chat ID，不传则从环境变量读取
            timeout: 请求超时时间
        """
        self.bot_token = bot_token or os.getenv('TELEGRAM_BOT_TOKEN', '')
        self.chat_id = chat_id or os.getenv('TELEGRAM_CHAT_ID', '')
        self.timeout = timeout
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"

        if not self.bot_token or not self.chat_id:
            logger.warning("Telegram Bot Token 或 Chat ID 未配置，推送功能将不可用")

    def is_available(self) -> bool:
        """检查 Telegram 推送是否可用"""
        return bool(self.bot_token and self.chat_id)

    def send_text(self, text: str) -> bool:
        """
        发送纯文本消息

        Args:
            text: 消息内容

        Returns:
            是否发送成功
        """
        if not self.is_available():
            logger.warning("Telegram Bot 配置未完整，跳过推送")
            return False

        url = f"{self.api_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text
        }

        return self._send_request(url, payload)

    def send_markdown(self, text: str) -> bool:
        """
        发送 Markdown 格式消息

        Args:
            text: Markdown 格式的消息内容

        Returns:
            是否发送成功
        """
        if not self.is_available():
            logger.warning("Telegram Bot 配置未完整，跳过推送")
            return False

        url = f"{self.api_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }

        return self._send_request(url, payload)

    def send_market_report(
        self,
        symbol_name: str,
        symbol: str,
        quote_data: Dict[str, Any],
        technical_data: Dict[str, Any],
        patterns: Dict[str, int] = None,
        llm_analysis: Dict[str, Any] = None
    ) -> bool:
        """
        发送市场分析报告（贵金属专用格式）

        Args:
            symbol_name: 品种名称
            symbol: 品种代码
            quote_data: 实时报价数据
            technical_data: 技术分析数据
            patterns: K线形态统计
            llm_analysis: LLM 分析结果

        Returns:
            是否发送成功
        """
        # 构建内容
        content = self._build_market_report_content(
            symbol_name, symbol, quote_data, technical_data, patterns, llm_analysis
        )

        # 添加标题和免责声明
        price = quote_data.get('price', 0) if quote_data else 0
        change_pct = quote_data.get('change_percent', 0) if quote_data else 0
        trend_icon = "🔺" if change_pct > 0 else ("🔻" if change_pct < 0 else "➖")

        header = f"*{trend_icon} {symbol_name} ${price:.2f} ({change_pct:+.2f}%)*\n"
        footer = f"\n{self.DISCLAIMER}\n_更新时间: {self._get_current_time()}_"

        full_content = header + content + footer

        # 如果内容过长，分批发送
        return self.send_chunked(full_content)

    def send_daily_summary(
        self,
        reports: List[Dict[str, Any]],
        gold_silver_ratio: float = None
    ) -> bool:
        """
        发送每日汇总报告

        Args:
            reports: 多个品种的分析报告列表
            gold_silver_ratio: 黄金白银比

        Returns:
            是否发送成功
        """
        content = self._build_daily_summary_content(reports, gold_silver_ratio)

        header = f"*📊 贵金属每日分析汇总 ({self._get_current_date()})*\n"
        footer = f"\n{self.DISCLAIMER}\n_更新时间: {self._get_current_time()}_"

        full_content = header + content + footer

        return self.send_chunked(full_content)

    def _get_current_time(self) -> str:
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def _get_current_date(self) -> str:
        """获取当前日期字符串"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d')

    def send_chunked(self, text: str, max_length: int = None) -> bool:
        """
        分批发送长消息

        Args:
            text: 完整内容
            max_length: 单条消息最大长度

        Returns:
            是否全部发送成功
        """
        if max_length is None:
            max_length = self.MAX_CHUNK_LENGTH

        if len(text) <= max_length:
            return self.send_markdown(text)

        # 按段落分割
        chunks = self._split_content(text, max_length)
        total_chunks = len(chunks)

        logger.info(f"Telegram 消息分批发送：共 {total_chunks} 批")

        success_count = 0
        for i, chunk in enumerate(chunks):
            chunk_header = f"*(第 {i + 1}/{total_chunks} 部分)*\n" if total_chunks > 1 else ""

            if self.send_markdown(chunk_header + chunk):
                success_count += 1
            else:
                logger.error(f"Telegram 第 {i + 1}/{total_chunks} 批发送失败")

            # 批次间间隔，避免触发限流
            if i < total_chunks - 1:
                time.sleep(1)

        return success_count == total_chunks

    def _split_content(self, content: str, max_length: int) -> List[str]:
        """按长度分割内容"""
        chunks = []
        current_chunk = ""

        # 按段落或分隔线分割
        if "\n---\n" in content:
            sections = content.split("\n---\n")
            separator = "\n---\n"
        elif "\n\n" in content:
            sections = content.split("\n\n")
            separator = "\n\n"
        else:
            sections = content.split("\n")
            separator = "\n"

        for section in sections:
            test_chunk = current_chunk + separator + section if current_chunk else section

            if len(test_chunk) > max_length and current_chunk:
                chunks.append(current_chunk)
                current_chunk = section
            else:
                current_chunk = test_chunk

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def _build_market_report_content(
        self,
        symbol_name: str,
        symbol: str,
        quote_data: Dict[str, Any],
        technical_data: Dict[str, Any],
        patterns: Dict[str, int] = None,
        llm_analysis: Dict[str, Any] = None
    ) -> str:
        """构建市场报告内容"""
        lines = []

        # === 行情概览 ===
        lines.append("📈 *实时行情*")
        if quote_data:
            price = quote_data.get('price', 0)
            change = quote_data.get('change', 0)
            change_pct = quote_data.get('change_percent', 0)
            high = quote_data.get('high', 0)
            low = quote_data.get('low', 0)
            open_price = quote_data.get('open', 0)

            lines.append("• 最新价: `${:.2f}`".format(price))
            lines.append("• 涨跌额: `{:+.2f}`".format(change))
            lines.append("• 涨跌幅: `{:+.2f}%`".format(change_pct))
            lines.append("• 今日区间: `${:.2f}` ~ `${:.2f}`".format(low, high))
            lines.append("• 开盘价: `${:.2f}`".format(open_price))
        else:
            lines.append("• 暂无行情数据")
        lines.append("")

        # === 技术指标 ===
        if technical_data:
            lines.append("📊 *技术指标*")

            trend = technical_data.get('trend', 'neutral')
            trend_text = {"bullish": "🔴 看涨", "bearish": "🟢 看跌", "neutral": "⚪ 中性"}.get(trend, "⚪ 中性")
            lines.append(f"• 趋势判断: {trend_text}")

            support = technical_data.get('support_levels', [])
            resistance = technical_data.get('resistance_levels', [])

            if support:
                support_str = ", ".join([f"${s:.2f}" if isinstance(s, (int, float)) else str(s) for s in support[:2]])
                lines.append(f"• 支撑位: {support_str}")

            if resistance:
                resistance_str = ", ".join([f"${r:.2f}" if isinstance(r, (int, float)) else str(r) for r in resistance[:2]])
                lines.append(f"• 阻力位: {resistance_str}")

            if 'rsi' in technical_data and technical_data['rsi'] is not None:
                rsi = technical_data['rsi']
                rsi_status = "超买" if rsi > 70 else ("超卖" if rsi < 30 else "正常")
                lines.append(f"• RSI(14): `{rsi:.1f}` ({rsi_status})")

            if 'macd_signal' in technical_data:
                macd_signal = technical_data['macd_signal']
                macd_text = "金叉 🔴" if macd_signal == 'bullish' else ("死叉 🟢" if macd_signal == 'bearish' else "震荡")
                lines.append(f"• MACD信号: {macd_text}")

            lines.append("")

        # === K线形态 ===
        if patterns:
            pattern_names = {
                'doji': '十字星',
                'hammer': '锤子线',
                'shooting_star': '射击之星',
                'engulfing_bullish': '看涨吞噬',
                'engulfing_bearish': '看跌吞噬',
                'morning_star': '启明星',
                'evening_star': '黄昏星',
                'three_white_soldiers': '三白兵',
                'three_black_crows': '三黑鸦'
            }

            has_patterns = False
            pattern_lines = []
            for pattern_key, pattern_data in patterns.items():
                if isinstance(pattern_data, list):
                    count = len(pattern_data)
                elif isinstance(pattern_data, (int, float)):
                    count = int(pattern_data)
                else:
                    count = 0

                if count > 0:
                    has_patterns = True
                    name = pattern_names.get(pattern_key, pattern_key)
                    pattern_lines.append(f"• {name}: {count}次")

            if has_patterns:
                lines.append("🕯️ *K线形态识别*")
                lines.extend(pattern_lines)
                lines.append("")

        # === LLM 分析 ===
        if llm_analysis:
            analysis_content = llm_analysis.get('analysis', {})

            if isinstance(analysis_content, dict):
                lines.append("🤖 *AI 智能分析*")

                if analysis_content.get('trend'):
                    trend_icon = "🔴" if analysis_content['trend'] in ['看涨', 'bullish'] else (
                        "🟢" if analysis_content['trend'] in ['看跌', 'bearish'] else "⚪"
                    )
                    lines.append(f"• 趋势判断: {trend_icon} {analysis_content['trend']}")

                if analysis_content.get('summary'):
                    lines.append(f"• 分析概要: {analysis_content['summary'][:200]}")

                if analysis_content.get('key_levels'):
                    lines.append(f"• 关键点位: {analysis_content['key_levels']}")

                if analysis_content.get('risk_level'):
                    risk_icon = {"低": "🟢", "中": "🟡", "高": "🔴"}.get(analysis_content['risk_level'], "⚪")
                    lines.append(f"• 风险等级: {risk_icon} {analysis_content['risk_level']}")

                lines.append("")

                if analysis_content.get('suggestion'):
                    suggestion = analysis_content['suggestion']
                    if len(suggestion) > 300:
                        suggestion = suggestion[:300] + "..."
                    lines.append("💡 *操作建议*")
                    lines.append(suggestion)
                    lines.append("")

            elif isinstance(analysis_content, str) and analysis_content:
                lines.append("🤖 *AI 智能分析*")
                if len(analysis_content) > 500:
                    analysis_content = analysis_content[:500] + "..."
                lines.append(analysis_content)
                lines.append("")

            elif llm_analysis.get('recommendation'):
                lines.append(f"💡 *操作建议*: {llm_analysis['recommendation']}")
                lines.append("")

        return "\n".join(lines)

    def _build_daily_summary_content(
        self,
        reports: List[Dict[str, Any]],
        gold_silver_ratio: float = None
    ) -> str:
        """构建每日汇总内容"""
        lines = []

        if gold_silver_ratio:
            lines.append("⚖️ *黄金白银比*")
            ratio_status = "白银相对强势" if gold_silver_ratio < 60 else ("黄金相对强势" if gold_silver_ratio > 80 else "正常区间")
            lines.append("• 当前比值: *{:.1f}*".format(gold_silver_ratio))
            lines.append("• 历史均值: 60-70")
            lines.append(f"• 研判: {ratio_status}")
            lines.append("")
            lines.append("---")
            lines.append("")

        for report in reports:
            symbol_name = report.get('symbol_name', '')
            symbol = report.get('symbol', '')
            quote = report.get('quote_data', {})
            technical = report.get('technical_data', {})

            price = quote.get('price', 0)
            change_pct = quote.get('change_percent', 0)
            trend = technical.get('trend', 'neutral')

            trend_icon = "🔺" if change_pct > 0 else ("🔻" if change_pct < 0 else "➖")
            trend_text = {"bullish": "看涨", "bearish": "看跌", "neutral": "震荡"}.get(trend, "震荡")

            lines.append("*{} {} ({})*".format(trend_icon, symbol_name, symbol))
            lines.append("• 价格: `${:.2f}` (`{:+.2f}%`)".format(price, change_pct))
            lines.append(f"• 趋势: {trend_text}")

            support = technical.get('support_levels', [])
            resistance = technical.get('resistance_levels', [])
            if support:
                lines.append("• 支撑: `${:.2f}`".format(support[0]) if isinstance(support[0], (int, float)) else f"• 支撑: {support[0]}")
            if resistance:
                lines.append("• 阻力: `${:.2f}`".format(resistance[0]) if isinstance(resistance[0], (int, float)) else f"• 阻力: {resistance[0]}")

            lines.append("")

        return "\n".join(lines)

    def _send_request(self, url: str, payload: Dict[str, Any]) -> bool:
        """发送请求到 Telegram Bot API"""
        try:
            response = requests.post(
                url,
                json=payload,
                timeout=self.timeout,
                headers={
                    "Content-Type": "application/json"
                }
            )

            if response.status_code == 200:
                result = response.json()

                if result.get('ok'):
                    logger.info("Telegram 消息发送成功")
                    return True
                else:
                    error_msg = result.get('description', '未知错误')
                    logger.error(f"Telegram 返回错误: {error_msg}")
                    return False
            else:
                logger.error(f"Telegram 请求失败: HTTP {response.status_code}")
                logger.debug(f"响应内容: {response.text}")
                return False

        except requests.exceptions.Timeout:
            logger.error("Telegram 请求超时")
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Telegram 请求异常: {e}")
            return False
