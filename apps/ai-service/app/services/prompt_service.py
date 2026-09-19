import uuid
from typing import Optional
from app.domain.prompt import PromptRequest, PromptTransformationResponse, RequirementLanguage
from app.engine.pipeline import CorePromptEnginePipeline


class PromptService:
    """Service layer coordinating core prompt engine operations."""

    @staticmethod
    def analyze_and_generate(request: PromptRequest) -> PromptTransformationResponse:
        """
        Executes the deterministic prompt engine pipeline on the given request.
        """
        return CorePromptEnginePipeline.execute(request)

    @classmethod
    def transform_text(
        cls,
        raw_text: str,
        request_id: Optional[str] = None,
        language: RequirementLanguage = RequirementLanguage.THAI,
    ) -> PromptTransformationResponse:
        """
        Convenience method to transform raw requirement text into a structured prompt.
        """
        req_id = request_id or str(uuid.uuid4())
        request = PromptRequest(id=req_id, raw_text=raw_text, language=language)
        return cls.analyze_and_generate(request)
