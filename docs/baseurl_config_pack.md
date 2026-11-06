# 5PCloud 三端 Base URL 配置包

> 模型名与倍率来自 `https://5pcloud.top/api/pricing` 2026-11-06 抓取。以控制台实时模型名为准。

统一 API 地址：`https://5pcloud.top/v1`

不要把 Key 放进 URL。不要把邮箱、密码放进 URL。

## 当前公开模型（只列本站真实名字）

| 模型 | 输入倍率 | 输出倍率 |
|---|---:|---:|
| gpt-6.1-sol | 0.1495 | 5 |
| deepseek-v4.1-flash | 0.4 | 4 |
| deepseek-v4-pro | 1.125 | 3 |
| deepseek-v4.1-flash-1017 | 0.25 | 4 |

## Cherry Studio

- 服务商类型：OpenAI Compatible
- API Host：`https://5pcloud.top/v1`
- API Key：控制台创建
- 模型：`deepseek-v4.1-flash-1017`

## Open WebUI

- Connection：OpenAI Compatible
- `OPENAI_API_BASE_URL=https://5pcloud.top/v1`
- `OPENAI_API_KEY=<5PCLOUD_API_KEY>`
- 模型：`gpt-6.1-sol`

## n8n

- Credential：OpenAI
- Base URL：`https://5pcloud.top/v1`
- API Key：控制台创建
- 模型：`deepseek-v4-pro`

## 三个最常见的 404 / 401 / 429

- 404：漏 `/v1`，或多写了尾斜杠变成 `/v1/v1`。
- 401：Key 没填、Key 失效，或复制时带空格。
- 429：先看 `error.code`、`Retry-After` 和余额；不要盲重试。

## 下一步

注册并创建 Key：https://5pcloud.top/register.html?utm_source=github&utm_medium=config_pack&utm_campaign=e2_baseurl_pack_20261106&utm_content=20261106_baseurl_config_pack&utm_id=c_20261106_e2_baseurl_pack
