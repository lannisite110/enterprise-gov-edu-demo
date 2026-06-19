#!/usr/bin/env bash
# 本子库全量验收：3 插件 manifest + 合规 + 规则引擎
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CORE="$ROOT/web3-edu-platform-core"
SUB="$ROOT/enterprise-gov-edu-demo"

cd "$CORE"

echo "==> validate-plugin (×3)"
for m in "$SUB"/plugins/*/plugin.manifest.yaml; do
  make validate-plugin MANIFEST="$m"
done

echo "==> compliance-check"
bash ci/compliance/compliance-check.sh "$SUB"

echo "==> rule engine evaluate (×3)"
PYTHONPATH="$CORE/rule-engine-py:$SUB" .venv/bin/python - <<'PY'
from plugins.registry import run_plugin, RuleInput

cases = [
    ("plugins.rules.bid_graph:evaluate", {"graph": "sample"}, ["fabric-local"], "bid-graph"),
    ("plugins.rules.supply_chain:evaluate", {"ledger": "sample"}, ["fabric-local"], "supply"),
    ("plugins.rules.multisig:evaluate", {"threshold": 2}, [11155111], "multisig"),
]
for entry, params, chains, name in cases:
    out = run_plugin(entry, RuleInput("demo", params, chains))
    assert out.compliance_passed, f"{name}: {out.rejection_reason}"
    print(f"OK {name}:", out.audit_hints[0])
PY

echo "==> enterprise-gov-edu-demo verify PASSED (3/3)"
