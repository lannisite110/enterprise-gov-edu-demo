# 多级多签审批 · 教学 Demo

> **plugin_id**: `edu.cn.gov.multisig`  
> **TaskType**: `CN_MULTISIG_APPROVAL_DEMO`  
> **Namespace**: `ns-domain-cn` · **chainId**: `11155111` (Sepolia)

## 教学目标

演示政企内控场景中的**多签权限模型**：N 个审批人、M-of-N 阈值、提案确认与执行分离。

## 功能说明

- 规则引擎：模拟 2-of-3 审批流（可配置 threshold / confirmations）
- 合约模板：`plugins/contracts/MultiSigApprovalDemo.sol`（Sepolia 测试网部署）

## 合规说明

- 非真实 OA/政务审批系统
- 仅 Sepolia 测试网，禁止主网部署
- 不涉及军队、涉密、作战表述

## 联调示例

```bash
curl -X POST http://127.0.0.1:8080/api/v1/labs/edu.cn.gov.multisig/simulate \
  -H 'Content-Type: application/json' \
  -d '{
    "user_prompt": "多签审批演示",
    "params": {
      "threshold": 2,
      "confirmations": [
        "0x1111111111111111111111111111111111111111",
        "0x2222222222222222222222222222222222222222"
      ]
    },
    "allowed_chain_ids": [11155111]
  }'
```

## 合约模板

见 `plugins/contracts/MultiSigApprovalDemo.sol`。
