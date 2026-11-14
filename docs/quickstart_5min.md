# 5 分钟首调 Quickstart（5PCloud）

> 目标：注册 → 拿 Key → 跑通第一次 API 调用。OpenAI 兼容，DeepSeek / GPT 系都行。

## 1. 注册建 Key

打开 https://5pcloud.top/register.html （送 1000 万 Token，不绑卡）。
登录控制台 → 创建 API Key，复制保存。

## 2. Python 跑通

```python
import openai

client = openai.OpenAI(
    base_url="https://5pcloud.top/v1",
    api_key="你的KEY",
)

r = client.chat.completions.create(
    model="deepseek-v4.1-flash-1017",
    messages=[{"role": "user", "content": "用一句话解释什么是上下文窗口"}],
)
print(r.choices[0].message.content)
```

## 3. 命令行一行验证

```bash
curl https://5pcloud.top/v1/chat/completions \
  -H "Authorization: Bearer 你的KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-v4.1-flash-1017","messages":[{"role":"user","content":"hi"}]}'
```

## 4. 接 Cherry Studio / Open WebUI / n8n

Base URL 统一填 `https://5pcloud.top/v1`，Key 用控制台创建的。
三端详细模板见 [baseurl_config_pack.md](baseurl_config_pack.md)。

## 常见坑

- 漏 `/v1` → 404
- Key 带空格 → 401
- 429 先查余额再退避，别盲重试（见 [429_troubleshooting.md](429_troubleshooting.md)）

追踪：utm_source=github&utm_medium=quickstart&utm_campaign=quickstart_5min_20261106&utm_content=20261106_first_call&utm_id=c_20261106_quickstart_5min
