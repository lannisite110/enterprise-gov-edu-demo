#!/usr/bin/env bash
# 本地联调验证：bid-graph 规则引擎 + manifest 校验
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CORE="$ROOT/web3-edu-platform-core"
SUB="$ROOT/enterprise-gov-edu-demo"

cd "$CORE"

echo "==> validate-plugin"
make validate-plugin MANIFEST="$SUB/plugins/bid-graph/plugin.manifest.yaml"

echo "==> compliance-check"
bash ci/compliance/compliance-check.sh "$SUB"

echo "==> rule engine evaluate (isolated PYTHONPATH)"
PYTHONPATH="$CORE/rule-engine-py:$SUB" .venv/bin/python - <<'PY'
from plugins.registry import run_plugin, RuleInput

out = run_plugin(
    "plugins.rules.bid_graph:evaluate",
    RuleInput("招投标关联分析", {"graph": "sample"}, ["fabric-local"]),
)
assert out.compliance_passed, out.rejection_reason
print("OK:", out.audit_hints[0])
PY

echo "==> bid-graph verify PASSED"
