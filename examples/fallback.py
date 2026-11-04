# -*- coding: utf-8 -*-
"""examples/fallback.py — 便宜模型挂了自动升级的真实演示。

跑法:
    LLM_BASE_URL=https://你的站/v1 LLM_API_KEY=sk-xxx python examples/fallback.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from switcher.client import SmartClient

c = SmartClient(
    base_url=os.environ["LLM_BASE_URL"],
    api_key=os.environ["LLM_API_KEY"],
    chain=["deepseek-v4.1-flash", "deepseek-v4-pro", "gpt-6.1-sol"],
)

# 正常场景: 第一档就成功
r1 = c.chat("用一句话介绍哈希表")
print("[OK]", r1["model"], "->", r1["text"][:80])

# 模拟降级: 故意把链路放一个不存在的模型名, 观察自动跳过
c2 = SmartClient(base_url=c.base_url, api_key=c.api_key,
                 chain=["not-exist-model-xxx", "deepseek-v4.1-flash"])
r2 = c2.chat("用一句话介绍二分查找")
print("[FALLBACK OK]", r2["model"], "->", r2["text"][:80])
