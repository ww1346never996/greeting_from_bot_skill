#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import time

# 基础路径配置
WORKSPACE = "/home/admin/.openclaw/workspace"
CURSOR_FILE = os.path.join(WORKSPACE, "memory_cursor.json")
DRAFT_FILE = os.path.join(WORKSPACE, "memory", "hourly_draft.md")

# 【注意】你需要确认刚才那个大 JSON 文件的确切路径
# 根据 OpenClaw 架构，通常在 agents/main 目录下，假设叫 state.json 或 sessions.json
STATE_JSON_PATH = "/home/admin/.openclaw/agents/main/sessions.json" 
QQ_ID = ""

def get_last_cursor():
    if os.path.exists(CURSOR_FILE):
        with open(CURSOR_FILE, "r") as f:
            return json.load(f).get("last_timestamp_ms", 0)
    return int((time.time() - 3600) * 1000)

def save_cursor(timestamp_ms):
    with open(CURSOR_FILE, "w") as f:
        json.dump({"last_timestamp_ms": timestamp_ms}, f)

def get_target_session_file():
    """从状态 JSON 中动态获取当前 QQ 主会话的 jsonl 路径"""
    if not os.path.exists(STATE_JSON_PATH):
        print(f"❌ 找不到状态文件: {STATE_JSON_PATH}")
        return None
        
    try:
        with open(STATE_JSON_PATH, "r", encoding="utf-8") as f:
            state_data = json.load(f)
            
        session_key = f"qq:{QQ_ID}"
        if session_key in state_data:
            return state_data[session_key].get("sessionFile")
    except Exception as e:
        print(f"❌ 解析状态文件失败: {e}")
        
    return None

def fetch_raw_messages(since_ts_ms):
    target_file = get_target_session_file()
    
    if not target_file or not os.path.exists(target_file):
        print("❌ 无法定位到 QQ 专属会话文件。")
        return []

    new_messages = []
    print(f"🔍 锁定目标文件: {target_file}")
    
    with open(target_file, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                event = json.loads(line)
                ts_ms = event.get("createdAtMs") or event.get("timestamp") or 0
                
                if ts_ms > since_ts_ms:
                    role = event.get("role")
                    content = event.get("content") or event.get("message")
                    
                    if role in ["user", "assistant", "model"] and content and isinstance(content, str):
                        new_messages.append({
                            "role": "User" if role == "user" else "OpenClaw",
                            "content": content,
                            "ts_ms": ts_ms
                        })
            except json.JSONDecodeError:
                continue

    new_messages.sort(key=lambda x: x["ts_ms"])
    return new_messages

def main():
    last_ts_ms = get_last_cursor()
    new_messages = fetch_raw_messages(last_ts_ms)
    
    if not new_messages:
        print("这小时内没有新对话。")
        return

    draft_content = "\n".join([
        f"- [{time.strftime('%m-%d %H:%M', time.localtime(m['ts_ms'] / 1000))}] {m['role']}: {m['content']}" 
        for m in new_messages
    ])
    
    os.makedirs(os.path.dirname(DRAFT_FILE), exist_ok=True)
    with open(DRAFT_FILE, "a", encoding="utf-8") as f:
        f.write(draft_content + "\n")
        
    save_cursor(new_messages[-1]['ts_ms'])
    print(f"✅ 成功抓取 {len(new_messages)} 条新消息并写入 {DRAFT_FILE}")

if __name__ == "__main__":
    main()