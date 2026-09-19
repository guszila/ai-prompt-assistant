import pytest
from app.domain.prompt import RequirementLanguage
from app.engine.normalizer import RequirementNormalizer
from tests.fixtures.requirements import (
    REQ_EMPTY,
    REQ_ENGLISH_TASKS,
    REQ_MIXED_EXPORT,
    REQ_THAI_CRUD,
    REQ_WHITESPACE,
)


def test_normalizer_preserves_original_text():
    raw = "  ระบบจัดการผู้ใช้  \n  เพิ่ม ลบ   "
    normalized = RequirementNormalizer.normalize(raw)
    assert normalized.original_text == raw
    assert normalized.normalized_text == "ระบบจัดการผู้ใช้\nเพิ่ม ลบ"
    assert normalized.char_count == len("ระบบจัดการผู้ใช้\nเพิ่ม ลบ")
    assert normalized.word_count > 0


def test_normalizer_detects_thai_language():
    normalized = RequirementNormalizer.normalize(REQ_THAI_CRUD)
    assert normalized.detected_language == RequirementLanguage.THAI


def test_normalizer_detects_english_language():
    normalized = RequirementNormalizer.normalize(REQ_ENGLISH_TASKS)
    assert normalized.detected_language == RequirementLanguage.ENGLISH


def test_normalizer_detects_mixed_language():
    normalized = RequirementNormalizer.normalize(REQ_MIXED_EXPORT)
    assert normalized.detected_language == RequirementLanguage.MIXED


def test_normalizer_handles_zero_width_chars():
    raw_with_zw = "ระบบ\u200bจัดการ\u200cผู้ใช้"
    normalized = RequirementNormalizer.normalize(raw_with_zw)
    assert "\u200b" not in normalized.normalized_text
    assert "\u200c" not in normalized.normalized_text
    assert normalized.normalized_text == "ระบบจัดการผู้ใช้"


def test_normalizer_rejects_empty_string():
    with pytest.raises(ValueError, match="cannot be empty"):
        RequirementNormalizer.normalize(REQ_EMPTY)


def test_normalizer_rejects_whitespace_only():
    with pytest.raises(ValueError, match="cannot be empty"):
        RequirementNormalizer.normalize(REQ_WHITESPACE)
