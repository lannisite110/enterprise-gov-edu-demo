# 政企内控 · 完整学习路径

> **子库** `enterprise-gov-edu-demo` v0.4.0 · 主库 ≥ v1.0.0 · **3 插件**  
> **Namespace**: `ns-domain-cn` · **链**: Fabric 沙箱 + Sepolia 测试网  
> 交叉引用：主库 [LEARNING_PATH.md](../web3-edu-platform-core/docs/LEARNING_PATH.md) **阶段 3C**

---

## 路线总览（约 1 周业余 / 3 天全职）

```text
bid-graph（招投标关联图谱 · 入口）
    → multisig（多级多签审批 · Sepolia）
    → supply（物资供应链存证 · Fabric）
```

---

## 第 0 步：环境与注册（所有 Lab 共用）

```bash
cd ~/web3home/web3-edu-platform-core
make register-plugins PLUGINS_DIR=..
make run-rule-engine & make run-scheduler & make run-gateway &
cd frontend-web && npm run dev
# → http://127.0.0.1:5173
```

详见 [QUICK_DEPLOY.md](QUICK_DEPLOY.md) 与主库 [QUICK_DEPLOY.md](../web3-edu-platform-core/docs/QUICK_DEPLOY.md)。

---

## 第 1 步：招投标关联图谱（必做 · 1–2 天）

| 项 | 内容 |
|----|------|
| 插件 | `edu.cn.gov.bid-graph` |
| 教程 | [tutorials/bid-graph-intro.md](tutorials/bid-graph-intro.md) |
| TaskType | `CN_BID_GRAPH_SIM` |
| UI | 图谱可视化 · 教学评分 · 疑点 findings |
| 数据 | `plugins/bid-graph/fixtures/sample-graph.json` |

**自检**：运行分析 → `suspicion_score` ≥ 40 → findings 列表可见。

---

## 第 2 步：多级多签审批（1 天）

| 项 | 内容 |
|----|------|
| 插件 | `edu.cn.gov.multisig` |
| 教程 | [tutorials/multisig-intro.md](tutorials/multisig-intro.md) |
| TaskType | `CN_MULTISIG_APPROVAL_DEMO` |
| UI | 逐步勾选签名人 · 提案 ID · 2-of-3 进度 |
| 合约 | `plugins/contracts/MultiSigApprovalDemo.sol` @ Sepolia |

**自检**：仅勾选 1 人 → `approved=false`；勾选 2 人 → `approved=true`。

---

## 第 3 步：物资供应链存证（1 天）

| 项 | 内容 |
|----|------|
| 插件 | `edu.cn.gov.supply` |
| 教程 | [tutorials/supply-intro.md](tutorials/supply-intro.md) |
| TaskType | `CN_SUPPLY_CHAIN_DEMO` |
| UI | 出入库事件 · 库存曲线 · 哈希链断点演示 |
| 数据 | `plugins/supply/fixtures/sample-ledger.json` |

**自检**：开启「模拟断链」→ `chain_intact=false` → 合规拒绝。

---

## 教程索引

[docs/tutorials/README.md](tutorials/README.md)

---

## 工程化验收

```bash
cd ~/web3home/enterprise-gov-edu-demo
make validate && make smoke

cd ../web3-edu-platform-core
make tutorial-audit PLUGINS_DIR=..
make integration-all-plugins
```

分阶段路线：[GOV_PHASES.md](GOV_PHASES.md)

---

## 合规速查

| 禁止 | 替代表述 |
|------|----------|
| 军队/涉密/作战 | 政企**内控教学** Demo |
| 信创认证宣称 | 信创**适配清单参考**（文档级） |
| 真实 OA/政府采购网 | 虚构数据 · 图算法/权限模型演示 |
| 主网 | Sepolia / `fabric-local` only |

全平台：[COMPLIANCE_MASTER.md](../../COMPLIANCE_MASTER.md)
