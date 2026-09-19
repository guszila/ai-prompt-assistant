import logging
from typing import Optional
from app.core.config import settings
from app.domain.prompt import PromptRequest, PromptTransformationResponse
from app.engine.analyzer import RequirementAnalyzer
from app.engine.composer import PromptComposer
from app.engine.enhancer import LLMRequirementEnhancer
from app.engine.normalizer import RequirementNormalizer
from app.engine.reconciler import GroundingReconciler
from app.engine.validator import PromptValidator
from app.llm.base import BaseLLMProvider
from app.llm.errors import LLMError
from app.llm.factory import get_llm_provider
from app.llm.models import LLMFallbackReason, LLMMetadata

logger = logging.getLogger(__name__)


class CorePromptEnginePipeline:
    """
    Orchestrates the prompt transformation pipeline.
    Preserves M2 deterministic normalization, analysis, composition, and validation
    as the authoritative baseline and guaranteed fallback.
    """

    @classmethod
    def execute(cls, request: PromptRequest) -> PromptTransformationResponse:
        """
        Synchronous deterministic M2 execution.
        Preserved for 100% backward compatibility with M2 consumers and tests.
        """
        normalized = RequirementNormalizer.normalize(request.raw_text)
        analysis = RequirementAnalyzer.analyze(request_id=request.id, norm=normalized)
        prompt = PromptComposer.compose(analysis=analysis)
        validation = PromptValidator.validate(analysis=analysis, prompt=prompt)

        return PromptTransformationResponse(
            request_id=request.id,
            normalized=normalized,
            analysis=analysis,
            prompt=prompt,
            validation=validation,
            llm_metadata=None,
        )

    @classmethod
    async def execute_async(
        cls,
        request: PromptRequest,
        provider: Optional[BaseLLMProvider] = None,
    ) -> PromptTransformationResponse:
        """
        Asynchronous execution supporting optional LLM enhancement with M2 baseline preservation
        and automatic fallback to M2 on any LLM failure.
        """
        # 1. Normalize requirement (M2 deterministic)
        normalized = RequirementNormalizer.normalize(request.raw_text)

        # 2. Complete M2 baseline analysis (authoritative ground truth)
        baseline_analysis = RequirementAnalyzer.analyze(request_id=request.id, norm=normalized)

        # 3. Determine if LLM enhancement is requested
        should_use_llm = request.enable_llm if request.enable_llm is not None else settings.LLM_ENABLED

        analysis = baseline_analysis
        llm_metadata: Optional[LLMMetadata] = None

        if should_use_llm:
            active_provider = provider
            try:
                if not active_provider:
                    active_provider = get_llm_provider(settings.LLM_PROVIDER)

                candidate, metadata = await LLMRequirementEnhancer.enhance(
                    normalized=normalized,
                    baseline=baseline_analysis,
                    provider=active_provider,
                )

                # Grounding reconciliation: Level 1 (Explicit Input) > Level 2 (M2) > Level 3 (LLM Candidate)
                analysis = GroundingReconciler.reconcile(
                    baseline=baseline_analysis,
                    candidate=candidate,
                )
                llm_metadata = metadata

            except LLMError as exc:
                logger.warning("LLM enhancement failed (%s); gracefully falling back to M2 baseline", exc.reason)
                provider_name = active_provider.provider_name if active_provider else settings.LLM_PROVIDER
                analysis = baseline_analysis
                llm_metadata = LLMMetadata(
                    provider=provider_name,
                    model=settings.LLM_MODEL,
                    enhanced=False,
                    fallback_used=True,
                    fallback_reason=exc.reason,
                )
            except Exception as exc:
                logger.warning("Unexpected error during LLM enhancement (%s); falling back to M2 baseline", str(exc))
                provider_name = active_provider.provider_name if active_provider else settings.LLM_PROVIDER
                analysis = baseline_analysis
                llm_metadata = LLMMetadata(
                    provider=provider_name,
                    model=settings.LLM_MODEL,
                    enhanced=False,
                    fallback_used=True,
                    fallback_reason=LLMFallbackReason.NETWORK_ERROR,
                )
        else:
            # LLM intentionally disabled: enhanced=False, fallback_used=False, fallback_reason=None
            llm_metadata = LLMMetadata(
                provider="none",
                model="none",
                enhanced=False,
                fallback_used=False,
                fallback_reason=None,
            )

        # 4. Compose structured engineering prompt (M2)
        prompt = PromptComposer.compose(analysis=analysis)

        # 5. Validate prompt structure and safety against requirement fabrication (M2)
        validation = PromptValidator.validate(analysis=analysis, prompt=prompt)

        return PromptTransformationResponse(
            request_id=request.id,
            normalized=normalized,
            analysis=analysis,
            prompt=prompt,
            validation=validation,
            llm_metadata=llm_metadata,
        )
