# 物资供应链存证 · 分步实验

> **插件**: `edu.cn.gov.supply` · **TaskType**: `CN_SUPPLY_CHAIN_DEMO` · **chainId**: `fabric-local`  
> **数据**: `plugins/supply/fixtures/sample-ledger.json` · **Job**: `k8s/overlays/ns-domain-cn/supply-job.yaml`  
> **路线**: [GOV_LEARNING_PATH.md](../GOV_LEARNING_PATH.md) 第 3 步

---

## 学习目标

- 理解出入库事件的**前序哈希链**与载荷哈希校验  
- 使用 **库存曲线** 跟踪 inbound/transfer/outbound  
- 开启「模拟断链」观察 `chain_intact=false`  

---

## 前置条件

- 主库 backend 已启动  

---

## 分步实验

### 步骤 1：打开 Lab

`http://127.0.0.1:5173/labs/edu.cn.gov.supply`

### 步骤 2：正常链

1. 不勾选「模拟断链」  
2. 提交校验 → `chain_intact=true` · balance=85  

### 步骤 3：断链演示

1. 勾选 **模拟哈希链断点**  
2. 提交 → eval-card 显示链异常 · `chain_intact=false`  

### 步骤 4：curl 验证

```bash
curl -s -X POST http://127.0.0.1:8080/api/v1/labs/edu.cn.gov.supply/simulate \
  -H 'Content-Type: application/json' \
  -d '{
    "user_prompt": "物资存证校验",
    "params": {
      "ledger": "sample",
      "asset_id": "MAT-2024-DEMO-001",
      "simulate_break": true
    },
    "allowed_chain_ids": ["fabric-local"],
    "task_type": "CN_SUPPLY_CHAIN_DEMO"
  }' | jq '.evaluation.audit_hints[:3]'
```

**期望**：`simulate_break=true` · `chain_intact=false`。

### 步骤 5：自检清单

- [ ] 库存曲线三行结存正确（100 → 100 → 85）  
- [ ] 哈希链示意在断链时高亮第 3 节  
- [ ] Fabric 通道 `edu-cn-gov-sandbox`  

---

## 合规说明

- 不对接真实 WMS/ERP · 信创表述仅限文档级参考  

---

> **合规脚注** · 虚构数据 only · Fabric 沙箱 only · 不对接真实 WMS/ERP
