"""
Metal Trend Analysis Tool - Main Program
"""
import sys
import os
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.config_loader import ConfigLoader
from src.utils.logger import setup_logger, get_logger
from src.data_fetchers.stooq_client import StooqClient
from src.data_fetchers.news_fetcher import NewsFetcher
from src.analyzers.technical import TechnicalAnalyzer
from src.analyzers.patterns import PatternRecognizer
from src.analyzers.news_sentiment import NewsSentimentAnalyzer
from src.analyzers.trading_advisor import TradingAdvisor
from src.llm.analyzer import LLMAnalyzer
from src.reporting.generator import ReportGenerator
from src.notification.feishu import FeishuNotifier
from src.notification.dingtalk import DingTalkNotifier
from src.notification.slack import SlackNotifier
from src.notification.telegram import TelegramNotifier
from src.notification.email import EmailNotifier


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Metal Trend Analysis Tool')
    parser.add_argument('--config', type=str, default='config.yaml',
                        help='Configuration file path')
    parser.add_argument('--instrument', type=str, default='all',
                        choices=['all', 'gold', 'silver', 'XAUUSD', 'XAGUSD'],
                        help='Instrument to analyze')
    parser.add_argument('--timeframe', type=str, default='1d',
                        help='Timeframe (1d/1w/1m - Stooq daily data)')
    parser.add_argument('--debug', action='store_true',
                        help='Debug mode')
    return parser.parse_args()


def initialize_analyzers(config: Dict[str, Any], logger) -> Tuple[Dict[str, Any], bool]:
    """
    Initialize all analyzer modules.

    Returns:
        Tuple of (analyzers_dict, success)
    """
    analyzers = {}

    try:
        # 根据配置选择数据源 (默认使用 Twelve Data 获取现货黄金)
        data_source = os.getenv('DATA_SOURCE', 'twelve_data').lower()

        if data_source == 'twelve_data':
            # Twelve Data (获取现货黄金 XAU/USD)
            from src.data_fetchers.twelve_data_client import TwelveDataClient
            twelve_config = config.get('api', {}).get('twelve_data', {})
            twelve_api_key = os.getenv('TWELVE_DATA_API_KEY', '') or twelve_config.get('api_key', '')
            
            if not twelve_api_key:
                logger.warning("TWELVE_DATA_API_KEY not set, falling back to yfinance")
                data_source = 'yfinance'
            else:
                twelve_config['api_key'] = twelve_api_key
                analyzers['data_client'] = TwelveDataClient(twelve_config)
                analyzers['data_source'] = 'twelve_data'
                logger.info("Twelve Data client initialized (XAU/USD spot gold)")
        else:
            # yfinance (获取黄金期货 GC=F)
            stooq_config = config.get('api', {}).get('stooq', {})
            analyzers['data_client'] = StooqClient(stooq_config)
            analyzers['data_source'] = 'yfinance'
            logger.info("Yahoo Finance client initialized (Gold Futures GC=F)")

        # Technical analyzer
        indicators_config = config.get('indicators', {})
        analyzers['technical_analyzer'] = TechnicalAnalyzer(indicators_config)
        logger.info("Technical analyzer initialized successfully")

        # Pattern recognizer
        analyzers['pattern_recognizer'] = PatternRecognizer()
        logger.info("Pattern recognizer initialized successfully")

        # LLM analyzer (must be before TradingAdvisor)
        llm_config = config.get('llm', {})
        analyzers['llm_analyzer'] = LLMAnalyzer(llm_config)
        logger.info("LLM analyzer initialized successfully")

        # Trading advisor (with LLM analyzer for AI-powered advice)
        analyzers['trading_advisor'] = TradingAdvisor(llm_analyzer=analyzers['llm_analyzer'])
        logger.info("Trading advisor initialized successfully")

        # Report generator
        reports_config = config.get('reports', {})
        analyzers['report_generator'] = ReportGenerator(reports_config)
        logger.info("Report generator initialized successfully")

        return analyzers, True

    except Exception as e:
        logger.error(f"Failed to initialize analyzers: {e}")
        return {}, False


