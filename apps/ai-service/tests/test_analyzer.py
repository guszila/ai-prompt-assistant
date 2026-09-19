from app.engine.analyzer import RequirementAnalyzer
from app.engine.normalizer import RequirementNormalizer
from tests.fixtures.requirements import (
    REQ_AUTHN_ONLY,
    REQ_DASHBOARD,
    REQ_THAI_CRUD,
)


def test_analyzer_crud_extraction():
    norm = RequirementNormalizer.normalize(REQ_THAI_CRUD)
    analysis = RequirementAnalyzer.analyze("req_1", norm)

    assert analysis.request_id == "req_1"
    assert "User" in analysis.entities
    assert "create" in analysis.requested_actions
    assert "delete" in analysis.requested_actions
    assert "update" in analysis.requested_actions
    assert "search" in analysis.requested_actions
    assert "User" in analysis.intent


def test_analyzer_preserves_explicit_constraints():
    raw = "ระบบบันทึกคะแนน ต้องอยู่ระหว่าง 1 ถึง 5 และห้ามคะแนนติดลบ"
    norm = RequirementNormalizer.normalize(raw)
    analysis = RequirementAnalyzer.analyze("req_2", norm)

    assert len(analysis.constraints) > 0
    joined_constraints = " ".join(analysis.constraints)
    assert "ต้องอยู่ระหว่าง 1 ถึง 5" in joined_constraints or "1 and 5" in joined_constraints


def test_analyzer_no_unrequested_constraints_fabricated():
    """
    Mandatory Rule 4: No requirement fabrication.
    If the user did not specify constraints, constraints list must be empty or contain only explicit user text.
    """
    norm = RequirementNormalizer.normalize(REQ_AUTHN_ONLY)
    analysis = RequirementAnalyzer.analyze("req_3", norm)

    for constraint in analysis.constraints:
        # Check no arbitrary latency or capacity constraints were invented
        assert "2 seconds" not in constraint
        assert "1000 users" not in constraint
        assert "99.9%" not in constraint


def test_analyzer_dashboard_intent():
    norm = RequirementNormalizer.normalize(REQ_DASHBOARD)
    analysis = RequirementAnalyzer.analyze("req_4", norm)

    assert "Sales" in analysis.entities
    assert any("Dashboard" in c.name for c in analysis.technical_concepts)
