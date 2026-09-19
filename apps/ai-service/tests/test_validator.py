from app.domain.prompt import Ambiguity, AmbiguitySeverity, EngineeringPrompt, RequirementAnalysis
from app.engine.analyzer import RequirementAnalyzer
from app.engine.composer import PromptComposer
from app.engine.normalizer import RequirementNormalizer
from app.engine.validator import PromptValidator
from tests.fixtures.requirements import REQ_THAI_CRUD


def test_validator_passes_on_valid_prompt():
    norm = RequirementNormalizer.normalize(REQ_THAI_CRUD)
    analysis = RequirementAnalyzer.analyze("req_val_1", norm)
    prompt = PromptComposer.compose(analysis)
    result = PromptValidator.validate(analysis, prompt)

    assert result.is_valid is True
    assert len(result.errors) == 0


def test_validator_fails_on_fabricated_performance_targets():
    """
    Mandatory Rule 4: Catch fabricated performance targets in acceptance criteria.
    """
    norm = RequirementNormalizer.normalize(REQ_THAI_CRUD)
    analysis = RequirementAnalyzer.analyze("req_val_2", norm)
    prompt = PromptComposer.compose(analysis)

    # Artificially inject fabricated criteria
    prompt.acceptance_criteria.append("The API must respond within 2 seconds.")

    result = PromptValidator.validate(analysis, prompt)
    assert result.is_valid is False
    assert any("fabricated performance target" in err for err in result.errors)


def test_validator_catches_missing_clarification_for_high_ambiguity():
    """
    When high severity functional ambiguity is present, clarification questions are mandatory.
    """
    analysis = RequirementAnalysis(
        request_id="req_val_3",
        original_requirement="vague requirement",
        normalized_requirement="vague requirement",
        intent="vague",
        requested_actions=[],
        entities=[],
        constraints=[],
        technical_concepts=[],
        ambiguities=[
            Ambiguity(
                ambiguity_id="amb_1",
                description="High severity missing operations",
                severity=AmbiguitySeverity.HIGH,
                related_requirement="vague requirement",
                clarification_question="What operations?",
                is_functional=True,
            )
        ],
        assumptions=[],
    )
    prompt = EngineeringPrompt(
        id="prompt_val_3",
        request_id="req_val_3",
        title="Specification",
        objective="vague",
        requirements=["Implement vague requirement"],
        clarification_questions=[],  # Missing clarification questions!
    )

    result = PromptValidator.validate(analysis, prompt)
    assert result.is_valid is False
    assert any("High-severity functional ambiguity" in err for err in result.errors)