def initialize_news_modules(config: Dict[str, Any], logger) -> Tuple[Optional[Any], Optional[Any], List[Dict[str, Any]]]:
    """
    Initialize news fetcher and sentiment analyzer.

    Returns:
        Tuple of (news_fetcher, sentiment_analyzer, news_articles)
    """
    news_config = config.get('news', {})

    if not news_config.get('enabled', False):
        logger.info("News fetching is disabled in configuration")
        return None, None, []

    try:
        # Load keywords
        keywords_file = Path('config/keywords.txt')
        keywords = []
        if keywords_file.exists():
            with open(keywords_file, 'r', encoding='utf-8') as f:
                keywords = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            logger.info(f"Loaded {len(keywords)} keywords from {keywords_file}")
        else:
            logger.warning(f"Keywords file not found: {keywords_file}")

        # Check if news sources are configured
        news_sources = news_config.get('sources', [])
        if not news_sources:
            logger.warning("No news sources configured in config.yaml")

        # Initialize news fetcher
        news_fetcher = NewsFetcher(config=news_config, keywords=keywords)
        logger.info(f"News fetcher initialized with {len(news_sources)} sources")

        # Initialize sentiment analyzer
        sentiment_analyzer = NewsSentimentAnalyzer()
        logger.info("News sentiment analyzer initialized successfully")

        # Fetch news
        logger.info("Fetching news articles...")
        news_articles = news_fetcher.fetch_all_news(use_cache=True)
        logger.info(f"Fetched {len(news_articles)} news articles")

        return news_fetcher, sentiment_analyzer, news_articles

    except Exception as e:
        logger.error(f"Failed to initialize news modules: {str(e)}")
        return None, None, []


def initialize_notifiers(config: Dict[str, Any], logger) -> Dict[str, Any]:
    """
    Initialize all notification services.

    Returns:
        Dictionary of available notifiers
    """
    notification_config = config.get('notification', {}).get('channels', {})
    notifiers = {}

    # Feishu notifier
    feishu_config = notification_config.get('feishu', {})
    feishu_webhook = feishu_config.get('webhook_url', '')
    if feishu_webhook:
        notifiers['Feishu'] = FeishuNotifier(
            webhook_url=feishu_webhook,
            timeout=feishu_config.get('timeout', 30)
        )
        logger.info("Feishu notifier initialized successfully")
    else:
        logger.info("Feishu webhook URL not configured, Feishu notifications disabled")

    # DingTalk notifier
    dingtalk_config = notification_config.get('dingtalk', {})
    dingtalk_webhook = dingtalk_config.get('webhook_url', '')
    if dingtalk_webhook:
        notifiers['DingTalk'] = DingTalkNotifier(
            webhook_url=dingtalk_webhook,
            timeout=dingtalk_config.get('timeout', 30)
        )
        logger.info("DingTalk notifier initialized successfully")
    else:
        logger.info("DingTalk webhook URL not configured, DingTalk notifications disabled")

    # Slack notifier
    slack_config = notification_config.get('slack', {})
    slack_webhook = slack_config.get('webhook_url', '')
    if slack_webhook:
        notifiers['Slack'] = SlackNotifier(
            webhook_url=slack_webhook,
            timeout=slack_config.get('timeout', 30)
        )
        logger.info("Slack notifier initialized successfully")
    else:
        logger.info("Slack webhook URL not configured, Slack notifications disabled")

    # Telegram notifier
    telegram_config = notification_config.get('telegram', {})
    telegram_bot_token = telegram_config.get('bot_token', '')
    telegram_chat_id = telegram_config.get('chat_id', '')
    if telegram_bot_token and telegram_chat_id:
        notifiers['Telegram'] = TelegramNotifier(
            bot_token=telegram_bot_token,
            chat_id=telegram_chat_id,
            timeout=telegram_config.get('timeout', 30)
        )
        logger.info("Telegram notifier initialized successfully")
    else:
        logger.info("Telegram bot token or chat ID not configured, Telegram notifications disabled")

    # Email notifier
    email_config = notification_config.get('email', {})
    email_from = email_config.get('from', '')
    email_password = email_config.get('password', '')
    email_to = email_config.get('to', '')
    if email_from and email_password and email_to:
        notifiers['Email'] = EmailNotifier(
            from_email=email_from,
            password=email_password,
            to_email=email_to,
            smtp_server=email_config.get('smtp_server'),
            smtp_port=email_config.get('smtp_port'),
            timeout=email_config.get('timeout', 30)
        )
        logger.info("Email notifier initialized successfully")
    else:
        logger.info("Email configuration not complete, Email notifications disabled")

    return notifiers


