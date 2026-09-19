from typing import Any, Dict


class PromptTemplateManager:
    """
    Manages prompt templates and meta-prompts.
    In M1, serves as architectural boundary.
    """

    def __init__(self) -> None:
        self._templates: Dict[str, str] = {}

    def get_template(self, template_name: str) -> str:
        if template_name not in self._templates:
            raise KeyError(f"Template '{template_name}' not found.")
        return self._templates[template_name]

    def register_template(self, name: str, template: str) -> None:
        self._templates[name] = template
