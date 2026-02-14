#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import datetime

WORKSPACE = "/home/admin/.openclaw/workspace"
DRAFT_FILE = os.path.join(WORKSPACE, "memory", "hourly_draft.md")
MEMORY_PROFILE = os.path.join(WORKSPACE, "MEMORY.md")

def summarize_with_llm(draft_content):
    # 构建强大的 Prompt，强迫 LLM 做三件事：日记、事实、清理
    prompt = f"""
    你是 OpenClaw 的记忆整理模块。以下是用户昨天的所有原始聊天记录草稿：
    
    <draft>
    {draft_content}
    </draft>
    
    请执行以下任务并返回 JSON 格式：
    1. "diary": 生成一段 150 字以内的昨日总结（第一人称视角，例如"今天用户和我聊了..."）。
    2. "new_facts": 提取出用户新的长期事实或偏好（比如"决定去杭州"），如果没有则为空列表。
    """
    
    # 伪代码：调用你的大模型 API
    # response = llm.chat(prompt, response_format="json")
    # return json.loads(response)
    pass

def main():
    if not os.path.exists(DRAFT_FILE):
        print("昨日无对话，无需整理。")
        return

    with open(DRAFT_FILE, "r", encoding="utf-8") as f:
        draft_content = f.read().strip()
        
    if not draft_content:
        return

    # 1. 调用大模型进行浓缩
    result = summarize_with_llm(draft_content)
    
    # 2. 写入每日日记 (YYYY-MM-DD.md)
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    diary_path = os.path.join(WORKSPACE, "memory", f"{yesterday}.md")
    
    with open(diary_path, "w", encoding="utf-8") as f:
        f.write(f"# {yesterday} 日记\n\n{result['diary']}")
        
    # 3. (可选) 如果有 new_facts，你可以写逻辑追加到 MEMORY.md 中
    
    # 4. 【退出机制：极其重要】清空草稿箱！
    # 使用 "w" 模式重新打开文件，直接清空，为新的一天腾出位置
    open(DRAFT_FILE, 'w').close()
    print(f"✅ {yesterday} 记忆压缩完毕，已清空 Draft。")

if __name__ == "__main__":
    main()