#!/usr/bin/env bash
# Phase 0 验收：注册 + 3 插件 curl 冒烟
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CORE="${CORE:-$ROOT/../web3-edu-platform-core}"

echo "==> register plugins"
cd "$CORE" && make register-plugins PLUGINS_DIR="$ROOT/.."

echo "==> gov plugin smoke (needs gateway :8080 + rule-engine :8081 + scheduler :8082)"
declare -A BODIES=(
  [edu.cn.gov.bid-graph]='{"user_prompt":"gov phase0","params":{"graph":"sample"},"allowed_chain_ids":["fabric-local"]}'
  [edu.cn.gov.multisig]='{"user_prompt":"gov phase0","params":{"threshold":2},"allowed_chain_ids":[11155111]}'
  [edu.cn.gov.supply]='{"user_prompt":"gov phase0","params":{"ledger":"sample"},"allowed_chain_ids":["fabric-local"]}'
)
for pid in edu.cn.gov.bid-graph edu.cn.gov.multisig edu.cn.gov.supply; do
  code=$(curl -sf -o /tmp/gov-smoke.json -w '%{http_code}' \
    -X POST "http://127.0.0.1:8080/api/v1/labs/${pid}/simulate" \
    -H 'Content-Type: application/json' \
    -d "${BODIES[$pid]}" || echo "000")
  if [ "$code" = "202" ] || [ "$code" = "200" ]; then
    echo "  OK $pid HTTP $code"
  else
    echo "  SKIP/FAIL $pid HTTP $code (start backend for full smoke)"
    exit 1
  fi
done

echo "==> gov phase0 smoke PASSED"
