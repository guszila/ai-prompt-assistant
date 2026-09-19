from typing import Dict


class HealthService:
    """Provides application health and readiness checks."""

    @staticmethod
    def get_health() -> Dict[str, str]:
        return {"status": "ok"}