def get_instruments_to_analyze(args: argparse.Namespace, config: Dict[str, Any]) -> List[Tuple[str, Dict[str, Any]]]:
    """
    Determine which instruments to analyze based on arguments and configuration.

    Returns:
        List of (instrument_name, instrument_config) tuples
    """
    instruments_config = config.get('instruments', {})
    instruments_to_analyze = []

    if args.instrument == 'all':
        instruments_to_analyze = [
            ('gold', instruments_config.get('gold', {})),
            ('silver', instruments_config.get('silver', {}))
        ]
    else:
        # Determine instrument based on parameter
        if args.instrument in ['gold', 'XAUUSD']:
            instruments_to_analyze.append(('gold', instruments_config.get('gold', {})))
        elif args.instrument in ['silver', 'XAGUSD']:
            instruments_to_analyze.append(('silver', instruments_config.get('silver', {})))

    return instruments_to_analyze


def analyze_instrument(
    instrument_name: str,
    instrument_config: Dict[str, Any],
    analyzers: Dict[str, Any],
    sentiment_analyzer: Optional[Any],
    news_articles: List[Dict[str, Any]],
    timeframe: str,
    logger,
    debug: bool = False
) -> Optional[Dict[str, Any]]:
    """
    Analyze a single instrument.

    Returns:
        Analysis results dictionary or None if failed
    """
    if not instrument_config.get('enabled', True):
        logger.info(f"{instrument_name} is not enabled, skipping")
        return None

    symbol = instrument_config.get('symbol')
    symbol_name = instrument_config.get('name')
    region = instrument_config.get('region', 'GB')
    stooq_symbol = instrument_config.get('stooq_symbol', symbol)

    logger.info(f"")
    logger.info(f"Starting analysis for {symbol_name} ({symbol})...")
    logger.info("-" * 60)

    try:
        data_client = analyzers['data_client']
        technical_analyzer = analyzers['technical_analyzer']
        pattern_recognizer = analyzers['pattern_recognizer']
        trading_advisor = analyzers['trading_advisor']
        llm_analyzer = analyzers['llm_analyzer']
        report_generator = analyzers['report_generator']
        data_client = analyzers['data_client']
        data_source = analyzers.get('data_source', 'yfinance')

        # Get real-time quote
        logger.info(f"Fetching real-time quote for {symbol} (Data Source: {data_source})...")
        quote_data = data_client.get_quote(stooq_symbol)
        if quote_data:
            quote_data['symbol'] = symbol

        if not quote_data:
            logger.error(f"Failed to fetch quote for {symbol}")
            return None

        logger.info(f"Current price: ${quote_data.get('price')}")
        logger.info(f"Change: {quote_data.get('change')} ({quote_data.get('change_percent')}%)")

        # Get K-line data (multi-timeframe)
        logger.info(f"Fetching K-line data for {symbol}...")

        # 获取多时间周期数据（用于交易建议）
        multi_timeframes = ['5m', '15m', '30m', '1h', '4h', '1d']
        logger.info(f"Fetching multi-timeframe data: {multi_timeframes}")

        # Twelve Data 的时间周期映射 (使用 API 支持的格式)
        if data_source == 'twelve_data':
            td_timeframes = ['5min', '15min', '30min', '1h', '4h', '1day']
            tf_map = dict(zip(multi_timeframes, td_timeframes))
            multi_timeframe_data = {}
            for tf in multi_timeframes:
                try:
                    df = data_client.get_kline(stooq_symbol, interval=tf_map.get(tf, tf))
                    if not df.empty:
                        multi_timeframe_data[tf] = df
                except Exception as e:
                    logger.warning(f"Failed to fetch {tf} data: {e}")
                    continue
        else:
            multi_timeframe_data = data_client.get_multi_timeframe_data(stooq_symbol, multi_timeframes)

        # 主时间周期数据
        kline_data = multi_timeframe_data.get(timeframe) if multi_timeframe_data else None
        if kline_data is None or kline_data.empty:
            # 回退到单时间周期获取
            kline_data = data_client.get_kline(stooq_symbol, timeframe)

        if kline_data.empty:
            logger.error(f"Failed to fetch K-line data for {symbol}")
            return None

        logger.info(f"Fetched {len(kline_data)} K-line records for main timeframe ({timeframe})")
        if multi_timeframe_data:
            for tf, df in multi_timeframe_data.items():
                logger.info(f"  - {tf}: {len(df)} records")

        # Save raw data
        if hasattr(data_client, 'save_raw_data'):
            data_client.save_raw_data(kline_data, symbol, timeframe)
        else:
            # Twelve Data 没有 save_raw_data 方法，手动保存
            from pathlib import Path
            output_dir = Path("data/raw")
            output_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{symbol}_{timeframe}_{timestamp}.csv"
            filepath = output_dir / filename
            kline_data.to_csv(filepath)
            logger.info(f"Raw data saved: {filepath}")

        # Calculate technical indicators
        logger.info("Calculating technical indicators...")
        indicator_data = technical_analyzer.calculate_all_indicators(kline_data)

        # Trend analysis
        trend_analysis = technical_analyzer.get_trend_analysis(indicator_data)

        # Support and resistance levels
        support_levels, resistance_levels = technical_analyzer.identify_support_resistance(kline_data)

        technical_result = {
            **trend_analysis,
            'support_levels': support_levels,
            'resistance_levels': resistance_levels
        }

        logger.info(f"Technical trend: {trend_analysis.get('trend', 'N/A')}")
        logger.info(f"Support levels: {[f'${s:.2f}' for s in support_levels[:2]]}")
        logger.info(f"Resistance levels: {[f'${r:.2f}' for r in resistance_levels[:2]]}")

        # Identify K-line patterns
        logger.info("Identifying K-line patterns...")
        patterns = pattern_recognizer.detect_patterns(kline_data)
        pattern_summary = pattern_recognizer.get_pattern_summary(patterns)

        logger.info("K-line patterns:")
        if pattern_summary:
            for line in pattern_summary.split('\n'):
                if line.strip():
                    logger.info(f"  {line}")

        technical_result['patterns'] = patterns

        # Generate trading advice (with multi-timeframe data)
        logger.info("Generating trading advice with multi-timeframe analysis...")
        current_price = quote_data.get('price', 0)
        advice = trading_advisor.generate_advice(
            kline_data,
            trend_analysis,
            support_levels,
            resistance_levels,
            current_price,
            timeframe,
            multi_timeframe_data=multi_timeframe_data
        )
        trading_advice_dict = trading_advisor.to_dict(advice)
        logger.info(f"Trading direction: {advice.get('direction', '未知')}")
        logger.info(f"Entry range: ${advice['entry_range'][0]:.2f} - ${advice['entry_range'][1]:.2f}")
        logger.info(f"Stop loss (standard): ${advice['stop_loss']['standard']:.2f}")
        logger.info(f"Take profit 1: ${advice['take_profit']['tp1']:.2f}")
        logger.info(f"Confidence: {advice.get('confidence_score', 0)}%")

        # LLM comprehensive analysis
        logger.info("Performing LLM comprehensive analysis...")
        llm_result = llm_analyzer.analyze_market(
            symbol,
            quote_data,
            technical_result,
            news_articles
        )

        if llm_result.get('error'):
            logger.warning(f"LLM analysis failed: {llm_result['error']}")
        else:
            logger.info("LLM analysis successful")
            analysis = llm_result.get('analysis', {})
            if analysis:
                logger.info(f"Trend direction: {analysis.get('trend', 'N/A')}")
                logger.info(f"Trading suggestion: {analysis.get('suggestion', 'N/A')}")
                logger.info(f"Risk level: {analysis.get('risk_level', 'N/A')}")

        # Generate report
        logger.info("Generating analysis report...")

        # Add news sentiment to technical result
        if sentiment_analyzer and news_articles:
            sentiment_result = sentiment_analyzer.analyze_articles_sentiment(news_articles)
            technical_result['news_sentiment'] = sentiment_result
            logger.info(f"News sentiment: {sentiment_result.get('overall_sentiment', 'N/A')}")

        report_content = report_generator.generate_markdown_report(
            symbol,
            symbol_name,
            quote_data,
            technical_result,
            news_articles,
            llm_result,
            trading_advice=trading_advice_dict
        )

        report_path = report_generator.save_report(report_content, symbol, timeframe)
        logger.info(f"Report saved to: {report_path}")

        logger.info(f"{symbol_name} analysis completed")
        logger.info("-" * 60)

        return {
            'symbol': symbol,
            'quote': quote_data,
            'technical': technical_result,
            'llm': llm_result,
            'trading_advice': trading_advice_dict,
            'report_path': report_path
        }

    except Exception as e:
        logger.error(f"Error analyzing {symbol_name}: {str(e)}")
        if debug:
            import traceback
            logger.error(traceback.format_exc())
        return None


