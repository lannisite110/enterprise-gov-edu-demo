# 多级多签审批 · 分步实验

> **插件**: `edu.cn.gov.multisig` · **TaskType**: `CN_MULTISIG_APPROVAL_DEMO` · **chainId**: Sepolia `11155111`  
> **合约**: `plugins/contracts/MultiSigApprovalDemo.sol` · **Job**: `k8s/overlays/ns-domain-cn/multisig-job.yaml`  
> **路线**: [GOV_LEARNING_PATH.md](../GOV_LEARNING_PATH.md) 第 2 步

---

## 学习目标

- 理解 M-of-N 多签**权限模型**（confirm / execute 分离）  
- 通过 UI **逐步勾选**签名人观察 `approved` hints  
- 了解 Sepolia 测试网合约模板定位  

---

## 前置条件

- 建议先完成 [bid-graph-intro.md](bid-graph-intro.md)  
- 主库 backend 已启动  

---

## 分步实验

### 步骤 1：打开 Lab

`http://127.0.0.1:5173/labs/edu.cn.gov.multisig`

### 步骤 2：未达阈值

1. 阈值设为 `2`  
2. 仅勾选 **Owner 1**  
3. 提交 → `approved=false` · status=pending  

### 步骤 3：达阈值

1. 勾选 Owner 1 + Owner 2  
2. 提交 → `approved=true` · status=approved  

### 步骤 4：curl 验证

```bash
curl -s -X POST http://127.0.0.1:8080/api/v1/labs/edu.cn.gov.multisig/simulate \
  -H 'Content-Type: application/json' \
  -d '{
    "user_prompt": "多签审批演示",
    "params": {
      "proposal_id": "PROPOSAL-DEMO-001",
      "threshold": 2,
      "confirmations": [
        "0x1111111111111111111111111111111111111111",
        "0x2222222222222222222222222222222222222222"
      ]
    },
    "allowed_chain_ids": [11155111],
    "task_type": "CN_MULTISIG_APPROVAL_DEMO"
  }' | jq '.evaluation.audit_hints'
```

### 步骤 5：自检清单

- [ ] 进度条随勾选变化  
- [ ] 三步审批状态指示正确  
- [ ] K8s Job 可 solc 编译 MultiSig 合约片段  

---

## 合规说明

- 非真实 OA/政务系统 · Sepolia only · 禁止主网  

---

> **合规脚注** · 虚构审批流 · Sepolia 测试网 only · 非真实 OA/政务审批系统
