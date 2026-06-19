# 招投标关联图谱 · 教学 Demo

> **plugin_id**: `edu.cn.gov.bid-graph`  
> **TaskType**: `CN_BID_GRAPH_SIM`  
> **Namespace**: `ns-domain-cn`

## 教学目标

演示如何基于**虚构**招投标参与方数据，通过图算法识别「疑似关联」模式，用于政企内控教学。

## 功能说明

- 输入：虚构供应商节点（名称、法定代表人、地址前缀、参与标段）
- 算法：连通分量、共享属性聚类、同标段共现分析
- 输出：0–100 教学评分 + 文字说明（**不构成真实审计结论**）

## 合规说明

- 全部数据为虚构，不对接政府采购网或任何真实监管系统
- 不涉及军队、国防、涉密、作战等表述
- 禁止将教学评分直接用于真实采购决策

## 联调示例

```bash
curl -X POST http://127.0.0.1:8080/api/v1/labs/edu.cn.gov.bid-graph/simulate \
  -H 'Content-Type: application/json' \
  -d '{
    "user_prompt": "招投标关联分析",
    "params": { "graph": "sample" },
    "allowed_chain_ids": ["fabric-local"]
  }'
```

## 样例数据

见 `plugins/bid-graph/fixtures/sample-graph.json`。
