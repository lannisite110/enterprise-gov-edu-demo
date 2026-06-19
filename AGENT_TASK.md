# Agent-3 任务书 · enterprise-gov-edu-demo

> **仓库**: `enterprise-gov-edu-demo`  
> **compliance_tier**: `cn_domain`  
> **Namespace**: `ns-domain-cn`

---

## 1. 目标

3 个**政企内控教学 Demo**（无军队/涉密/作战表述）。

| # | 模块 | plugin_id | TaskType |
|---|------|-----------|----------|
| 1 | 招投标关联图谱 | `edu.cn.gov.bid-graph` | `CN_BID_GRAPH_SIM` |
| 2 | 多级多签审批 | `edu.cn.gov.multisig` | `CN_MULTISIG_APPROVAL_DEMO` |
| 3 | 物资供应链存证 | `edu.cn.gov.supply` | `CN_SUPPLY_CHAIN_DEMO` |

---

## 2. 技术要点

- **bid-graph**: 纯图算法 + 虚构供应商节点，输出「疑似关联」教学评分，不连接政府采购网
- **multisig**: Solidity 多签合约 @ Sepolia + 审批流 UI
- **supply**: Fabric 或 Sepolia 存证（择一，manifest 声明）

---

## 3. 合规红线

- ❌ 军队、国防、作战、武器、涉密
- ❌ 「国资 30 年生产归档」等产品承诺
- ❌ 信创认证宣称 → ✅「信创**适配清单参考**（文档级）」
- ✅ 物资**出入库存证算法**、多签**权限模型**教学

---

## 4. 目录

```
enterprise-gov-edu-demo/
├── plugins/bid-graph/
├── plugins/multisig/
├── plugins/supply/
├── k8s/overlays/ns-domain-cn/
└── docs/tutorials/
```

---

## 5. 验收

同 Agent-2，`validate-plugin` × 3 + `compliance-check` 无军队关键词。

**CI 额外禁止词**: `军事`, `作战`, `weapon`, `classified`, `涉密`
