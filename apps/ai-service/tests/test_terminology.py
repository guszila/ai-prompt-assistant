from app.engine.terminology import EngineeringTerminologyMapper
from tests.fixtures.requirements import (
    REQ_AUTH_COMBINED,
    REQ_AUTHN_ONLY,
    REQ_AUTHZ_EXPLICIT,
    REQ_DASHBOARD,
    REQ_GENERIC_API,
    REQ_REST_API,
)


def test_authn_only_does_not_infer_authorization():
    """
    Mandatory Rule 1: 'เข้าสู่ระบบ / Login' -> Authentication.
    Do NOT infer Authorization from Login alone.
    """
    concepts, assumptions = EngineeringTerminologyMapper.map_concepts(REQ_AUTHN_ONLY)
    concept_names = [c.name for c in concepts]

    assert "Authentication" in concept_names
    assert "Authorization" not in concept_names


def test_authz_explicit_maps_to_authorization():
    """
    Mandatory Rule 1: 'กำหนดสิทธิ์ / roles / permissions' -> Authorization.
    Do NOT include Authentication unless explicitly requested.
    """
    concepts, assumptions = EngineeringTerminologyMapper.map_concepts(REQ_AUTHZ_EXPLICIT)
    concept_names = [c.name for c in concepts]

    assert "Authorization" in concept_names
    assert "Authentication" not in concept_names


def test_combined_authn_and_authz():
    """
    When both login and roles/permissions are requested, both concepts must be mapped.
    """
    concepts, assumptions = EngineeringTerminologyMapper.map_concepts(REQ_AUTH_COMBINED)
    concept_names = [c.name for c in concepts]

    assert "Authentication" in concept_names
    assert "Authorization" in concept_names


def test_generic_api_maps_to_api_interface_not_restful():
    """
    Mandatory Rule 2: Generic 'API' -> API Interface.
    Do NOT infer REST unless explicitly stated.
    """
    concepts, assumptions = EngineeringTerminologyMapper.map_concepts(REQ_GENERIC_API)
    concept_names = [c.name for c in concepts]

    assert "API Interface" in concept_names
    assert "RESTful API" not in concept_names


def test_explicit_rest_api_maps_to_restful_api():
    """
    Mandatory Rule 2: Explicit 'RESTful API' / 'REST API' -> RESTful API.
    """
    concepts, assumptions = EngineeringTerminologyMapper.map_concepts(REQ_REST_API)
    concept_names = [c.name for c in concepts]

    assert "RESTful API" in concept_names


def test_dashboard_mapping():
    """
    Test UI and reporting interface mapping for dashboard requirement.
    """
    concepts, _ = EngineeringTerminologyMapper.map_concepts(REQ_DASHBOARD)
    concept_names = [c.name for c in concepts]

    assert "Dashboard / Reporting Interface" in concept_names
