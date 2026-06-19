<p align="center">
  <img src="assets/icon.png" alt="Web3 Education Platform" width="128"/>
</p>

# Enterprise & Government Education Demo

国内政企内控**教学 Demo**（子库3）· **v0.2.0**

**依赖**: `web3-edu-platform-core` ≥ **v0.3.0**

**不含**军队、涉密、作战系统。

见 [TASK.md](TASK.md).

## 插件清单

| 模块 | plugin_id | TaskType | 状态 |
|------|-----------|----------|------|
| 招投标关联图谱 | `edu.cn.gov.bid-graph` | `CN_BID_GRAPH_SIM` | ✅ |
| 物资供应链存证 | `edu.cn.gov.supply` | `CN_SUPPLY_CHAIN_DEMO` | ✅ |
| 多级多签审批 | `edu.cn.gov.multisig` | `CN_MULTISIG_APPROVAL_DEMO` | ✅ |

## 验收

```bash
# 本子库 3 插件全量验收
bash scripts/verify-all.sh

# 主库注册（在 web3-edu-platform-core 下）
make register-plugins PLUGINS_DIR=..
```

License: PolyForm Noncommercial 1.0.0
