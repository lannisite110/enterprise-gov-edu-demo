<p align="center">
  <img src="assets/icon.png" alt="Web3 Education Platform" width="128"/>
</p>

# Enterprise & Government Education Demo

国内政企内控**教学 Demo**（子库3）· **v0.4.0** · 主库 LEARNING_PATH **阶段 3C**

**不含**军队、涉密、作战系统。

## 文档

- [完整学习路径](docs/GOV_LEARNING_PATH.md) · [教程索引](docs/tutorials/README.md)
- [学习路径（子库入口）](docs/LEARNING_PATH.md) · [快速部署](docs/QUICK_DEPLOY.md)
- [分阶段工程路线](docs/GOV_PHASES.md)

**依赖**: [web3-edu-platform-core](https://github.com/lannisite110/web3-edu-platform-core) **v1.1.0**

见 [TASK.md](TASK.md) · [CHANGELOG.md](CHANGELOG.md)

## 插件清单

| 模块 | plugin_id | TaskType |
|------|-----------|----------|
| 招投标关联图谱 | `edu.cn.gov.bid-graph` | `CN_BID_GRAPH_SIM` |
| 多级多签审批 | `edu.cn.gov.multisig` | `CN_MULTISIG_APPROVAL_DEMO` |
| 物资供应链存证 | `edu.cn.gov.supply` | `CN_SUPPLY_CHAIN_DEMO` |

## 验收

```bash
make validate && make smoke
bash scripts/verify-all.sh
bash scripts/joint-debug-smoke.sh   # 需主库后端栈
```

主库注册：

```bash
cd ../web3-edu-platform-core
make register-plugins PLUGINS_DIR=..
make tutorial-audit PLUGINS_DIR=..
```

License: PolyForm Noncommercial 1.0.0
