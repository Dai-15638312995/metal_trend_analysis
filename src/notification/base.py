"""
Base notifier class for standardized notification interface.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from loguru import logger

from ..utils.exceptions import NotificationError, ValidationError


class BaseNotifier(ABC):
    """Base class for all notification services."""

    def __init__(self, timeout: int = 30, **kwargs):
        """
        Initialize base notifier.

        Args:
            timeout: Request timeout in seconds
            **kwargs: Additional configuration parameters
        """
        self.timeout = timeout
        self.logger = logger.bind(name=self.__class__.__name__)
        self._validate_config(**kwargs)

    @abstractmethod
    def _validate_config(self, **kwargs) -> None:
        """
        Validate notifier-specific configuration.

        Raises:
            ValidationError: If configuration is invalid
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the notifier is properly configured and available.

        Returns:
            True if notifier is available, False otherwise
        """
        pass

    @abstractmethod
    def _send_message(self, message: str, **kwargs) -> bool:
        """
        Send a raw message through the notification service.

        Args:
            message: Message content to send
            **kwargs: Additional service-specific parameters

        Returns:
            True if message was sent successfully, False otherwise

        Raises:
            NotificationError: If sending fails
        """
        pass

    def send_text(self, text: str) -> bool:
        """
        Send a plain text message.

        Args:
            text: Text message to send

        Returns:
            True if sent successfully, False otherwise
        """
        if not self.is_available():
            self.logger.warning(f"{self.__class__.__name__} is not available, skipping notification")
            return False

        try:
            return self._send_message(text)
        except Exception as e:
            self.logger.error(f"Failed to send text message: {e}")
            return False

    def send_daily_summary(self, reports: List[Dict[str, Any]], gold_silver_ratio: Optional[float] = None) -> bool:
        """
        Send daily analysis summary.

        Args:
            reports: List of analysis reports
            gold_silver_ratio: Gold-silver ratio if available

        Returns:
            True if sent successfully, False otherwise
        """
        try:
            summary = self._format_daily_summary(reports, gold_silver_ratio)
            return self.send_text(summary)
        except Exception as e:
            self.logger.error(f"Failed to send daily summary: {e}")
            return False

    def send_market_report(
        self,
        symbol_name: str,
        symbol: str,
        quote_data: Dict[str, Any],
        technical_data: Dict[str, Any],
        patterns: Optional[Dict[str, Any]] = None,
        llm_analysis: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Send detailed market analysis report.

        Args:
            symbol_name: Human-readable symbol name
            symbol: Trading symbol
            quote_data: Real-time quote data
            technical_data: Technical analysis results
            patterns: Candlestick patterns
            llm_analysis: LLM analysis results

        Returns:
            True if sent successfully, False otherwise
        """
        try:
            report = self._format_market_report(
                symbol_name, symbol, quote_data, technical_data, patterns, llm_analysis
            )
            return self.send_text(report)
        except Exception as e:
            self.logger.error(f"Failed to send market report for {symbol}: {e}")
            return False

    def _format_daily_summary(self, reports: List[Dict[str, Any]], gold_silver_ratio: Optional[float]) -> str:
        """
        Format daily summary message.

        Args:
            reports: List of analysis reports
            gold_silver_ratio: Gold-silver ratio if available

        Returns:
            Formatted summary message
        """
        try:
            lines = ["📊 贵金属市场日报"]
            lines.append("=" * 30)

            for report in reports:
                quote = report.get('quote_data', {})
                price = quote.get('price', 0)
                change = quote.get('change', 0)
                change_percent = quote.get('change_percent', 0)

                change_emoji = "📈" if change >= 0 else "📉"
                change_sign = "+" if change >= 0 else ""

                lines.append(f"{change_emoji} {report.get('symbol_name', 'Unknown')}")
                lines.append(f"  价格: ${price:.2f}")
                lines.append(f"  涨跌: {change_sign}{change:.2f} ({change_sign}{change_percent:.2f}%)")

                # Add trend if available
                technical = report.get('technical_data', {})
                trend = technical.get('trend', 'N/A')
                if trend != 'N/A':
                    lines.append(f"  趋势: {trend}")

                lines.append("")

            # Add gold-silver ratio
            if gold_silver_ratio:
                lines.append(f"💎 金银比: {gold_silver_ratio:.1f}")
                if gold_silver_ratio < 60:
                    lines.append("   白银表现强劲")
                elif gold_silver_ratio > 70:
                    lines.append("   黄金表现强劲")
                else:
                    lines.append("   金银比正常范围")

            lines.append("")
            lines.append("⚠️ AI生成，仅供参考，不构成投资建议")

            return "\n".join(lines)

        except Exception as e:
            self.logger.error(f"Error formatting daily summary: {e}")
            return "贵金属市场日报（格式化失败）"

    def _format_market_report(
        self,
        symbol_name: str,
        symbol: str,
        quote_data: Dict[str, Any],
        technical_data: Dict[str, Any],
        patterns: Optional[Dict[str, Any]] = None,
        llm_analysis: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Format detailed market report.

        Args:
            symbol_name: Human-readable symbol name
            symbol: Trading symbol
            quote_data: Real-time quote data
            technical_data: Technical analysis results
            patterns: Candlestick patterns
            llm_analysis: LLM analysis results

        Returns:
            Formatted report message
        """
        try:
            lines = [f"📊 {symbol_name} ({symbol}) 分析报告"]
            lines.append("=" * 40)

            # Price information
            price = quote_data.get('price', 0)
            change = quote_data.get('change', 0)
            change_percent = quote_data.get('change_percent', 0)
            change_sign = "+" if change >= 0 else ""

            lines.append("💰 价格信息")
            lines.append(f"  当前价格: ${price:.2f}")
            lines.append(f"  涨跌幅: {change_sign}{change:.2f} ({change_sign}{change_percent:.2f}%)")

            # Technical analysis
            trend = technical_data.get('trend', 'N/A')
            if trend != 'N/A':
                lines.append("")
                lines.append("📈 技术分析")
                lines.append(f"  趋势方向: {trend}")

            # Support and resistance
            support_levels = technical_data.get('support_levels', [])
            resistance_levels = technical_data.get('resistance_levels', [])

            if support_levels or resistance_levels:
                lines.append("")
                lines.append("🎯 关键点位")
                if resistance_levels:
                    lines.append(f"  阻力位: ${resistance_levels[0]:.2f}")
                if support_levels:
                    lines.append(f"  支撑位: ${support_levels[0]:.2f}")

            # LLM analysis
            if llm_analysis and not llm_analysis.get('error'):
                analysis = llm_analysis.get('analysis', {})
                if analysis:
                    lines.append("")
                    lines.append("🤖 AI分析")

                    ai_trend = analysis.get('trend', '')
                    if ai_trend:
                        lines.append(f"  趋势判断: {ai_trend}")

                    suggestion = analysis.get('suggestion', '')
                    if suggestion:
                        lines.append(f"  交易建议: {suggestion}")

                    risk = analysis.get('risk_level', '')
                    if risk:
                        lines.append(f"  风险等级: {risk}")

            lines.append("")
            lines.append("⚠️ AI生成，仅供参考，不构成投资建议")

            return "\n".join(lines)

        except Exception as e:
            self.logger.error(f"Error formatting market report: {e}")
            return f"{symbol_name} 市场报告（格式化失败）"

    def _truncate_message(self, message: str, max_length: int) -> str:
        """
        Truncate message if it exceeds maximum length.

        Args:
            message: Original message
            max_length: Maximum allowed length

        Returns:
            Truncated message with ellipsis if needed
        """
        if len(message.encode('utf-8')) <= max_length:
            return message

        # Try to truncate at word boundaries
        lines = message.split('\n')
        truncated_lines = []
        current_length = 0

        for line in lines:
            line_bytes = len(line.encode('utf-8'))
            if current_length + line_bytes + 10 > max_length:  # Leave room for ellipsis
                truncated_lines.append("...")
                break
            truncated_lines.append(line)
            current_length += line_bytes + 1  # +1 for newline

        return '\n'.join(truncated_lines)