import re
from app.domain.prompt import NormalizedRequirement, RequirementLanguage


class RequirementNormalizer:
    """
    Deterministic normalizer for incoming user requirements.
    Preserves original text, cleans formatting noise, and handles Thai Unicode safely.
    """

    THAI_CHAR_PATTERN = re.compile(r"[\u0e00-\u0e7f]")
    LATIN_CHAR_PATTERN = re.compile(r"[a-zA-Z]")

    @classmethod
    def normalize(cls, raw_text: str) -> NormalizedRequirement:
        """
        Normalize input text while preserving original text and semantic meaning.
        Raises ValueError if text is empty or blank.
        """
        if not raw_text or not raw_text.strip():
            raise ValueError("Input requirement cannot be empty or whitespace only.")

        original_text = raw_text

        # 1. Normalize line endings to \n
        cleaned = raw_text.replace("\r\n", "\n").replace("\r", "\n")

        # 2. Normalize invisible control characters and zero-width spaces (except standard \n and \t)
        cleaned = re.sub(r"[\u200B-\u200D\uFEFF]", "", cleaned)

        # 3. Collapse multiple horizontal spaces and tabs into a single space
        lines = [re.sub(r"[ \t]+", " ", line).strip() for line in cleaned.split("\n")]

        # 4. Collapse consecutive blank lines (max 1 blank line between paragraphs)
        compact_lines: list[str] = []
        for line in lines:
            if line:
                compact_lines.append(line)
            elif compact_lines and compact_lines[-1] != "":
                compact_lines.append("")

        normalized_text = "\n".join(compact_lines).strip()

        if not normalized_text:
            raise ValueError("Input requirement cannot be empty or whitespace only.")

        # 5. Language detection (deterministic heuristic based on scripts)
        has_thai = bool(cls.THAI_CHAR_PATTERN.search(normalized_text))
        has_latin = bool(cls.LATIN_CHAR_PATTERN.search(normalized_text))

        if has_thai and has_latin:
            detected_language = RequirementLanguage.MIXED
        elif has_thai:
            detected_language = RequirementLanguage.THAI
        else:
            detected_language = RequirementLanguage.ENGLISH

        # 6. Word count estimation
        # For English/mixed, space-separated count; for Thai without spaces, character length provides a baseline
        words = [w for w in re.split(r"\s+", normalized_text) if w]
        word_count = len(words)

        return NormalizedRequirement(
            original_text=original_text,
            normalized_text=normalized_text,
            detected_language=detected_language,
            char_count=len(normalized_text),
            word_count=word_count,
        )