def calculate_gold_silver_ratio(analysis_results: Dict[str, Any], logger) -> Optional[float]:
    """Calculate and log gold-silver ratio if both metals are analyzed."""
    if len(analysis_results) >= 2 and 'gold' in analysis_results and 'silver' in analysis_results:
        gold_price = analysis_results['gold']['quote'].get('price')
        silver_price = analysis_results['silver']['quote'].get('price')

        if gold_price and silver_price and silver_price > 0:
            gold_silver_ratio = gold_price / silver_price
            logger.info(f"")
            logger.info(f"Gold-Silver Ratio: {gold_silver_ratio:.1f}")
            logger.info(f"Historical average: 60-70")

            if gold_silver_ratio < 60:
                logger.info("Insight: Silver is performing strongly relative to gold")
            elif gold_silver_ratio > 70:
                logger.info("Insight: Gold is performing strongly relative to silver")
            else:
                logger.info("Insight: Gold-silver ratio is within normal range")

            return gold_silver_ratio

    return None


def send_notifications(
    notifiers: Dict[str, Any],
    analysis_results: Dict[str, Any],
    instruments_config: Dict[str, Any],
    logger
) -> None:
    """Send notifications to all available notifiers."""
    if not notifiers or not analysis_results:
        return

    logger.info(f"Sending notifications to: {', '.join(notifiers.keys())}...")

    # Prepare notification data
    reports_for_push = []
    for instrument_name, result in analysis_results.items():
        instrument_cfg = instruments_config.get(instrument_name, {})
        reports_for_push.append({
            'symbol': result['symbol'],
            'symbol_name': instrument_cfg.get('name', instrument_name),
            'quote_data': result['quote'],
            'technical_data': result['technical'],
            'patterns': result['technical'].get('patterns', {}),
            'llm_analysis': result.get('llm', {}),
            'trading_advice': result.get('trading_advice', {})
        })

    # Calculate gold-silver ratio
    gold_silver_ratio_value = None
    if 'gold' in analysis_results and 'silver' in analysis_results:
        gold_p = analysis_results['gold']['quote'].get('price', 0)
        silver_p = analysis_results['silver']['quote'].get('price', 0)
        if gold_p and silver_p and silver_p > 0:
            gold_silver_ratio_value = gold_p / silver_p

    # Send notifications to each available notifier
    for notifier_name, notifier in notifiers.items():
        try:
            # Send daily summary
            if notifier.send_daily_summary(reports_for_push, gold_silver_ratio_value):
                logger.info(f"{notifier_name} daily summary sent successfully")
            else:
                logger.warning(f"Failed to send {notifier_name} daily summary")
        except Exception as e:
            logger.error(f"Error sending {notifier_name} notification: {e}")

        # Send detailed reports for each instrument
        for report_data in reports_for_push:
            try:
                if notifier.send_market_report(
                    symbol_name=report_data['symbol_name'],
                    symbol=report_data['symbol'],
                    quote_data=report_data['quote_data'],
                    technical_data=report_data['technical_data'],
                    patterns=report_data.get('patterns'),
                    llm_analysis=report_data.get('llm_analysis'),
                    trading_advice=report_data.get('trading_advice')
                ):
                    logger.info(f"{notifier_name} report for {report_data['symbol']} sent successfully")
                else:
                    logger.warning(f"Failed to send {notifier_name} report for {report_data['symbol']}")
            except Exception as e:
                logger.error(f"Error sending {notifier_name} report for {report_data['symbol']}: {e}")


