"""
邮件通知推送模块

功能：
1. 使用 SMTP 协议发送邮件
2. 支持 HTML 格式邮件
3. 自动检测常见邮件服务商的 SMTP 配置
4. 支持多个收件人
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr, formatdate
from typing import Dict, Any, List, Optional
from loguru import logger


class EmailNotifier:
    """邮件通知推送器"""

    # 常见邮件服务商的 SMTP 配置（自动检测）
    SMTP_CONFIGS = {
        'gmail.com': {
            'host': 'smtp.gmail.com',
            'port': 587,
            'use_ssl': False,
            'use_tls': True
        },
        'qq.com': {
            'host': 'smtp.qq.com',
            'port': 587,
            'use_ssl': False,
            'use_tls': True
        },
        '163.com': {
            'host': 'smtp.163.com',
            'port': 465,
            'use_ssl': True,
            'use_tls': False
        },
        '126.com': {
            'host': 'smtp.126.com',
            'port': 465,
            'use_ssl': True,
            'use_tls': False
        },
        'outlook.com': {
            'host': 'smtp-mail.outlook.com',
            'port': 587,
            'use_ssl': False,
            'use_tls': True
        },
        'hotmail.com': {
            'host': 'smtp-mail.outlook.com',
            'port': 587,
            'use_ssl': False,
            'use_tls': True
        },
        'live.com': {
            'host': 'smtp-mail.outlook.com',
            'port': 587,
            'use_ssl': False,
            'use_tls': True
        },
        'sina.cn': {
            'host': 'smtp.sina.cn',
            'port': 465,
            'use_ssl': True,
            'use_tls': False
        },
        'sina.com': {
            'host': 'smtp.sina.com',
            'port': 465,
            'use_ssl': True,
            'use_tls': False
        },
        'sohu.com': {
            'host': 'smtp.sohu.com',
            'port': 465,
            'use_ssl': True,
            'use_tls': False
        },
        'aliyun.com': {
            'host': 'smtp.aliyun.com',
            'port': 465,
            'use_ssl': True,
            'use_tls': False
        },
        'yandex.com': {
            'host': 'smtp.yandex.com',
            'port': 465,
            'use_ssl': True,
            'use_tls': False
        },
        'icloud.com': {
            'host': 'smtp.mail.me.com',
            'port': 587,
            'use_ssl': False,
            'use_tls': True
        },
        '189.cn': {
            'host': 'smtp.189.cn',
            'port': 465,
            'use_ssl': True,
            'use_tls': False
        }
    }

    # 免责声明
    DISCLAIMER = "⚠️ AI生成，仅供参考，不构成投资建议"

    def __init__(
        self,
        from_email: str = None,
        password: str = None,
        to_email: str = None,
        smtp_server: str = None,
        smtp_port: int = None,
        use_ssl: bool = None,
        use_tls: bool = None,
        timeout: int = 30
    ):
        """
        初始化邮件推送器

        Args:
            from_email: 发件人邮箱地址
            password: 邮箱密码或授权码
            to_email: 收件人邮箱地址（多个用逗号分隔）
            smtp_server: SMTP 服务器地址（可选，自动检测）
            smtp_port: SMTP 端口（可选，自动检测）
            use_ssl: 是否使用 SSL（可选，自动检测）
            use_tls: 是否使用 TLS（可选，自动检测）
            timeout: 请求超时时间
        """
        # 从环境变量读取配置
        self.from_email = from_email
        self.password = password
        self.to_email = to_email or ""
        self.smtp_config = self._detect_smtp_config(from_email)
        self.timeout = timeout

        # 如果提供了自定义配置，覆盖自动检测的配置
        if smtp_server:
            self.smtp_config['host'] = smtp_server
        if smtp_port:
            self.smtp_config['port'] = smtp_port
        if use_ssl is not None:
            self.smtp_config['use_ssl'] = use_ssl
        if use_tls is not None:
            self.smtp_config['use_tls'] = use_tls

        if not self.from_email or not self.password:
            logger.warning("邮件配置未完整，邮件推送功能将不可用")

    def _detect_smtp_config(self, email: str) -> Dict[str, Any]:
        """
        根据邮箱地址自动检测 SMTP 配置

        Args:
            email: 邮箱地址

        Returns:
            SMTP 配置字典
        """
        if not email:
            return {
                'host': None,
                'port': 587,
                'use_ssl': False,
                'use_tls': True
            }

        # 提取域名
        domain = email.split('@')[-1].lower()

        # 查找预定义配置
        if domain in self.SMTP_CONFIGS:
            config = self.SMTP_CONFIGS[domain].copy()
            logger.info(f"自动检测到邮箱服务商: {domain}")
            return config

        # 默认配置
        logger.warning(f"未识别的邮箱服务商: {domain}，使用默认 SMTP 配置")
        return {
            'host': None,
            'port': 587,
            'use_ssl': False,
            'use_tls': True
        }

    def is_available(self) -> bool:
        """检查邮件推送是否可用"""
        return bool(self.from_email and self.password and self.to_email and self.smtp_config['host'])

    def send_html(self, subject: str, html_content: str) -> bool:
        """
        发送 HTML 格式邮件

        Args:
            subject: 邮件主题
            html_content: HTML 内容

        Returns:
            是否发送成功
        """
        if not self.is_available():
            logger.warning("邮件配置未完整，跳过邮件推送")
            return False

        try:
            # 创建邮件对象
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = formataddr(('Metal Trend Analysis', self.from_email))
            msg['Date'] = formatdate(localtime=True)

            # 添加收件人（支持多个）
            to_emails = [email.strip() for email in self.to_email.split(',') if email.strip()]
            msg['To'] = ', '.join(to_emails)

            # 添加 HTML 内容
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)

            # 连接 SMTP 服务器
            smtp_class = smtplib.SMTP_SSL if self.smtp_config['use_ssl'] else smtplib.SMTP
            smtp = smtp_class(
                self.smtp_config['host'],
                self.smtp_config['port'],
                timeout=self.timeout
            )

            # 启用 TLS（如果配置）
            if self.smtp_config['use_tls']:
                smtp.starttls()

            # 登录
            smtp.login(self.from_email, self.password)

            # 发送邮件
            smtp.sendmail(self.from_email, to_emails, msg.as_string())

            # 关闭连接
            smtp.quit()

            logger.info("邮件发送成功")
            return True

        except smtplib.SMTPAuthenticationError:
            logger.error("邮件发送失败: 认证错误，请检查邮箱和密码（可能是需要授权码）")
            return False
        except smtplib.SMTPRecipientsRefused:
            logger.error("邮件发送失败: 收件人地址无效")
            return False
        except smtplib.SMTPServerDisconnected:
            logger.error("邮件发送失败: SMTP 服务器断开连接")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"邮件发送失败: SMTP 错误 - {str(e)}")
            return False
        except Exception as e:
            logger.error(f"邮件发送失败: {str(e)}")
            return False

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
        发送市场分析报告邮件

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
        subject = f"📊 {symbol_name} 分析报告 - {self._get_current_time()}"

        html_content = self._build_html_report(
            symbol_name, symbol, quote_data, technical_data, patterns, llm_analysis
        )

        return self.send_html(subject, html_content)

    def send_daily_summary(
        self,
        reports: List[Dict[str, Any]],
        gold_silver_ratio: float = None
    ) -> bool:
        """
        发送每日汇总报告邮件

        Args:
            reports: 多个品种的分析报告列表
            gold_silver_ratio: 黄金白银比

        Returns:
            是否发送成功
        """
        subject = f"📊 贵金属每日分析汇总 - {self._get_current_time()}"

        html_content = self._build_html_summary(reports, gold_silver_ratio)

        return self.send_html(subject, html_content)

    def _get_current_time(self) -> str:
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M')

    def _build_html_report(
        self,
        symbol_name: str,
        symbol: str,
        quote_data: Dict[str, Any],
        technical_data: Dict[str, Any],
        patterns: Dict[str, int] = None,
        llm_analysis: Dict[str, Any] = None
    ) -> str:
        """构建 HTML 格式的市场报告"""
        # 构建市场报告内容
        content_lines = self._build_market_report_content(
            symbol_name, symbol, quote_data, technical_data, patterns, llm_analysis
        )

        # 转换 Markdown 为 HTML（简化版）
        html_lines = []
        for line in content_lines.split('\n'):
            if line.startswith('**'):
                # 标题
                text = line.replace('**', '').strip()
                html_lines.append(f'<h3>{text}</h3>')
            elif line.startswith('•'):
                # 列表项
                text = line.replace('•', '').strip()
                # 处理加粗标记
                text = text.replace('**', '<strong>').replace('**', '</strong>')
                html_lines.append(f'<p>{text}</p>')
            elif line.strip() == '':
                html_lines.append('<br/>')
            else:
                text = line.replace('**', '<strong>').replace('**', '</strong>')
                html_lines.append(f'<p>{text}</p>')

        html_content = '\n'.join(html_lines)

        # 添加免责声明
        disclaimer = f'<p style="color: #888; font-size: 12px;">{self.DISCLAIMER}</p>'

        return self._wrap_html(html_content + disclaimer, symbol_name)

    def _build_html_summary(
        self,
        reports: List[Dict[str, Any]],
        gold_silver_ratio: float = None
    ) -> str:
        """构建 HTML 格式的每日汇总"""
        # 构建每日汇总内容
        content_lines = self._build_daily_summary_content(reports, gold_silver_ratio)

        # 转换 Markdown 为 HTML（简化版）
        html_lines = []
        for line in content_lines.split('\n'):
            if line.startswith('**'):
                # 标题
                text = line.replace('**', '').strip()
                html_lines.append(f'<h3>{text}</h3>')
            elif line.startswith('•'):
                # 列表项
                text = line.replace('•', '').strip()
                text = text.replace('**', '<strong>').replace('**', '</strong>')
                html_lines.append(f'<p>{text}</p>')
            elif line.strip() == '---':
                html_lines.append('<hr/>')
            elif line.strip() == '':
                html_lines.append('<br/>')
            else:
                text = line.replace('**', '<strong>').replace('**', '</strong>')
                html_lines.append(f'<p>{text}</p>')

        html_content = '\n'.join(html_lines)

        # 添加免责声明
        disclaimer = f'<p style="color: #888; font-size: 12px;">{self.DISCLAIMER}</p>'

        return self._wrap_html(html_content + disclaimer, "贵金属每日分析汇总")

    def _wrap_html(self, content: str, title: str) -> str:
        """包装为完整的 HTML 文档"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h3 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-top: 30px;
        }}
        p {{
            margin: 10px 0;
        }}
        strong {{
            color: #2c3e50;
        }}
        hr {{
            border: none;
            border-top: 1px solid #ecf0f1;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    {content}
</body>
</html>
        """

    def _build_market_report_content(
        self,
        symbol_name: str,
        symbol: str,
        quote_data: Dict[str, Any],
        technical_data: Dict[str, Any],
        patterns: Dict[str, int] = None,
        llm_analysis: Dict[str, Any] = None
    ) -> str:
        """构建市场报告内容（与 Feishu 格式保持一致）"""
        lines = []

        # === 行情概览 ===
        lines.append("**📈 实时行情**")
        if quote_data:
            price = quote_data.get('price', 0)
            change = quote_data.get('change', 0)
            change_pct = quote_data.get('change_percent', 0)
            high = quote_data.get('high', 0)
            low = quote_data.get('low', 0)
            open_price = quote_data.get('open', 0)

            lines.append(f"• 最新价: **${price:.2f}**")
            lines.append(f"• 涨跌额: {change:+.2f}")
            lines.append(f"• 涨跌幅: {change_pct:+.2f}%")
            lines.append(f"• 今日区间: ${low:.2f} ~ ${high:.2f}")
            lines.append(f"• 开盘价: ${open_price:.2f}")
        else:
            lines.append("• 暂无行情数据")
        lines.append("")

        # === 技术指标 ===
        if technical_data:
            lines.append("**📊 技术指标**")

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
                lines.append(f"• RSI(14): {rsi:.1f} ({rsi_status})")

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
                lines.append("**🕯️ K线形态识别**")
                lines.extend(pattern_lines)
                lines.append("")

        # === LLM 分析 ===
        if llm_analysis:
            analysis_content = llm_analysis.get('analysis', {})

            if isinstance(analysis_content, dict):
                lines.append("**🤖 AI 智能分析**")

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
                    lines.append(f"**💡 操作建议**")
                    lines.append(suggestion)
                    lines.append("")

            elif isinstance(analysis_content, str) and analysis_content:
                lines.append("**🤖 AI 智能分析**")
                if len(analysis_content) > 500:
                    analysis_content = analysis_content[:500] + "..."
                lines.append(analysis_content)
                lines.append("")

            elif llm_analysis.get('recommendation'):
                lines.append(f"**💡 操作建议**: {llm_analysis['recommendation']}")
                lines.append("")

        return "\n".join(lines)

    def _build_daily_summary_content(
        self,
        reports: List[Dict[str, Any]],
        gold_silver_ratio: float = None
    ) -> str:
        """构建每日汇总内容（与 Feishu 格式保持一致）"""
        lines = []

        if gold_silver_ratio:
            lines.append("**⚖️ 黄金白银比**")
            ratio_status = "白银相对强势" if gold_silver_ratio < 60 else ("黄金相对强势" if gold_silver_ratio > 80 else "正常区间")
            lines.append(f"• 当前比值: **{gold_silver_ratio:.1f}**")
            lines.append(f"• 历史均值: 60-70")
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

            lines.append(f"**{trend_icon} {symbol_name} ({symbol})**")
            lines.append(f"• 价格: ${price:.2f} ({change_pct:+.2f}%)")
            lines.append(f"• 趋势: {trend_text}")

            support = technical.get('support_levels', [])
            resistance = technical.get('resistance_levels', [])
            if support:
                lines.append(f"• 支撑: ${support[0]:.2f}" if isinstance(support[0], (int, float)) else f"• 支撑: {support[0]}")
            if resistance:
                lines.append(f"• 阻力: ${resistance[0]:.2f}" if isinstance(resistance[0], (int, float)) else f"• 阻力: {resistance[0]}")

            lines.append("")

        return "\n".join(lines)
