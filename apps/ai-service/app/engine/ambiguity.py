from typing import List
from app.domain.prompt import Ambiguity, AmbiguitySeverity


class AmbiguityDetector:
    """
    Detects missing functional information that materially affects system behavior.
    Focuses strictly on functional requirements:
      - Does NOT demand technical preferences (e.g., database, frontend framework, cloud).
      - Produces targeted, actionable clarification questions for missing operations or scopes.
    """

    @classmethod
    def detect(
        cls,
        text: str,
        actions: List[str],
        entities: List[str],
        intent: str,
    ) -> List[Ambiguity]:
        """
        Analyze requirement context to identify functional ambiguities.
        """
        ambiguities: List[Ambiguity] = []
        text_lower = text.lower()

        # 1. Broad / Vague Scope with Zero Specific Actions
        # Example: "ทำเว็บจัดการพนักงาน", "ทำระบบสินค้า", "build user system"
        if not actions and entities:
            entity_str = ", ".join(entities)
            ambiguities.append(
                Ambiguity(
                    ambiguity_id="amb_missing_functional_operations",
                    description=f"The requirement requests management of {entity_str}, but does not specify the functional operations required.",
                    severity=AmbiguitySeverity.HIGH,
                    related_requirement=text,
                    clarification_question=f"What operations are required for managing {entity_str}? (e.g., create, update, delete, view profile, or search)",
                    is_functional=True,
                )
            )

        # 2. Authentication Mentioned Without Scope of User Types or Self-Service
        # If user explicitly asks for authentication, check if password recovery or self-registration scope is clear
        if any(term in text for term in ["เข้าสู่ระบบ", "login", "ล็อกอิน"]) and not any(
            term in text for term in ["ลืมรหัสผ่าน", "รีเซ็ต", "สมัครสมาชิก", "register", "password reset"]
        ):
            # Only generate a LOW severity note; do not block with high severity
            ambiguities.append(
                Ambiguity(
                    ambiguity_id="amb_auth_self_service_scope",
                    description="Authentication is requested, but self-registration or password reset flows are not mentioned.",
                    severity=AmbiguitySeverity.LOW,
                    related_requirement=text,
                    clarification_question="Should the authentication system include self-registration and password recovery capabilities?",
                    is_functional=True,
                )
            )

        # 3. Search Mentioned Without Search Target or Criteria
        # e.g. "อยากให้ค้นหาได้" without entity or criteria
        if any(term in text for term in ["ค้นหา", "search"]) and not entities:
            ambiguities.append(
                Ambiguity(
                    ambiguity_id="amb_search_criteria_unspecified",
                    description="Search capability was requested without specifying the target entity or searchable fields.",
                    severity=AmbiguitySeverity.MEDIUM,
                    related_requirement=text,
                    clarification_question="What data or entity should be searchable, and by which fields?",
                    is_functional=True,
                )
            )

        # 4. Notification Mentioned Without Delivery Channel or Trigger Event
        if any(term in text for term in ["แจ้งเตือน", "notification"]) and not any(
            term in text_lower for term in ["email", "sms", "push", "line", "webhook", "เมล", "ข้อความ"]
        ):
            ambiguities.append(
                Ambiguity(
                    ambiguity_id="amb_notification_channel_unspecified",
                    description="Notification capability requested without specifying delivery channels or trigger events.",
                    severity=AmbiguitySeverity.MEDIUM,
                    related_requirement=text,
                    clarification_question="What delivery channels (e.g., in-app, email, webhook) and triggering events should initiate notifications?",
                    is_functional=True,
                )
            )

        return ambiguities
