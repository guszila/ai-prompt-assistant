from app.domain.prompt import PromptRequest
from app.engine.pipeline import CorePromptEnginePipeline
from tests.fixtures.requirements import (
    REQ_AUTH_COMBINED,
    REQ_DASHBOARD,
    REQ_GENERIC_API,
    REQ_REST_API,
    REQ_THAI_CRUD,
)


def test_pipeline_determinism_thai_crud():
    """
    Mandatory Rule: 10 repeated executions of the pipeline on identical input
    must yield bit-for-bit identical markdown and structural analysis.
    """
    req = PromptRequest(id="det_test_req_1", raw_text=REQ_THAI_CRUD)

    reference_result = CorePromptEnginePipeline.execute(req)
    ref_markdown = reference_result.prompt.raw_markdown
    ref_concepts = [c.name for c in reference_result.analysis.technical_concepts]
    ref_actions = list(reference_result.analysis.requested_actions)

    for i in range(10):
        run_result = CorePromptEnginePipeline.execute(req)
        assert run_result.prompt.raw_markdown == ref_markdown, f"Run {i+1} markdown diverged!"
        assert [c.name for c in run_result.analysis.technical_concepts] == ref_concepts
        assert run_result.analysis.requested_actions == ref_actions
        assert run_result.validation.is_valid is True


def test_pipeline_determinism_across_varied_fixtures():
    """
    Ensure determinism across multiple different requirements.
    """
    fixtures = [REQ_AUTH_COMBINED, REQ_DASHBOARD, REQ_GENERIC_API, REQ_REST_API]
    for fixture in fixtures:
        req = PromptRequest(id="det_test_multi", raw_text=fixture)
        first_run = CorePromptEnginePipeline.execute(req)
        second_run = CorePromptEnginePipeline.execute(req)

        assert first_run.prompt.raw_markdown == second_run.prompt.raw_markdown
        assert first_run.prompt.requirements == second_run.prompt.requirements
        assert first_run.prompt.acceptance_criteria == second_run.prompt.acceptance_criteria
        assert first_run.validation.is_valid is True
