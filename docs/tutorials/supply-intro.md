# 物资供应链存证 · 教学 Demo

> **plugin_id**: `edu.cn.gov.supply`  
> **TaskType**: `CN_SUPPLY_CHAIN_DEMO`  
> **Namespace**: `ns-domain-cn` · **chainId**: `fabric-local`

## 教学目标

演示物资**出入库存证算法**：每条记录携带前序哈希，形成可校验的哈希链，并计算 Merkle 根用于批次摘要。

## 功能说明

- 入库（inbound）、调拨（transfer）、出库（outbound）事件序列
- 校验前序哈希链接与载荷哈希一致性
- 输出库存余额与 Merkle 根

## 合规说明

- 全部数据为虚构，不对接真实 WMS/ERP
- 不涉及军队、涉密、作战表述
- 禁止「国资 30 年生产归档」等产品承诺
- 信创相关表述仅限「信创适配清单参考（文档级）」

## 联调示例

```bash
curl -X POST http://127.0.0.1:8080/api/v1/labs/edu.cn.gov.supply/simulate \
  -H 'Content-Type: application/json' \
  -d '{
    "user_prompt": "物资存证校验",
    "params": { "ledger": "sample" },
    "allowed_chain_ids": ["fabric-local"]
  }'
```

## 样例数据

见 `plugins/supply/fixtures/sample-ledger.json`。
