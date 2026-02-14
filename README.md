# 请按下面的方法配置cron job

```json
[
  {
    "id": "memory-hourly-gatherer",
    "agentId": "main",
    "name": "每小时记忆拾荒",
    "enabled": true,
    "schedule": {
      "kind": "cron",
      "expr": "0 * * * *", 
      "tz": "Asia/Shanghai"
    },
    "sessionTarget": "isolated",
    "wakeMode": "immediate",
    "payload": {
      "kind": "agentTurn",
      "message": "Use the exec/shell tool to forcefully run: `/usr/bin/python3 /home/admin/.openclaw/workspace/skills/memory-learner/scripts/hourly_gatherer.py`. Reply 'OK' when done.",
      "timeoutSeconds": 60
    },
    "delivery": { "channel": "qq", "to": "heartbeat" } 
  },
  {
    "id": "memory-daily-synthesizer",
    "agentId": "main",
    "name": "每日记忆浓缩与清理",
    "enabled": true,
    "schedule": {
      "kind": "cron",
      "expr": "0 4 * * *", 
      "tz": "Asia/Shanghai"
    },
    "sessionTarget": "isolated",
    "wakeMode": "immediate",
    "payload": {
      "kind": "agentTurn",
      "message": "Use the exec/shell tool to forcefully run: `/usr/bin/python3 /home/admin/.openclaw/workspace/skills/memory-learner/scripts/daily_routine.py`. Inform me of the summary and confirm the draft was cleared.",
      "timeoutSeconds": 180
    },
    "delivery": { "channel": "qq", "mode": "announce", "to": "291724540" }
  },
  {
    "id": "proactive-random-chat",
    "agentId": "main",
    "name": "随机主动搭话嗅探",
    "enabled": true,
    "schedule": {
      "kind": "cron",
      "expr": "30 * * * *", 
      "tz": "Asia/Shanghai"
    },
    "sessionTarget": "isolated",
    "wakeMode": "immediate",
    "payload": {
      "kind": "agentTurn",
      "message": "Use the exec/shell tool to forcefully run: `/usr/bin/python3 /home/admin/.openclaw/workspace/skills/memory-learner/scripts/random_chat.py`. If it outputs messages, do not repeat them to me, just reply 'Chat handled'.",
      "timeoutSeconds": 120
    },
    "delivery": { "channel": "qq", "to": "heartbeat" }
  }
]
```