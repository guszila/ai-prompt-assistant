import uuid
from typing import Optional
from app.domain.prompt import PromptRequest, PromptTransformationResponse, RequirementLanguage
from app.engine.pipeline import CorePromptEnginePipeline
from app.llm.base import BaseLLMProvider


class PromptService:
    """Service layer coordinating core prompt engine operations."""

    @staticmethod
    def analyze_and_generate(request: PromptRequest) -> PromptTransformationResponse:
        """
        Executes the deterministic prompt engine pipeline on the given request.
        """
        return CorePromptEnginePipeline.execute(request)

    @staticmethod
    async def analyze_and_generate_async(
        request: PromptRequest,
        provider: Optional[BaseLLMProvider] = None,
    ) -> PromptTransformationResponse:
        """
        Executes the prompt engine pipeline asynchronously with optional LLM enhancement
        and automatic fallback to M2 on failure.
        """
        return await CorePromptEnginePipeline.execute_async(request, provider=provider)

    @classmethod
    async def transform_text_async(
        cls,
        raw_text: str,
        request_id: Optional[str] = None,
        language: RequirementLanguage = RequirementLanguage.THAI,
        enable_llm: Optional[bool] = None,
        provider: Optional[BaseLLMProvider] = None,
    ) -> PromptTransformationResponse:
        """
        Convenience method to transform raw requirement text with optional LLM enhancement.
        """
        req_id = request_id or str(uuid.uuid4())
        request = PromptRequest(
            id=req_id,
            raw_text=raw_text,
            language=language,
            enable_llm=enable_llm,
        )
        return await cls.analyze_and_generate_async(request, provider=provider)

    @classmethod
    def transform_text(
        cls,
        raw_text: str,
        request_id: Optional[str] = None,
        language: RequirementLanguage = RequirementLanguage.THAI,
    ) -> PromptTransformationResponse:
        """
        Synchronous convenience method to transform raw requirement text into a structured prompt.
        """
        req_id = request_id or str(uuid.uuid4())
        request = PromptRequest(id=req_id, raw_text=raw_text, language=language)
        return cls.analyze_and_generate(request)
