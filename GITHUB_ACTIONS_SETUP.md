# GitHub Actions 部署指南

## 📋 提交到 GitHub 前的准备

### 1. 创建 .gitignore 文件

确保敏感信息不会被提交：

```bash
# 在项目根目录创建 .gitignore
cat > .gitignore << 'EOF'
# 环境变量和敏感信息
.env
.env.local
.env.*.local

# 输出文件
output/
*.log

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
EOF
```

### 2. 提交代码到 GitHub

```bash
# 初始化 Git（如果还没初始化）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Gold & Silver Analysis System"

# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 推送
git push -u origin main
```

---

## 🔐 配置 GitHub Secrets

进入你的 GitHub 仓库 → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

需要添加以下 Secrets：

| Secret Name | Value | 说明 |
|-------------|-------|------|
| `LLM_API_KEY` | `sk-54f9bcd598b244ecbefc4d8b7fc19a93` | 通义千问 API Key |
| `LLM_BASE_URL` | `https://dashscope.aliyuncs.com/compatible-mode/v1` | 通义千问 API 地址 |
| `LLM_MODEL_NAME` | `qwen-max` | 模型名称 |
| `FEISHU_WEBHOOK_URL` | `https://open.feishu.cn/open-apis/bot/v2/hook/...` | 飞书机器人 Webhook |

### 可选的其他通知渠道

| Secret Name | 说明 |
|-------------|------|
| `DINGTALK_WEBHOOK_URL` | 钉钉机器人 Webhook |
| `SLACK_WEBHOOK_URL` | Slack Incoming Webhook |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID |
| `EMAIL_FROM` | 发件邮箱 |
| `EMAIL_PASSWORD` | 邮箱授权码 |
| `EMAIL_TO` | 收件邮箱 |
| `EMAIL_SMTP_SERVER` | SMTP 服务器 |
| `EMAIL_SMTP_PORT` | SMTP 端口 |

---

## 🚀 运行方式

### 方式一：自动定时运行

GitHub Actions 已配置为：
- **北京时间 09:00** (UTC 01:00)
- **北京时间 21:00** (UTC 13:00)
- **周一到周五** 自动运行

### 方式二：手动触发

1. 进入 GitHub 仓库 → **Actions** 标签
2. 选择 **Gold & Silver Analysis** 工作流
3. 点击 **Run workflow**
4. 选择要分析的品种：
   - `all` - 分析黄金和白银
   - `gold` - 只分析黄金
   - `silver` - 只分析白银
5. 点击 **Run workflow**

---

## 📊 查看运行结果

### 1. 飞书通知

每次运行完成后，飞书群会收到：
- 📊 每日汇总（含金银比）
- 🥇 黄金分析报告（含做单建议）
- 🥈 白银分析报告（含做单建议）

### 2. GitHub Actions 日志

进入 **Actions** → 点击某次运行 → 查看日志

### 3. 下载报告

每次运行会自动上传报告文件：
- 进入 **Actions** → 点击某次运行
- 底部 **Artifacts** 部分
- 下载 `analysis-reports-xxx` 文件

---

## ⚠️ 注意事项

1. **GitHub Actions 免费额度**：
   - 公共仓库：无限制
   - 私有仓库：每月 2000 分钟

2. **API 调用费用**：
   - 通义千问 API 按调用量计费
   - 请确保账户有足够余额

3. **时区问题**：
   - GitHub Actions 使用 UTC 时间
   - 已配置为北京时间 09:00 和 21:00

4. **节假日**：
   - 目前配置为周一到周五运行
   - 如需调整，修改 `.github/workflows/gold-analysis.yml` 中的 cron 表达式

---

## 🔧 故障排查

### 问题：Actions 运行失败

1. 检查 Secrets 是否配置正确
2. 查看 Actions 日志中的错误信息
3. 确认 API Key 余额充足

### 问题：收不到飞书通知

1. 检查 `FEISHU_WEBHOOK_URL` 是否正确
2. 确认飞书机器人没有被禁言
3. 查看 Actions 日志中的通知发送状态

### 问题：数据分析失败

1. 检查网络连接（Yahoo Finance 访问）
2. 查看 `output/logs/app.log` 日志文件
