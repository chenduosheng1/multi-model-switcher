# 429 Failover 隔离原型：给真实开发者看的说明

> 这不是线上产品，不改生产，不收钱，不承诺 SLA。只用于收集真实反馈和使用意愿。

## 我遇到什么问题时用得上

- 单模型上游 429 / 5xx / 529，自动化流程中断。
- 客户端把 429 变 400，丢掉 `Retry-After`。
- 模型名变更或下线，`model not found`。
- HTTP 200，但 content 为空 / tool_calls 缺参数 / finish_reason 异常。

真实来源：
- OpenAI 429 官方排障：https://help.openai.com/en/articles/5955604-how-can-i-solve-429-too-many-requests-errors
- Open WebUI #31326：https://github.com/open-webui/open-webui/issues/31326
- Dify #29464：https://github.com/langgenius/dify/issues/29464
- OpenAI status 事故页：https://status.openai.com/incidents/01KT5XJ5ATD6RMYP908WS69FVD/write-up

## 原型验证了什么

隔离模拟 20 次请求：
- 单上游：成功 10 / 20
- 带 failover：成功 20 / 20
- fallback 使用：15 次

这不是真实客户结果，只是说明「策略代码能跑」。

证据：`D:/PY_Scripts/growth/failover_experiment/failover_probe_result.json`

## 想请你回答 3 个问题

1. 你实际遇到 429 / 上游故障的频率？
2. 现在怎么处理：重试、切模型、排队，还是人工修？
3. 如果统一网关能自动切备用模型并给错误诊断，你愿意为此付费吗？愿意为什么价值付费？

不需要 API Key，不需要注册，不需要改生产。

## 如果只是想先跑 5PCloud 首调

注册并创建 Key：
https://5pcloud.top/register.html?utm_source=github&utm_medium=demo_page&utm_campaign=failover_20261106&utm_content=20261106_failover_demo&utm_id=c_20261106_failover_demo

5 分钟 Quickstart：
https://github.com/chenduosheng1/multi-model-switcher
