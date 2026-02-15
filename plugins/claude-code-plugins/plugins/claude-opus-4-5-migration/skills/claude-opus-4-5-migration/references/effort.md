# 努力参数（Beta）

**在迁移期间添加设置为 `"high"` 的努力参数。** 这是 Opus 4.5 获得最佳性能的默认配置。

## 概述

努力参数控制 Claude 使用令牌的积极程度。它影响所有令牌：思考、文本响应和函数调用。

| 努力级别 | 使用场景 |
|--------|----------|
| `high` | 最佳性能，深度推理（默认） |
| `medium` | 成本/延迟与性能之间的平衡 |
| `low` | 简单的高容量查询；显著节省令牌 |

## 实现

在 API 调用中需要 beta 标志 `effort-2025-11-24`。

**Python SDK:**
```python
response = client.messages.create(
    model="claude-opus-4-5-20251101",
    max_tokens=1024,
    betas=["effort-2025-11-24"],
    output_config={
        "effort": "high"  # or "medium" or "low"
    },
    messages=[...]
)
```

**TypeScript SDK:**
```typescript
const response = await client.messages.create({
  model: "claude-opus-4-5-20251101",
  max_tokens: 1024,
  betas: ["effort-2025-11-24"],
  output_config: {
    effort: "high"  // or "medium" or "low"
  },
  messages: [...]
});
```

**Raw API:**
```json
{
  "model": "claude-opus-4-5-20251101",
  "max_tokens": 1024,
  "anthropic-beta": "effort-2025-11-24",
  "output_config": {
    "effort": "high"
  },
  "messages": [...]
}
```

## 努力参数与思考预算

努力参数独立于思考预算：

- 高努力 + 无思考 = 更多令牌，但没有思考令牌
- 高努力 + 32k 思考 = 更多令牌，但思考上限为 32k

## 建议

1. 首先确定努力级别，然后设置思考预算
2. 最佳性能：高努力 + 高思考预算
3. 成本/延迟优化：中等努力
4. 简单的高容量查询：低努力
