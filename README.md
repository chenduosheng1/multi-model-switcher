# Multi Model Switcher · OpenAI 兼容多模型路由示例

一句话：**一份 OpenAI 兼容代码，按"成本/质量"自动切多个模型**，含真实成本对比表和可直接跑的示例。

适合谁：
- 想用 DeepSeek / GPT 系多家模型、不想为每家改代码的开发者
- 在意 Token 成本，想先跑便宜模型、失败自动升级贵模型的应用
- 想要一个中转聚合入口统一管理 Key 的团队

## 目录

```
switcher/
  client.py        # Python：多模型路由客户端（降级链）
  client.js        # Node.js：同功能实现
benchmark/
  cost_table.md    # 真实计费倍率对比（2026-11-04 抓取）
examples/
  chat.py          # 基础对话
  fallback.py      # 便宜模型失败自动升级
  stream.py        # 流式输出
```

## 30 秒上手

```python
from switcher.client import SmartClient

# 任何 OpenAI 兼容端点都行：自建 new-api / one-api / openrouter 等
c = SmartClient(
    base_url="https://你的聚合站地址/v1",
    api_key="sk-xxx",
    chain=["deepseek-v4.1-flash", "deepseek-v4-pro", "gpt-6.1-sol"],
)

print(c.chat("用一句话介绍快速排序"))   # 默认走最便宜的
print(c.chat("复杂推理任务...", tier="pro"))  # 指定高档模型
```

便宜模型超时/报错 → 自动按链路升级 → 全挂才抛异常。

## 为什么这么设计（真实踩坑）

| 问题 | 方案 |
|---|---|
| 单家限流/宕机导致应用挂 | 降级链：flash 挂了自动切 pro |
| 高峰期 flash 延迟飘 | 超时阈值内无响应视为失败，直接升级 |
| 多 Key 管理乱 | 聚合站统一一个 Key，后端配多家 |
| 成本失控 | benchmark/cost_table.md 按倍率算钱，先估后调 |

## 真实成本对比（倍率越低越便宜）

| 模型 | 输入倍率 | 输出倍率 | 相对成本 |
|---|---|---|---|
| deepseek-v4.1-flash-1017 | 0.25 | 4x | 最便宜 |
| gpt-6.1-sol | 0.1495 | 5x | 输入最便宜之一 |
| deepseek-v4.1-flash | 0.4 | 4x | 便宜 |
| deepseek-v4-pro | 1.125 | 3x | 高档 |

完整表见 [benchmark/cost_table.md](benchmark/cost_table.md)（含同任务多模型实测输出质量主观评分）。

## 免责与说明

- cost_table 倍率抓自公开 pricing 接口，会随时间变化，以你的站点为准
- 本仓库不绑定任何服务商：`base_url` 填你自己的即可（自建 new-api/one-api/官方 API/OpenRouter 均兼容）
- 示例代码 MIT 许可，随便用

## 贡献

发现某个聚合站/模型的兼容性问题，欢迎开 issue 附上报错原文。
## 429 Failover：为什么值得内置

单一模型上游一挂，应用就跟着挂。最常见的不是「模型不够聪明」，而是这几类：

- HTTP 429：真限流、余额耗尽、spend limit、TPM/RPM 超限。
- HTTP 5xx / 529：上游过载或短暂故障。
- 模型下线 / 改名：`model not found`，旧 slug 失效。
- HTTP 200 但输出结构坏：content 为空、tool_calls 缺参数、finish_reason 异常。

盲重试会拖垮队列。正确做法是先分类，再决定「等、换、停」。

## 最小决策表

| 返回 | 先看什么 | 动作 |
|---|---|---|
| 429 | `error.code`、`Retry-After`、余额/限额 | 真限流才退避；余额/额度问题立刻停并提示 |
| 5xx / 529 | 上游状态、超时时间 | 快速失败，切备用模型 |
| 404 / model not found | `/v1/models` 与控制台模型名 | 更新模型名，不反复撞旧名 |
| 200 但结构坏 | content / finish_reason / tool_calls | 判为失败，切备用或直接报错 |

## 最小 Python 逻辑

```python
def call_with_fallback(client, models, prompt):
    for model in models:
        r = client.chat(model, prompt)
        if r.status == 429 and not r.retry_after:
            continue                   # 可能是余额/额度问题，不盲重试
        if r.status in (429, 500, 502, 503, 529):
            continue                   # 切下一个模型
        if r.status == 200 and r.content_valid:
            return r
    raise RuntimeError("全部上游不可用")
```

真正上线还要做：结构化日志、按内容 ID 归因、预算闸门、输出结构校验、流式断流处理。

## 用一个统一入口少写一层胶水代码

5PCloud 提供 OpenAI 兼容端点 `https://5pcloud.top/v1`。  
如果你正在自己维护多个模型 Key 和 fallback 链，可以先拿体验额度跑一遍最小请求：

https://5pcloud.top/register.html?utm_source=github&utm_medium=readme&utm_campaign=failover_20261106&utm_content=20261106_failover_github&utm_id=c_20261106_failover_github

> 说明：Failover 原型目前在隔离环境验证，不代表线上已默认提供。不要把它当 SLA 承诺。

想看隔离验证和反馈问题：[429 Failover demo](docs/failover_demo.md)
