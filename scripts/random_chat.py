#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import random
import time
from datetime import datetime

# 配置路径 (根据你的 OpenClaw 环境调整)
WORKSPACE = "/home/admin/.openclaw/workspace"
MEMORY_FILE = os.path.join(WORKSPACE, "MEMORY.md")
STATE_FILE = os.path.join(WORKSPACE, "proactive_state.json")

# 1. 静默网关 (Gatekeeper)
def should_trigger():
    now = datetime.now()
    # 勿扰时间 (例如凌晨 1点到 8点)
    if 1 <= now.hour < 8:
        return False
        
    # 冷却时间检查 (距离上次主动发起是否超过 4 小时)
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
            last_time = state.get("last_trigger_time", 0)
            if time.time() - last_time < 4 * 3600:
                return False

    # 随机性抛点 (例如 30% 的概率触发)
    if random.random() > 0.3:
        return False
        
    return True

# 2. 读取上下文与历史记录
def get_context():
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        memory = f.read()
        
    past_topics = []
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            past_topics = json.load(f).get("past_topics", [])
            
    return memory, past_topics

# 3. 构建大模型 Prompt (包含退出机制)
def generate_prompt(memory, past_topics):
    return f"""
你现在要决定是否主动向用户发起一次闲聊。

[当前状态]
时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}
用户画像: {memory}

[防重复机制]
你最近已经主动聊过以下话题，绝对不可重复：
{", ".join(past_topics) if past_topics else "无"}

[你的任务]
1. 结合用户画像（比如摄影、键盘、日常）、当前时间和天气等，想一个**非常自然、简短**的开场白。
2. 就像朋友随口一提，不要像机器人汇报。
3. **【退出机制】** 如果你觉得现在没什么特别有趣或相关的话题，或者你想说的话题和上面列表高度重合，请直接输出纯文本：`SKIP`。

[输出格式要求]
如果是 SKIP，只输出 `SKIP`。
如果决定发起聊天，输出 JSON 格式：
{{
    "topic_tag": "简短的当前话题标签(用于记录，如 '胶片摄影' 或 '夜宵')",
    "message": "你想对用户说的话"
}}
"""

def main():
    if not should_trigger():
        print("未通过静默网关，退出。")
        return

    memory, past_topics = get_context()
    prompt = generate_prompt(memory, past_topics)
    
    # 伪代码：这里替换为你调用 LLM 的实际逻辑
    # response_text = llm_client.chat(prompt)
    response_text = '{"topic_tag": "机械键盘", "message": "看到个好看的75%套件，突然想起来你之前在看键盘，有定下来买哪把吗？"}' 
    
    if response_text.strip() == "SKIP":
        print("大模型判定无新话题，触发退出机制。")
        return
        
    try:
        data = json.loads(response_text)
        message = data["message"]
        new_topic = data["topic_tag"]
        
        # 4. 发送消息 (伪代码，替换为你的 NapCatQQ API)
        # send_to_qq(message)
        print(f"发送消息: {message}")
        
        # 5. 更新状态 (持久化)
        past_topics.append(new_topic)
        # 维护一个长度为 5 的 FIFO 队列，避免无限增长
        if len(past_topics) > 5:
            past_topics.pop(0)
            
        with open(STATE_FILE, "w") as f:
            json.dump({
                "last_trigger_time": time.time(),
                "past_topics": past_topics
            }, f, ensure_ascii=False, indent=2)
            
    except json.JSONDecodeError:
        print("LLM 输出解析失败。")

if __name__ == "__main__":
    main()