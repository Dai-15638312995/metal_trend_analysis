"""
通知推送模块

支持的渠道：
- 飞书 Webhook
- 钉钉 (DingTalk) Webhook
"""

from .feishu import FeishuNotifier
from .dingtalk import DingTalkNotifier

__all__ = ['FeishuNotifier', 'DingTalkNotifier']
