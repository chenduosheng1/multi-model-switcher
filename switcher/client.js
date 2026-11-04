// SmartClient.js — OpenAI 兼容多模型降级链 (Node 18+, 无依赖, 原生 fetch)

export class SmartClient {
  constructor({ baseUrl, apiKey, chain, timeoutMs = 60000 }) {
    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.apiKey = apiKey;
    this.chain = chain;          // ["便宜模型", "贵模型"]
    this.timeoutMs = timeoutMs;
  }

  async chat(prompt, { tier = null, temperature = 0.7, maxTokens = 2048 } = {}) {
    const models = tier === "pro" ? [this.chain[this.chain.length - 1]] : this.chain;
    const errors = [];
    for (const model of models) {
      try {
        const ctrl = new AbortController();
        const timer = setTimeout(() => ctrl.abort(), this.timeoutMs);
        const r = await fetch(`${this.baseUrl}/chat/completions`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${this.apiKey}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            model,
            messages: [{ role: "user", content: prompt }],
            temperature,
            max_tokens: maxTokens,
          }),
          signal: ctrl.signal,
        });
        clearTimeout(timer);
        const data = await r.json();
        if (r.ok && data.choices?.[0]) {
          return { text: data.choices[0].message.content, model, usage: data.usage };
        }
        errors.push(`${model}: HTTP ${r.status} ${JSON.stringify(data).slice(0, 120)}`);
      } catch (e) {
        errors.push(`${model}: ${e.name}`);
      }
    }
    throw new Error("全链路失败:\n" + errors.join("\n"));
  }
}

// node --input-type=module 测试:
// const c = new SmartClient({baseUrl:"https://你的站/v1", apiKey:"sk-xxx",
//   chain:["deepseek-v4.1-flash","deepseek-v4-pro"]});
// console.log((await c.chat("用一句话介绍快速排序")).text);
