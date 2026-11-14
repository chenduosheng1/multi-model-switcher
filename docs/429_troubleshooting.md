# API 返回 429，不一定是限流：一张排障树

> 模型价格与倍率来自 `https://5pcloud.top/api/pricing`（2026-11-06 抓取）。以控制台实时为准。

很多人看到 429 就狂重试，结果越限越死。先看清是哪一类。

## 429 的三类真因

1. **真限流**：上游 RPM/TPM 满了。看 `error.code` 和响应头 `Retry-After`，按秒退避，别硬冲。
2. **余额/额度不足**：很多网关把"余额不够"也返回 429。先查账户余额，不是速率问题。
3. **客户端误报**：Open WebUI / Dify 等把上游 429 转成 400，丢掉 `Retry-After`，看起来像参数错。

## 排障顺序

```
429
 ├─ 看 error.code / message
 │   ├─ rate_limit_exceeded → 退避 + 降并发
 │   ├─ 余额相关 → 充值，不是重试
 │   └─ 无明确 code → 抓原始响应，别信客户端翻译
 ├─ 看 HTTP 状态码是不是被客户端改过（200/400/429 漂移）
 └─ 看 finish_reason / content 是否为空（假成功）
```

## 用统一网关怎么省心

把多家模型接到一个 OpenAI 兼容端点，上游 429 时自动切备用模型，并保留原始诊断：

```
https://5pcloud.top/v1   # OpenAI 兼容，DeepSeek / GPT 系都可
```

注册建 Key（送 1000 万 Token，不绑卡）：
https://5pcloud.top/register.html?utm_source=github&utm_medium=seo_article&utm_campaign=growth_20261106&utm_content=20261106_429_troubleshooting&utm_id=c_20261106_429
