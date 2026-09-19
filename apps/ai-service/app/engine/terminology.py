import re
from typing import List, Tuple
from app.domain.prompt import Assumption, TechnicalConcept


class EngineeringTerminologyMapper:
    """
    Extensible terminology transformation layer.
    Maps natural-language user expressions (Thai/English) into precise software engineering concepts.
    Enforces strict boundaries:
      - Separates Authentication from Authorization (never infer Authorization from Login alone).
      - Separates generic API from RESTful API (never infer REST without explicit mention).
      - Clearly marks inferred concepts (is_inferred = True) and generates explicit Assumptions.
    """

    @classmethod
    def map_concepts(cls, text: str) -> Tuple[List[TechnicalConcept], List[Assumption]]:
        """
        Analyze text to extract technical concepts and generate associated assumptions for inferred concepts.
        """
        text_lower = text.lower()
        concepts: List[TechnicalConcept] = []
        assumptions: List[Assumption] = []
        seen_concept_names: set[str] = set()

        def add_concept(concept: TechnicalConcept, assumption_desc: str | None = None) -> None:
            if concept.name in seen_concept_names:
                return
            seen_concept_names.add(concept.name)
            concepts.append(concept)
            if concept.is_inferred and assumption_desc:
                assumptions.append(
                    Assumption(
                        assumption_id=f"assump_{concept.name.lower().replace(' ', '_')}",
                        description=assumption_desc,
                        source_concept=concept.name,
                        requires_confirmation=True,
                    )
                )

        # -------------------------------------------------------------
        # 1. API: Generic API vs RESTful API (Strict Separation)
        # -------------------------------------------------------------
        # Check explicit REST API first
        if re.search(r"\brest(\s|-)?api\b|\brestful\b", text_lower):
            add_concept(
                TechnicalConcept(
                    name="RESTful API",
                    category="architecture",
                    confidence=1.0,
                    source_terms=["REST API" if "rest api" in text_lower else "RESTful"],
                    is_inferred=False,
                )
            )
        elif re.search(r"\bapi\b", text_lower):
            add_concept(
                TechnicalConcept(
                    name="API Interface",
                    category="architecture",
                    confidence=1.0,
                    source_terms=["API"],
                    is_inferred=False,
                )
            )

        # -------------------------------------------------------------
        # 2. Authentication vs Authorization (Strict Separation)
        # -------------------------------------------------------------
        # Authentication triggers (Login, Sign-in, Register, Password reset)
        authn_terms = []
        if any(term in text for term in ["เข้าสู่ระบบ", "ล็อกอิน", "ลืมรหัสผ่าน", "รีเซ็ตรหัส", "สมัครสมาชิก", "ลงชื่อเข้าใช้"]):
            authn_terms.append("เข้าสู่ระบบ/จัดการบัญชี")
        if re.search(r"\b(login|sign(\s|-)?in|authenticate|authentication|auth|password(\s|-)?reset)\b", text_lower):
            authn_terms.append("login/authentication")

        if authn_terms:
            add_concept(
                TechnicalConcept(
                    name="Authentication",
                    category="security",
                    confidence=1.0,
                    source_terms=authn_terms,
                    is_inferred=False,
                )
            )

        # Authorization triggers (Roles, Permissions, Access Control, กำหนดสิทธิ์)
        authz_terms = []
        if any(term in text for term in ["กำหนดสิทธิ์", "สิทธิ์การเข้าถึง", "สิทธิ์ผู้ใช้", "ระดับผู้ใช้"]):
            authz_terms.append("กำหนดสิทธิ์/ระดับผู้ใช้")
        if re.search(r"\b(role|roles|permission|permissions|authorization|rbac|access(\s|-)?control)\b", text_lower):
            authz_terms.append("roles/permissions")

        if authz_terms:
            add_concept(
                TechnicalConcept(
                    name="Authorization",
                    category="security",
                    confidence=1.0,
                    source_terms=authz_terms,
                    is_inferred=False,
                )
            )

        # Specific Authentication tokens (JWT)
        if "jwt" in text_lower:
            add_concept(
                TechnicalConcept(
                    name="JWT Authentication",
                    category="security",
                    confidence=1.0,
                    source_terms=["JWT"],
                    is_inferred=False,
                )
            )

        # -------------------------------------------------------------
        # 3. CRUD Operations
        # -------------------------------------------------------------
        has_create = any(term in text for term in ["เพิ่ม", "สร้าง"]) or bool(re.search(r"\b(create|add|new)\b", text_lower))
        has_update = any(term in text for term in ["แก้ไข", "อัปเดต", "อัพเดท"]) or bool(re.search(r"\b(update|edit|modify)\b", text_lower))
        has_delete = any(term in text for term in ["ลบ"]) or bool(re.search(r"\b(delete|remove)\b", text_lower))

        if has_create and has_update and has_delete:
            add_concept(
                TechnicalConcept(
                    name="CRUD Operations",
                    category="data",
                    confidence=0.9,
                    source_terms=["เพิ่ม, ลบ, แก้ไข"],
                    is_inferred=True,
                ),
                assumption_desc="The combination of create, update, and delete actions is interpreted as standard CRUD operations.",
            )

        # -------------------------------------------------------------
        # 4. Search & Query Capabilities
        # -------------------------------------------------------------
        search_terms = []
        if any(term in text for term in ["ค้นหา", "สืบค้น"]):
            search_terms.append("ค้นหา")
        if re.search(r"\b(search|query|filter|filtering)\b", text_lower):
            search_terms.append("search/filter")

        if search_terms:
            add_concept(
                TechnicalConcept(
                    name="Search / Query Capability",
                    category="data",
                    confidence=1.0,
                    source_terms=search_terms,
                    is_inferred=False,
                )
            )

        # -------------------------------------------------------------
        # 5. Data Persistence
        # -------------------------------------------------------------
        if any(term in text for term in ["ฐานข้อมูล", "database", "db"]):
            add_concept(
                TechnicalConcept(
                    name="Data Persistence",
                    category="data",
                    confidence=1.0,
                    source_terms=["ฐานข้อมูล / database"],
                    is_inferred=False,
                )
            )
        elif any(term in text for term in ["เก็บข้อมูล", "บันทึกข้อมูล"]):
            add_concept(
                TechnicalConcept(
                    name="Data Persistence",
                    category="data",
                    confidence=0.85,
                    source_terms=["เก็บข้อมูล / บันทึกข้อมูล"],
                    is_inferred=True,
                ),
                assumption_desc="The requirement to store or record data implies a data persistence layer.",
            )

        # -------------------------------------------------------------
        # 6. Dashboard / Reporting Interface
        # -------------------------------------------------------------
        dashboard_terms = []
        if any(term in text for term in ["หน้าสรุป", "สรุปยอด", "รายงาน", "กราฟ"]):
            dashboard_terms.append("รายงาน/หน้าสรุป")
        if re.search(r"\b(dashboard|report|reporting|chart|analytics)\b", text_lower):
            dashboard_terms.append("dashboard/report")

        if dashboard_terms:
            add_concept(
                TechnicalConcept(
                    name="Dashboard / Reporting Interface",
                    category="ui",
                    confidence=0.9,
                    source_terms=dashboard_terms,
                    is_inferred=True,
                ),
                assumption_desc="Summaries, reports, or charts are interpreted as a dashboard or reporting interface.",
            )

        # -------------------------------------------------------------
        # 7. Microservices Architecture (if explicitly mentioned)
        # -------------------------------------------------------------
        if re.search(r"\bmicroservices?\b|ไมโครเซอร์วิส", text_lower):
            add_concept(
                TechnicalConcept(
                    name="Microservice Architecture",
                    category="architecture",
                    confidence=1.0,
                    source_terms=["microservice"],
                    is_inferred=False,
                )
            )

        return concepts, assumptions
