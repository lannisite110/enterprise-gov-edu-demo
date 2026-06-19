"""招投标关联图谱 — 纯图算法教学 Demo（虚构供应商节点，不对接政府采购网）."""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_FIXTURE = Path(__file__).resolve().parents[1] / "bid-graph" / "fixtures" / "sample-graph.json"


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


def _load_graph(params: dict[str, Any]) -> dict[str, Any]:
    if params.get("graph") == "custom" and "nodes" in params:
        return {"nodes": params["nodes"], "edges": params.get("edges", [])}
    with _FIXTURE.open(encoding="utf-8") as f:
        return json.load(f)


def _union_find_components(nodes: list[dict], edges: list[dict]) -> list[list[str]]:
    parent: dict[str, str] = {n["id"]: n["id"] for n in nodes}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for edge in edges:
        union(edge["source"], edge["target"])

    groups: dict[str, list[str]] = defaultdict(list)
    for node in nodes:
        groups[find(node["id"])].append(node["id"])
    return [sorted(g) for g in groups.values() if len(g) > 1]


def _shared_attribute_clusters(nodes: list[dict], key: str) -> list[list[str]]:
    buckets: dict[str, list[str]] = defaultdict(list)
    for node in nodes:
        buckets[node[key]].append(node["id"])
    return [sorted(ids) for ids in buckets.values() if len(ids) > 1]


def _co_bid_pairs(edges: list[dict]) -> list[tuple[str, str, str]]:
    pairs: list[tuple[str, str, str]] = []
    for edge in edges:
        if edge.get("type") == "co_bid":
            pairs.append((edge["source"], edge["target"], edge.get("bid_id", "")))
    return pairs


def _suspicion_score(
    nodes: list[dict],
    edges: list[dict],
    rep_clusters: list[list[str]],
    addr_clusters: list[list[str]],
    components: list[list[str]],
) -> tuple[int, list[str]]:
    score = 0
    findings: list[str] = []
    node_map = {n["id"]: n for n in nodes}

    if rep_clusters:
        score += 30
        for cluster in rep_clusters:
            rep = node_map[cluster[0]]["legal_rep"]
            names = ", ".join(node_map[nid]["name"] for nid in cluster)
            findings.append(f"共享法定代表人「{rep}」: {names}")

    if addr_clusters:
        score += 25
        for cluster in addr_clusters:
            addr = node_map[cluster[0]]["address_prefix"]
            names = ", ".join(node_map[nid]["name"] for nid in cluster)
            findings.append(f"注册地址前缀相同「{addr}」: {names}")

    dense = [c for c in components if len(c) >= 3]
    if dense:
        score += 20
        for cluster in dense:
            findings.append(f"关联子图 ≥3 节点: {', '.join(cluster)}")

    co_bids = _co_bid_pairs(edges)
    bid_participants: dict[str, set[str]] = defaultdict(set)
    for src, tgt, bid_id in co_bids:
        bid_participants[bid_id].update({src, tgt})
    repeated = {bid: sorted(ids) for bid, ids in bid_participants.items() if len(ids) >= 3}
    if repeated:
        score += 15
        for bid_id, ids in repeated.items():
            findings.append(f"同一标段多主体共现 {bid_id}: {', '.join(ids)}")

    score = min(score, 100)
    if score >= 70:
        findings.insert(0, f"教学评分 {score}/100 — 疑似关联（高）")
    elif score >= 40:
        findings.insert(0, f"教学评分 {score}/100 — 需进一步核查（中）")
    else:
        findings.insert(0, f"教学评分 {score}/100 — 关联较弱（低）")

    return score, findings


def analyze_graph(graph: dict[str, Any]) -> dict[str, Any]:
    nodes: list[dict] = graph["nodes"]
    edges: list[dict] = graph.get("edges", [])

    rep_clusters = _shared_attribute_clusters(nodes, "legal_rep")
    addr_clusters = _shared_attribute_clusters(nodes, "address_prefix")
    components = _union_find_components(nodes, edges)
    score, findings = _suspicion_score(nodes, edges, rep_clusters, addr_clusters, components)

    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "connected_components": components,
        "shared_legal_rep_clusters": rep_clusters,
        "shared_address_clusters": addr_clusters,
        "co_bid_edges": len(_co_bid_pairs(edges)),
        "suspicion_score": score,
        "findings": findings,
        "disclaimer": "虚构数据 · 教学算法演示 · 不构成真实审计结论",
    }


def evaluate(inp: RuleInput) -> RuleOutput:
    if inp.params.get("target_network") == "mainnet":
        return RuleOutput(
            recommended_template="",
            recommended_language="",
            audit_hints=[],
            compliance_passed=False,
            rejection_reason="mainnet forbidden",
        )

    graph = _load_graph(inp.params)
    report = analyze_graph(graph)

    hints = [
        f"suspicion_score={report['suspicion_score']}",
        f"nodes={report['node_count']}",
        f"edges={report['edge_count']}",
        *report["findings"][:6],
        report["disclaimer"],
    ]

    return RuleOutput(
        recommended_template="plugins/bid-graph/fixtures/sample-graph.json",
        recommended_language="graph",
        audit_hints=hints,
        compliance_passed=True,
    )
