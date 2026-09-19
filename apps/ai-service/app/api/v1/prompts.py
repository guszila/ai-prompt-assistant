from fastapi import APIRouter, HTTPException, status
from app.domain.prompt import PromptRequest, PromptTransformationResponse
from app.services.prompt_service import PromptService

router = APIRouter(prefix="/prompts", tags=["Prompts"])


@router.post(
    "/analyze",
    response_model=PromptTransformationResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze natural language requirement and compose structured prompt",
)
async def analyze_prompt(request: PromptRequest) -> PromptTransformationResponse:
    """
    Transforms a natural language requirement into a structured engineering prompt.
    Executes normalization, analysis, terminology mapping, composition, and validation.
    """
    try:
        return PromptService.analyze_and_generate(request)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing requirement: {str(exc)}",
        ) from exc
