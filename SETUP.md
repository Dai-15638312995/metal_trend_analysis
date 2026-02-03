# 安装和配置指南

## ✅ 适用环境

- Python 3.10+（推荐使用 3.10/3.11）
- macOS / Linux / Windows

## 🚀 快速开始（5分钟）

### 步骤 1: 克隆项目

```bash
cd /path/to/your/workspace
# git clone <repository_url>
cd metal_trend_analysis
```

### 步骤 2: 一键初始化（可选）

```bash
./start.sh
```

该脚本会自动：
- 检查 Python 版本
- 创建虚拟环境
- 安装依赖
- 检查配置文件

## 🧰 手动配置（推荐）

### 1. 环境准备

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

pip install --upgrade pip
pip install -r requirements.txt
```

### 2. 获取 API 密钥

#### iTick API（必需）

1. 访问 https://itick.org 注册账号
2. 进入控制台获取 API Token
3. 免费套餐：5次/分钟调用

#### LLM API（必需）

可选择：OpenAI / DeepSeek / 通义千问 / 其他兼容 OpenAI 接口的服务。

### 3. 配置系统

#### 方法 A: 使用环境变量（推荐）

```bash
cp .env.example .env
vim .env
```

填写配置：

```env
ITICK_API_TOKEN=your_itick_token_here
LLM_API_KEY=your_llm_api_key_here
LLM_BASE_URL=https://api.deepseek.com/v1  # 可选
LLM_MODEL_NAME=gpt-4o  # 或 deepseek-chat

# 可选：飞书推送（留空则不启用）
FEISHU_WEBHOOK_URL=

# 可选：钉钉推送（留空则不启用）
DINGTALK_WEBHOOK_URL=
```

#### 方法 B: 直接编辑配置文件

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
    - name: "凤凰网财经"
      type: "rss"
      url: "https://finance.ifeng.com/rss/index.xml"
      enabled: true
```

### 4. 验证配置

```bash
source venv/bin/activate
python src/main.py --debug
```

## ⚙️ 详细配置说明

### iTick API 配置

`config/itick_config.yaml`：

```yaml
base_url: "https://api.itick.org/forex"
token: ""  # 你的 API Token
timeout: 30
retry: 3
retry_delay: 2
```

### LLM 配置

`config/config.yaml`：

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

### 飞书推送配置（可选）

1. 飞书群 → 群设置 → 群机器人 → 添加「自定义机器人」
2. 复制 Webhook URL
3. 写入 `.env`：

```env
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx
```

若 `FEISHU_WEBHOOK_URL` 为空，则不会发送飞书推送。

```yaml
notification:
  enabled: true
  channels:
    feishu:
      enabled: true
      webhook_url: "${FEISHU_WEBHOOK_URL}"
    dingtalk:
      enabled: false  # 启用钉钉推送
      webhook_url: "${DINGTALK_WEBHOOK_URL}"
```

#### 推送效果

- 📊 每日汇总报告（黄金白银概览 + 黄金白银比）
- 📈 单品种详细报告（行情、技术指标、K线形态、新闻情感分析、AI分析）
- 🔔 支持多渠道推送：飞书、钉钉
- 🔔 支持卡片/Markdown消息格式，移动端阅读友好

### 新闻关键词配置

新闻抓取模块会使用`config/keywords.txt`中的关键词来筛选相关新闻。你可以编辑这个文件：

```bash
# 编辑关键词文件
vim config/keywords.txt
```

文件格式（每行一个关键词）：
```
# 贵金属相关关键词
gold
silver
precious metals
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

- 以 `#` 开头的行是注释
- 系统会自动忽略空行
- 关键词不区分大小写
- 建议包含中英文关键词以获得更全面的覆盖

### 新闻源配置

系统内置以下已验证可用的新闻源：

#### 英文新闻源
- **Bloomberg Markets** - 全球领先的商业和金融市场信息提供商
- **CNBC Market News** - 美国商业新闻权威机构

#### 中文新闻源  
- **凤凰网财经** - 知名中文财经媒体

