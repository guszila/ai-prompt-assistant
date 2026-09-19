from app.domain.prompt import AmbiguitySeverity
from app.engine.ambiguity import AmbiguityDetector
from tests.fixtures.requirements import (
    REQ_AMBIGUOUS_NOTIFICATION,
    REQ_THAI_CRUD,
)


def test_ambiguity_detected_for_vague_notification():
    """
    Mandatory Rule 3: Detect missing functional information (channels, triggers).
    """
    ambiguities = AmbiguityDetector.detect(
        text=REQ_AMBIGUOUS_NOTIFICATION,
        actions=[],
        entities=["Notification"],
        intent="Implement Notification management capability",
    )
    assert len(ambiguities) > 0
    # Must be functional ambiguity
    for amb in ambiguities:
        assert amb.is_functional is True
        # Clarification questions must NOT demand arbitrary tech stacks like React, Redis, Celery, AWS
        lower_q = amb.clarification_question.lower()
        assert "redis" not in lower_q
        assert "postgresql" not in lower_q
        assert "react" not in lower_q
        assert "docker" not in lower_q


def test_clear_crud_has_no_high_severity_functional_ambiguity():
    """
    Requirements with explicit CRUD actions (เพิ่ม, ลบ, แก้ไข, ค้นหา) should not flag missing operations.
    """
    ambiguities = AmbiguityDetector.detect(
        text=REQ_THAI_CRUD,
        actions=["create", "update", "delete", "search"],
        entities=["User"],
        intent="Implement User management with create, update, delete, search capabilities",
    )
    high_severities = [a for a in ambiguities if a.severity == AmbiguitySeverity.HIGH]
    assert len(high_severities) == 0


def test_vague_entity_without_actions_flags_missing_operations():
    """
    Vague entity without any actions specified flags missing operations.
    """
    ambiguities = AmbiguityDetector.detect(
        text="ทำระบบจัดการพนักงาน",
        actions=[],
        entities=["Employee"],
        intent="Manage Employee",
    )
    missing_ops = [a for a in ambiguities if a.ambiguity_id == "amb_missing_functional_operations"]
    assert len(missing_ops) == 1
    assert "operations are required" in missing_ops[0].clarification_question.lower()
