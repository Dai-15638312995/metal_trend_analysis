#!/bin/bash
# Docker 容器启动脚本

set -e

# 确保必要的目录存在
mkdir -p /app/data/cache
mkdir -p /app/output/reports
mkdir -p /app/output/logs

# 设置时区
export TZ=${TZ:-Asia/Shanghai}
ln -snf /usr/share/zoneinfo/$TZ /etc/localtime 2>/dev/null || true
echo $TZ > /etc/timezone

echo "======================================"
echo "Metal Trend Analysis Docker"
echo "======================================"
echo "Timezone: $TZ"
echo "Instrument: ${INSTRUMENT:-all}"
echo "Timeframe: ${TIMEFRAME:-default}"
echo "Feishu enabled: $([ -n "$FEISHU_WEBHOOK_URL" ] && echo 'true' || echo 'false')"
echo "DingTalk enabled: $([ -n "$DINGTALK_WEBHOOK_URL" ] && echo 'true' || echo 'false')"
echo "Slack enabled: $([ -n "$SLACK_WEBHOOK_URL" ] && echo 'true' || echo 'false')"
echo "Telegram enabled: $([ -n "$TELEGRAM_BOT_TOKEN" ] && echo 'true' || echo 'false')"
echo "Email enabled: $([ -n "$EMAIL_FROM" ] && echo 'true' || echo 'false')"
echo "======================================"

# 如果设置了定时任务，使用 cron
if [ -n "$CRON_SCHEDULE" ]; then
    echo "Installing cron job: $CRON_SCHEDULE"

    # 创建 cron 日志文件
    touch /app/output/logs/cron.log

    # 安装 cron 任务
    echo "$CRON_SCHEDULE cd /app && python src/main.py --instrument ${INSTRUMENT:-all} ${TIMEFRAME:+--timeframe $TIMEFRAME} >> /app/output/logs/cron.log 2>&1" | crontab -

    # 启动 cron 守护进程
    echo "Starting cron daemon..."
    service cron start

    echo "Waiting for cron jobs..."
    echo "View logs: docker logs -f <container_name>"
    echo "======================================"

    # 保持容器运行并查看日志
    tail -f /app/output/logs/cron.log 2>/dev/null || sleep infinity
else
    echo "No CRON_SCHEDULE set, running once..."
    echo "======================================"

    # 执行一次分析
    exec python src/main.py --instrument ${INSTRUMENT:-all} ${TIMEFRAME:+--timeframe $TIMEFRAME}
fi
