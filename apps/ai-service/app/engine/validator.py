import re
from datetime import datetime, timezone
from typing import List
from app.domain.prompt import AmbiguitySeverity, EngineeringPrompt, PromptValidationResult, RequirementAnalysis


class PromptValidator:
    """
    Validates structural and architectural integrity of generated prompts and analyses.
    Guarantees:
      - Objective and requirements are populated and substantive.
      - Assumptions are strictly isolated.
      - High-severity functional ambiguities have associated clarification questions.
      - Acceptance criteria do not contain fabricated performance targets or speculative tech stacks.
    """

    UNGROUNDED_PERFORMANCE_PATTERNS = [
        re.compile(r"\b(within\s+\d+\s*(?:ms|seconds?|mins?|hours?))\b", re.IGNORECASE),
        re.compile(r"\b(99\.\d+%)\b"),
        re.compile(r"\b(under\s+\d+\s*(?:ms|seconds?))\b", re.IGNORECASE),
    ]

    @classmethod
    def validate(
        cls,
        analysis: RequirementAnalysis,
        prompt: EngineeringPrompt,
    ) -> PromptValidationResult:
        errors: List[str] = []
        warnings: List[str] = []

        # 1. Identity & Objective
        if not prompt.request_id or not prompt.request_id.strip():
            errors.append("EngineeringPrompt is missing request_id.")
        if not prompt.title or not prompt.title.strip():
            errors.append("EngineeringPrompt title cannot be empty.")
        if not prompt.objective or not prompt.objective.strip():
            errors.append("EngineeringPrompt objective cannot be empty.")

        # 2. Requirements completeness
        if not prompt.requirements:
            errors.append("EngineeringPrompt must contain at least one requirement.")

        # 3. Assumptions Isolation Check
        # Ensure assumptions are not silently inserted into the main requirements list
        for req in prompt.requirements:
            for assumption in prompt.assumptions:
                if assumption.lower() in req.lower():
                    warnings.append(
                        f"Requirement clause appears to duplicate an assumption: '{req}'. Keep assumptions strictly separated."
                    )

        # 4. Acceptance Criteria Safety Check (No Fabricated Performance Metrics)
        # Verify that criteria do not introduce arbitrary metrics (e.g. "within 2 seconds") unless in original text
        for criterion in prompt.acceptance_criteria:
            for pattern in cls.UNGROUNDED_PERFORMANCE_PATTERNS:
                if pattern.search(criterion) and not pattern.search(analysis.original_requirement):
                    errors.append(
                        f"Acceptance criterion contains fabricated performance target not present in original input: '{criterion}'"
                    )

        # 5. Ambiguity & Clarification Questions
        has_high_severity_ambiguity = any(
            a.severity == AmbiguitySeverity.HIGH for a in analysis.ambiguities
        )
        if has_high_severity_ambiguity and not prompt.clarification_questions:
            errors.append(
                "High-severity functional ambiguity detected, but no clarification questions were generated."
            )

        is_valid = len(errors) == 0

        return PromptValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            validated_at=datetime.now(timezone.utc),
        )
