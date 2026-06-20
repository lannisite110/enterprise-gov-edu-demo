# 招投标关联图谱 · 分步实验

> **插件**: `edu.cn.gov.bid-graph` · **TaskType**: `CN_BID_GRAPH_SIM` · **Namespace**: `ns-domain-cn`  
> **数据**: `plugins/bid-graph/fixtures/sample-graph.json` · **Job**: `k8s/overlays/ns-domain-cn/bid-graph-job.yaml`  
> **路线**: [GOV_LEARNING_PATH.md](../GOV_LEARNING_PATH.md) 第 1 步

---

## 学习目标

- 理解虚构供应商图谱上的**连通分量**与**共享属性聚类**  
- 阅读 `suspicion_score` / `risk_level` audit_hints  
- 区分教学评分与真实审计结论  

---

## 前置条件

- 主库四服务已启动（见 [QUICK_DEPLOY.md](../../web3-edu-platform-core/docs/QUICK_DEPLOY.md)）  
- `make register-plugins PLUGINS_DIR=..` 已完成  

---

## 分步实验

### 步骤 1：打开 Lab

`http://127.0.0.1:5173/labs/edu.cn.gov.bid-graph`

### 步骤 2：UI 操作

1. 查看 **关联图谱（示意）** — 橙色节点为共享法人「张某某」  
2. 点击 **运行关联分析**  
3. 观察评分条与 **评分解释** findings 列表  

### 步骤 3：curl 验证

```bash
curl -s -X POST http://127.0.0.1:8080/api/v1/labs/edu.cn.gov.bid-graph/simulate \
  -H 'Content-Type: application/json' \
  -d '{
    "user_prompt": "招投标关联分析",
    "params": { "graph": "sample", "scenario": "sample" },
    "allowed_chain_ids": ["fabric-local"],
    "task_type": "CN_BID_GRAPH_SIM"
  }' | jq '.evaluation.audit_hints[:4]'
```

**期望**：`suspicion_score=75` 量级、`risk_level=high`（sample 数据）。

### 步骤 4：自检清单

- [ ] 规则评估卡片显示评分与风险等级  
- [ ] findings 含「共享法定代表人」类说明  
- [ ] 任务 `completed`  

---

## K8s Job（可选）

```bash
cd ../../web3-edu-platform-core && make k8s-job-smoke
```

---

## 合规说明

- 不对接政府采购网 · 禁止军队/涉密/作战表述  
- 教学评分**不构成**真实采购决策  

---

> **合规脚注** · `compliance_tier: cn_domain` · 虚构数据 only · 教学评分不构成真实审计或采购决策
