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

### 2. Get API Keys

#### iTick API (Required)

1. Visit https://itick.org and register
2. Go to the console and get your API Token
3. Free tier: 5 calls/minute

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
ITICK_API_TOKEN=your_itick_token_here
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
  itick:
    token: "your_itick_token_here"

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

### iTick API

`config/itick_config.yaml`:

```yaml
base_url: "https://api.itick.org/forex"
token: ""  # Your API Token
timeout: 30
retry: 3
retry_delay: 2
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

If `FEISHU_WEBHOOK_URL` is empty, no Feishu notifications will be sent.

### DingTalk Notifications (Optional)

1. DingTalk group → Group settings → Smart Group Assistant → Add custom bot
2. Copy the Webhook URL
3. Add to `.env`:

```env
DINGTALK_WEBHOOK_URL=https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxx
```

In `config/config.yaml`, enable the corresponding notification channel:

```yaml
notification:
  enabled: true
  channels:
    feishu:
      enabled: true
      webhook_url: "${FEISHU_WEBHOOK_URL}"
    dingtalk:
      enabled: false  # Enable DingTalk
      webhook_url: "${DINGTALK_WEBHOOK_URL}"
```

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
- 🔔 Multi-channel notification support: Feishu, DingTalk
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

**Problem**: `ta-lib` installation fails

**Solution**:
```bash
# Mac
brew install ta-lib

# Ubuntu/Debian
sudo apt-get install ta-lib

# Windows
# Download pre-compiled package from https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
# Then install: pip install TA_Lib-0.4.xx-cpxx-cpxx-win_amd64.whl
```

### Q2: iTick API returns 401

**Problem**: API Token invalid

**Solution**:
1. Check if token in `.env` file is correct
2. Regenerate token from iTick console
3. Ensure no extra spaces or quotes

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
