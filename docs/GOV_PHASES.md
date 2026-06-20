# 政企内控子库 · 分阶段路线图

> **仓库**: `enterprise-gov-edu-demo` · **v0.4.0** ✅  
> **插件**: 3（招投标 / 多签 / 供应链）· **Namespace**: `ns-domain-cn`  
> **参照**: [supervision-trace-edu-suite/docs/TRACE_PHASES.md](../supervision-trace-edu-suite/docs/TRACE_PHASES.md)

---

## 现状（v0.4.0）

| 项 | 状态 |
|----|------|
| 前端 | 三插件领域 UI + eval-card + 任务轮询 |
| 规则 | risk_level / proposal_id / simulate_break |
| K8s Job | python / evm solc / fabric-tools 门禁 |
| 教程 | 3 篇扩写 + [GOV_LEARNING_PATH.md](GOV_LEARNING_PATH.md) |
| 主库 | LEARNING_PATH 阶段 3C 已链接 |

---

## Phase 0 — 共享 composable + Job 审计 ✅

`useLabSimulate` · `parseHints` · eval-card · Job 门禁 · 验收脚本

---

## Phase 1 — 总入口文档 ✅

| 任务 | 状态 |
|------|------|
| `GOV_LEARNING_PATH.md` | ✅ bid-graph → multisig → supply |
| `docs/tutorials/README.md` | ✅ |
| 主库 LEARNING_PATH 3C | ✅ |

---

## Phase 2 — 三插件领域 UI 对齐 ✅

| 插件 | 状态 |
|------|------|
| bid-graph | ✅ SVG 图谱 · 评分条 · findings |
| multisig | ✅ 逐步签名 · 提案 · 进度条 |
| supply | ✅ 库存曲线 · 哈希链断点 |

---

## Phase 3 — 规则 + Job + 合约 ✅

| 任务 | 状态 |
|------|------|
| bid-graph | ✅ scenario · risk_level hints |
| multisig | ✅ proposal_id · 完整 MultiSig solc Job |
| supply | ✅ asset_id · simulate_break |

---

## Phase 4 — 教程扩写 + v0.4.0 ✅

- manifest `0.4.0` · `make tutorial-audit` PASS  
- **Tag**: `v0.4.0`（待 push 时打 tag）

---

## P0 下一子库

| 顺序 | 子库 | 目标 |
|------|------|------|
| 下一 | `global-social-edu-sandbox` | v0.4.0 · `GLOBAL_PHASES.md` |
| 收官 | `web3-edu-platform-core` | v1.1.0 · 3A/3B/3C/3D 齐全 |

---

## 相关文档

- [GOV_LEARNING_PATH.md](GOV_LEARNING_PATH.md) · [TASK.md](../TASK.md)
