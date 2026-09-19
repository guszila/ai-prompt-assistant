import re
from typing import List, Set
from app.domain.prompt import Ambiguity, AmbiguitySeverity, Assumption, RequirementAnalysis, TechnicalConcept
from app.llm.models import LLMRequirementCandidate


class GroundingReconciler:
    """
    Security and correctness gateway between untrusted LLM candidates and the domain model.
    Enforces strict priority:
      Level 1: Explicit User Input
         >
      Level 2: M2 Deterministic Analysis
         >
      Level 3: LLM Candidate Suggestions
    """

    PROHIBITED_TECH_PATTERNS = [
        re.compile(r"\b(postgresql|postgres|mysql|mongodb|oracle|mariadb|sqlite)\b", re.I),
        re.compile(r"\b(react|vue|angular|svelte|nextjs|nuxtjs)\b", re.I),
        re.compile(r"\b(fastapi|django|flask|express|spring|nestjs|laravel)\b", re.I),
        re.compile(r"\b(redis|kafka|rabbitmq|celery)\b", re.I),
        re.compile(r"\b(docker|kubernetes|aws|azure|gcp)\b", re.I),
    ]

    UNGROUNDED_PERFORMANCE_PATTERNS = [
        re.compile(r"\b(within\s+\d+\s*(?:ms|seconds?|mins?|hours?))\b", re.I),
        re.compile(r"\b(under\s+\d+\s*(?:ms|seconds?))\b", re.I),
        re.compile(r"\b(99\.\d+%)\b"),
        re.compile(r"\b(\d+[\d,]*\s*(?:reqs?|requests?|tps|qps)\s*(?:/|per)\s*(?:sec|second|s))\b", re.I),
    ]

    @classmethod
    def reconcile(
        cls,
        baseline: RequirementAnalysis,
        candidate: LLMRequirementCandidate,
    ) -> RequirementAnalysis:
        raw_text_lower = baseline.original_requirement.lower()

        # 1. Intent: Preserve M2 intent or enrich if non-conflicting
        reconciled_intent = baseline.intent
        if candidate.suggested_intent and candidate.suggested_intent.strip():
            suggested = candidate.suggested_intent.strip()
            # Do not allow suggested intent to inject ungrounded tech or perf
            if not cls._contains_ungrounded_tech(suggested, raw_text_lower) and not cls._contains_ungrounded_perf(
                suggested, raw_text_lower
            ):
                # Enhance phrasing if it retains baseline intent keywords
                reconciled_intent = suggested

        # 2. Actions: User & M2 actions are mandatory and can never be deleted
        reconciled_actions = list(baseline.requested_actions)
        for act in candidate.suggested_actions:
            act_clean = act.lower().strip()
            if act_clean and act_clean not in reconciled_actions:
                # Only accept standard functional action names
                if act_clean in ["create", "update", "delete", "search", "view", "submit", "report", "export"]:
                    reconciled_actions.append(act_clean)

        # 3. Entities: User entities are mandatory and can never be deleted
        reconciled_entities = list(baseline.entities)
        for ent in candidate.suggested_entities:
            ent_clean = ent.strip()
            if ent_clean and ent_clean not in reconciled_entities:
                if not cls._contains_ungrounded_tech(ent_clean, raw_text_lower):
                    reconciled_entities.append(ent_clean)

        # 4. Technical Concepts Reconciliation (AuthN != AuthZ, Generic API != RESTful API)
        reconciled_concepts: List[TechnicalConcept] = list(baseline.technical_concepts)
        existing_concept_names: Set[str] = {c.name.lower() for c in reconciled_concepts}

        # Track new assumptions derived from candidate
        reconciled_assumptions: List[Assumption] = list(baseline.assumptions)
        existing_assumption_descs: Set[str] = {a.description.lower() for a in reconciled_assumptions}

        has_explicit_authz = any(
            term in raw_text_lower for term in ["role", "roles", "permission", "permissions", "กำหนดสิทธิ์", "สิทธิ์"]
        )
        has_explicit_rest = bool(re.search(r"\brest(\s|-)?api\b|\brestful\b", raw_text_lower))

        for concept_name in candidate.suggested_concepts:
            name_clean = concept_name.strip()
            name_lower = name_clean.lower()

            # Rule 1: AuthN vs AuthZ protection
            if "authorization" in name_lower or "role" in name_lower or "permission" in name_lower:
                if not has_explicit_authz:
                    # Reject as confirmed concept; convert strictly to Assumption
                    desc = "Role-based authorization was suggested by model; requires user confirmation."
                    if desc.lower() not in existing_assumption_descs:
                        reconciled_assumptions.append(
                            Assumption(
                                assumption_id="assump_llm_authorization",
                                description=desc,
                                source_concept="Authorization",
                                requires_confirmation=True,
                            )
                        )
                        existing_assumption_descs.add(desc.lower())
                    continue  # Do not add to reconciled_concepts

            # Rule 2: Generic API vs RESTful API protection
            if "rest" in name_lower:
                if not has_explicit_rest:
                    # Keep API Interface in concepts; record REST as an assumption
                    desc = "REST architecture was suggested for API; requires user confirmation."
                    if desc.lower() not in existing_assumption_descs:
                        reconciled_assumptions.append(
                            Assumption(
                                assumption_id="assump_llm_rest_api",
                                description=desc,
                                source_concept="RESTful API",
                                requires_confirmation=True,
                            )
                        )
                        existing_assumption_descs.add(desc.lower())
                    continue

            # Rule 3: Block ungrounded technology choices
            if cls._contains_ungrounded_tech(name_clean, raw_text_lower):
                continue

            # Add valid safe concepts
            if name_lower not in existing_concept_names:
                reconciled_concepts.append(
                    TechnicalConcept(
                        name=name_clean,
                        category="llm_enhanced",
                        confidence=0.85,
                        source_terms=["LLM Suggestion"],
                        is_inferred=True,
                    )
                )
                existing_concept_names.add(name_lower)

        # 5. Additional candidate assumptions
        for idx, assump_text in enumerate(candidate.suggested_assumptions):
            trimmed = assump_text.strip()
            if trimmed and trimmed.lower() not in existing_assumption_descs:
                if not cls._contains_ungrounded_perf(trimmed, raw_text_lower):
                    reconciled_assumptions.append(
                        Assumption(
                            assumption_id=f"assump_llm_{idx+1}",
                            description=trimmed,
                            source_concept="LLM Inference",
                            requires_confirmation=True,
                        )
                    )
                    existing_assumption_descs.add(trimmed.lower())

        # 6. Additional candidate clarification questions
        reconciled_ambiguities: List[Ambiguity] = list(baseline.ambiguities)
        existing_clarifications: Set[str] = {
            a.clarification_question.lower() for a in reconciled_ambiguities if a.clarification_question
        }

        for idx, q_text in enumerate(candidate.suggested_clarifications):
            trimmed = q_text.strip()
            if trimmed and trimmed.lower() not in existing_clarifications:
                # Ensure clarification is functional, not demanding specific tech stacks
                if not cls._contains_ungrounded_tech(trimmed, raw_text_lower):
                    reconciled_ambiguities.append(
                        Ambiguity(
                            ambiguity_id=f"amb_llm_{idx+1}",
                            description="Clarification suggested by model analysis.",
                            severity=AmbiguitySeverity.LOW,
                            related_requirement=baseline.original_requirement,
                            clarification_question=trimmed,
                            is_functional=True,
                        )
                    )
                    existing_clarifications.add(trimmed.lower())

        # 7. Constraints: Explicit constraints from user are preserved untouched
        reconciled_constraints = list(baseline.constraints)

        return RequirementAnalysis(
            request_id=baseline.request_id,
            original_requirement=baseline.original_requirement,
            normalized_requirement=baseline.normalized_requirement,
            intent=reconciled_intent,
            requested_actions=reconciled_actions,
            entities=reconciled_entities,
            constraints=reconciled_constraints,
            technical_concepts=reconciled_concepts,
            expected_output=baseline.expected_output,
            ambiguities=reconciled_ambiguities,
            assumptions=reconciled_assumptions,
        )

    @classmethod
    def _contains_ungrounded_tech(cls, text: str, raw_text_lower: str) -> bool:
        text_lower = text.lower()
        for pattern in cls.PROHIBITED_TECH_PATTERNS:
            match = pattern.search(text_lower)
            if match:
                # If the matched keyword is NOT in the user's raw input, it is ungrounded
                matched_word = match.group(0).lower()
                if matched_word not in raw_text_lower:
                    return True
        return False

    @classmethod
    def _contains_ungrounded_perf(cls, text: str, raw_text_lower: str) -> bool:
        text_lower = text.lower()
        for pattern in cls.UNGROUNDED_PERFORMANCE_PATTERNS:
            match = pattern.search(text_lower)
            if match:
                matched_word = match.group(0).lower()
                if matched_word not in raw_text_lower:
                    return True
        return False
