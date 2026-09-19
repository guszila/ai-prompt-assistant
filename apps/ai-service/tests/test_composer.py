from app.engine.analyzer import RequirementAnalyzer
from app.engine.composer import PromptComposer
from app.engine.normalizer import RequirementNormalizer
from tests.fixtures.requirements import (
    REQ_AUTHN_ONLY,
    REQ_THAI_CRUD,
)


def test_composer_assembles_required_sections():
    norm = RequirementNormalizer.normalize(REQ_THAI_CRUD)
    analysis = RequirementAnalyzer.analyze("req_composer_1", norm)
    prompt = PromptComposer.compose(analysis)

    assert prompt.title.startswith("User")
    assert prompt.role == "Senior Software Engineer"
    assert "User" in prompt.objective
    assert len(prompt.requirements) > 0
    assert len(prompt.acceptance_criteria) > 0
    assert prompt.raw_markdown.startswith("# User")
    assert "## ROLE" in prompt.raw_markdown
    assert "## OBJECTIVE" in prompt.raw_markdown
    assert "## REQUIREMENTS" in prompt.raw_markdown
    assert "## ACCEPTANCE CRITERIA" in prompt.raw_markdown


def test_composer_omits_empty_sections():
    """
    If there are no explicit constraints, CONSTRAINTS section should be omitted from markdown.
    """
    norm = RequirementNormalizer.normalize(REQ_AUTHN_ONLY)
    analysis = RequirementAnalyzer.analyze("req_composer_2", norm)
    prompt = PromptComposer.compose(analysis)

    # REQ_AUTHN_ONLY has no explicit constraints
    if not prompt.constraints:
        assert "## CONSTRAINTS" not in prompt.raw_markdown


def test_composer_acceptance_criteria_has_no_fabricated_metrics():
    """
    Mandatory Rule 4: Acceptance criteria must formalize explicit requirements without
    introducing unrequested technical constraints or arbitrary performance metrics.
    """
    norm = RequirementNormalizer.normalize(REQ_THAI_CRUD)
    analysis = RequirementAnalyzer.analyze("req_composer_3", norm)
    prompt = PromptComposer.compose(analysis)

    for ac in prompt.acceptance_criteria:
        lower_ac = ac.lower()
        # Ensure no invented latencies or uptime numbers
        assert "within 2 seconds" not in lower_ac
        assert "under 500ms" not in lower_ac
        assert "99.9%" not in lower_ac
        assert "postgresql" not in lower_ac
        assert "mongodb" not in lower_ac
