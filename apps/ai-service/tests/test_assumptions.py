from app.engine.terminology import EngineeringTerminologyMapper


def test_inferred_concepts_generate_assumptions():
    """
    Test that when an inferred concept is derived, an explicit Assumption is generated.
    """
    # "ระบบจัดการผู้ใช้ เพิ่ม ลบ แก้ไข ค้นหา"
    # Note: CRUD operations infer Persistence/Storage with is_inferred=True
    concepts, assumptions = EngineeringTerminologyMapper.map_concepts(
        "ระบบจัดการผู้ใช้ เพิ่ม ลบ แก้ไข ค้นหา"
    )

    inferred_concepts = [c for c in concepts if c.is_inferred]
    assert len(inferred_concepts) > 0

    # Ensure each inferred concept with an assumption is represented in assumptions list
    for concept in inferred_concepts:
        related_assumptions = [a for a in assumptions if a.source_concept == concept.name]
        assert len(related_assumptions) > 0
        for a in related_assumptions:
            assert a.requires_confirmation is True


def test_explicit_concepts_are_not_inferred():
    """
    Explicitly requested concepts (like Authentication from 'login', RESTful API from 'REST API')
    must have is_inferred=False.
    """
    concepts, assumptions = EngineeringTerminologyMapper.map_concepts(
        "สร้าง RESTful API และ login เข้าสู่ระบบ"
    )

    concept_map = {c.name: c for c in concepts}
    assert "RESTful API" in concept_map
    assert concept_map["RESTful API"].is_inferred is False

    assert "Authentication" in concept_map
    assert concept_map["Authentication"].is_inferred is False
