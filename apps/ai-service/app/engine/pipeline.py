from app.domain.prompt import PromptRequest, PromptTransformationResponse
from app.engine.analyzer import RequirementAnalyzer
from app.engine.composer import PromptComposer
from app.engine.normalizer import RequirementNormalizer
from app.engine.validator import PromptValidator


class CorePromptEnginePipeline:
    """
    Orchestrates the deterministic transformation pipeline:
    PromptRequest
        ↓
    RequirementNormalizer
        ↓
    RequirementAnalyzer
        ↓
    PromptComposer
        ↓
    PromptValidator
        ↓
    PromptTransformationResponse
    """

    @classmethod
    def execute(cls, request: PromptRequest) -> PromptTransformationResponse:
        # 1. Normalize requirement (preserves original text)
        normalized = RequirementNormalizer.normalize(request.raw_text)

        # 2. Analyze requirement (intent, actions, entities, concepts, ambiguities, assumptions)
        analysis = RequirementAnalyzer.analyze(request_id=request.id, norm=normalized)

        # 3. Compose structured engineering prompt
        prompt = PromptComposer.compose(analysis=analysis)

        # 4. Validate prompt structure and safety against requirement fabrication
        validation = PromptValidator.validate(analysis=analysis, prompt=prompt)

        return PromptTransformationResponse(
            request_id=request.id,
            normalized=normalized,
            analysis=analysis,
            prompt=prompt,
            validation=validation,
        )