#### 配置说明
新闻源配置在 `config/config.yaml` 的 `news.sources` 部分：

```yaml
news:
  sources:
    # 英文RSS新闻源
    - name: "Bloomberg Markets"
      type: "rss"
      url: "https://feeds.bloomberg.com/markets/news.rss"
      enabled: true  # 启用或禁用该新闻源
    - name: "CNBC Market News"
      type: "rss"
      url: "https://www.cnbc.com/id/10000664/device/rss/rss.html"
      enabled: true
    
    # 中文RSS新闻源
    - name: "凤凰网财经"
      type: "rss"
      url: "https://finance.ifeng.com/rss/index.xml"
      enabled: true
```

#### 添加自定义新闻源
你可以添加其他RSS新闻源：

```yaml
- name: "自定义新闻源"
  type: "rss"
  url: "https://example.com/rss.xml"
  enabled: true
```

#### 注意
以下新闻源已验证不可用或需要特殊处理，已暂时禁用：
- Reuters: DNS解析失败
- Financial Times: 404错误
- MarketWatch: 403禁止访问
- 新浪财经: 404错误
- 腾讯财经: 301重定向
- 网易财经: 404错误
- 和讯网: 需要JavaScript处理
- 东方财富网: 无RSS内容
- 澎湃新闻: 302重定向

### 技术指标配置

在 `config/config.yaml` 中可以调整技术指标参数：

```yaml
indicators:
  ma:
    periods: [5, 10, 20, 60]  # MA 周期
  macd:
    fast: 12
    slow: 26
    signal: 9
  rsi:
    period: 14
    overbought: 70  # 超买阈值
    oversold: 30  # 超卖阈值
  bollinger:
    period: 20
    std_dev: 2  # 标准差倍数
```

## 常见问题

### Q1: pip 安装失败

**问题**: `ta-lib` 安装失败

**解决方案**:
```bash
# Mac
brew install ta-lib

# Ubuntu/Debian
sudo apt-get install ta-lib

# Windows
# 从 https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib 下载预编译包
# 然后安装: pip install TA_Lib-0.4.xx-cpxx-cpxx-win_amd64.whl
```

### Q2: iTick API 返回 401

**问题**: API Token 无效

**解决方案**:
1. 检查 `.env` 文件中的 token 是否正确
2. 访问 iTick 控制台重新生成 token
3. 确保没有多余的空格或引号

### Q3: LLM API 超时

**问题**: LLM 请求超时

**解决方案**:
1. 增加 `timeout` 参数（如 120 秒）
2. 使用更快的模型（如 gpt-3.5-turbo）
3. 检查网络连接

### Q4: 虚拟环境激活失败

**问题**: 无法激活虚拟环境

**解决方案**:
```bash
# 删除旧的虚拟环境
rm -rf venv

# 重新创建
python3 -m venv venv

# 激活
source venv/bin/activate
```

### Q5: 新闻抓取失败

**问题**: 无法获取新闻

**解决方案**:
1. 检查网络连接
2. 增加 `config.yaml` 中的 `timeout` 值
3. 暂时禁用有问题的新闻源

### Q6: 新闻情感分析不准确

**问题**: 情感分析结果与实际新闻内容不符

**解决方案**:
1. 检查 `config/keywords.txt` 是否包含相关关键词
2. 调整新闻源的 `enabled` 设置，只启用高质量的新闻源
3. 更新情感词典（修改 `src/analyzers/news_sentiment.py` 中的词汇列表）

### Q7: 新闻抓取速度慢

**问题**: 新闻抓取占用太多时间

**解决方案**:
1. 减少 `news.max_articles` 的值
2. 启用缓存功能（`news.cache_duration`）
3. 禁用不必要的新闻源
4. 增加 `news.fetch.delay` 减少请求频率

## 运行示例

### 基本运行

