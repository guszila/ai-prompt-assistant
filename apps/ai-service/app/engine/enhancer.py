from typing import Tuple
from app.domain.prompt import NormalizedRequirement, RequirementAnalysis
from app.llm.base import BaseLLMProvider
from app.llm.models import LLMMetadata, LLMRequirementCandidate

SYSTEM_PROMPT = """You are a senior software engineering assistant.
Your task is to analyze user software requirements and suggest technical refinements,
architectural assumptions, and targeted clarification questions.

RULES:
1. Do NOT invent unrequested technologies, frameworks, or databases (e.g., PostgreSQL, Redis, React, FastAPI).
2. Do NOT invent unrequested performance targets or SLAs (e.g., "< 500ms", "99.9% uptime").
3. Suggest unconfirmed inferences strictly as assumptions that require user confirmation.
4. Output strictly valid JSON matching the specified schema.
"""


class LLMRequirementEnhancer:
    """
    Coordinates LLM invocation for requirement enrichment.
    Supplies the raw user input along with the authoritative M2 baseline analysis.
    """

    @classmethod
    async def enhance(
        cls,
        normalized: NormalizedRequirement,
        baseline: RequirementAnalysis,
        provider: BaseLLMProvider,
    ) -> Tuple[LLMRequirementCandidate, LLMMetadata]:
        prompt_lines = [
            f"Raw Requirement: {normalized.normalized_text}",
            "\nDeterministic M2 Baseline Analysis:",
            f"- Identified Intent: {baseline.intent}",
            f"- Requested Actions: {', '.join(baseline.requested_actions) if baseline.requested_actions else 'None'}",
            f"- Target Entities: {', '.join(baseline.entities) if baseline.entities else 'None'}",
            f"- Explicit Constraints: {', '.join(baseline.constraints) if baseline.constraints else 'None'}",
            f"- Technical Concepts: {', '.join([c.name for c in baseline.technical_concepts]) if baseline.technical_concepts else 'None'}",
            "\nPlease review and suggest refined technical wording, explicit assumptions for inferences, or functional clarifications.",
        ]

        user_prompt = "\n".join(prompt_lines)

        return await provider.generate_structured(
            prompt=user_prompt,
            response_model=LLMRequirementCandidate,
            system_prompt=SYSTEM_PROMPT,
        )
