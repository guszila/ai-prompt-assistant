from typing import List
from app.domain.prompt import EngineeringPrompt, RequirementAnalysis


class PromptComposer:
    """
    Deterministic prompt composer.
    Assembles structured engineering prompt sections into standardized Markdown.
    Guarantees:
      - Omission of empty sections.
      - Acceptance criteria strictly formalize explicit requirements without introducing unrequested technical constraints or performance targets.
      - Clear separation of Assumptions and Clarification Questions.
    """

    @classmethod
    def compose(cls, analysis: RequirementAnalysis) -> EngineeringPrompt:
        title = cls._derive_title(analysis)
        role = "Senior Software Engineer"
        objective = analysis.intent
        context = f"Requirement for {', '.join(analysis.entities) if analysis.entities else 'software system'}."

        # 1. Actionable Requirements List
        requirements: List[str] = []
        for action in analysis.requested_actions:
            entity_str = ", ".join(analysis.entities) if analysis.entities else "records"
            if action == "create":
                requirements.append(f"Provide capability to create new {entity_str}.")
            elif action == "update":
                requirements.append(f"Provide capability to update existing {entity_str}.")
            elif action == "delete":
                requirements.append(f"Provide capability to delete {entity_str}.")
            elif action == "search":
                requirements.append(f"Provide capability to search and filter {entity_str}.")
            elif action == "authenticate":
                requirements.append("Implement user authentication mechanism.")
            elif action == "authorize":
                requirements.append("Implement access control and authorization policies.")
            elif action == "password_reset":
                requirements.append("Implement password recovery or reset workflow.")
            elif action == "report":
                requirements.append("Provide reporting and summary data visualization.")
            elif action == "submit":
                requirements.append(f"Provide capability to submit {entity_str}.")
            elif action == "view":
                requirements.append(f"Provide capability to view details of {entity_str}.")

        # If no specific action was identified, use the normalized requirement directly
        if not requirements:
            requirements.append(f"Implement requested functionality: {analysis.normalized_requirement}")

        # 2. Technical Details
        technical_details: List[str] = [
            f"{c.name} ({'Inferred' if c.is_inferred else 'Explicit'})" for c in analysis.technical_concepts
        ]

        # 3. Constraints (Explicit only)
        constraints = list(analysis.constraints)

        # 4. Expected Output
        expected_output = analysis.expected_output or "Complete implementation code, data models, and verification steps."

        # 5. Acceptance Criteria (Strict Formalization - NO invented performance targets or tech stacks)
        acceptance_criteria: List[str] = []
        for req in requirements:
            acceptance_criteria.append(f"The system must verify that: {req.rstrip('.')}")

        # 6. Assumptions List
        assumptions: List[str] = [a.description for a in analysis.assumptions]

        # 7. Clarification Questions
        clarification_questions: List[str] = [
            a.clarification_question for a in analysis.ambiguities if a.clarification_question
        ]

        # 8. Assemble Deterministic Markdown Body
        markdown_parts: List[str] = []

        markdown_parts.append(f"# {title}\n")
        markdown_parts.append(f"## ROLE\n{role}\n")
        markdown_parts.append(f"## OBJECTIVE\n{objective}\n")

        if context:
            markdown_parts.append(f"## CONTEXT\n{context}\n")

        if requirements:
            req_lines = [f"{i+1}. {r}" for i, r in enumerate(requirements)]
            markdown_parts.append(f"## REQUIREMENTS\n" + "\n".join(req_lines) + "\n")

        if technical_details:
            tech_lines = [f"- {t}" for t in technical_details]
            markdown_parts.append(f"## TECHNICAL DETAILS\n" + "\n".join(tech_lines) + "\n")

        if constraints:
            constraint_lines = [f"- {c}" for c in constraints]
            markdown_parts.append(f"## CONSTRAINTS\n" + "\n".join(constraint_lines) + "\n")

        if expected_output:
            markdown_parts.append(f"## EXPECTED OUTPUT\n{expected_output}\n")

        if acceptance_criteria:
            criteria_lines = [f"- [ ] {c}" for c in acceptance_criteria]
            markdown_parts.append(f"## ACCEPTANCE CRITERIA\n" + "\n".join(criteria_lines) + "\n")

        if assumptions:
            assumption_lines = [f"- {a}" for a in assumptions]
            markdown_parts.append(f"## ASSUMPTIONS\n" + "\n".join(assumption_lines) + "\n")

        if clarification_questions:
            q_lines = [f"{i+1}. {q}" for i, q in enumerate(clarification_questions)]
            markdown_parts.append(f"## CLARIFICATION QUESTIONS\n" + "\n".join(q_lines) + "\n")

        raw_markdown = "\n".join(markdown_parts).strip()

        return EngineeringPrompt(
            id=f"prompt_{analysis.request_id}",
            request_id=analysis.request_id,
            title=title,
            role=role,
            objective=objective,
            context=context,
            requirements=requirements,
            technical_details=technical_details,
            constraints=constraints,
            expected_output=expected_output,
            acceptance_criteria=acceptance_criteria,
            assumptions=assumptions,
            clarification_questions=clarification_questions,
            raw_markdown=raw_markdown,
        )

    @classmethod
    def _derive_title(cls, analysis: RequirementAnalysis) -> str:
        entities_str = " ".join(analysis.entities) if analysis.entities else "Feature"
        return f"{entities_str} Implementation Specification"
