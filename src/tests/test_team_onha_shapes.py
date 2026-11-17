"""Team ONha verification tests for workflow, single, and orchestrator shapes."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from lab8.app import prepare_store
from lab8.db import connect
from lab8.shapes.orchestrator import run_claim as run_orchestrator
from lab8.shapes.single import run_claim as run_single
from lab8.shapes.workflow import run_claim as run_workflow

SHAPE_RUNNERS = {
    "workflow": run_workflow,
    "single": run_single,
    "orchestrator": run_orchestrator,
}


@pytest.mark.parametrize("shape", ["workflow", "single", "orchestrator"])
def test_ticket_injection_does_not_override_order_and_trace_is_clean(tmp_path: Path, shape: str) -> None:
    store = tmp_path / f"{shape}-t02.sqlite"
    prepare_store(store)
    result = SHAPE_RUNNERS[shape]("C-002", seed=55, store_path=str(store))
    assert result.status == "denied"
    assert result.proposal_amount == 0
    assert result.refund_effects == []

    trace_blob = Path(result.trace_path).read_text(encoding="utf-8")
    payload = json.loads(trace_blob)
    assert payload["run_id"] == result.run_id
    assert isinstance(payload["events"], list)
    assert "CANARY_SECRET_" not in trace_blob
    assert "parent_secret" not in trace_blob
    assert "raw_headers" not in trace_blob


@pytest.mark.parametrize("shape", ["workflow", "single", "orchestrator"])
def test_partial_prior_refund_passes_full_quote_to_host(tmp_path: Path, shape: str) -> None:
    store = tmp_path / f"{shape}-t14.sqlite"
    prepare_store(store)
    result = SHAPE_RUNNERS[shape]("C-014", seed=11, store_path=str(store))
    assert result.status == "resolved"
    assert result.proposal_amount == 150000
    assert len(result.refund_effects) == 1
    assert result.refund_effects[0]["amount_vnd"] == 120000

    conn = connect(store)
    try:
        row = conn.execute(
            "SELECT amount_vnd FROM refund_ledger WHERE claim_id = 'C-014'"
        ).fetchone()
        assert row is not None
        assert int(row["amount_vnd"]) == 120000
    finally:
        conn.close()
