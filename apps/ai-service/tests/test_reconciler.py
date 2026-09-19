from app.engine.analyzer import RequirementAnalyzer
from app.engine.normalizer import RequirementNormalizer
from app.engine.reconciler import GroundingReconciler
from app.llm.models import LLMRequirementCandidate
from tests.fixtures.requirements import (
    REQ_AUTHN_ONLY,
    REQ_GENERIC_API,
    REQ_THAI_CRUD,
)


def test_reconciler_protects_authn_vs_authz():
    """
    Mandatory Rule: If user requested only login, LLM candidate suggesting
    Authorization must NOT become a confirmed technical concept.
    It must become an Assumption requiring confirmation.
    """
    norm = RequirementNormalizer.normalize(REQ_AUTHN_ONLY)
    baseline = RequirementAnalyzer.analyze("req_rec_1", norm)

    # Candidate model untrusted suggestion proposing Authorization
    candidate = LLMRequirementCandidate(
        suggested_intent="User authentication and authorization system",
        suggested_concepts=["Authentication", "Authorization", "Role-based Access Control"],
        suggested_assumptions=["JWT will be used"],
    )

    reconciled = GroundingReconciler.reconcile(baseline, candidate)

    concept_names = [c.name for c in reconciled.technical_concepts]
    assert "Authentication" in concept_names
    assert "Authorization" not in concept_names
    assert "Role-based Access Control" not in concept_names

    # Authorization was converted to an assumption
    assumption_descs = [a.description for a in reconciled.assumptions]
    assert any("Role-based authorization was suggested" in desc for desc in assumption_descs)


def test_reconciler_protects_generic_api():
    """
    Mandatory Rule: Generic 'API' must not be converted to 'RESTful API' by LLM candidate.
    """
    norm = RequirementNormalizer.normalize(REQ_GENERIC_API)
    baseline = RequirementAnalyzer.analyze("req_rec_2", norm)

    candidate = LLMRequirementCandidate(
        suggested_concepts=["RESTful API"],
    )

    reconciled = GroundingReconciler.reconcile(baseline, candidate)

    concept_names = [c.name for c in reconciled.technical_concepts]
    assert "API Interface" in concept_names
    assert "RESTful API" not in concept_names

    assumption_descs = [a.description for a in reconciled.assumptions]
    assert any("REST architecture was suggested" in desc for desc in assumption_descs)


def test_reconciler_blocks_ungrounded_technologies():
    """
    Candidate suggesting PostgreSQL or Redis when user did not specify them must be blocked.
    """
    norm = RequirementNormalizer.normalize(REQ_THAI_CRUD)
    baseline = RequirementAnalyzer.analyze("req_rec_3", norm)

    candidate = LLMRequirementCandidate(
        suggested_intent="User management using PostgreSQL and Redis",
        suggested_concepts=["PostgreSQL Database", "Redis Cache", "React Frontend"],
    )

    reconciled = GroundingReconciler.reconcile(baseline, candidate)

    concept_names = [c.name for c in reconciled.technical_concepts]
    assert "PostgreSQL Database" not in concept_names
    assert "Redis Cache" not in concept_names
    assert "React Frontend" not in concept_names
    assert "PostgreSQL" not in reconciled.intent


def test_reconciler_blocks_ungrounded_performance_targets():
    """
    Candidate suggesting arbitrary latency or uptime SLAs must be blocked.
    """
    norm = RequirementNormalizer.normalize(REQ_THAI_CRUD)
    baseline = RequirementAnalyzer.analyze("req_rec_4", norm)

    candidate = LLMRequirementCandidate(
        suggested_intent="User management responding under 200ms with 99.9% uptime",
        suggested_assumptions=["System must respond within 500ms"],
    )

    reconciled = GroundingReconciler.reconcile(baseline, candidate)

    assert "under 200ms" not in reconciled.intent
    assert "99.9%" not in reconciled.intent
    assumption_descs = [a.description for a in reconciled.assumptions]
    assert not any("within 500ms" in desc for desc in assumption_descs)


def test_reconciler_preserves_explicit_user_actions_and_entities():
    """
    Candidate cannot delete user-commanded actions or entities.
    """
    norm = RequirementNormalizer.normalize(REQ_THAI_CRUD)
    baseline = RequirementAnalyzer.analyze("req_rec_5", norm)

    candidate = LLMRequirementCandidate(
        suggested_actions=["only_one_action"],
        suggested_entities=["DifferentEntity"],
    )

    reconciled = GroundingReconciler.reconcile(baseline, candidate)

    assert "User" in reconciled.entities
    assert "create" in reconciled.requested_actions
    assert "delete" in reconciled.requested_actions
    assert "update" in reconciled.requested_actions
    assert "search" in reconciled.requested_actions
