from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

_REPO_ROOT = Path(__file__).resolve().parent.parent
_WORKFLOW = _REPO_ROOT / ".github" / "workflows" / "check-attribution.yml"


def _workflow() -> dict[str, Any]:
    workflow = yaml.safe_load(_WORKFLOW.read_text(encoding="utf-8"))
    if True in workflow:
        workflow["on"] = workflow.pop(True)
    return workflow


def test_workflow_checks_bot_authors_in_required_job() -> None:
    workflow = _workflow()
    trigger_types = workflow["on"]["pull_request_target"]["types"]
    job = workflow["jobs"]["check-bot-coauthors"]
    ordered_steps = job["steps"]
    steps = {step.get("name"): step for step in ordered_steps}

    assert "pull_request" not in workflow["on"]
    assert trigger_types == ["opened", "synchronize", "reopened", "edited"]
    assert workflow["permissions"] == {"contents": "read"}
    assert workflow["concurrency"]["group"] == (
        "${{ github.workflow }}-${{ github.event.pull_request.number }}"
    )

    checkout = steps["Check out trusted workflow revision"]
    assert checkout["with"]["ref"] == "${{ github.workflow_sha }}"
    assert checkout["with"]["ref"] != "${{ github.event.pull_request.base.sha }}"
    assert checkout["with"]["persist-credentials"] is False
    assert checkout["with"]["fetch-depth"] == 1

    fetch = steps["Fetch PR commits"]
    assert "Check PR model attribution" not in steps
    assert fetch["env"]["BASE_REF"] == "${{ github.event.pull_request.base.ref }}"
    assert fetch["env"]["PR_NUMBER"] == "${{ github.event.pull_request.number }}"
    assert 'case "$PR_NUMBER"' in fetch["run"]
    assert 'git check-ref-format "refs/heads/${BASE_REF}"' in fetch["run"]
    assert '"refs/heads/${BASE_REF}"' in fetch["run"]
    assert '"refs/pull/${PR_NUMBER}/head"' in fetch["run"]
    assert "git checkout" not in fetch["run"]

    for name in ("Check for bot Co-Authored-By lines", "Check for bot commit authors"):
        assert steps[name]["env"]["BASE_SHA"] == (
            "${{ github.event.pull_request.base.sha }}"
        )
        assert steps[name]["env"]["HEAD_SHA"] == (
            "${{ github.event.pull_request.head.sha }}"
        )
