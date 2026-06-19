"""多级多签审批 — 权限模型教学 Demo（Sepolia 测试网合约模板）."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

_TEMPLATE = "plugins/contracts/MultiSigApprovalDemo.sol"
_SEPOLIA = 11155111


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


def _parse_approvers(params: dict[str, Any]) -> tuple[list[str], int]:
    approvers = params.get("approvers") or [
        "0x1111111111111111111111111111111111111111",
        "0x2222222222222222222222222222222222222222",
        "0x3333333333333333333333333333333333333333",
    ]
    threshold = int(params.get("threshold", 2))
    return list(approvers), threshold


def simulate_approval(params: dict[str, Any]) -> dict[str, Any]:
    approvers, threshold = _parse_approvers(params)
    confirmations = list(params.get("confirmations") or approvers[:threshold])
    proposal_id = params.get("proposal_id", "0x" + "ab" * 32)

    valid_confirmations = [a for a in confirmations if a in approvers]
    unique = list(dict.fromkeys(valid_confirmations))
    approved = len(unique) >= threshold

    return {
        "proposal_id": proposal_id,
        "approvers": approvers,
        "threshold": threshold,
        "confirmations": unique,
        "confirmation_count": len(unique),
        "approved": approved,
        "status": "approved" if approved else "pending",
        "disclaimer": "虚构审批流 · Sepolia 测试网 · 非真实 OA/政务系统",
    }


def evaluate(inp: RuleInput) -> RuleOutput:
    blocked = {1, 56, 137, 42161, 10, 8453}
    for cid in inp.allowed_chain_ids:
        if isinstance(cid, int) and cid in blocked:
            return RuleOutput(
                recommended_template="",
                recommended_language="",
                audit_hints=[],
                compliance_passed=False,
                rejection_reason=f"mainnet chainId {cid} blocked",
            )

    if inp.params.get("target_network") == "mainnet":
        return RuleOutput(
            recommended_template="",
            recommended_language="",
            audit_hints=[],
            compliance_passed=False,
            rejection_reason="mainnet forbidden",
        )

    approvers, threshold = _parse_approvers(inp.params)
    if threshold <= 0 or threshold > len(approvers):
        return RuleOutput(
            recommended_template="",
            recommended_language="",
            audit_hints=[],
            compliance_passed=False,
            rejection_reason=f"invalid threshold {threshold} for {len(approvers)} approvers",
        )

    report = simulate_approval(inp.params)
    hints = [
        f"threshold={threshold}-of-{len(approvers)}",
        f"status={report['status']}",
        f"confirmations={report['confirmation_count']}",
        f"chain_id={_SEPOLIA} (Sepolia testnet)",
        report["disclaimer"],
    ]

    return RuleOutput(
        recommended_template=_TEMPLATE,
        recommended_language="solidity",
        audit_hints=hints,
        compliance_passed=True,
    )
