import re
from typing import List, Tuple
from app.domain.prompt import NormalizedRequirement, RequirementAnalysis
from app.engine.ambiguity import AmbiguityDetector
from app.engine.terminology import EngineeringTerminologyMapper


class RequirementAnalyzer:
    """
    Deterministic requirement analyzer.
    Extracts intent, actions, entities, explicit constraints, technical concepts, and functional ambiguities.
    """

    # Common entity patterns in Thai and English
    ENTITY_PATTERNS: List[Tuple[str, str]] = [
        (r"สินค้า|product", "Product"),
        (r"พนักงาน|employee|staff", "Employee"),
        (r"ผู้ใช้|ผู้ใช้งาน|สมาชิก|user|member|customer", "User"),
        (r"คำสั่งซื้อ|การสั่งซื้อ|order", "Order"),
        (r"อาหาร|เมนู|food|menu", "Food Menu"),
        (r"ข้อเสนอแนะ|ความคิดเห็น|feedback|comment", "Feedback"),
        (r"ยอดขาย|รายรับ|sales?|revenue", "Sales"),
        (r"บทความ|โพสต์|article|post", "Article"),
        (r"การแจ้งเตือน|notification", "Notification"),
    ]

    # Action patterns
    ACTION_PATTERNS: List[Tuple[str, str]] = [
        (r"เพิ่ม|สร้าง|create|add|new", "create"),
        (r"แก้ไข|อัปเดต|อัพเดท|update|edit|modify", "update"),
        (r"ลบ|delete|remove", "delete"),
        (r"ค้นหา|สืบค้น|search|query|filter", "search"),
        (r"เข้าสู่ระบบ|ล็อกอิน|login|authenticate|sign(\s|-)?in", "authenticate"),
        (r"กำหนดสิทธิ์|สิทธิ์|permission|role|authorize", "authorize"),
        (r"ลืมรหัสผ่าน|รีเซ็ตรหัส|reset password", "password_reset"),
        (r"รายงาน|สรุป|report|summary", "report"),
        (r"ส่งข้อความ|ส่งข้อมูล|submit", "submit"),
        (r"ดู|แสดง|view|display", "view"),
    ]

    @classmethod
    def analyze(cls, request_id: str, norm: NormalizedRequirement) -> RequirementAnalysis:
        text = norm.normalized_text
        text_lower = text.lower()

        # 1. Action Extraction
        actions: List[str] = []
        for pattern, action_name in cls.ACTION_PATTERNS:
            if re.search(pattern, text_lower) and action_name not in actions:
                actions.append(action_name)

        # 2. Entity Extraction
        entities: List[str] = []
        for pattern, entity_name in cls.ENTITY_PATTERNS:
            if re.search(pattern, text_lower) and entity_name not in entities:
                entities.append(entity_name)

        # 3. Explicit Constraints Extraction
        # Look for explicit constraint phrases: "ต้อง...", "ห้าม...", "ไม่เกิน...", "must...", "cannot..."
        constraints: List[str] = []
        # Split into sentences or clauses (including Thai conjunctions)
        clauses = re.split(r"[\n,\.;]+|\s*(?:โดย|และ)\s+", text)
        for clause in clauses:
            trimmed = clause.strip()
            if not trimmed:
                continue
            trimmed_lower = trimmed.lower()

            # Thai constraint extraction
            thai_match = re.search(r"(?:ต้อง(?!การ)|ห้าม|ไม่เกิน|กำหนดให้).*$", trimmed)
            if thai_match:
                extracted = thai_match.group(0).strip()
                if extracted and extracted not in constraints:
                    constraints.append(extracted)
            # English constraint extraction
            elif any(kw in trimmed_lower for kw in ["must ", "cannot ", "should not ", "maximum ", "minimum "]):
                if trimmed not in constraints:
                    constraints.append(trimmed)
            elif any(kw in trimmed_lower for kw in ["rating 1-5", "1-5", "1 ถึง 5"]):
                const_desc = "Rating scale must be between 1 and 5."
                if const_desc not in constraints:
                    constraints.append(const_desc)

        # 4. Technical Concepts & Inferred Assumptions via Terminology Mapper
        concepts, assumptions = EngineeringTerminologyMapper.map_concepts(text)

        # 5. Intent Formulation
        intent = cls._derive_intent(actions, entities, text)

        # 6. Expected Output (if explicitly mentioned)
        expected_output = None
        if "endpoint" in text_lower or "rest api" in text_lower or "api" in text_lower:
            expected_output = "API endpoints with request and response contracts."
        elif "หน้า" in text or "web" in text_lower or "เว็บ" in text or "dashboard" in text_lower:
            expected_output = "User interface and application workflow specifications."

        # 7. Ambiguity Detection
        ambiguities = AmbiguityDetector.detect(text, actions, entities, intent)

        return RequirementAnalysis(
            request_id=request_id,
            original_requirement=norm.original_text,
            normalized_requirement=norm.normalized_text,
            intent=intent,
            requested_actions=actions,
            entities=entities,
            constraints=constraints,
            technical_concepts=concepts,
            expected_output=expected_output,
            ambiguities=ambiguities,
            assumptions=assumptions,
        )

    @classmethod
    def _derive_intent(cls, actions: List[str], entities: List[str], text: str) -> str:
        """Formulate a concise, clear intent description without hallucination."""
        entity_label = " / ".join(entities) if entities else "specified domain"
        if "create" in actions and "update" in actions and "delete" in actions:
            action_label = "CRUD operations"
        elif actions:
            action_label = ", ".join(actions)
        else:
            action_label = "management"

        return f"Implement {action_label} for {entity_label} based on user requirements."
