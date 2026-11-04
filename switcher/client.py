# -*- coding: utf-8 -*-
"""SmartClient: OpenAI 兼容多模型降级链客户端。

便宜模型在前, 超时/报错自动升级下一档, 全挂才抛。
依赖: pip install requests
"""
import time
import requests


class SmartClient:
    def __init__(self, base_url, api_key, chain, timeout=60):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.chain = list(chain)          # ["flash模型", "pro模型", ...]
        self.timeout = timeout
        self.last_errors = {}             # debug 用

    def chat(self, prompt, tier=None, temperature=0.7, max_tokens=2048):
        """tier=None 按链路从便宜到贵; tier="pro" 直接用链路最后一档。"""
        models = [self.chain[-1]] if tier == "pro" else self.chain
        errors = []
        for m in models:
            try:
                r = requests.post(
                    self.base_url + "/chat/completions",
                    headers={"Authorization": "Bearer " + self.api_key,
                             "Content-Type": "application/json"},
                    json={"model": m,
                          "messages": [{"role": "user", "content": prompt}],
                          "temperature": temperature,
                          "max_tokens": max_tokens},
                    timeout=self.timeout)
                data = r.json()
                if r.status_code == 200 and data.get("choices"):
                    return {"text": data["choices"][0]["message"]["content"],
                            "model": m, "usage": data.get("usage")}
                errors.append(f"{m}: HTTP {r.status_code} {str(data)[:120]}")
            except (requests.Timeout, requests.ConnectionError) as e:
                errors.append(f"{m}: {type(e).__name__}")
        raise RuntimeError("全链路失败:\n" + "\n".join(errors))

    def chat_stream(self, prompt, **kw):
        """流式: 逐块 yield 文本。走链路第一档, 失败不自动升级(简化)。"""
        r = requests.post(
            self.base_url + "/chat/completions",
            headers={"Authorization": "Bearer " + self.api_key,
                     "Content-Type": "application/json"},
            json={"model": self.chain[0], "stream": True,
                  "messages": [{"role": "user", "content": prompt}], **kw},
            timeout=self.timeout, stream=True)
        r.raise_for_status()
        for line in r.iter_lines():
            if not line or not line.startswith(b"data: "):
                continue
            chunk = line[6:].decode("utf-8", "ignore")
            if chunk == "[DONE]":
                return
            import json
            delta = json.loads(chunk)["choices"][0].get("delta", {})
            if delta.get("content"):
                yield delta["content"]


if __name__ == "__main__":
    import os
    c = SmartClient(
        base_url=os.environ["LLM_BASE_URL"],
        api_key=os.environ["LLM_API_KEY"],
        chain=["deepseek-v4.1-flash", "deepseek-v4-pro"],
    )
    print(c.chat("用一句话介绍快速排序")["text"])