def main():
    """Main function"""
    # Parse command line arguments
    args = parse_arguments()

    # Setup logging
    log_level = 'DEBUG' if args.debug else 'INFO'
    logger = setup_logger(level=log_level)
    logger = get_logger('main')

    logger.info("=" * 60)
    logger.info("Metal Trend Analysis Tool Started")
    logger.info("=" * 60)

    try:
        # Load configuration
        logger.info("Loading configuration file...")
        config_loader = ConfigLoader()
        config = config_loader.load_main_config(args.config)
        logger.info("Configuration loaded successfully")

        # Initialize modules
        logger.info("Initializing modules...")
        analyzers, analyzers_success = initialize_analyzers(config, logger)
        if not analyzers_success:
            logger.error("Failed to initialize analyzers")
            sys.exit(1)

        # Initialize news modules
        news_fetcher, sentiment_analyzer, news_articles = initialize_news_modules(config, logger)

        # Initialize notifiers
        notifiers = initialize_notifiers(config, logger)

        # Determine instruments to analyze
        instruments_to_analyze = get_instruments_to_analyze(args, config)
        logger.info(f"Instruments to analyze: {[inst[0] for inst in instruments_to_analyze]}")

        # Analyze each instrument
        analysis_results = {}
        for instrument_name, instrument_config in instruments_to_analyze:
            result = analyze_instrument(
                instrument_name,
                instrument_config,
                analyzers,
                sentiment_analyzer,
                news_articles,
                args.timeframe,
                logger,
                args.debug
            )
            if result:
                analysis_results[instrument_name] = result

        # Calculate gold-silver ratio
        gold_silver_ratio = calculate_gold_silver_ratio(analysis_results, logger)

        # Send notifications
        instruments_config = config.get('instruments', {})
        send_notifications(notifiers, analysis_results, instruments_config, logger)

        # Complete
        logger.info("")
        logger.info("=" * 60)
        logger.info("Analysis Complete!")
        logger.info("=" * 60)
        logger.info("")
        logger.info(f"Total {len(analysis_results)} instruments analyzed:")
        for instrument_name, result in analysis_results.items():
            logger.info(f"  - {instrument_name}: {result['report_path']}")
        if notifiers:
            logger.info(f"  - Notifications sent to: {', '.join(notifiers.keys())}")
        logger.info("")

    except Exception as e:
        logger.error(f"Program error: {str(e)}")
        if args.debug:
            import traceback
            logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    main()