```bash
# 分析所有品种（黄金和白银），包含新闻情感分析
python src/main.py

# 只分析黄金
python src/main.py --instrument gold

# 只分析白银
python src/main.py --instrument silver

# 指定时间周期
python src/main.py --timeframe 4h

# 调试模式
python src/main.py --debug

# 禁用新闻功能
python src/main.py --no-news
```

### 使用启动脚本

```bash
# 基本运行
./start.sh

# 传递参数
./start.sh --instrument gold --timeframe 4h
```

## 查看报告

生成的报告保存在 `output/reports/` 目录：

```bash
# 查看最新的报告
ls -lt output/reports/ | head -5

# 查看报告内容
cat output/reports/report_XAUUSD_20260127_101523.md
```

## Docker 部署（推荐）

MetalTrend AI 支持使用 Docker 进行快速部署，支持定时任务自动执行分析。

### 快速开始

```bash
# 1. 构建并启动容器
docker-compose up -d

# 2. 查看日志
docker-compose logs -f

# 3. 停止容器
docker-compose down
```

### 配置定时任务

使用 `CRON_SCHEDULE` 环境变量设置定时执行分析（Cron 格式）：

```bash
# 每天早上 9 点执行分析
docker-compose run -e CRON_SCHEDULE="0 9 * * *" metal-trend-analysis

# 每小时执行一次分析
docker-compose run -e CRON_SCHEDULE="0 * * * *" metal-trend-analysis

# 工作日早上 9 点执行分析
docker-compose run -e CRON_SCHEDULE="0 9 * * 1-5" metal-trend-analysis

# 每 30 分钟执行一次分析
docker-compose run -e CRON_SCHEDULE="*/30 * * * *" metal-trend-analysis
```

### 自定义配置参数

在 `docker-compose.yml` 或通过环境变量配置：

```bash
# 指定分析品种（gold/silver/all）
docker-compose run -e INSTRUMENT=gold metal-trend-analysis

# 指定时间周期（1m, 5m 等）
docker-compose run -e TIMEFRAME=4h metal-trend-analysis

# 自定义时区
docker-compose run -e TZ=America/New_York metal-trend-analysis
```

### Cron 格式说明

```
┌───────────── 分钟 (0 - 59)
│ ┌───────────── 小时 (0 - 23)
│ │ ┌───────────── 日 (1 - 31)
│ │ │ ┌───────────── 月 (1 - 12)
│ │ │ │ ┌───────────── 星期 (0 - 6) (0=周日)
│ │ │ │ │
* * * * * 命令
```

**示例**:
- `0 9 * * *` - 每天 9:00
- `0 */2 * * *` - 每 2 小时
- `*/30 * * * *` - 每 30 分钟
- `0 9 * * 1-5` - 工作日 9:00
- `0 9,18 * * *` - 每天 9:00 和 18:00

### 数据持久化

容器会自动挂载以下目录，数据会持久化到宿主机：

- `./config` - 配置文件目录
- `./data` - 数据缓存目录
- `./output` - 输出目录（报告、日志）

### 查看输出

```bash
# 查看容器日志
docker-compose logs -f

# 查看生成的报告
ls -lt output/reports/

# 查看分析日志
tail -f output/logs/app.log

# 查看定时任务日志
tail -f output/logs/cron.log
```

### 手动执行分析

如果不使用定时任务，可以手动执行一次分析：

```bash
# 方式 1：不设置 CRON_SCHEDULE
docker-compose run --rm -e CRON_SCHEDULE= metal-trend-analysis

# 方式 2：直接运行 Python 脚本
docker-compose run --rm metal-trend-analysis python src/main.py --instrument all
```

## 下一步

配置完成后，你可以：

1. **定期分析**: 使用 cron 或定时任务定期运行
2. **自定义配置**: 根据需求调整技术指标参数
3. **扩展功能**: 添加新的技术指标或新闻源
4. **数据可视化**: 集成图表库生成可视化报告

## 技术支持

如有问题，请查看：
- README.md - 项目说明
- output/logs/app.log - 运行日志
- 使用 `--debug` 参数运行查看详细信息

---

**祝使用愉快！**
