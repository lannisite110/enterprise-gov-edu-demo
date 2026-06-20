"""物资供应链存证 — 出入库哈希链教学 Demo（Fabric 沙箱，虚构数据）."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_FIXTURE = Path(__file__).resolve().parents[1] / "supply" / "fixtures" / "sample-ledger.json"


@dataclass
class RuleInput:
    user_prompt: str
    params: dict[str, Any]
    allowed_chain_ids: list


@dataclass
class RuleOutput:
    recommended_template: str
    recommended_language: str
    audit_hints: list[str]
    compliance_passed: bool
    rejection_reason: str | None = None


def _event_record_hash(event: dict[str, Any]) -> str:
    body = {
        "seq": event["seq"],
        "type": event["type"],
        "warehouse": event["warehouse"],
        "quantity": event["quantity"],
        "unit": event["unit"],
        "operator": event["operator"],
        "timestamp": event["timestamp"],
        "prev_hash": event["prev_hash"],
    }
    digest = hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    return digest


def _load_ledger(params: dict[str, Any]) -> dict[str, Any]:
    if params.get("ledger") == "custom" and "events" in params:
        return params
    with _FIXTURE.open(encoding="utf-8") as f:
        return json.load(f)


def verify_ledger(ledger: dict[str, Any]) -> dict[str, Any]:
    events: list[dict] = ledger.get("events", [])
    findings: list[str] = []
    chain_intact = True
    balance = 0

    for i, event in enumerate(events):
        expected_prev = "0" if i == 0 else events[i - 1]["payload_hash"]
        if event.get("prev_hash") != expected_prev:
            chain_intact = False
            findings.append(f"序号 {event['seq']} 前序哈希不匹配")

        computed = _event_record_hash(event)
        if computed != event.get("payload_hash"):
            chain_intact = False
            findings.append(f"序号 {event['seq']} 载荷哈希校验失败")

        qty = int(event["quantity"])
        if event["type"] == "inbound":
            balance += qty
        elif event["type"] == "outbound":
            balance -= qty
        elif event["type"] == "transfer":
            pass

    if balance < 0:
        findings.append(f"库存余额异常: {balance}")
        chain_intact = False

    leaf_hashes = [e["payload_hash"] for e in events]
    merkle_root = leaf_hashes[0] if len(leaf_hashes) == 1 else _merkle_root(leaf_hashes)

    if chain_intact and balance >= 0:
        findings.insert(0, f"哈希链完整 · 当前库存 {balance} 件")
    else:
        findings.insert(0, "存证链校验未通过")

    return {
        "asset_id": ledger.get("asset_id", ""),
        "event_count": len(events),
        "chain_intact": chain_intact,
        "balance": balance,
        "merkle_root": merkle_root,
        "findings": findings,
        "disclaimer": "虚构数据 · Fabric 沙箱教学 · 非真实仓储系统",
    }


def _merkle_root(hashes: list[str]) -> str:
    layer = hashes[:]
    while len(layer) > 1:
        nxt: list[str] = []
        for i in range(0, len(layer), 2):
            left = layer[i]
            right = layer[i + 1] if i + 1 < len(layer) else left
            combined = hashlib.sha256((left + right).encode()).hexdigest()
            nxt.append(combined)
        layer = nxt
    return layer[0]


def evaluate(inp: RuleInput) -> RuleOutput:
    if inp.params.get("target_network") == "mainnet":
        return RuleOutput(
            recommended_template="",
            recommended_language="",
            audit_hints=[],
            compliance_passed=False,
            rejection_reason="mainnet forbidden",
        )

    ledger = _load_ledger(inp.params)
    if inp.params.get("simulate_break"):
        events = [dict(e) for e in ledger.get("events", [])]
        if events:
            events[-1]["prev_hash"] = "0xbroken-demo-hash"
            ledger = {**ledger, "events": events}

    asset_id = str(inp.params.get("asset_id", ledger.get("asset_id", "MAT-2024-DEMO-001")))
    report = verify_ledger(ledger)

    hints = [
        f"asset_id={asset_id}",
        f"simulate_break={'true' if inp.params.get('simulate_break') else 'false'}",
        f"chain_intact={'true' if report['chain_intact'] else 'false'}",
        f"balance={report['balance']}",
        f"event_count={report['event_count']}",
        f"merkle_root={report['merkle_root'][:16]}",
        *report["findings"][:5],
        report["disclaimer"],
    ]

    return RuleOutput(
        recommended_template="plugins/supply/fixtures/sample-ledger.json",
        recommended_language="chaincode",
        audit_hints=hints,
        compliance_passed=True,
    )
