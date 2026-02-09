# Installation and Configuration Guide

## ✅ Prerequisites

- Python 3.10+ (recommended: 3.10/3.11)
- macOS / Linux / Windows

## 🚀 Quick Start (5 minutes)

### Step 1: Clone the Project

```bash
cd /path/to/your/workspace
# git clone <repository_url>
cd metal_trend_analysis
```

### Step 2: One-Click Setup (Optional)

```bash
./start.sh
```

This script will automatically:
- Check Python version
- Create virtual environment
- Install dependencies
- Validate configuration files

## 🧰 Manual Setup (Recommended)

### 1. Environment Setup

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Data Source

#### Stooq (Free, No API Key Required)

Stooq provides public daily data with weekly/monthly resampling support.

#### LLM API (Required)

Use OpenAI / DeepSeek / Qwen, or any OpenAI-compatible service.

### 3. Configure the System

#### Method A: Environment Variables (Recommended)

```bash
cp .env.example .env
vim .env
```

Fill in your credentials:

```env
LLM_API_KEY=your_llm_api_key_here
LLM_BASE_URL=https://api.deepseek.com/v1  # Optional
LLM_MODEL_NAME=gpt-4o  # Or deepseek-chat

# Optional: Feishu notifications (leave empty to disable)
FEISHU_WEBHOOK_URL=
```

#### Method B: Direct Config File Edit

```bash
vim config/config.yaml
```

```yaml
api:
  stooq:
    base_url: "https://stooq.com/q/d/l/"
    timeout: 20
    retry: 3
    retry_delay: 2
    default_kline_count: 200

llm:
  api_key: "your_llm_api_key_here"
  base_url: "https://api.deepseek.com/v1"
  model: "gpt-4o"

news:
  enabled: true
  max_articles: 10
  cache_duration: 300
  fetch:
    timeout: 15
    delay: 2
    max_retries: 3
  sources:
    - name: "Bloomberg Markets"
      type: "rss"
      url: "https://feeds.bloomberg.com/markets/news.rss"
      enabled: true
    - name: "CNBC Market News"
      type: "rss"
      url: "https://www.cnbc.com/id/10000664/device/rss/rss.html"
      enabled: true
    - name: "Phoenix Finance"
      type: "rss"
      url: "https://finance.ifeng.com/rss/index.xml"
      enabled: true
```

### 4. Verify Configuration

```bash
source venv/bin/activate
python src/main.py --debug
```

## ⚙️ Detailed Configuration

### Stooq

`config/config.yaml`:

```yaml
api:
  stooq:
    base_url: "https://stooq.com/q/d/l/"
    timeout: 20
    retry: 3
    retry_delay: 2
    default_kline_count: 200
```

### LLM

`config/config.yaml`:

```yaml
llm:
  provider: "openai"
  api_key: "${LLM_API_KEY}"
  base_url: "${LLM_BASE_URL}"
  model: "${LLM_MODEL_NAME}"
  temperature: 0.7
  max_tokens: 2000
  timeout: 60
```

**Supported Models**:
- OpenAI: gpt-4o, gpt-4-turbo, gpt-3.5-turbo
- DeepSeek: deepseek-chat, deepseek-coder
- Qwen: qwen-turbo, qwen-plus, qwen-max

### Feishu Notifications (Optional)

1. Feishu group → Group settings → Bots → Add custom bot
2. Copy the Webhook URL
3. Add to `.env`:

```env
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx
```

**Important**: Notification is enabled only when the corresponding webhook URL is configured in `.env`. Once you configure `FEISHU_WEBHOOK_URL`, Feishu notifications will be automatically enabled.

### DingTalk Notifications (Optional)

1. DingTalk group → Group settings → Smart Group Assistant → Add custom bot
2. Copy the Webhook URL
3. Add to `.env`:

```env
DINGTALK_WEBHOOK_URL=https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxx
```

**Important**: Notification is enabled only when the corresponding webhook URL is configured in `.env`. Once you configure `DINGTALK_WEBHOOK_URL`, DingTalk notifications will be automatically enabled.

### Slack Notifications (Optional)

