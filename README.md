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