1. Visit [Slack API](https://api.slack.com/apps)
2. Click "Create New App" → "From scratch"
3. Enter App name and select workspace, then click "Create App"
4. Go to "Incoming Webhooks" page and toggle "Activate Incoming Webhooks" to **On**
5. Click "Add New Webhook to Workspace", select a channel and authorize
6. Copy the Webhook URL
7. Add to `.env`:

```env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXXXXXXX/XXXXXXXX/XXXXXXXX
```

**Important**: Notification is enabled only when the corresponding webhook URL is configured in `.env`. Once you configure `SLACK_WEBHOOK_URL`, Slack notifications will be automatically enabled.

### Telegram Notifications (Optional)

1. Search for `@BotFather` in Telegram (ensure it has the blue checkmark)
2. Send `/newbot` to create a new bot, follow the prompts to set name and username
3. Copy the returned Bot Token (format: `123456789:AAH...`)
4. Send a message to your bot (any content)
5. Visit the following URL in your browser to get the Chat ID:

```
https://api.telegram.org/bot<TOKEN>/getUpdates
```

   Replace `<TOKEN>` with your Bot Token, find the `"id"` number in the returned JSON
6. Add to `.env`:

```env
TELEGRAM_BOT_TOKEN=123456789:AAH...
TELEGRAM_CHAT_ID=123456789
```

**Notes**:
- Chat ID is a number, not a URL
- To send to a group, you need to add the bot to the group first, then get the group ID
- **Important**: Notification is enabled only when both Bot Token and Chat ID are configured in `.env`. Once you configure both `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`, Telegram notifications will be automatically enabled.

### Email Notifications (Optional)

1. Prepare email information:
   - Sender email address
   - Email password or authorization code (some email providers require authorization code instead of login password)
   - Recipient email addresses (comma-separated for multiple recipients)

2. **How to get Authorization Code** (for Gmail, QQ Mail, etc.):
   - Log in to your email web interface
   - Go to Settings → Account Security
   - Enable SMTP service (or two-factor authentication)
   - Generate authorization code (Application-specific password)

3. Add to `.env`:

```env
EMAIL_FROM=your_email@gmail.com
EMAIL_PASSWORD=your_password_or_app_code
EMAIL_TO=recipient1@example.com,recipient2@example.com
```

4. **Optional: Custom SMTP Configuration** (if auto-detection fails)

The system automatically detects SMTP configurations for common email providers, including: Gmail, QQ Mail, 163 Mail, 126 Mail, Outlook, Hotmail, Sina Mail, Sohu Mail, Aliyun Mail, Yandex, iCloud, 189 Mail, etc.

If auto-detection fails, you can manually configure:

```env
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
```

**Important**: Notification is enabled only when sender email, password, and recipient email are configured in `.env`. Once you configure all three (`EMAIL_FROM`, `EMAIL_PASSWORD`, and `EMAIL_TO`), email notifications will be automatically enabled.

### News Keywords Configuration
黄金
白银
贵金属
XAUUSD
XAGUSD
美元
美联储
通胀
利率
```

- Lines starting with `#` are comments
- Empty lines are automatically ignored
- Keywords are case-insensitive
- Include both English and Chinese keywords for better coverage

### Notification Delivery Effects

- 📊 Daily summary report (Gold/Silver overview + Gold/Silver ratio)
- 📈 Single instrument detailed report (quotes, technical indicators, candlestick patterns, news sentiment analysis, AI analysis)
- 🔔 Multi-channel notification support: Feishu, DingTalk, Slack, Telegram, Email
- 🔔 Supports card/Markdown message format for mobile-friendly reading

### News Sources Configuration

The system includes the following verified news sources:

#### English News Sources
- **Bloomberg Markets** - World's leading business and financial market information provider
- **CNBC Market News** - Authoritative US business news source

#### Chinese News Sources
- **Phoenix Finance** - Well-known Chinese financial media

#### Adding Custom News Sources
You can add other RSS news sources:

```yaml
- name: "Custom News Source"
  type: "rss"
  url: "https://example.com/rss.xml"
  enabled: true
```

#### Note
The following news sources have been verified as unavailable or require special handling, and are temporarily disabled:
- Reuters: DNS resolution failed
- Financial Times: 404 error
- MarketWatch: 403 Forbidden
- Sina Finance: 404 error
- Tencent Finance: 301 Redirect
- NetEase Finance: 404 error
- Hexun: Requires JavaScript processing
- East Money: No RSS content
- The Paper: 302 Redirect

### Q1: pip install fails

**Problem**: Dependency installation fails or version conflicts occur

**Solution**:
```bash
# Upgrade build tools
python -m pip install --upgrade pip setuptools wheel

# If it still fails, recreate the virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

Make sure you are using Python 3.10 or higher.

### Q2: Stooq data is empty

**Problem**: No data returned or latest data missing

**Solution**:
1. Verify `stooq_symbol` in `config/config.yaml` (e.g., `xauusd`, `xagusd`)
2. Ensure network access to `https://stooq.com/q/d/l/`
3. Use `1d/1w/1m` timeframes

### Q3: LLM API timeout

**Problem**: LLM request timeout

**Solution**:
1. Increase `timeout` parameter (e.g., 120 seconds)
2. Use faster model (e.g., gpt-3.5-turbo)
3. Check network connection

### Q4: Virtual environment activation fails

**Problem**: Cannot activate virtual environment

**Solution**:
```bash
# Delete old virtual environment
rm -rf venv

# Recreate
python3 -m venv venv

# Activate
source venv/bin/activate
```

### Q5: News scraping fails

**Problem**: Cannot fetch news

**Solution**:
1. Check network connection
2. Increase `timeout` value in `config.yaml`
3. Temporarily disable problematic news sources

### Q6: News sentiment analysis inaccurate

**Problem**: Sentiment analysis results don't match actual news content

**Solution**:
1. Check if `config/keywords.txt` contains relevant keywords
2. Adjust news source `enabled` settings, only enable high-quality sources
3. Update sentiment lexicon (modify vocabulary lists in `src/analyzers/news_sentiment.py`)

### Q7: News fetching is slow

**Problem**: News fetching takes too much time

**Solution**:
1. Reduce `news.max_articles` value
2. Enable caching (`news.cache_duration`)
3. Disable unnecessary news sources
4. Increase `news.fetch.delay` to reduce request frequency

## Running Examples

### Basic Run

```bash
# Analyze all instruments (gold and silver), includes news sentiment analysis
python src/main.py

# Analyze gold only
python src/main.py --instrument gold

# Analyze silver only
python src/main.py --instrument silver

# Specify timeframe
python src/main.py --timeframe 4h

# Debug mode
python src/main.py --debug

# Disable news feature
python src/main.py --no-news
```

### Using Startup Script

```bash
# Basic run
./start.sh

# Pass parameters
./start.sh --instrument gold --timeframe 4h
```

## Viewing Reports

Generated reports are saved in `output/reports/`:

```bash
# View latest reports
ls -lt output/reports/ | head -5

# View report content
cat output/reports/report_XAUUSD_20260127_101523.md
```

## Docker Deployment (Recommended)

MetalTrend AI supports Docker for quick deployment with scheduled execution.

### Quick Start

```bash
# 1. Build and start container
docker-compose up -d

# 2. View logs
docker-compose logs -f

# 3. Stop container
docker-compose down
```

### Configure Scheduled Tasks

Use `CRON_SCHEDULE` environment variable to set up automated analysis (Cron format):

```bash
# Run analysis at 9 AM daily
docker-compose run -e CRON_SCHEDULE="0 9 * * *" metal-trend-analysis

# Run analysis every hour
docker-compose run -e CRON_SCHEDULE="0 * * * *" metal-trend-analysis

# Run analysis at 9 AM on weekdays
docker-compose run -e CRON_SCHEDULE="0 9 * * 1-5" metal-trend-analysis

# Run analysis every 30 minutes
docker-compose run -e CRON_SCHEDULE="*/30 * * * *" metal-trend-analysis
```

### Custom Configuration Parameters

Configure via `docker-compose.yml` or environment variables:

```bash
# Specify instrument (gold/silver/all)
docker-compose run -e INSTRUMENT=gold metal-trend-analysis

# Specify timeframe (1m, 5m, etc.)
docker-compose run -e TIMEFRAME=4h metal-trend-analysis

# Custom timezone
docker-compose run -e TZ=America/New_York metal-trend-analysis
```

### Cron Format Explanation

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6) (0=Sunday)
│ │ │ │ │
* * * * * command
```

**Examples**:
- `0 9 * * *` - Daily at 9:00
- `0 */2 * * *` - Every 2 hours
- `*/30 * * * *` - Every 30 minutes
- `0 9 * * 1-5` - Weekdays at 9:00
- `0 9,18 * * *` - Daily at 9:00 and 18:00

### Data Persistence

The container automatically mounts the following directories for data persistence:

- `./config` - Configuration files
- `./data` - Data cache directory
- `./output` - Output directory (reports, logs)

### View Output

```bash
# View container logs
docker-compose logs -f

# View generated reports
ls -lt output/reports/

# View analysis logs
tail -f output/logs/app.log

# View cron job logs
tail -f output/logs/cron.log
```

### Manual Execution

For one-time analysis without scheduling:

```bash
# Method 1: Don't set CRON_SCHEDULE
docker-compose run --rm -e CRON_SCHEDULE= metal-trend-analysis

# Method 2: Run Python script directly
docker-compose run --rm metal-trend-analysis python src/main.py --instrument all
```

## Next Steps

After configuration, you can:

1. **Regular Analysis**: Use cron or scheduled tasks for periodic runs
2. **Custom Configuration**: Adjust technical indicator parameters as needed
3. **Extend Functionality**: Add new technical indicators or news sources
4. **Customize LLM Prompts**: Modify prompts in `src/llm/analyzer.py`
5. **Data Visualization**: Integrate chart libraries for visual reports

## Technical Support

For issues, please check:
- README.md - Project documentation
- README_EN.md - English documentation
- output/logs/app.log - Runtime logs
- Use `--debug` parameter for detailed information

---

**Happy Using!**
